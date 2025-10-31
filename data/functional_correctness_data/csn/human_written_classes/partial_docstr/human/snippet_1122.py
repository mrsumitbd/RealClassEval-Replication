from bs4 import BeautifulSoup
import os

class HTMLParser:
    """
    HTMLParser contains a set of functions for parsing, scraping, and updating an HTML page.
    """

    def __init__(self, filename=None, html=None):
        self.filename = filename
        self.html = html
        self.link_tags = {'a': 'href', 'audio': 'src', 'img': 'src', 'link': 'href', 'script': 'src'}

    def get_links(self):
        """
        Retrieves all links contained within the page.

        :return: A list of local and remote URLs in the page.
        """
        basename = None
        if self.html is None:
            basename = os.path.basename(self.filename)
            self.html = open(self.filename).read()
        soup = BeautifulSoup(self.html, 'html.parser')
        extracted_links = []
        for tag_name in self.link_tags:
            tags = soup.find_all(tag_name)
            for tag in tags:
                link = tag.get(self.link_tags[tag_name])
                if link and (basename and (not link.startswith(basename))) and (not link.strip().startswith('#')):
                    if '?' in link:
                        link, query = link.split('?')
                    if '#' in link:
                        link, marker = link.split('#')
                    extracted_links.append(link)
        return extracted_links

    def get_local_files(self):
        """
        Returns a list of files that are contained in the same directory as the HTML page or in its subdirectories.

        :return: A list of local files
        """
        links = self.get_links()
        local_links = []
        for link in links:
            if '://' not in link:
                local_links.append(link)
        return local_links

    def replace_links(self, links_to_replace):
        """
        Updates page links using the passed in replacement dictionary.

        :param links_to_replace: A dictionary of OriginalURL -> ReplacementURL key value pairs.
        :return: An HTML string of the page with all links replaced.
        """
        if self.html is None:
            self.html = open(self.filename).read()
        soup = BeautifulSoup(self.html, 'html.parser')
        for tag_name in self.link_tags:
            tags = soup.find_all(tag_name)
            for tag in tags:
                link = tag.get(self.link_tags[tag_name])
                if link in links_to_replace:
                    tag[self.link_tags[tag_name]] = links_to_replace[link]
        return soup.prettify()