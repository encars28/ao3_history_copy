from history_page import HistoryPage
from aux import get, post, LOGIN_URL, MAIN_SITE
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

class Reader:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.url = MAIN_SITE + f"/users/{self.username}"

        self.login()

        self.history = HistoryPage(self.session, self.url + "/readings")
        self.marked_for_later = HistoryPage(self.session, self.url + "/readings?show=to-read")

    def login(self):
        # first we have to obtain the token
        # I dont bother with making the login page an attribute, for it will only be used here
        soup = BeautifulSoup(get(LOGIN_URL, self.session).content, features="lxml")
        token = soup.find("input", {"name": "authenticity_token"})
        assert isinstance(token, Tag)
        token =  token['value']

        # Now we can login
        p = post(LOGIN_URL, self.session, allow_redirects=False, params={
            "authenticity_token": token,
            "user[login]": self.username,
            "user[password]": self.password,
            "user[remember_me]": 0,
            "commit": "Log+in"
        })

        if not p.status_code == 302:
            raise Exception("Invalid username or password")
    
    def __del__(self):
        self.session.close()