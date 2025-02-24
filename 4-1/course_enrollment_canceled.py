"""사용법
수강신청 창 진입하고 q누르면 시작
강의 하나라도 잡으면 바로 이메일 발송. (네이버 이메일이 4초정도로 가장 빠름)
"""

from enhanced_selenium import EnhancedChrome
import random
import smtplib
from email.mime.text import MIMEText
import dotenv
import os

dotenv.load_dotenv()

# 장바구니에 담은 몇번째 강의를 신청할건지 (1부터 시작)
ls = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

web = EnhancedChrome(timeout=3, freq=0.01)
web.set_window_size(1920 * 3 // 4, 1080)
web.set_window_position(0, 0)
web.get("https://hana-prd-ap-4.ssu.ac.kr:8443/zu4a/zcmui2245")
id, pw = os.getenv("SOONGSIL_ID"), os.getenv("SOONGSIL_PW")
web.find(title="아이디 입력").send_keys(id)
web.find(title="비밀번호 입력").send_keys(pw + "\n")

try:
    web.find(id="sapSL_DEFAULT_BUTTON").click()
except:
    pass


def macro():
    while True:
        try:
            web.find(id="__button1").click("enter")
            web.wait(dur=0.5)

            for i in ls:
                idx = 1 + (i - 1) * 13
                try:
                    web.find(id=f"__button6-__clone{idx}").click()

                    return
                except:
                    pass

        except:
            pass

        web.wait(dur=random.uniform(0.5, 1))


web.wait_hotkey("q")
web._retry = lambda f: f()
macro()


def smtp():
    sender = os.getenv("NAVER_ID")
    receiver = os.getenv("NAVER_ID")
    subject = "수강신청"
    body = ""

    msg = MIMEText(body)
    msg["X-Priority"] = "1"
    msg["X-MSMail-Priority"] = "High"
    msg["Importance"] = "High"
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP("smtp.naver.com", 587) as server:
            server.starttls()
            server.login(sender, os.getenv("NAVER_PW"))
            server.sendmail(sender, receiver, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


smtp()
