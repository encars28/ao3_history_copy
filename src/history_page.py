from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup
from bs4.element import Tag
from aux import get, MAIN_SITE

class HistoryPage:
    def __init__(self, sess, url) -> None:
        if sess is None:
            raise Exception("Something went wrong with the session")
        
        self.sess = sess
        self.url = url

    @property 
    def pages(self):
        html = BeautifulSoup(get(self.url, self.sess).content, features="lxml")

        # The last li element is the button next, so we have to get the second to last
        pagination = html.find("ol", {"class": "pagination actions"})
        assert isinstance(pagination, Tag)

        # If there is no pagination, there is only one page
        if pagination is None:
            return 1

        return int(pagination.find_all("li")[-2].text)

    @property
    def works_urls(self):
        history = []

        # Iterate and get urls
        # Tqdm is a progress bar
        for i in tqdm(range(1, self.pages + 1)):
            soup =  BeautifulSoup(get(f"{self.url}?page={i}", self.sess).content, features="lxml")

            page = soup.find("ol", {"class": "reading work index group"})
            assert isinstance(page, Tag)

            # If there is no ol class then there are no works in the page
            # After the break the function returns the history (which is empty)
            if page is None:
                break

            for li in page.find_all("li", {"role": "article"}):

                # It is a mystery work if it doesnt have a div with the class header module
                work = li.find("div", {"class": "header module"})
                if work is None:
                    continue

                history.append(MAIN_SITE + work.h4.a['href'])

            # I let this sleep so the page doesnt get overloaded
            sleep(5)

        return history