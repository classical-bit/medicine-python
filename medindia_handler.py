from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import string
import csv

url_base = 'https://www.medindia.net/doctors/drug_information/'
url = url_base + 'home.asp?alpha='


def get_soup(url_string):
    client = urlopen(url_string)
    page_content = client.read()
    client.close()
    return soup(page_content, 'html5lib')


alphabets = list(string.ascii_uppercase)
# alphabets = ['A']
drug_details = list()
try:
    for alpha in range(len(alphabets)):
        page_soup = get_soup(url+alphabets[alpha]).find_all('li', {'class': 'list-item'})
        for index, element in enumerate(page_soup):
            with open('drug_details_from_medindia.csv', 'a', encoding='utf8', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([element.h4.a.text, str.replace(element.text, '\n', ''), url_base+element.h4.a['href']])
            print("DONE:", alphabets[alpha], index + 1, '/', len(page_soup))
finally:
    csv_file.close()
