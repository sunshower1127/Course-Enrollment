from es.models.core.driver import ChromeDriver

from es.utils import get_idpw

# from es.models.debugger import debugger
# debugger.start(__file__)

web = ChromeDriver(keep_alive=True)
web.set_window_size(1920 * 3 // 4, 1080)
web.set_window_position(0, 0)
web.set_repeat(3, 0.01)
web.get("https://hana-prd-ap-4.ssu.ac.kr:8443/zu4a/zcmui2245")
id, pw = get_idpw()
web.find(title="아이디 입력").send_keys(id)
web.find(title="비밀번호 입력").send_keys(pw + "\n")

web.uncertain(lambda: web.find(id="sapSL_DEFAULT_BUTTON").click())

# 아래 realtime을 timetest.py에서 뽑아내야함. 일단 0.4초는 통과고, 0.2초 도전해보자.
web.wait(realtime="10:00:17.00", timeformat="%H:%M:%S.%f")
web.refresh()


def pick(i):
    idx = 1 + (i - 1) * 13
    print(f"{i}번째 강의신청: {idx=}")
    try:
        web.goto_window(-1)
    except:
        pass

    web.uncertain(
        lambda: web.find(id=f"__button6-__clone{idx}").click(),
        timeout=0.1,
        freq=0.01,
    )


# 수동방식 : q누르면 수강신청, w누르면 강의 번호 변경
# 자동방식 : e누르면 현재수강인원/최대수강인원이 가장 높은 강의를 신청
web.wait(
    key="esc",
    keys=[(str(i), lambda i=i: pick(i)) for i in range(1, 10)],
)


# debugger.end()
