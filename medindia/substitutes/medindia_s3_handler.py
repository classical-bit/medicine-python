from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import csv


def get_soup(url_string):
    client = urlopen(url_string)
    page_content = client.read()
    client.close()
    return soup(page_content, 'html5lib')


drug_names = list()
drug_names = ['Abacavir .csv']
drug_url = list()
for drug_name in drug_names:
    try:
        with open(drug_name, 'r', encoding='utf8') as in_file:
            in_file_reader = csv.reader(in_file)
            for row in in_file_reader:
                drug_url.append(row[1])
        in_file.close()
    except FileNotFoundError:
        print('FileNotFoundError:')
        exit(0)

    try:
        d = list()
        details = list()
        for each_drug_url in drug_url:
            details = []
            d = []
            page_soup = get_soup(each_drug_url)
            d.append(str.replace(page_soup.find('div', {'class': 'report-content'}).text, '\xa0', ''))
            for b_elem in page_soup.find('div', {'class': 'ybox'}).find_all('b'):
                d.append(b_elem.text)
            prescribed_for = ''
            for div_elem in page_soup.find_all('div', {'class': 'col-sm-1 col-md-2'}):
                prescribed_for += div_elem.b.text + '| '
            d.append(prescribed_for)
            for div_elem in page_soup.find_all('p', {'class': 'drug-content'}):
                d.append(div_elem.text)

            for detail in d:
                detail = detail.replace('\n', '').replace('\t', '')
                details.append(detail)
            try:
                with open('detailed/' + drug_name, 'a', encoding='utf8', newline='') as out_file:
                    out_file_writer = csv.writer(out_file)
                    out_file_writer.writerow(details)
                out_file.close()
            except AttributeError:
                print('AttributeError:')
            except FileNotFoundError:
                print('FileNotFoundError:')
                exit(0)
            print('DONE:', each_drug_url)
    except AttributeError:
        print('AttributeError:', drug_name)


