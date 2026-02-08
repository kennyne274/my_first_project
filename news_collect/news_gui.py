import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 뉴스 섹션

SECTION_MAP = {
    "정치": "100",
    "경제": "101",
    "사회": "102",
    "생활/문화": "103",
    "세계": "104",
    "IT/과학": "105"
}


# 뉴스 수집

def collect_news(section_code):
    url = f"https://news.naver.com/section/{section_code}"

    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
    response = requests.get(url, headers=headers, timeout=10)

    titles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = soup.select(".sa_text_title")[:15]

        for h in headlines:
            titles.append(h.get_text().strip())
    else:
        messagebox.showerror("알림" , "뉴스 가져오기 실패")
        return []


    return list(dict.fromkeys(titles))


# 저장
def save_to_csv(titles):
    now = datetime.now()
    folder = now.strftime("%Y-%m-%d")
    os.makedirs(folder, exist_ok=True)

    filename = now.strftime("%H%M")
    filepath = os.path.join(folder, f"news_{filename}.csv")

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["헤드라인"])
        for t in titles:
            writer.writerow([t])

def create_wordcloud(text):
    now = datetime.now()
    folder = now.strftime("%Y-%m-%d")
    os.makedirs(folder, exist_ok=True)

    filename = now.strftime("%H%M")
    filepath = os.path.join(folder, f"wordcloud_{filename}.png")

    wc = WordCloud(
        font_path="malgun.ttf",
        width=950,
        height=700,
        max_font_size=140,
        background_color="white"
    ).generate(text)

    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(filepath, dpi=300)
    plt.show(block=False)


# 실행

def collection():


    section = section_combo.get()
    
    code = SECTION_MAP[section]

    titles = collect_news(code)

    if titles:
        save_to_csv(titles)
        create_wordcloud(" ".join(titles))
        status_label.config(text="CSV + WordCloud 저장 완료")


# 버튼 기능
def start():
    collection()

def exit_program():
    plt.close('all')               
    root.quit()
    root.destroy()

# GUI
root = tk.Tk()
root.title("뉴스 헤드라인 수집기")
root.geometry("420x210")

tk.Label(root, text="뉴스 종류").pack(pady=10)
section_combo = ttk.Combobox(root, values=list(SECTION_MAP.keys()), state="readonly")
section_combo.current(0)
section_combo.pack(pady=(20,10))


exit_btn = tk.Button(root, text="Exit", width=10, height=2, command=exit_program)
exit_btn.pack(side="right",padx=10)
start_btn = tk.Button(root, text="Start", width=10,  height=2,command=start)
start_btn.pack(side="right",padx=10)

status_label = tk.Label(root, text="대기중")
status_label.pack(pady=10)


root.mainloop()
