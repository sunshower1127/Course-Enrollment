from es.models.core.driver import ChromeDriver
from es.models.debugger import debugger
from es.utils import get_idpw

debugger.start(__file__)

web = ChromeDriver()

web.get("https://hana-prd-ap-4.ssu.ac.kr:8443/zu4a/zcmui2245")
id, pw = get_idpw()
web.find(title="아이디 입력").send_keys(id)
web.find(title="비밀번호 입력").send_keys(pw + "\n")

web.uncertain(lambda: web.find(id="sapSL_DEFAULT_BUTTON").click(), timeout=2)

web.wait(key="esc", keys=[("q", lambda: print("q")), ("w", lambda: print("w"))])

debugger.end()
