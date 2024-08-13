"""

전체 수강신청날에 채플 시간 바꾸려고 짠 로직임.

그냥 바로 해당 시간에 접속해서 맨 첫번째 강의 신청함.

"""

from es.models.core.driver import ChromeDriver
from es.utils import get_idpw

# from es.models.debugger import debugger
# debugger.start(__file__)

web = ChromeDriver()
web.set_window_size(1920 * 3 // 4, 1080)
web.set_window_position(0, 0)
web.set_repeat(3, 0.01)
web.get("https://hana-prd-ap-4.ssu.ac.kr:8443/zu4a/zcmui2245")
id, pw = get_idpw()
web.find(title="아이디 입력").send_keys(id)
web.find(title="비밀번호 입력").send_keys(pw + "\n")

# 연속으로 접속하면 기기 하나만 접속할 수 있다는 창이 뜸. 그거 예 버튼임.
web.uncertain(lambda: web.find(id="sapSL_DEFAULT_BUTTON").click())

# 아래 0.1초 도전해봄
web.wait(realtime="10:00:14.30", timeformat="%H:%M:%S.%f")
web.refresh()

# timeout을 몇초줘야하는지.
# window 변경도 없음. 그냥 가는거야.

with web.no_error, web.set_wait(30, 0.01):
    web.find(id="__button6-__clone1").click()


print("완료")

# debugger.end()
