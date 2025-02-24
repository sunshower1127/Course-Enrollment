"""사용법
1. clock.py 띄워놓고
2. 콘솔에 "x.x"초 입력해서 새로고침 테스트함.
3. 몇초에 누를건지 결정했으면 ENTER 누르고 최종시간 적으면됨. (예: "10:00:00.5") (tip: 0.1초 여유둬야함)
4. 진입되면 바로 몇번째 강의 수강신청할건지 키보드로 누르면됨 (예: 장바구니에서 2번째 강의 신청하려면 2 누르기)
5. 다했으면 esc 누르면 끝 (창이 꺼지진않음)
"""

from enhanced_selenium import EnhancedChrome
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv()

web = EnhancedChrome(timeout=3, freq=0.01)
web.set_window_size(1920 * 3 // 4, 1080)
web.set_window_position(0, 0)
web.get("https://hana-prd-ap-4.ssu.ac.kr:8443/zu4a/zcmui2245")
id, pw = os.getenv("SOONGSIL_ID"), os.getenv("SOONGSIL_PW")
web.find(title="아이디 입력").send_keys(id)
web.find(title="비밀번호 입력").send_keys(pw + "\n")

try:
    web.find(id="sapSL_DEFAULT_BUTTON").click("enter")  # enter가 가장 안전함
except:
    pass

# 새로고침 타이밍 테스트
while userInput := input():
    while (
        cur_secs := datetime.now().strftime("%H:%M:%S.%f")[-8:-5]
    ) != userInput:
        ...
    print(datetime.now().strftime("%H:%M:%S.%f")[:-5])
    web.find(role="button").click()

final_time = input("최종시간(10:00:10.7): ")
print("최종시간")
print(final_time)
print("현재시간")
print(datetime.now().strftime("%H:%M:%S.%f")[:-5])

# 세팅은 0.1초
while (cur_secs := datetime.now().strftime("%H:%M:%S.%f")[:-5]) != final_time:
    ...
web.find(role="button").click()  # refresh


def pick(i):
    idx = 1 + (i - 1) * 13
    print(f"{i}번째 강의신청: {idx=}")

    try:
        web.find(id=f"__button6-__clone{idx}").click("enter")
    except:
        pass

    print(f"{i}번째 강의신청 완료")


for i in range(1, 10):
    web.add_hotkey(str(i), lambda i=i: pick(i))

web.wait_hotkey("esc")
