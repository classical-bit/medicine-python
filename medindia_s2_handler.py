from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import csv
from time import sleep

drug_address = list()


def get_soup(url_string):
    client = urlopen(url_string)
    page_content = client.read()
    client.close()
    return soup(page_content, 'html5lib')


def self_func(count_drugs):
    try:
        with open('drug_detail_s2_filter.csv', 'a', encoding='utf8', newline='') as csv_file_out:
            main_writer = csv.writer(csv_file_out)
            for drug_address_element in drug_address[count_drugs:]:
                page_soup = get_soup(drug_address_element[1])
                drug_content_list = list()

                try:
                    flag_check_more = None
                    flag_check_more = page_soup.find('a', {'class': 'view-all pull-right'}).text
                    page_more_soup = get_soup(page_soup.find('a', {'class': 'view-all pull-right'})['href'])
                    all_extra_substitutes = page_more_soup.find_all('td', {'class': ' report-content'})
                except AttributeError:
                    # print('\tAttributeError: flag_check_more', flag_check_more)
                    pass

                try:
                    all_substitutes = None
                    all_substitutes = page_soup.find('div', {'class': 'links'}).find_all('a')
                except AttributeError:
                    # print('\tAttributeError: all_substitutes', all_substitutes)
                    pass

                try:
                    drug_contents = page_soup.find_all('p', {'class': 'drug-content'})
                except AttributeError:
                    print('\tAttributeError: drugs_contents')


                if flag_check_more is None and all_substitutes is None:
                    print('\tNoSubsFound...')
                    with open('drugs_with_no_subs.csv', 'a', encoding='utf8', newline='') as no_sub_file:
                        sub_writer = csv.writer(no_sub_file)
                        sub_writer.writerow([drug_address_element[0]])
                    no_sub_file.close()
                    print('\tLOGGED: \'drugs_with_no_subs.csv\'')

                elif flag_check_more is None:
                    with open(drug_address_element[0] + '.csv', 'a', encoding='utf8', newline='') as sub_file:
                        sub_writer = csv.writer(sub_file)
                        for all_substitute in all_substitutes:
                            sub_writer.writerow([all_substitute.text, all_substitute['href']])
                    sub_file.close()
                    print('\tCREATED: ', drug_address_element[0] + '.csv')
                else:
                    print('\tMoreSubsFound...')
                    with open(drug_address_element[0] + '.csv', 'a', encoding='utf8', newline='') as sub_file:
                        sub_writer = csv.writer(sub_file)
                        for extra_substitute in all_extra_substitutes:
                            sub_writer.writerow([extra_substitute.a.text, extra_substitute.a['href']])
                    sub_file.close()
                    print('\tCREATED: ', drug_address_element[0] + '.csv')

                for drug_content in drug_contents:
                    drug_content_list.append(str.replace(drug_content.text, '\n', ''))

                if len(drug_content_list) == 0:
                    print('**********************************************')
                    print("D.O.S: Try After An Appropiate Long Break")
                    print('**********************************************')

                    # Comment Out Below Before SetOn Auto
                    exit(0)
                    # Uncomment Code To SetOn Auto
                    # Initial Break Time in Minutes
                    # break_time = 10
                    # sleep(break_time)
                    # break_time += 5
                    # self_func(count_drugs)

                elif len(drug_content_list) == 7:
                    main_writer.writerow([
                        drug_address_element[0],
                        'INDICATION: ' + drug_content_list[0],
                        'CONTRADICTION: ' + drug_content_list[1],
                        'DOSAGE: ' + drug_content_list[2],
                        'HOWTOTAKE: ' + drug_content_list[3],
                        'WARNINGS: ' + drug_content_list[4],
                        'SIDEEFFECTS: ',
                        'PRECAUTION: ' + drug_content_list[5],
                        'STORAGE: ' + drug_content_list[6],
                    ])
                elif len(drug_content_list) == 8:
                    main_writer.writerow([
                        drug_address_element[0],
                        'INDICATION: ' + drug_content_list[0],
                        'CONTRADICTION: ' + drug_content_list[1],
                        'DOSAGE: ' + drug_content_list[2],
                        'HOWTOTAKE: ' + drug_content_list[3],
                        'WARNINGS: ' + drug_content_list[4],
                        'SIDEEFFECTS: ' + drug_content_list[5],
                        'PRECAUTION: ' + drug_content_list[6],
                        'STORAGE: ' + drug_content_list[7],
                    ])
                elif len(drug_content_list) == 9:
                    main_writer.writerow([
                        drug_address_element[0],
                        'INDICATION: ' + drug_content_list[0],
                        'CONTRADICTION: ' + drug_content_list[1],
                        'DOSAGE: ' + drug_content_list[2],
                        'HOWTOTAKE: ' + drug_content_list[3],
                        'WARNINGS: ' + drug_content_list[4],
                        'SIDEEFFECTS: ' + drug_content_list[5],
                        'PRECAUTION: ' + drug_content_list[6],
                        'INTERACTION: ' + drug_content_list[7],
                        'STORAGE: ' + drug_content_list[8],
                    ])
                elif len(drug_content_list) == 10:
                    main_writer.writerow([
                        drug_address_element[0],
                        'OVERVIEW: ' + drug_content_list[0],
                        'INDICATION: ' + drug_content_list[1],
                        'CONTRADICTION: ' + drug_content_list[2],
                        'DOSAGE: ' + drug_content_list[3],
                        'HOWTOTAKE: ' + drug_content_list[4],
                        'WARNINGS: ' + drug_content_list[5],
                        'SIDEEFFECTS: ' + drug_content_list[6],
                        'PRECAUTION: ' + drug_content_list[7],
                        'INTERACTION: ' + drug_content_list[8],
                        'STORAGE: ' + drug_content_list[9],
                    ])
                elif len(drug_content_list) < 7 or len(drug_content_list) > 10:
                    print('\tColumnMismatch... ')
                    with open('drug_columns_dismatch.csv', 'a', encoding='utf8', newline='') as dismatch_file:
                        dimatch_file_writer = csv.writer(dismatch_file)
                        dimatch_file_writer.writerow([drug_address_element[0]])
                    dismatch_file.close()
                    print('\tLOGGED: \'drug_columns_dismatch.csv\'')

                    # with open('dismatch_'+drug_address_element[0]+'.csv', 'a', encoding='utf8', newline='')
                    # as dismatch_drug_file:
                    #     dismatch_drug_writer = csv.writer(dismatch_drug_file)
                    #     for content in drug_content_list:
                    #         dismatch_drug_writer.writerow([content])
                    # dismatch_drug_file.close()

                    main_writer.writerow(drug_content_list)

                count_drugs += 1
                with open('log_medindia_s2.csv', 'w', encoding='utf8') as log_file:
                    log_writer = csv.writer(log_file)
                    log_writer.writerow([count_drugs, len(drug_address), drug_address_element[0]])
                log_file.close()

                print('DONE:', count_drugs, '/', len(drug_address), '[', drug_address_element[0], ']')
                print('----------------------------------------------')
    finally:
        csv_file_out.close()


try:
    with open('drug_details_from_medindia.csv', 'r', encoding='utf8') as csv_file_in:
        reader = csv.reader(csv_file_in)

        for row in reader:
            drug_address.append((row[0], row[2]))
except FileNotFoundError:
    print("FileNotFound: \'drug_details_from_medindia.csv\'")
finally:
    try:
        csv_file_in.close()
    except NameError:
        pass

try:
    with open('log_medindia_s2.csv', 'r', encoding='utf8') as log_file_in:
        log_reader = csv.reader(log_file_in)
        for row in log_reader:
            countDrugs = int(row[0])
            print('----------------------------------------------')
            print('LogFound: Continuing From index', countDrugs)
            print('----------------------------------------------')
            self_func(countDrugs)
except IndexError:
    pass
except FileNotFoundError:
    countDrugs = 0
    print('----------------------------------------------')
    print('LogNotFound: Starting from index 1')
    print('----------------------------------------------')
    self_func(countDrugs)
