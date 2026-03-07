import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from playsound3 import playsound
from gtts import gTTS
import os

# 음성 AI 서비스 프로그램

# 문자를 음성으로 변환하여 재생
def play(text):
    lang = languages[input_lang.get()]
    speed = speed_menu.get()

    if speed == "slow":
        slow = True
    else:
        slow = False
    # 음성 변환
    tts = gTTS(text ,
                lang = lang, 
                slow = slow)
    
    filename = "test_voice.mp3"
    tts.save(filename)
    playsound(filename)
    # 재생한 파일 삭제
    if os.path.exists(filename):
        os.remove(filename)
       
    
# 텍스트에 입력한 문자를 받아오는 함수
def speak_text():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "음성 변환할 문장을 입력하세요")
        return
    play(text)

# 저장
def save_audio():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "문장을 입력하세요")
        return

    file = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 files", "*.mp3")]
    )

    if not file:
        return

    lang = languages[input_lang.get()]
    tts = gTTS(text, lang=lang)
    tts.save(file)

# 번역 가능 언어 목록
languages = {  
    "한국어": "ko",
    "영어": "en",
    "중국어(간체)": "zh-CN",
    "중국어 (번체)": "zh-TW",
    "일본어": "ja",
    "프랑스어": "fr",
    "독일어": "de",
    "스페인어": "es",
    "아랍어": "ar",
    "이탈리아어": "it",
    "러시아어": "ru",
    "태국어": "th",
    "폴란드어": "pl",
    "히브리어": "he",
    "베트남어": "vi",
    "힌디어": "hi"
}


# ==================tkinter GUI==================

root = tk.Tk()
root.title("text to speech convertor")
root.geometry("600x450")
root.resizable(0, 0)

#제목
title_label = ttk.Label(root, text="AI 음성 서비스", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# text_frame
text_frame = tk.Frame(root)
text_frame.pack()

# scroballbar
scroballbar = tk.Scrollbar(text_frame)
scroballbar.pack(side="right", fill="y")

# text_area
text_area = tk.Text(text_frame, height=12, width=80, font=("Arial", 12, "bold"))
text_area.pack(side="left")
text_area.config(yscrollcommand=scroballbar.set)
scroballbar.config(command=text_area.yview)

# Frame for options
options_frame = ttk.Frame(root)
options_frame.pack(pady=10)

# 음성 재생 속도
ttk.Label(options_frame, text="Speed :").grid(row=0, column=0)
speed_var = tk.StringVar(value="fast")
speed_menu = ttk.Combobox(options_frame, textvariable=speed_var, values=["fast", "slow"], width=15, state="readonly")
speed_menu.grid(row=0, column=1, pady=10, padx=10)
speed_menu.set("fast")

tk.Label(options_frame, text="입력 언어").grid(row=0, column=2, pady=10, padx=10)

# 음성 언어 콤보박스 
input_lang = ttk.Combobox(options_frame, values=list((languages.keys())), state="readonly", width=15)
input_lang.grid(row=0, column=3, pady=10, padx=10)
input_lang.set("한국어")


# buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=15)

# 재생 버튼
speak_btn = tk.Button(button_frame, text="Speak", 
                      command=speak_text, 
                      width=10, 
                      height=1, 
                      font=("Times New Roman", 15, "bold"),
                      bg="#049F95", 
                      fg="white")
speak_btn.grid(row=0, column=2, padx=10)

# 저장 버튼
save_btn = tk.Button(button_frame, 
                     text="Save", 
                     command=save_audio, 
                     width=10, 
                     height=1, 
                     font=("Times New Roman", 15, "bold"),
                     bg="#1BA0F3", 
                     fg="white")
save_btn.grid(row=0, column=3, padx=10)


tk.mainloop()
