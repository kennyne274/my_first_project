# 날씨와 시간을 표시하는 디지털 시계
# 날씨 정보는 공공데이터 포털에서 API키를 발급받아 합니다.

import tkinter as tk
import requests
from datetime import datetime


# 기상청 API 설정

API_KEY = "" # <=여기에 API 키를 넣으세요.

WEATHER_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

NX = 60   # 서울 종로 기준
NY = 127

# 시계 폰트(디지털 폰트가 없으면 자동 변경)
try:
    FONT_TIME = ("DS-Digital", 75)
    
except:
    FONT_TIME = ("Courier", 75)
   


# 날씨 가져오기
def get_weather():
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = now.strftime("%H%M") 

    params = {
        "serviceKey": API_KEY,
        "numOfRows": 10,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": NX,
        "ny": NY
    }

    try:
        res = requests.get(WEATHER_URL, params=params)
        items = res.json()["response"]["body"]["items"]["item"]

        temp = "?"
        sky = "?"

        for item in items:
            if item["category"] == "T1H":
                temp = item["obsrValue"]
            elif item["category"] == "PTY":
                sky = item["obsrValue"]

        if sky == "0":
            sky_text = "맑음 ☀️"
        elif sky == "1":
            sky_text = "비 🌧"
        elif sky == "3":
            sky_text = "눈 ❄️"
        else:
            sky_text = "구름 ☁️"

        return f"{temp}℃ / {sky_text}"

    except:
        return "날씨 정보 없음"


# 시간 업데이트
def update():
    now = datetime.now()

    date_label.config(text=now.strftime("%Y.%m.%d"))
    day_label.config(text=now.strftime("%a"))
    ampm_label.config(text=now.strftime("%p"))

    time_label.config(text=now.strftime("%H:%M:%S"))


    root.after(1000, update)

# 날씨 업데이트(한 시간에 한번)
def update_weather():
    weather_label.config(text=get_weather())
    root.after(60000, update_weather)



# GUI 설정
root = tk.Tk()
root.title("Digital Clock with Date & Day")
root.geometry("640x360")
root.configure(bg="#1a1a1a")
root.resizable(False, False)


# 외곽 프레임
outer = tk.Frame(root, bg="#1a1a1a", bd=20, relief="raised")
outer.pack(padx=15, pady=15, fill="both", expand=True)


# 시계 상단(날짜, 요일, AMPM)
top = tk.Frame(outer, bg="#111", bd=14, relief="raised", height=2)
top.pack(fill="x", padx=10, pady=5)

date_label = tk.Label(
    top, font=("Times New Roman", 18, "bold"),
    fg="white", bg="#111", width=12
)
date_label.grid(row=0, column=0, padx=20)

day_label = tk.Label(
    top, font=("Times New Roman", 18, "bold"),
    fg="yellow", bg="#111", width=6
)
day_label.grid(row=0, column=1, padx=15)

ampm_label = tk.Label(
    top, font=("Times New Roman", 18, "bold"),
    fg="red", bg="#111", width=6
)
ampm_label.grid(row=0, column=2, padx=15)


# 메인 시계 영역(현재 시간)
time_frame = tk.Frame(outer, bg="#000")
time_frame.pack(fill="both", expand=True, padx=10, pady=10)

time_label = tk.Label(
    time_frame,
    font=FONT_TIME,
    fg="#00ffff",
    bg="#000"
)
time_label.pack(expand=True)


# 하단 날씨
weather_label = tk.Label(
    outer,
    font=("Times New Roman", 16, "bold"),
    fg="#03FC3D",
    bg="#1a1a1a"
)
weather_label.pack(pady=5)

update()
update_weather()
root.mainloop()
