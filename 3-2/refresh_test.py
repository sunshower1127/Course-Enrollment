from datetime import datetime
from es.models.core.driver import ChromeDriver
from es.models.debugger import debugger
from es.utils import get_idpw


es = ChromeDriver()

es.get("https://hana-prd-ap-4.ssu.ac.kr:8443/zu4a/zcmui2245")
id, pw = get_idpw()

es.implicitly_wait(3, 0.01)
es.find(title="아이디 입력").send_keys(id)
es.find(title="비밀번호 입력").send_keys(pw + "\n")

es.uncertain(lambda: es.find(id="sapSL_DEFAULT_BUTTON").click())

# 여기까지가 로그인하는 부분.

while True:
    es.wait(key="q")
    수강인원 = int(es.find(id="__text34-__clone9").text)
    최대수강인원 = int(es.find(id="__text35-__clone10").text)
    print(f"{수강인원=}, {최대수강인원=}")
    es.find(id="__button1").click()
