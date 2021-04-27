# Facebook Profile Scrap / fb-scrapping

## About

* Facebook Profile scrapping

### Features

## Code
```
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile



#Load FireFox Profile
profile = FirefoxProfile(r'C:\Users\lapt\AppData\Roaming\Mozilla\Firefox\Profiles\g1mwnsjp.default-release')
url = input("Enter the profile url :") #Get Url
binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe") #Set Binary
# driver = webdriver.Firefox(firefox_binary=binary, executable_path="C:\\geckodriver.exe", firefox_profile=profile)
driver = webdriver.Firefox(firefox_binary=binary, executable_path="C:\\Users\\lapt\\PycharmProjects\\facebook_help_needed\\geckodriver.exe")
# driver = webdriver.Firefox()
driver.get('https://www.facebook.com')
time.sleep(10)
driver.find_element_by_xpath("//input[@name='email']").send_keys('')
password = driver.find_element_by_xpath("//input[@name='pass']")
password.send_keys('')
password.submit()
time.sleep(20)
na = url.split('https://www.facebook.com/')
print(na[1]) #Profile Name
driver.get(url)
time.sleep(5)
com_names = []
com_links = []
com_texts = []
names_list = []
names_links = []
time.sleep(5)
i=-1
while True:
    try:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        main_div = driver.find_element_by_xpath('//div[@data-pagelet="ProfileTimeline"]')
        divs = main_div.find_elements_by_xpath('.//div[@class="j83agx80 cbu4d94t"]')
        if len(divs) > 5:
            for i in range(i+1,len(divs)):
                com_names = []
                com_links = []
                com_texts = []
                names_list = []
                names_links = []
                print('post: '+str(i))
                driver.execute_script("arguments[0].scrollIntoView();", divs[i])
                action = ActionChains(driver)
                action.move_to_element(divs[i]).perform()
                time.sleep(13)
                p_name = divs[i].find_element_by_xpath('.//div[@class="nc684nl6"]//span').text  # poster's name
                pi_link = driver.find_elements_by_xpath('.//div[@class="nc684nl6"]//a')[i]
                p_link = pi_link.get_attribute('href')
                post_content = driver.find_elements_by_xpath('//div[@class="l9j0dhe7"]')[i]
                st_link = driver.find_elements_by_xpath('//div[@class="l9j0dhe7"]//a')[i]
                post_link = st_link.get_attribute('href')
                with open(f"Facebook{na[1]}.txt", 'a+', encoding='utf-8') as f:
                    f.write("Posted By :" f'{p_name}\n\n')
                    f.write("\tPosters Link :" f'{p_link}\n\n\n')
                    f.write("\t\tContent Link :" f'{post_link}\n\n\n')
                f.close()

                likes_button = divs[i].find_elements_by_xpath('//span[@class="pcp91wgn"]')
                driver.execute_script("arguments[0].click();", likes_button[i]);  # Likes Button Click
                time.sleep(3)
                likes_div = driver.find_element_by_css_selector(
                    'div.q5bimw55.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.eg9m0zos.l9j0dhe7.du4w35lb.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.kh7kg01d.c3g1iek1.otl40fxz.cxgpxx05.rz4wbd8a.sj5x9vvc.a8nywdso')
                current_len = len(likes_div.find_elements_by_xpath('//div[@class="q9uorilb"]//a'))
                while True:
                    likes_div.find_element_by_xpath('.//div[@class="q9uorilb"]//a').send_keys(Keys.END)
                    try:
                        WebDriverWait(driver, 5).until(
                            lambda x: len(driver.find_elements_by_xpath('.//div[@class="q9uorilb"]//a')) > current_len)
                        current_len = len(driver.find_elements_by_xpath('.//div[@class="q9uorilb"]//a'))
                    except TimeoutException:
                        name_eles = [name_ele for name_ele in
                                     driver.find_elements_by_xpath('.//div[@class="q9uorilb"]//a')]
                        time.sleep(5)
                        for name in name_eles:
                            names_list.append(name.text)
                            n_li = name.get_attribute('href')
                            with open(f"Facebook{na[1]}.txt", 'a+', encoding='utf-8') as f:
                                f.write("\t\t\tLiked By :" f'{name.text}\n')
                                f.write("\t\t\t\tLiker's Profile Link :" f'{n_li}\n\n')
                            f.close()
                        close = driver.find_element_by_xpath('//div[@class="cypi58rs pmk7jnqg fcg2cn6m tkr6xdv7"]//div')
                        driver.execute_script("arguments[0].click();", close);
                        break
                try:
                    while True:
                        try:
                            more_comments = divs[i].find_element_by_xpath('.//span[@class="j83agx80 fv0vnmcu hpfvmrgz"]')
                            driver.execute_script("arguments[0].click();", more_comments);
                            time.sleep(5)
                        except:
                            comment_div = divs[i].find_elements_by_css_selector(
                                'div.g3eujd1d.ni8dbmo4.stjgntxs.hv4rvrfc')
                            for comment in comment_div:
                                com_name = comment.find_element_by_xpath('.//a').text
                                com_names.append(com_name)
                                com_link = comment.find_element_by_xpath('.//a').get_attribute('href')
                                com_links.append(com_link)
                                try:
                                    com_text = comment.find_element_by_xpath(
                                        './/div[@class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"]').text
                                except:
                                    com_text = ""
                                com_texts.append(com_text)
                            break
                    for co_name, co_link, co_text in zip(com_names, com_links, com_texts):
                        with open(f"Facebook{na[1]}.txt", 'a+', encoding='utf-8') as f:
                            f.write("\t\t\t\t\tComment by :" f'{co_name}\n\n')
                            f.write("\t\t\t\t\tCommenter's link " f'{co_link}\n\n')
                            f.write("\t\t\t\t\tComment Text :" f'{co_text}\n\n')
                        f.close()
                except:
                    pass
    except:
        pass
```

[![Build Status](https://qa.nuxeo.org/jenkins/buildStatus/icon?job=/nuxeo/addons_nuxeo-sample-project-master)](https://qa.nuxeo.org/jenkins/job/nuxeo/job/addons_nuxeo-sample-project-master/)

### Content

Facebook Profile scrapping

### Requirements

- Install Python
- Install Selenium Python Package
