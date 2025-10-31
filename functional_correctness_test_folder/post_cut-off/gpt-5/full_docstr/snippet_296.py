import os
import json
import html
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _fmt_val(self, v: Any) -> str:
        if v is None:
            return ''
        if isinstance(v, (int, float)):
            if isinstance(v, float):
                return f"{v:.4g}"
            return str(v)
        if isinstance(v, (list, dict)):
            try:
                return html.escape(json.dumps(v, ensure_ascii=False, separators=(',', ':')))
            except Exception:
                return html.escape(str(v))
        if isinstance(v, (datetime,)):
            return v.isoformat()
        # try to interpret epoch seconds
        if isinstance(v, (int, float)) and v > 10000000:
            try:
                return datetime.fromtimestamp(v).isoformat(sep=' ', timespec='seconds')
            except Exception:
                pass
        return html.escape(str(v))

    def _extract_results(self, summary_data: Dict[str, Any], results_data: Optional[Any]) -> List[Dict[str, Any]]:
        if isinstance(results_data, list):
            return results_data
        if isinstance(results_data, dict):
            for key in ('results', 'problems', 'items', 'data'):
                v = results_data.get(key)
                if isinstance(v, list):
                    return v
        for key in ('results', 'problems', 'items', 'data'):
            v = summary_data.get(key)
            if isinstance(v, list):
                return v
        return []

    def _problem_id_from_result(self, item: Dict[str, Any]) -> str:
        for k in ('problem_id', 'id', 'task_id', 'problem', 'name', 'slug', 'title', 'key'):
            v = item.get(k)
            if v is not None:
                return str(v)
        # fallback to index later
        return ''

    def _problem_title_from_result(self, item: Dict[str, Any]) -> str:
        for k in ('title', 'name', 'problem', 'slug', 'id', 'problem_id'):
            v = item.get(k)
            if v is not None:
                return str(v)
        return ''

    def _status_from_result(self, item: Dict[str, Any]) -> str:
        for k in ('status', 'outcome', 'result', 'pass', 'passed', 'success'):
            if k in item:
                v = item[k]
                if isinstance(v, bool):
                    return 'PASS' if v else 'FAIL'
                return str(v).upper()
        # Infer from score if available
        score = item.get('score')
        if isinstance(score, (int, float)):
            return 'PASS' if score > 0 else 'FAIL'
        return ''

    def _score_from_result(self, item: Dict[str, Any]) -> Any:
        for k in ('score', 'reward', 'accuracy', 'grade', 'points'):
            if k in item:
                return item[k]
        return ''

    def _cost_from_result(self, item: Dict[str, Any]) -> Any:
        for k in ('cost', 'tokens', 'token_cost', 'price', 'total_cost'):
            if k in item:
                return item[k]
        return ''

    def _duration_from_result(self, item: Dict[str, Any]) -> Any:
        for k in ('duration', 'time', 'elapsed', 'runtime', 'latency', 'seconds'):
            if k in item:
                return item[k]
        # try start/end
        start = item.get('start_time') or item.get('started_at')
        end = item.get('end_time') or item.get(
            'ended_at') or item.get('finished_at')
        try:
            if isinstance(start, (int, float)) and isinstance(end, (int, float)):
                return max(0, end - start)
        except Exception:
            pass
        return ''

    def _discover_visualizations(self, visualizations_dir: Optional[str]) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        if not visualizations_dir:
            return mapping
        base = Path(visualizations_dir)
        if not base.exists():
            return mapping
        for p in base.rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.html', '.htm'):
                key = p.stem
                mapping[key] = str(p)
                # also map parent dir name for index.html patterns
                if p.name.lower() in ('index.html', 'index.htm'):
                    mapping[p.parent.name] = str(p)
        return mapping

    def _resolve_viz_for_problem(self, pid: str, item: Dict[str, Any], discovered: Dict[str, str], provided: Optional[Dict[str, str]]) -> Optional[str]:
        # explicit fields on item
        for k in ('visualization', 'viz', 'html', 'html_path', 'viz_path', 'visualization_path', 'report', 'link'):
            v = item.get(k)
            if isinstance(v, str) and v.strip():
                return v
        # provided mapping
        if provided:
            if pid in provided:
                return provided[pid]
            # also try title/name keys
            title = self._problem_title_from_result(item)
            if title and title in provided:
                return provided[title]
        # discovered mapping from directory
        if discovered:
            if pid and pid in discovered:
                return discovered[pid]
            title = self._problem_title_from_result(item)
            if title and title in discovered:
                return discovered[title]
            # try slug-like normalization
            slug = (pid or title or '').strip().lower().replace(
                ' ', '-').replace('/', '-')
            if slug and slug in discovered:
                return discovered[slug]
        return None

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        '''
        Generate HTML for visualizing benchmark summary with links to problem visualizations.
        Args:
            summary_data: Dictionary with benchmark summary data
            results_data: List of problem results data
            problem_visualizations: Optional dictionary mapping problem_id to visualization file paths
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        results = self._extract_results(summary_data or {}, results_data)
        provided_map = problem_visualizations or {}
        discovered_map = {}  # handled at visualize time; keep empty here

        page_title = title or summary_data.get('title') or 'Benchmark Summary'

        # Build summary key-value table excluding bulky fields
        exclude_keys = {'results', 'problems', 'items', 'data'}
        summary_rows = []
        for k, v in (summary_data or {}).items():
            if k in exclude_keys:
                continue
            summary_rows.append((str(k), self._fmt_val(v)))
        summary_rows.sort(key=lambda x: x[0].lower())

        # Build results rows
        result_rows_html = []
        for idx, item in enumerate(results, start=1):
            pid = self._problem_id_from_result(item)
            pname = self._problem_title_from_result(item)
            status = self._status_from_result(item)
            score = self._score_from_result(item)
            cost = self._cost_from_result(item)
            duration = self._duration_from_result(item)
            link = self._resolve_viz_for_problem(
                pid, item, discovered_map, provided_map)

            status_class = 'pass' if str(status).upper() in (
                'PASS', 'PASSED', 'SUCCESS', 'OK', 'TRUE') else ('fail' if status else '')
            link_html = f'<a href="{html.escape(link)}" target="_blank">View</a>' if link else ''

            result_rows_html.append(
                f"<tr>"
                f"<td>{idx}</td>"
                f"<td>{html.escape(pid) if pid else ''}</td>"
                f"<td>{html.escape(pname) if pname else ''}</td>"
                f"<td class='{status_class}'>{html.escape(str(status)) if status is not None else ''}</td>"
                f"<td>{self._fmt_val(score)}</td>"
                f"<td>{self._fmt_val(cost)}</td>"
                f"<td>{self._fmt_val(duration)}</td>"
                f"<td>{link_html}</td>"
                f"</tr>"
            )

        summary_table_html = ""
        if summary_rows:
            rows = "".join(
                f"<tr><th>{html.escape(k)}</th><td>{v}</td></tr>" for k, v in summary_rows)
            summary_table_html = f"""
            <section>
                <h2>Summary</h2>
                <table class="kv">{rows}</table>
            </section>
            """

        results_table_html = f"""
        <section>
            <h2>Results</h2>
            <table class="results">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Problem ID</th>
                        <th>Title</th>
                        <th>Status</th>
                        <th>Score</th>
                        <th>Cost</th>
                        <th>Duration</th>
                        <th>Visualization</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(result_rows_html)}
                </tbody>
            </table>
        </section>
        """

        css = """
        body { font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 20px; color: #222; }
        h1 { margin-top: 0; }
        h2 { margin: 24px 0 8px; }
        .meta { color: #666; font-size: 0.9em; }
        table { border-collapse: collapse; width: 100%; }
        table.kv th { text-align: left; white-space: nowrap; vertical-align: top; padding: 8px; background: #f8f8f8; border: 1px solid #e5e5e5; width: 220px; }
        table.kv td { padding: 8px; border: 1px solid #e5e5e5; }
        table.results th, table.results td { padding: 8px; border: 1px solid #e5e5e5; }
        table.results thead th { background: #f3f3f3; position: sticky; top: 0; z-index: 1; }
        tr:nth-child(even) td { background: #fcfcfc; }
        .pass { color: #0a7d17; font-weight: 600; }
        .fail { color: #b00020; font-weight: 600; }
        .footer { margin-top: 24px; color: #666; font-size: 0.85em; }
        .container { max-width: 1200px; margin: 0 auto; }
        """

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(page_title)}</title>
<style>{css}</style>
</head>
<body>
<div class="container">
  <h1>{html.escape(page_title)}</h1>
  <div class="meta">Generated at {now_str}</div>
  {summary_table_html}
  {results_table_html}
  <div class="footer">Benchmark Visualizer</div>
</div>
</body>
</html>
"""
        return html_doc

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        '''
        Generate HTML visualization from benchmark summary file with links to problem visualizations.
        Args:
            summary_file: Path to the benchmark summary JSON file
            results_file: Optional path to the benchmark results JSON file
            visualizations_dir: Optional directory containing problem visualizations
            output_file: Optional path to save the HTML output
        Returns:
            Path to the generated HTML file
        '''
        summary_path = Path(summary_file)
        if not summary_path.exists():
            raise FileNotFoundError(f"Summary file not found: {summary_file}")

        with summary_path.open('r', encoding='utf-8') as f:
            summary_data = json.load(f)

        results_data = None
        if results_file:
            rf_path = Path(results_file)
            if not rf_path.exists():
                raise FileNotFoundError(
                    f"Results file not found: {results_file}")
            with rf_path.open('r', encoding='utf-8') as f:
                results_data = json.load(f)

        discovered_map = self._discover_visualizations(visualizations_dir)

        # Build provided mapping (exact by problem_id where possible)
        provided_map: Dict[str, str] = {}
        results_list = self._extract_results(summary_data, results_data)
        for item in results_list:
            pid = self._problem_id_from_result(item)
            # priority: explicit fields in item
            path = self._resolve_viz_for_problem(pid, item, {}, {})
            if path:
                provided_map[pid] = path
                continue
            # discovered mapping
            if discovered_map:
                path2 = self._resolve_viz_for_problem(
                    pid, item, discovered_map, {})
                if path2:
                    provided_map[pid] = path2

        title = summary_data.get(
            'title') or f"Benchmark Summary - {summary_path.stem}"
        html_str = self.generate_summary_html(
            summary_data, results_list, problem_visualizations=provided_map, title=title)

        if output_file:
            out_path = Path(output_file)
        else:
            out_name = f"{summary_path.stem}_summary.html"
            out_path = self.output_dir / out_name

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open('w', encoding='utf-8') as f:
            f.write(html_str)

        return str(out_path)
