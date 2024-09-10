from datetime import datetime

from es.models.core.driver import ChromeDriver
from es.models.debugger import debugger
from es.utils import get_idpw

debugger.start(__file__)

es = ChromeDriver()

es.get("https://hana-prd-ap-4.ssu.ac.kr:8443/zu4a/zcmui2245")
id, pw = get_idpw()
es.find(title="아이디 입력").send_keys(id)
es.find(title="비밀번호 입력").send_keys(pw + "\n")

es.uncertain(lambda: es.find(id="sapSL_DEFAULT_BUTTON").click())

# 여기까지가 로그인하는 부분.

while True:
    es.wait(key="q")
    begin_time = datetime.now()
    es.refresh()
    es.wait(6)
    t = es.find(text_contains="현재시간").text.split(" ")[2]
    end_time = datetime.strptime(t, "%H:%M:%S")
    end_time = datetime.now().replace(
        hour=end_time.hour, minute=end_time.minute, second=end_time.second
    )
    print(f"{begin_time=}\n{end_time=}\n{(end_time - begin_time).total_seconds()=}")


debugger.end()
