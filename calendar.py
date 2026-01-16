
# 코드를 실행하면 콘솔과 윈도우 창의 텍스트에 달력이 출력됩니다.
# 이번 달 달력과 올해 전체 달력을 버튼으로 선택할 수 있습니다.
# 사용한 모듈은 파이썬 기본 모듈이기 때문에 따로 설치할 필요없습니다.

import tkinter as tk
from datetime import datetime
import calendar


now = datetime.now()

YEAR = now.year
MONTH = now.month
BG = "aliceblue"
FONT = ("함초롱바탕", 12, "bold")

root = tk.Tk()
root.title("달력")
root.geometry("630x530")
root.config(bg=BG)
root.resizable(False, False)

def date():
    cal_str = calendar.month(YEAR,MONTH)
    print(calendar.month(YEAR,MONTH))
    text.delete(1.0, tk.END)
    text.insert(tk.END, cal_str+"\n")
def year():
    print(calendar.prcal(YEAR))
    cal_year = calendar.calendar(YEAR)
    text.delete(1.0, tk.END)
    text.insert(tk.END, cal_year+"\n")
    text.insert(tk.END, "2026년 달력이 출력되었습니다\n")


label = tk.Label(text = "달력 출력 프로그램", bg = BG, font=("휴먼편지체", 12, "bold"))
label.pack(pady=(20,5))

text = tk.Text(width= 70, height= 20, font=("휴먼편지체", 11, "bold"))
text.pack(pady=(20))

btn_frame = tk.Frame(root, bg="lightblue")
btn_frame.pack(pady=10)

btn = tk.Button(btn_frame, text="이번달 달력", width = 12, height= 2, bg=BG, font=FONT, command=date)
btn.grid(row=0, column=0)
btn2 = tk.Button(btn_frame, text="올해의 달력", width = 12, height= 2, bg=BG, font=FONT, command=year)
btn2.grid(row=0, column=1)
root.mainloop()
