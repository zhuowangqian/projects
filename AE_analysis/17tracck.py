from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as PE
from selenium.webdriver.common.proxy import Proxy, ProxyType
import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd

df = pd.read_excel(r'C:\Users\Administrator\Desktop\aliexpress\sunyou.xlsx', sheet_name='Sheet2')

service = Service(executable_path=r'C:\Users\Administrator\Desktop\python\ticket_purchase\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://www.17track.net/zh-cn')
# input()
time.sleep(1)
action = ActionChains(driver)
# print(df["logistics_number"])
for y in range(20, 101, 20):
    print(y)
    df1 = df['logistics_number'][:y].values
    x = ''
    logist_numbers = []
    for i in df1:
        logist_numbers.append(i)
        i = i + '\n'
        x = x + i
    logist_number_group = x
    logist_numbers_text = logist_number_group
    inp = driver.find_element(By.XPATH, '//*[@id="jsTrackBox"]/div[1]/div/div[6]')
    action.move_to_element(inp)
    action.send_keys_to_element(inp, logist_numbers_text)
    action.perform()
    # 遍历写入,太慢了
    # for index, logist_number in enumerate(logist_numbers):
    #     inp = driver.find_element(By.XPATH,
    #                               f'//*[@id="jsTrackBox"]/div[1]/div/div[6]/div[1]/div/div/div/div[5]/div[{index + 1}]/pre')
    #     action.move_to_element(inp)
    #     action.send_keys_to_element(inp, logist_number, Keys.ENTER)
    #     action.perform()

    driver.find_element(By.XPATH, '//*[@id="yqiTrackBtn"]').click()
    driver.refresh()
    input()
    # 进入主界面 /html/body/div[7]/div/div[6]/a[3]
    # 验证码识别
    for logist_number in logist_numbers:
        ship_from = driver.find_element(By.XPATH,
                                        f'//*[@id="tn-{logist_number}"]/div[1]/div[2]/div[1]/div[2]/div/span').text
        ship_to = driver.find_element(By.XPATH,
                                      f'//*[@id="tn-{logist_number}"]/div[1]/div[2]/div[3]/div[2]/div/span').text
        print(logist_number, ship_from, ship_to)
        ship_info = ''
        page = 1
        driver.find_element(By.XPATH, f'//*[@id="tn-{logist_number}"]/div[1]/div[3]').click()
        status = driver.find_element(By.XPATH, f'//*[@id="tn-{logist_number}"]/div[3]/div[1]/div/div[1]').text
        while True:
            try:
                ship_info_time = driver.find_element(By.XPATH,
                                                     f'//*[@id="tn-{logist_number}"]/div[3]/div[1]/dl/dd[{page}]/div/time').text

                ship_info_content = driver.find_element(By.XPATH,
                                                        f'//*[@id="tn-{logist_number}"]/div[3]/div[1]/dl/dd[{page}]/div/p').text

                ship_info = ship_info + '\n' + ship_info_time + '\n' + ship_info_content
                page += 1
            except:
                break
        print(ship_info)
    driver.back()
input()


# 验证码破解
# 单号无数据情况返回设定
# sql数据的读取和写入（包含excel)