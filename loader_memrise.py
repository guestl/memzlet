import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class loader_memrise(object):
    def __init__(self, ):
        self.memrise_link = "https://www.memrise.com"

    def parse(self, text_to_parse):
        logger.debug("parsing process started")

        result_dict = dict()
        terms_dict = dict()

#        parser = etree.HTMLParser()
#        tree = etree.parse(self.text_to_parse, parser)

#        links_in_content = tree.xpath('//*[@id="content"]/div/a')

#        print(links_in_content[0].text)

        soup = BeautifulSoup(text_to_parse, 'html.parser')

        next_navigation = soup.find(class_="level-nav level-nav-next")

        next_link_url = None
        if next_navigation:
            next_link_url = next_navigation.get('href')

        if next_link_url:
            next_link_url = self.memrise_link + next_link_url

        result_dict['next_url'] = next_link_url

        terms = list()
        translation = list()

        html_terms_list = soup.find_all(class_="col_a col text")
        for single_term in html_terms_list:
            terms.append(single_term.get_text())

        html_trans_list = soup.find_all(class_="col_b col text")
        for single_trans in html_trans_list:
            translation.append(single_trans.get_text())

        terms_dict = dict(zip(terms, translation))

        result_dict['terms'] = terms_dict

        title = soup.find(class_="progress-box-title").get_text()

        result_dict['title'] = title.rstrip().lstrip()

        filename = soup.find(class_="level-number").get_text()

        filename = filename.strip()
        result_dict['filename'] = filename + '.txt'

        logger.debug("parsing process finished")
        return result_dict
