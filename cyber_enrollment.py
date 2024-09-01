"""

사강 잡으려고 짠 로직임
수강신청 중에선 나름 가장 최신 로직임.

"""

import pathlib
import sys

# 현재 파일의 디렉토리 경로 얻기
es_dir = pathlib.Path(__file__).parent.parent / "Enhanced-Selenium"

# sys.path에 es 디렉토리 경로 추가
sys.path.append(str(es_dir))


from models.core.driver import ChromeDriver
from utils import get_idpw

web = ChromeDriver()
web.set_window_size(1200, 1080)
web.set_window_position(0, 0)
web.set_repeat(5, 0.01)

web.get("https://hana-prd-ap-4.ssu.ac.kr:8443/zu4a/zcmui2245")
id, pw = get_idpw()
web.find(title="아이디 입력").send_keys(id)
web.find(title="비밀번호 입력").send_keys(pw + "\n")

# 연속으로 접속하면 기기 하나만 접속할 수 있다는 창이 뜸. 그거 예 버튼임.
with web.no_error:
    web.find(id="sapSL_DEFAULT_BUTTON").click()


# 초단위 딜레이 계속해서 계산해주면 됨.
web.wait(realtime="10:00:14.30", timeformat="%H:%M:%S.%f")
web.refresh()

with web.no_error, web.set_repeat(1000, 0.01):
    web.find(id="__button6-__clone1").click()


print("완료")
