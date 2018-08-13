from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import string


def get_soup(url_string):
    web_client = uReq(url_string)
    page_content = web_client.read()
    web_client.close()
    return soup(page_content, 'html5lib')


alphabets = list(string.ascii_lowercase)
alpha = 0

page_number = 1

url = 'https://www.mims.com/india/browse/alphabet/'+alphabets[alpha]+'?cat=drug&tab=generic&page=' + str(page_number)
