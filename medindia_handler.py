from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import string
import csv

url = 'https://www.medindia.net/drug-price/index.asp?alpha='

def get_soup(url_string):
    client = urlopen(url_string)
    page_content = client.read()
    client.close()
    return soup(page_content, 'html5lib')


alphabets = list(string.ascii_uppercase)
drug_details = list()

# print(get_soup(url+alphabets[0]).find('table', {'class': 'table-bordered table'}).find_all('a'))
for alpha in range(len(alphabets)):
    for element in get_soup(url+alphabets[alpha]).find('table', {'class': 'table-bordered table'}).find_all('a'):
        u = element['href']
        with open('drug_details_from_medindia.csv', 'a', encoding='utf8', newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            if u[:4] == 'http':
                print(element.text, u)
                writer.writerow([element.text, u])
