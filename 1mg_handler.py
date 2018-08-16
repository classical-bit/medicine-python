from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv


def get_soup(url_string):
    web_client = uReq(url_string)
    page_content = web_client.read()
    web_client.close()
    return soup(page_content, 'html5lib')


url = 'https://www.1mg.com/search/all?name='
drug = 'Bacitracin'

for element in get_soup(url+drug).find_all('div', {'class', 'SkuInfoCards__div-info-card___2vtcl'}):
    try:
        result_name = element.find('div', {'class': 'SkuInfoCards__info-header___1966o'}).text
        result_detail = element.find('div', {'class': 'SkuInfoCards__sku-info___3D-Dm'}).text

        print(result_name, '[', result_detail, ']')

        # with open('1mg_search_result.csv', 'w', newline='') as mg_search_result_file:
        #     writer = csv.writer(mg_search_result_file, delimiter=',')
        #     writer.writerow([])
    except AttributeError:
        result_detail = ''
        result_name = element.find('div', {'class': 'SkuInfoCards__info-header___1966o'}).text

        print(result_name, '[', result_detail, ']')
