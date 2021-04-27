import sys
import time
import traceback
import getpass
import tkinter as tk
import xlsxwriter
from PIL import Image, ImageChops
from io import BytesIO
import lxml.html
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os

chrome_path = r'C:\Users\lapt\PycharmProjects\facebook\chromedriver'
driver = webdriver.Chrome(executable_path=chrome_path)
driver.get('https://www.google.co.in')

try:
    try:
        os.mkdir('./screenshots/')
    except:
        pass
    # *************************************************************************
    # User is prompted to provide facebook username, password and profile link
    # *************************************************************************
    username = input("Please enter username: ")
    password = getpass.getpass('Please enter password: ')
    profile_path = input("Please enter the name of the file with profiles: ") or "input_profiles.txt"
    # profile_path = input("Please enter profile link here: ")

    f = open("input_profiles.txt", 'r')
    lines = f.readlines()
    f.close()

    # *******************************************************************************
    # This section logs into facebook, opens profile link and scrolls to end of page
    # *******************************************************************************
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-notifications')
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.headless = True
    browser = webdriver.Chrome(options=options)
    # browser.set_window_size(1920, 1080)
    url = "https://web.facebook.com/login/"
    # url = 'https://whatismyipaddress.com/proxy-check'
    browser.get(url)

    login_username = browser.find_element_by_id('email')
    login_password = browser.find_element_by_id('pass')

    login_username.send_keys(username)
    login_password.send_keys(password)

    browser.find_element_by_id('loginbutton').click()
    time.sleep(2)

    for line in lines:
        # line=profile_path
        profile = line.split('/')[3].strip()
        pf = profile.split("id=")
        if len(pf) > 1:
            profile = pf[1]

        print("Scraping: " + profile)
        try:
            os.mkdir(f'./screenshots/{profile}')
            os.mkdir(f'./screenshots/{profile}/newtab')
        except:
            pass

        browser.get(line)
        time.sleep(5)
        last_height = browser.execute_script("return document.body.scrollHeight")

        count = 0
        counter = 1

        element = browser.find_element_by_xpath(
            '//body/div[@class = "_li"]/div[@id = "globalContainer"]/div[@class = "fb_content clearfix "]/div/div[@id = "mainContainer"]/div[@id = "contentCol"]/div[@id = "contentArea"]/div[@id = "pagelet_timeline_main_column"]/div[@id = "pagelet_main_column_personal"]/div[@id = "timeline_tab_content"]/div[@class="clearfix _ikh _3-8y"]/div[2]/div[@id = "timeline_story_column"]')  # find the part of the page you want to crop
        location = element.location
        size = element.size
        root = tk.Tk()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        current_height = location['y'] - 90
        scroll_height = 99999999
        rep_count = 0

        js_delete = """var elements = document.getElementsByClassName(\"_5pcr userContentWrapper\");
                        var itr;
                        for (itr=0; itr < elements.length - 10; itr++){
                            elements[itr].remove();
                        }
                    """

        js_delete2 = """var elements = document.getElementsByClassName(\"_5pcb _4b0l _2q8l\");
                        var itr;
                        for (itr=0; itr < 1; itr++){
                            elements[itr].remove();
                        }
                    """

        shot_count = 0
        run_count = 0

        browser.execute_script("window.scrollBy(0,50)")

        try:
            os.mkdir("./Posts/")
        except:
            pass

        title = "Profile"
        title = browser.find_element_by_xpath('//a[@class="_2nlw _2nlv"]').text
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(f'./Posts/{profile}.xlsx')

        cell_border = workbook.add_format()
        cell_border.set_border()
        cell_border.set_text_wrap()

        cell_format = workbook.add_format()
        cell_format.set_border()
        cell_format.set_text_wrap()
        cell_format.set_font_color('red')

        worksheet = workbook.add_worksheet(title)
        worksheet.write('A1', 'POST DATE ', cell_border)
        worksheet.write('B1', 'POST ID', cell_border)
        worksheet.write('C1', 'TEXT POST', cell_border)
        worksheet.write('D1', 'IMAGE POST', cell_border)
        worksheet.write('E1', 'EXTERNAL LINK POST', cell_border)
        worksheet.write('F1', 'LIFE EVENT POST', cell_border)
        worksheet.write('G1', 'LIFE EVENT ADDITIONAL TEXT', cell_border)
        worksheet.write('H1', 'COMMENTS AND REPLIES', cell_border)

        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 40)
        worksheet.set_column(2, 6, 70)
        worksheet.set_column(7, 7, 120)

        k = 0

        while True:
            browser.execute_script("window.scrollBy(0,50)")

            ##***************************************************************************************************************
            ## This section looks for hyperlinks(view xx more comments; see more; replied xx replies) and clicks on each one
            ##***************************************************************************************************************
            agg_link = []
            agg_link += browser.find_elements_by_xpath('//span[@class = " _4ssp"]')
            agg_link += browser.find_elements_by_xpath('//span[@class = "_4sso _4ssp"]')
            agg_link += browser.find_elements_by_xpath('//a[@class = "_5v47 fss"]')
            temp_links = []
            for tp in browser.find_elements_by_xpath("//a[contains(@onclick,'var func = function(e)')]"):
                if tp.is_displayed():
                    temp_links.append(tp)
                else:
                    continue
            agg_link += temp_links
            agg_link = agg_link + browser.find_elements_by_xpath('//a[@class = "see_more_link"]')
            agg_link = agg_link + browser.find_elements_by_xpath("//*[@class = '_4sxc _42ft']")
            agg_link = agg_link + browser.find_elements_by_xpath("//a[@class = '_5v47 fss']")
            agg_link = agg_link + browser.find_elements_by_xpath(
                '//span[@class = "text_exposed_link"]/a[@class = "see_more_link"]')
            if agg_link:
                for i in range(len(agg_link)):
                    try:
                        browser.execute_script("arguments[0].click();", agg_link[i])
                    except:
                        pass

            agg_link = []
            agg_link += browser.find_elements_by_xpath('//span[@class = " _4ssp"]')
            agg_link += browser.find_elements_by_xpath('//span[@class = "_4sso _4ssp"]')
            agg_link += browser.find_elements_by_xpath('//a[@class = "_5v47 fss"]')
            temp_links = []
            for tp in browser.find_elements_by_xpath("//a[contains(@onclick,'var func = function(e)')]"):
                if tp.is_displayed():
                    temp_links.append(tp)
                else:
                    continue
            agg_link += temp_links
            agg_link = agg_link + browser.find_elements_by_xpath('//a[@class = "see_more_link"]')
            agg_link = agg_link + browser.find_elements_by_xpath("//*[@class = '_4sxc _42ft']")
            agg_link = agg_link + browser.find_elements_by_xpath("//a[@class = '_5v47 fss']")
            agg_link = agg_link + browser.find_elements_by_xpath(
                '//span[@class = "text_exposed_link"]/a[@class = "see_more_link"]')
            if agg_link:
                for i in range(len(agg_link)):
                    try:
                        browser.execute_script("arguments[0].click();", agg_link[i])
                        time.sleep(0.5)
                    except:
                        pass

            if current_height > last_height + screen_height:
                current_height = last_height
                ##************************************************************************************************************
            ## This section screenshots each scroll down and crops out the timeline area and saves in a folder
            ##************************************************************************************************************
            try:
                screen = browser.find_element_by_xpath('//div[@class="_5pcr userContentWrapper"]')
            except:
                time.sleep(5)
                screen = browser.find_elements_by_xpath('//div[@class="_5pcr userContentWrapper"]')
                while not screen:
                    screen = browser.find_elements_by_xpath('//div[@class="_5pcr userContentWrapper"]')
                    browser.save_screenshot(f"./screenshots/{profile}/" + "dummy1.png")
                    browser.save_screenshot(f"./screenshots/{profile}/" + "dummy2.png")
                    imshot = Image.open(
                        f"./screenshots/{profile}/" + "dummy1.png")  # uses PIL library to open image in memory
                    imshot = imshot.crop((left, 90, right, screen_height - 80))  # defines crop points
                    imshot.save(f"./screenshots/{profile}/" + "dummy1.png")
                    imshot = Image.open(
                        f"./screenshots/{profile}/" + "dummy2.png")  # uses PIL library to open image in memory
                    imshot = imshot.crop((left, 90, right, screen_height - 80))  # defines crop points
                    imshot.save(f"./screenshots/{profile}/" + "dummy2.png")
                    check1 = Image.open(f"./screenshots/{profile}/" + "dummy1.png").convert('RGB')
                    check2 = Image.open(f"./screenshots/{profile}/" + "dummy2.png").convert('RGB')
                    diff = ImageChops.difference(check1, check2)
                    time.sleep(5)
                    if diff.getbbox():
                        shot_count = 0
                    else:
                        shot_count += 1
                        if shot_count > 5:
                            print("Break")
                            break
                try:
                    screen = screen[0]
                except:
                    break

            loc = screen.location
            siz = screen.size
            left = loc['x']
            top = loc['y']
            right = loc['x'] + siz['width']
            bottom = loc['y'] + siz['height']
            current_height = top - 100

            while current_height < bottom - (0.553 * screen_height) + 300:
                # print(f"Screenshot {current_height}")
                browser.execute_script("window.scrollTo(arguments[0], arguments[1]);", 0, current_height)
                time.sleep(0.5)
                browser.save_screenshot(f"./screenshots/{profile}/" + str(counter) + ".png")
                ## Calculate new scroll height and compare with last scroll height.
                imshot = Image.open(
                    f"./screenshots/{profile}/" + str(counter) + ".png")  # uses PIL library to open image in memory
                imshot = imshot.crop((left, 90, right, screen_height - 80))  # defines crop points
                imshot.save(f"./screenshots/{profile}/" + str(counter) + ".png")
                current_height = current_height + (0.553 * screen_height)
                counter = counter + 1

                # time.sleep(5)

            ## ************************************************************************************************************
            ## This section saves post, replies and comments
            ## ************************************************************************************************************
            text = browser.find_element_by_xpath('//div[@class="_5pcb _4b0l _2q8l"]')
            pid = text.get_attribute("id").rsplit(':', 1)[-1]
            if pid == str(0):
                pid = text.get_attribute("id").rsplit(':', 2)[-2]
            if pid == str(1):
                pid = text.get_attribute("id").rsplit(':', 2)[-2]

            print(pid)
            details = text.get_attribute('innerHTML')
            tree = html.fromstring(details)

            colC = ""
            colD = ""
            colE = ""
            colF = ""
            colG = ""
            postdate = tree.xpath('//span[@class="timestampContent"]')
            linkpost = tree.xpath('//div[@class="_6ks"]/a')
            textpost = tree.xpath('//div[@data-testid="post_message"]')
            lifepost = tree.xpath('//div[@class="_52jv"]')
            lifeposttext = tree.xpath('//div[@class="_3-8x"]')
            imgpost = tree.xpath('//img[@class="_46-i img"]')
            replies = []
            qq = tree.xpath('//ul[@class="_7791"]/li')
            commentandreply = []
            if qq:
                for j in range(len(qq)):

                    details2 = lxml.html.tostring(qq[j])
                    tree2 = html.fromstring(details2)
                    comments = tree2.xpath('//div[contains(@class,"_4eek clearfix _4eez")]')
                    if comments:
                        print(comments[0].text_content())
                    commentandreply.append(comments[0].text_content())

                    replies = tree2.xpath('//div[@class = "_4eek _4efk clearfix clearfix"]')
                    if replies:
                        for element in replies:
                            print(element.text_content())
                            commentandreply.append("REPLY: " + element.text_content())
            else:
                commentandreply.append("no comments")
            if textpost:
                print(textpost[0].text_content())
                colC = textpost[0].text_content()
            if linkpost:
                print(linkpost[0].attrib['href'])
                colE = linkpost[0].attrib['href']
            if lifepost:
                print(lifepost[0].text_content())
                colF = lifepost[0].text_content()
            if lifeposttext:
                print(lifeposttext[0].text_content())
                colG = lifeposttext[0].text_content()
            if not lifepost and not textpost:
                print("Post is an image")
            if imgpost:
                print(imgpost[0].attrib['src'])
                colD = imgpost[0].attrib['src']

            worksheet.write('A' + str(k + 2), postdate[0].text_content(), cell_border)
            worksheet.write('B' + str(k + 2), pid, cell_border)
            worksheet.write('C' + str(k + 2), colC, cell_border)
            worksheet.write('D' + str(k + 2), colD, cell_border)
            worksheet.write('E' + str(k + 2), colE, cell_border)
            worksheet.write('F' + str(k + 2), colF, cell_border)
            worksheet.write('G' + str(k + 2), colG, cell_border)
            worksheet.write('H' + str(k + 2), '\n\n'.join(commentandreply), cell_border)
            k += 1

            browser.execute_script(js_delete2)
            time.sleep(1)
            run_count += 1

        workbook.close()
        print(f"Finished scraping {profile}")
        # # browser.quit()


except Exception as e:
    print("Error: " + str(e))
    print(traceback.format_exc())
    time.sleep(30)