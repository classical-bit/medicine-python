from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import urllib.error

LOG_STRICT = False

url = 'https://www.1mg.com'
url_stage1 = '/search/all?name='
drug_names = list()


def get_soup(url_string):
    web_client = uReq(url_string)
    page_content = web_client.read()
    web_client.close()
    return soup(page_content, 'html5lib')


def get_drug_info(url_drug):
    s4_soup = get_soup(url+url_drug)

    drug_details = []
    if url_drug[1:2] is 'd':
        print('\t\t\t\t\t\tDRUG:')
        try:
            name_of_drug = s4_soup.find('h1', {'class': 'DrugInfo__drug-name-heading___adCs-'}).text
            drug_details.append(name_of_drug)
        except AttributeError:
            print('AttributeError: name_of_drug')
            try:
                name_of_drug = s4_soup.find('h1', {'class': 'DrugInfo__drug-name-heading___adCs-'}).text
                drug_details.append(name_of_drug)
            except AttributeError:
                print('AttributeError x2: name_of_drug')
                try:
                    name_of_drug = s4_soup.find('h1', {'class': 'DrugInfo__drug-name-heading___adCs-'}).text
                    drug_details.append(name_of_drug)
                except AttributeError:
                    print('AttributeError x3: name_of_drug [Exiting]')
                    exit()

        drug_details.append(url+url_drug)

        with open('raw/'+str.replace(name_of_drug, '/', 'or')+'.txt', 'a', encoding='utf8') as raw_output_file:
            raw_output_file.write(str(s4_soup))
            with open('raw/raw_files_name.csv', 'a', encoding='utf8', newline='') as raw_files_name_csv_file:
                raw_files_name_csv_file_writer = csv.writer(raw_files_name_csv_file)
                raw_files_name_csv_file_writer.writerow([str.replace(name_of_drug, '/', 'or')])

        print('\t\t\t\t\t\tRAW OUTPUT CREATED: ', name_of_drug)

        try:
            manufacturer_of_drug = s4_soup.find('div', {'class': 'DrugInfo__company-name___39Abk'}).text
            drug_details.append(manufacturer_of_drug)
        except AttributeError:
            print('AttributeError: manufacturer_of_drug')
            drug_details.append('')

        try:
            composition_of_drug = s4_soup.find('div', {'class': 'saltInfo DrugInfo__salt-name___2-9Vh'}).a.text
            drug_details.append(composition_of_drug)
        except AttributeError:
            print('AttributeError: composition_of_drug')
            drug_details.append('')

        try:
            primary_use_of_drug = s4_soup.find('div', {'class': 'DrugInfo__uses___381Re'}).a.text
            drug_details.append(primary_use_of_drug)
        except AttributeError:
            print('AttributeError: primary_use_of_drug')
            drug_details.append('')

        try:
            prescription_of_drug = s4_soup.find('div', {'class': 'col-xs-4 DrugInfo__prescription-requirement___21T_g'}).text
            drug_details.append(prescription_of_drug)
        except AttributeError:
            print('AttributeError: prescription_of_drug')
            drug_details.append('NOT REQUIRED')

        try:
            price_of_drug = s4_soup.find('div', {'class': 'DrugPriceBox__price___dj2lv'}).text
            drug_details.append(price_of_drug)
        except AttributeError:
            print('AttributeError: price_of_drug')
            drug_details.append('')

        try:
            price_per_tablet_of_drug = s4_soup.find('div', {'class': 'DrugPriceBox__price-tablet___2CZLa'}).text
            drug_details.append(price_per_tablet_of_drug)
        except AttributeError:
            print('AttributeError: price_per_tablet_of_drug')
            drug_details.append('')

        try:
            quantity_of_drug = s4_soup.find('div', {'class': 'DrugPriceBox__quantity___2LGBX'}).text
            drug_details.append(quantity_of_drug)
        except AttributeError:
            print('AttributeError: quantity_of_drug')
            drug_details.append('')

        try:
            uses_of_drug = s4_soup.find('div', {'id': 'uses_0'}).find('div', {'class': 'DrugUses__content___38C-l'}).text
            drug_details.append(uses_of_drug)
        except AttributeError:
            print('AttributeError: uses_of_drug')
            drug_details.append('')

        try:
            sideeffect_of_drug = s4_soup.find('div', {'id': 'side_effects_0'}).p.text
            drug_details.append(sideeffect_of_drug)
        except AttributeError:
            print('AttributeError: sideeffect_of_drug')
            drug_details.append('')

        try:
            howtouse_of_drug = s4_soup.find('div', {'id': 'how_to_use_0'}).find('div', {'class': 'DrugConsumption__content___3mfDy'}).text
            drug_details.append(howtouse_of_drug)
        except AttributeError:
            print('AttributeError: howtouse_of_drug')
            drug_details.append('')

        try:
            howitworks_of_drug = s4_soup.find('div', {'id': 'how_it_works_0'}).find('div', {'class': 'DrugProcess__content___232QU'}).text
            drug_details.append(howitworks_of_drug)
        except AttributeError:
            print('AttributeError: howitworks_of_drug')
            drug_details.append('')

        try:
            substitutes_of_drugs = s4_soup.find_all('div', {'class': 'row SubstituteItem__item___1wbMv'})
            subs_list = []
            for subs in substitutes_of_drugs:
                subs_list.append((subs.div.a['href'], subs.div.a.div.text, subs.div.find('div', {'class': 'SubstituteItem__manufacturer-name___2X-vB'}).text))
            drug_details.append(subs_list)
        except AttributeError:
            print('AttributeError: substitutes_of_drugs')
            drug_details.append('')

        try:
            precaution_of_drug = s4_soup.find('div', {'id': 'precautions'}).find_all('div', {'class': 'col-md-3'})
            prec_list = []
            for precaution in precaution_of_drug:
                prec_list.append((precaution.find('div', {'class': 'WarningItem__title___2HTPF'}).text, precaution.find('div', {'class': 'WarningItem__description___1Wnw9'}).text))
            drug_details.append(prec_list)
        except AttributeError:
            print('AttributeError: precaution_of_drug')
            drug_details.append('')

        with open('output_from_1mg.csv', 'a', encoding='utf8', newline='') as output_from_1mg_file:
            output_from_1mg_file_writer = csv.writer(output_from_1mg_file)
            output_from_1mg_file_writer.writerow(drug_details)

        print('\t\t\t\t\t\tUSER-FRIENDLY OUTPUT CREATED: ', name_of_drug)

    elif url_drug[1:2] is 'o':
        print('\t\t\t\t\t\tOTC:')
        with open('output_from_1mg.csv', 'a', encoding='utf8', newline='') as output_from_1mg_file:
            output_from_1mg_file_writer = csv.writer(output_from_1mg_file)
            output_from_1mg_file_writer.writerow([url_drug])

        print('\t\t\t\t\t\tLOGGED: ')

    output_from_1mg_file.close()
    raw_files_name_csv_file.close()
    raw_output_file.close()


def lists_found_in_s2(lists_containing_s2):
    for li_s2_index, li_s2 in enumerate(lists_containing_s2.find_all('li')):

        # print(li_s2.a.text, li_s2.a['href'])
        try:
            url_to_s3 =  li_s2.a['href']
        except AttributeError:
            print('AttributeError: url_to_s3')
        print('\t\tSTAGE-2[', li_s2_index + 1, '/', len(lists_containing_s2.find_all('li')), ']', url_to_s3)

        s3_soup = get_soup(url+url_to_s3)

        try:
            divs_containing_s3_result = s3_soup.find_all('div', {'class': 'style__product-box___3oEU6'})
        except AttributeError:
            print('AttributeError: divs_containing_s3_result')

        for div_s3_index, div_s3 in enumerate(divs_containing_s3_result):
            try:
                url_to_s4 = div_s3.a['href']
                print('\t\t\t\tSTAGE-3[', div_s3_index + 1, '/', len(divs_containing_s3_result), ']', url_to_s4)
                get_drug_info(url_to_s4)
            except AttributeError:
                print('AttributeError: url_to_s4')


try:
    with open('drug_details_from_medindia.csv', 'r', encoding='utf8') as stage1_input_file:
        stage1_reader = csv.reader(stage1_input_file)
        for row in stage1_reader:
            drug_names.append(row[0])

except FileNotFoundError:
    print('FileNotFoundError: drug_details_from_medindia.csv')


startFrom = 0

try:
    with open('log_1mg.csv', 'r', encoding='utf8') as log_1mg_in_file:
        log_1mg_in_file_reader = csv.reader(log_1mg_in_file)
        row = next(log_1mg_in_file_reader)
        startFrom = int(row[0])

    print('LogFound: Continuing From Index', startFrom)
    print('----------------------------------------------------------------------------------------------------------')
except FileNotFoundError:
    print('LogNotFound')
    if LOG_STRICT:
        print('LOG_STRICT Enabled: Exiting')
        print(
            '----------------------------------------------------------------------------------------------------------')
        exit(0)
    else:
        print('Strating From Index 1')
        print(
            '----------------------------------------------------------------------------------------------------------')

for drug_index, drug_name in enumerate(drug_names[startFrom:]):
    print('STARTING[', drug_index+1, '/', len(drug_names), ']', drug_name)
    print('----------------------------------------------------------------------------------------------------------')

    with open('log_1mg.csv', 'w', encoding='utf8') as log_1mg_out_file:
        log_1mg_out_file_writer = csv.writer(log_1mg_out_file)
        log_1mg_out_file_writer.writerow([drug_index, len(drug_names), drug_name])


    try:
        page_soup = get_soup(url+url_stage1+drug_name)
        try:
            divs_containing_s1_result = page_soup.find_all('div', {'class': 'col-xs-12 col-md-3 col-sm-4 SkuInfoCards__container___2BkSD'})
        except AttributeError:
            print('AttributeError: divs_containing_s1_result')

        for div_s1_index, div_s1 in enumerate(divs_containing_s1_result):
            try:
                url_to_s2 = div_s1.a['href']
                print('STAGE-1[', div_s1_index+1, '/', len(divs_containing_s1_result), ']', url_to_s2)
            except AttributeError:
                print('AttributeError: url_to_s2')

            s2_soup = get_soup(url+url_to_s2)

            try:
                lists_containing_s2_results = s2_soup.find('ul', {'class': 'gl item-list'})
                lists_found_in_s2(lists_containing_s2_results)
            except AttributeError:
                print('No Medicine Available')
    except urllib.error.HTTPError:
        print('HTTPError: No Match Found | Bad Gateway')


log_1mg_out_file.close()
log_1mg_in_file.close()
stage1_input_file.close()
