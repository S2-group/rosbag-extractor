from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.ui as ui

chrome = webdriver.Chrome(executable_path= r'./driver/chromedriver')

with open('part-repos.txt') as f:
    lines = f.readlines()
    for l in lines:
        chrome.get(l)
        time.sleep(3)
        links_main = chrome.find_elements_by_tag_name('a')
        for link_main in links_main:
            if "Go to file" in link_main.text:
                files_href = link_main.get_attribute('href')
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
        time.sleep(5)