from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.ui as ui

chrome = webdriver.Chrome(executable_path= r'./driver/chromedriver')

with open('repos.txt') as f:
    lines = f.readlines()
    for l in lines:
        chrome.get(l)
        time.sleep(2)
        links_main = chrome.find_elements_by_tag_name('a')
        for link_main in links_main:
            if "Go to file" in link_main.text:
                files_href = link_main.get_attribute('href')
                #print(files_href)
                chrome.get(files_href)
                time.sleep(2)
                try:
                    tree = chrome.find_element_by_xpath('//*[@id="tree-browser"]')
                    links = tree.find_elements_by_tag_name('a')
                    for link in links:
                        dest_file = link.get_attribute('href')
                        if ".bag" in dest_file:
                            print(l.strip()+","+dest_file)
                except NoSuchElementException:
                    pass
                break
        time.sleep(3)

# def get_text(xpath):
#     time.sleep(0.2)
#     try:
#         print(chrome.find_element_by_xpath(xpath).text)
#     except NoSuchElementException:
#         print('None')


# def get_data(urls):
#     for url in urls:
#         chrome.get(url)
#         time.sleep(0.5)
#         print('-----------')
#         print('- Repository link: ' + url)
#         print('- Username:')
#         get_text('//*[@id="js-repo-pjax-container"]/div[1]/div[1]/div/h1/span[1]')
#         print('- Repository name:')
#         get_text('//*[@id="js-repo-pjax-container"]/div[1]/div[1]/div/h1/strong/a')
#         print('- About:')
#         get_text('//*[@id="js-repo-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[1]/div/p')
#         print('- Description:')
#         get_text('//*[@id="readme"]/div[3]/article/h2[1]')
#         print('- Contributors:')
#         get_text('//*[@id="js-repo-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[5]/div/h2/a')
#         print('- Languages:')
#         get_text('//*[@id="js-repo-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[5]/div/ul')
#         print('- Stars:')
#         get_text('//*[@id="js-repo-pjax-container"]/div[1]/div[1]/ul/li[2]/a[2]')
#         print('- Last Update:')
#         get_text('//*[@id="js-repo-pjax-container"]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[2]/a['
#                  '2]/relative-time')
#         print('-----------\n')


# options = Options()
# options.add_argument('--headless')
# chrome = webdriver.Chrome(executable_path='./driver/chromedriver', options=options)


# next_exists = False
# urls = []

# for q in search:
#     print('init')
#     chrome.get('https://github.com/search?q=' + q.replace(" ", "+"))
#     print("\n--- Searching for " + q + " ---\n")
#     time.sleep(2)

#     html_list = chrome.find_element_by_class_name("repo-list")
#     items = html_list.find_elements_by_tag_name("li")

#     for item in items:
#         first_div = item.find_element_by_class_name("mt-n1")
#         second_div = first_div.find_element_by_class_name("f4")
#         tag_a = second_div.find_element_by_class_name("v-align-middle")
#         link = tag_a.get_attribute("href")
#         urls.append(link)
#         print(urls)

#     try:
#         next_page = chrome.find_element_by_class_name('next_page')
#         next_page_class = next_page.get_attribute('class')
#         if 'disable' in next_page_class:
#             next_exists = False
#         else:
#             next_exists = True
#         print(next_exists)
#     except NoSuchElementException:
#         print('None')

#     while next_exists:
#         next_page.click()
#         time.sleep(2)
#         html_list = chrome.find_element_by_class_name("repo-list")
#         items = html_list.find_elements_by_tag_name("li")
#         time.sleep(2)
#         for item in items:
#             first_div = item.find_element_by_class_name("mt-n1")
#             second_div = first_div.find_element_by_class_name("f4")
#             tag_a = second_div.find_element_by_class_name("v-align-middle")
#             link = tag_a.get_attribute("href")
#             urls.append(link)
#             print(urls)
#         try:
#             next_page = chrome.find_element_by_class_name('next_page')
#             next_page_class = next_page.get_attribute('class')
#             if 'disable' in next_page_class:
#                 next_exists = False
#                 print('disable')
#             else:
#                 next_exists = True
#         except NoSuchElementException:
#             print('None')

# get_data(urls)
