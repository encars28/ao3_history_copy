from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup
from bs4.element import Tag

MAIN_SITE = "https://archiveofourown.org"
LOGIN_URL = MAIN_SITE + "/users/login"

def get(url, sess, **kwargs):
    """
    Get a request and check if it is a 429 error (too many requests)
    """
    req = sess.get(url, **kwargs)
    if req.status_code == 429:
        raise Exception("Too many requests")
    return req

def post(url, sess, **kwargs):
    """
    Post a request and check if it is a 429 error (too many requests)
    """
    req = sess.post(url, **kwargs)
    if req.status_code == 429:
        raise Exception("Too many requests")
    return req


