from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import time
from datetime import datetime

import keyboard

XPATH = By.XPATH
CLASS_NAME = By.CLASS_NAME

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

safety_delay = 0.1
safety_time = 4

def safety(func) :
    for _ in range(int(safety_time / safety_delay)) :
        try :
            return func()
        except WebDriverException :
            time.sleep(safety_delay)
    
    raise WebDriverException


def url(path) :
    safety(lambda : driver.get(path))


def find(path, by=XPATH, parent=driver) :
    return safety(lambda : parent.find_element(by, path))


def finds(path, by=XPATH, parent=driver) : 
    return safety(lambda : parent.find_elements(by, path))


def iframe(path = "default", by=XPATH) :
    if path == "default" :
        safety(driver.switch_to.default_content)
    else :
        safety(lambda : driver.switch_to.frame(find(path, by)))


def sendkeys(path, input, by=XPATH, parent=driver) :
    safety(lambda : find(path, by, parent).send_keys(input))


def click(path, by=XPATH, parent=driver) :
    safety(find(path, by, parent).click())



# 사용자 로그인 후

# 새로고침 화면에서 n6초마다 새로고침 버튼누르게 세팅해놓기.
# while True :
   
# 들어가지면 버튼 누르게 하기
cnt = 1

def on_f_pressed(event):
    global cnt
    try :
      driver.find_element(By.XPATH, f'//*[@id="__button6-__clone{cnt}"]').click()
    except :
        print(f'실패')
    print(cnt)
    cnt += 13
    


keyboard.on_press_key('f', on_f_pressed)

keyboard.wait('esc')

# url('https://lms.ssu.ac.kr/')
# click('//*[@id="visual"]/div/div[2]/div[2]/a')
# sendkeys('//*[@id="userid"]', my_id)
# sendkeys('//*[@id="pwd"]', my_pw)
# click('//*[@id="sLogin"]/div/div[1]/form/div/div[2]/a')
# click('//*[@id="xnm2_content"]/div[1]/div[1]/div[1]/div/a')
# time.sleep(5)
# iframe('//*[@id="fulliframe"]')


# while True :
#     try :
#         subjects = finds('//span[@class="xntc-title" and text()="동영상"]/../a[number(text())>0]')
#     except Exception :
#         break
    
#     my_sub = None
#     titles = None
#     for subject in subjects :
#         click('../../../../div[1]/button', parent=subject)
#         time.sleep(2)
#         titles = [title.text for title in reversed(finds('//i[@class="xnsti-left-icon video"]/../a'))]
#         titles = [title for title in titles if title not in ban_list]
#         if len(titles) > 0 :
#             my_sub = subject
#             break
#     else :
#         print('완료.')
#         break

#     my_sub.click()
#     for title in titles:
#         iframe()
#         iframe('//*[@id="tool_content"]')
#         click(f'//i[contains(@class, "zoom") or contains(@class, "movie") or contains(@class, "mp4")]/..//a[text()="{title}"]')
#         time.sleep(5)
#         iframe()
#         iframe('//*[@id="tool_content"]')
#         iframe('//*[@id="root"]/div/div[2]/div[2]/iframe')
#         click('//*[@id="front-screen"]/div/div[2]/div[1]/div') # 영상 재생 버튼
#         time.sleep(7)
#         try : 
#             click('//*[@id="confirm-dialog"]/div/div/div[2]/div[1]') # 영상 이어 보기 버튼
#         except Exception :
#             pass
#         time.sleep(3)

#         iframe()
#         iframe('//*[@id="tool_content"]')

#         total_duration = find('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/span/span[2]').text
#         total_duration = gettime(total_duration)
#         current_time = find('//span[@class="xnvc-progress-info-text" and position()=2]').text

#         current_time = current_time.split('(')[0]
#         current_time = gettime(current_time)

#         time_left = (total_duration - current_time).total_seconds()
#         time.sleep(time_left)
#         driver.back()
#         time.sleep(1)
#         try :
#             driver.switch_to.alert.accept()
#         except Exception :
#             pass
        
#     time.sleep(5)
#     iframe()
#     click('//*[@id="context_external_tool_67_menu_item"]/a')
#     time.sleep(5)
#     iframe('//*[@id="tool_content"]')



