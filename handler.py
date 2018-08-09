from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import string


def get_soup(url_string):
   web_client = uReq(url_string)
   page_content = web_client.read()
   web_client.close()
   return soup(page_content, 'html5lib')


def get_total_pages():
   total = page_soup.find('span', {'class': 'style__countInfo___sVIyR'}).text
   total = total.split()
   total = total[0]
   total = int(total.replace(',', ''))
   return total//len(drugs_list)


url = 'https://www.1mg.com'
url_base = url + "/search/all?name="
# alphabets = list(string.ascii_lowercase)
alphabets = ['a']
drugs_list = list()
output_csv = list()
csv_file_header_set = False
drug_data = dict(NAME='', COMPANY='', COMPOSITION='', PRESCRIPTION='', DRUGINFO='', COST='', QUANTITY='',
                USES='', SIDEEFFECTS='', HOWTOUSE='', HOWITWORKS='', EXPERTADVICE=[], SUBSTITUTE=[])

for alpha in range(0, 1):
   url_base_alpha = url_base + alphabets[alpha]
   page_soup = get_soup(url_base_alpha)

   for link in page_soup.find_all("a", {"class": "style__product-link___1hWpa"}):
       drugs_list.append(link.get("href"))

   # total_pages = get_total_pages()
   total_pages = 1

   for page in range(0, total_pages):
       if page == 0:
           url_page = ''
       else:
           url_page = '&filter=false&state='+'1' '''str(page)'''

       for drug_address in range(0, len(drugs_list)):
           if list(drugs_list[drug_address])[1] == 'd':

               url_drug = url + drugs_list[drug_address] + url_page
               page_soup = get_soup(url_drug)
               drug_data['NAME'] = page_soup.find('h1', {"class": "DrugInfo__drug-name-heading___adCs-"}).string
               drug_data['COMPANY'] = page_soup.find('div', {"class": "DrugInfo__company-name___39Abk"}).string
               drug_data['COMPOSITION'] = page_soup.find('div', {"class": "saltInfo DrugInfo__salt-name___2-9Vh"}).a.string
               drug_data['PRESCRIPTION'] = page_soup.find('div',
                                                          {"class": "DrugInfo__prescription-requirement___21T_g"}).text
               drug_data['DRUGINFO'] = page_soup.find('div', {"class": "DrugInfo__title___2qdTY"}).text
               drug_data['COST'] = page_soup.find('div', {"class": "DrugPriceBox__price___dj2lv"}).text
               drug_data['QUANTITY'] = page_soup.find('div', {"class": "DrugPriceBox__quantity___2LGBX"}).text
               drug_data['USES'] = page_soup.find('div', {"class": "DrugUses__content___38C-l"}).text
               drug_data['SIDEEFFECTS'] = page_soup.find('div', {"class": "DrugSideEffects__block___2yk_W"}).text
               drug_data['HOWTOUSE'] = page_soup.find('div', {"class": "DrugConsumption__content___3mfDy"}).text
               drug_data['HOWITWORKS'] = page_soup.find('div', {"class": "DrugProcess__content___232QU"}).text

               # try:
               #     for info in page_soup.find('div', {"class": "ExpertAdviceItem__content___1Djk2"})
               # .ul.find_all('li'):
               #         drug_data['EXPERTADVICE'].append(info.string)
               # except AttributeError:
               #     pass

               for anchors in page_soup.find_all('div', {"class": "row SubstituteItem__item___1wbMv"}):
                   temp = []
                   temp = [anchors.a["href"], anchors.find("div", {'class': 'SubstituteItem__name___PH8Al'}).text,
                           anchors.find("div", {'class': 'SubstituteItem__manufacturer-name___2X-vB'}).text,
                           anchors.find("div", {'class': 'SubstituteItem__unit-price___MIbLo'}).text]
                   drug_data['SUBSTITUTE'].append(temp)

               output_csv = [
                   [drug_data['NAME'], url_drug, drug_data['COMPANY'], drug_data['COMPOSITION'], drug_data['PRESCRIPTION'],
                    drug_data['DRUGINFO'], drug_data['COST'], drug_data['QUANTITY'], drug_data['USES'],
                    drug_data['SIDEEFFECTS'], drug_data['HOWTOUSE'], drug_data['HOWITWORKS'], drug_data['EXPERTADVICE'],
                    drug_data['SUBSTITUTE']]]

               with open('csv_file.csv', 'a') as my_drug_file:
                   writer = csv.writer(my_drug_file)
                   if not csv_file_header_set:
                       writer.writerows([['NAME', 'URL', 'COMPANY', 'COMPOSITION', 'PRESCRIPTION', 'DRUGINFO', 'COST',
                                          'QUANTITY', 'USES', 'SIDE EFFECTS', 'HOW TO USE', 'HOW IT WORKS',
                                          'EXPERT ADVICE', 'SUBSTITUTE']])
                   writer.writerows(output_csv)
               csv_file_header_set = True
           else:
               with open('otc_csv.csv', 'a') as my_otc_file:
                   writer = csv.writer(my_otc_file)
                   writer.writerows([[drugs_list[drug_address]]])

           print("%s - PAGE[%d/%d] - DRUG[%d/%d]" % (alphabets[alpha], page+1, total_pages, drug_address+1,
                                                     len(drugs_list)))
           with open('log_file.csv', 'w') as my_log_file:
               writer = csv.writer(my_log_file)
               writer.writerows([[alphabets[alpha], page, drug_address]])


