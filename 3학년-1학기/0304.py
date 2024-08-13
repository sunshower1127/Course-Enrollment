from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import time
import keyboard
from datetime import datetime

XPATH = By.XPATH
CLASS_NAME = By.CLASS_NAME

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

'''
새창으로 이동
'''
def on_q_pressed(event):
    try:
        driver.switch_to.window(driver.window_handles[-1])
    except:
        print('새창이동 에러')


'''
수동 새로고침
'''
def on_w_pressed(event):
    driver.refresh()


idx = 1
'''
신청 버튼
'''
def on_e_pressed(event):
    global idx
    on_q_pressed(None)
    try :
        driver.find_element(By.XPATH, f'//*[@id="__button6-__clone{idx}"]').click()
    except :
        print('신청버튼 에러')

'''
다음 강의준비
'''
def on_r_pressed(event):
    global idx
    idx += 13
    print(f'{(idx-1)//13 + 1}번째로 세팅완료')



# def on_f_pressed(event):
#     N = 9
#     while True :
#         refresh_btn = None
#         for i in range(10000) :
#             try :
#                 time.sleep(0.01)
#                 refresh_btn = driver.find_element(By.ID, '__button1')
#                 break
#             except :
#                 continue
        
#         print('ok')
#         refresh_btn.click()
#         html_tag = driver.find_element(By.XPATH, '/html')
#         for i in range(10000) :
#             if 'sapUiBLyBack' in html_tag.get_attribute('class') :
#                 time.sleep(0.01)
#             else :
#                 break

'''
Q -> 새 창으로 이동
W -> 새로고침
E -> 신청 버튼
R -> 다음 강의

Q는 한번만 누르고,
네이비즘 켜고 W 누르면서 시간 맞추기.
들어가졌을때, 아직 테스트는 못했는데
E누르면서 

'''


keyboard.on_press_key('q', on_q_pressed)
keyboard.on_press_key('w', on_w_pressed)
keyboard.on_press_key('e', on_e_pressed)
keyboard.on_press_key('r', on_r_pressed)

keyboard.wait('esc')
