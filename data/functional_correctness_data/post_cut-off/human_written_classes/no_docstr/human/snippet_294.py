from typing import Dict, List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
from googleapiclient.discovery import build
import bs4

class OnlineSearchEngine:

    def __init__(self, config):
        self.config = config

    def collect_context(self, snippet: str, doc: str) -> str:
        snippets = parse_snippet(snippet)
        ctx_paras = []
        for s in snippets:
            pos = doc.replace('\n', ' ').find(s)
            if pos == -1:
                continue
            sta = pos
            while sta > 0 and doc[sta] != '\n':
                sta -= 1
            end = pos + len(s)
            while end < len(doc) and doc[end] != '\n':
                end += 1
            para = doc[sta:end].strip()
            if para not in ctx_paras:
                ctx_paras.append(para)
        return '\n'.join(ctx_paras)

    def fetch_web_content(self, search_results: List[Dict]) -> Dict[str, str]:
        links = filter_links(search_results)
        contents = asyncio.run(fetch_all(links))
        content_dict = {}
        for html, link in zip(contents, links):
            soup = bs4.BeautifulSoup(html, 'html.parser')
            text = '\n'.join([p.get_text() for p in soup.find_all('p')])
            content_dict[link] = text
        return content_dict

    def search(self, search_term: str, num_iter: int=1) -> List[Dict]:
        service = build('customsearch', 'v1', developerKey=self.config.api_key)
        results = []
        sanitize_search_term = sanitize_search_query(search_term)
        if search_term.isspace():
            return results
        res = service.cse().list(q=sanitize_search_term, cx=self.config.cse_id).execute()
        results.append(res)
        for _ in range(num_iter - 1):
            if 'nextPage' not in res.get('queries', {}):
                break
            start_idx = res['queries']['nextPage'][0]['startIndex']
            res = service.cse().list(q=search_term, cx=self.config.cse_id, start=start_idx).execute()
            results.append(res)
        return results

    def batch_search(self, queries: List[str]) -> List[List[str]]:
        with ThreadPoolExecutor() as executor:
            return list(executor.map(self._retrieve_context, queries))

    def _retrieve_context(self, query: str) -> List[str]:
        search_results = self.search(query)
        if self.config.snippet_only:
            contexts = []
            for result in search_results:
                for item in result.get('items', []):
                    title = item.get('title', '')
                    context = ' '.join(parse_snippet(item.get('snippet', '')))
                    if title != '' or context != '':
                        title = 'No title.' if not title else title
                        context = 'No snippet available.' if not context else context
                        contexts.append({'document': {'contents': f'"{title}"\n{context}'}})
        else:
            content_dict = self.fetch_web_content(search_results)
            contexts = []
            for result in search_results:
                for item in result.get('items', []):
                    link = item['link']
                    title = item.get('title', '')
                    snippet = item.get('snippet', '')
                    if link in content_dict:
                        context = self.collect_context(snippet, content_dict[link])
                        if title != '' or context != '':
                            title = 'No title.' if not title else title
                            context = 'No snippet available.' if not context else context
                            contexts.append({'document': {'contents': f'"{title}"\n{context}'}})
        return contexts[:self.config.topk]