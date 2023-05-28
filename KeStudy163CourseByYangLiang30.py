import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import re
from urllib.parse import unquote
import html2text


class KeStudy163CourseByYangLiang30(object):
    page_url = "https://study.163.com/"
    waitTimes = 30
    wait = None
    classLinks = []
    output = './output/d/'

    def __init__(self, driver, waitTimes=30):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, waitTimes)
        self.waitTimes = waitTimes
        self.init()

    def init(self):
        print(f'打开网址: {self.page_url}')
        self.driver.get(self.page_url)

        print(f'同意隐私条款')
        self.driver.find_element(By.XPATH, "//*[@id='ux-modal']/div[3]/span").click()

        print(f'打开登录页面, 请手动登录, 等待 {self.waitTimes}s')
        self.driver.find_element(By.XPATH, "//*[@id='j-nav-login']/span").click()

        self.wait.until_not(EC.visibility_of_element_located((By.XPATH, "//*[@id='j-nav-login']/span")))
        print(f'登录成功')

        print(f'进入: 我的学习')
        self.driver.find_element(By.XPATH, "//*[@id='j-nav-my-class']").click()

        print(f'请选择课程, 等待 {self.waitTimes}s')
        self.wait.until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[1])

        print(f'进入每日学习')
        self.driver.find_element(By.XPATH, "//span[@title='每日学习']").click()

        [ixvv.click() for ixvv in self.driver.find_elements('class name', 'ixVV')[2:]]
        self.classLinks = self.driver.find_elements('class name', 'sipq')[10:-48]

    def download(self):
        num = 1
        for linkBut in self.classLinks[0:]:
            try:
                self.driver.execute_script('arguments[0].click();', linkBut)
                self.wait.until(EC.number_of_windows_to_be(3))
                self.driver.switch_to.window(self.driver.window_handles[2])
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            except BaseException as e:
                print(f'{num} 似乎没有课程')
                self.driver.find_element(By.XPATH, "//*[@id='dialog']/div[2]/div[2]/a").click()
                num = num + 1
                continue

            try:
                if '网易云课堂' != self.driver.title:
                    try:
                        self.wait.until(
                            EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/article/section/div[2]/a")))
                        self.driver.find_element(By.XPATH, "//*[@id='root']/article/section/div[2]/a").click()
                        self.wait.until(
                            EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/article/section/div[2]/a")))
                    except BaseException as e:
                        print(f'*** {num} - {self.driver.title} 似乎没有内容')

                print(f'>>> [{num}/{len(self.classLinks)}] - {self.driver.title}')

                time.sleep(1)
                links = [element.get_attribute('src') for element in self.driver.find_elements(By.XPATH, "//*[@src]") if
                         not element.get_attribute('src').endswith('.js') and (
                                 '.mp3' in element.get_attribute('src') or '.mp4' in element.get_attribute(
                             'src') or element.get_attribute('src').startswith(
                             'https://ydschool') or element.get_attribute(
                             'src').startswith('http://ydschool') or element.get_attribute('src').startswith(
                             'https://nos.netease.com/ydschool') or element.get_attribute('src').startswith(
                             'http://nos.netease.com/ydschool') or element.get_attribute('src').startswith(
                             'https://edu-cms.nosdn.127.net') or element.get_attribute('src').startswith(
                             'http://edu-cms.nosdn.127.net'))]

                jpg_links = [link for link in links if link.endswith('.png') or link.endswith('.jpg')]
                if len(jpg_links) > 0:
                    for link in jpg_links:
                        vc = self.driver.find_element(By.XPATH, "//div[@data-poster='" + link + "']")
                        vc.click()
                        time.sleep(1)
                        vc.click()

                    time.sleep(1)
                    links = [element.get_attribute('src') for element in
                             self.driver.find_elements(By.XPATH, "//*[@src]") if
                             not element.get_attribute('src').endswith('.js') and (
                                     '.mp3' in element.get_attribute('src') or '.mp4' in element.get_attribute('src'))]

                title = re.sub(r'[\\/:*?"<>|]', '', self.driver.title)
                the_dir = self.output + f'{str(num)} - {title}/'
                if not os.path.exists(the_dir):
                    os.makedirs(the_dir)

                i = 1
                for link in links:
                    response = requests.get(link)
                    filename = link.split('/')[-1]
                    filename = re.sub(r'^\d+', '', filename)
                    filename = unquote(filename)
                    filename = the_dir + str(i) + '-' + filename
                    i = i + 1
                    with open(filename, 'wb') as file:
                        file.write(response.content)

                try:
                    with open(the_dir + title + '.all.html', 'w', encoding='utf-8') as file:
                        file.write(self.driver.page_source)
                    with open(the_dir + title + '.html', 'w', encoding='utf-8') as file:
                        file.write(self.driver.page_source.replace('https://edu-cms.nosdn.127.net/js/ydk/ydk-1.6.7.js',
                                                                   '').replace(
                            'https://crcdn.ydstatic.com/static/front-ke-tiku/dist/tiku/dist/vendor.1.2.0.bundle.js',
                            ''))
                except BaseException as e:
                    with open(the_dir + 'index.all.html', 'w', encoding='utf-8') as file:
                        file.write(self.driver.page_source)
                    with open(the_dir + 'index.html', 'w', encoding='utf-8') as file:
                        file.write(self.driver.page_source.replace('https://edu-cms.nosdn.127.net/js/ydk/ydk-1.6.7.js',
                                                                   '').replace(
                            'https://crcdn.ydstatic.com/static/front-ke-tiku/dist/tiku/dist/vendor.1.2.0.bundle.js',
                            ''))

            finally:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[1])
                num = num + 1
                time.sleep(1)
