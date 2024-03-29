# 從google上爬取圖片

import time
import os, sys
import argparse
import urllib.request
from selenium import webdriver

category_num = 500  # 欲爬取每個種類的圖像張數

parser = argparse.ArgumentParser(
    description="Do you wish to scan for live hosts or conduct a port scan?")
parser.add_argument("-n",
                    dest='number',
                    action='store',
                    help='Number of downloads',
                    default=category_num)
parser.add_argument("-c",
                    dest='category',
                    action='store',
                    help='Name of category')
args = parser.parse_args()

f = open("classes.txt", "r", encoding='utf-8')
lines = f.readlines()
f.readline()
for line in lines:
    line = line.strip('\n')
    print(line)
    args.category = line

    current_path = os.path.abspath(os.getcwd())
    Path = current_path + '\image'
    if (args.category):
        save_path = os.path.join(Path, args.category)
        category = args.category
        url = "https://www.google.com.tw/search?q=" + category + "&source=lnms&tbm=isch&sa=X"
    else:
        sys.exit("Error! Category not define!")

    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    if (args.number):
        target_num = int(args.number)
    else:
        print("Undefined Target Number(default value:1000)")
        target_num = 1000

    # The path of ChromeDriver
    chromeDriver = current_path + r'/chromedriver.exe'

    # Target element xpath
    xpath = "//img[contains(@class,'Q4LuWd')]"

    # Ignition chrome
    driver = webdriver.Chrome(chromeDriver)

    # Maximize browser window size
    driver.maximize_window()

    pos = 0
    photo_num = 0
    Idle_count = 0
    done = False
    img_url_dic = {}
    driver.get(url)

    while not done:
        pos += 500
        js = "document.documentElement.scrollTop=%d" % pos
        driver.execute_script(js)
        time.sleep(5)

        for element in driver.find_elements_by_xpath(xpath):
            try:
                img_url = element.get_attribute('src')

                if img_url != None and not img_url in img_url_dic:
                    img_url_dic[img_url] = ''
                    Idle_count = 0
                    photo_num += 1
                    filename = category + '_' + str(photo_num) + '.jpg'
                    print(filename)
                    urllib.request.urlretrieve(
                        img_url, os.path.join(save_path, filename))
                else:
                    Idle_count += 1

                if photo_num >= target_num or Idle_count >= 2000:
                    done = True
                    break
            except OSError:
                print('Occur OSError!')
                print(pos)
                break

    print("[{}]\nPython crawler download progress is completed.".format(
        category))
    print("Total downloaded %d images\n" % photo_num)
    driver.close()