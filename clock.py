"""
datetime 시계

"""

import tkinter as tk
from datetime import datetime


def update_time():
    # 현재 시간을 가져와서 밀리초까지 포맷팅
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-4]
    # Label 위젯에 현재 시간 설정
    time_label.config(text=current_time)
    # 10밀리초마다 update_time 함수를 호출하여 시간 업데이트
    root.after(10, update_time)


# Tkinter 윈도우 생성
root = tk.Tk()
root.title("Real-time Clock")

# Label 위젯 생성
time_label = tk.Label(root, font=("Helvetica", 48), fg="black")
time_label.pack(pady=20)

# 시간 업데이트 시작
update_time()

# Tkinter 이벤트 루프 시작
root.mainloop()
