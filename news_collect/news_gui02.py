import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os
from tkinter import filedialog
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
    code = SECTION_MAP.get(section)

    if not code:
        status_label.config(text="섹션을 선택해주세요", fg="red")
        return

    status_label.config(text="뉴스 수집 중...", fg="blue")
    root.update()   # UI 즉시 갱신

    titles = collect_news(code)

    # 텍스트 박스 내용 지우기
    log_text.delete(1.0, tk.END)

    if not titles:
        log_text.insert(tk.END, "→ 수집된 뉴스가 없습니다.\n")
        status_label.config(text="수집 실패", fg="red")
        return

    # 텍스트 박스에 출력
    log_text.insert(tk.END, f"[{section}] 섹션 뉴스 헤드라인 ({len(titles)}개)\n")
    log_text.insert(tk.END, "─" * 50 + "\n")

    for i, title in enumerate(titles, 1):
        log_text.insert(tk.END, f"{i:2d}. {title}\n")

    log_text.insert(tk.END, "\n" + "─" * 50 + "\n")
    log_text.see(tk.END)           # 자동으로 맨 아래로 스크롤

    # CSV 저장 & 워드클라우드 생성
    save_to_csv(titles)
    create_wordcloud(" ".join(titles))
    my_folder = os.getcwd()

    status_label.config(text=f"완료! {my_folder}에 파일 저장됨", fg="green")

# 버튼 기능
def start():
    collection()

def exit_program():
    plt.close('all')               
    root.quit()
    root.destroy()


def open_csv_file():
    file_path = filedialog.askopenfilename(
        title="CSV 파일 선택",
        filetypes=[("CSV Files", "*.csv")],
        initialdir=os.getcwd()
    )

    if not file_path:
        return

    csv_entry.delete(0, tk.END)
    csv_entry.insert(0, file_path)
    load_csv_to_text(file_path)


def load_csv_to_text(file_path):
    log_text.delete(1.0, tk.END)

    try:
        with open(file_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = list(reader)

        log_text.insert(tk.END, f"[CSV 파일 열기]\n{file_path}\n")
        log_text.insert(tk.END, "─" * 50 + "\n")

        for i, row in enumerate(rows[1:], 1):  # 헤더 제외
            log_text.insert(tk.END, f"{i:2d}. {row[0]}\n")

        log_text.see(tk.END)
        status_label.config(text="CSV 파일 로드 완료", fg="green")

    except Exception as e:
        messagebox.showerror("오류", f"CSV 파일 열기 실패\n{e}")


root = tk.Tk()
root.title("Scraping Tool")
root.geometry("600x700")
root.resizable(False, False)

# =====================
# 전체 여백 설정
# =====================
main = tk.Frame(root, padx=15, pady=15)
main.pack(fill="both", expand=True)

# =====================
# 제목
# =====================
title_label = tk.Label(
    main,
    text="네이버 뉴스 헤드라인 수집기",
    font=("맑은 고딕", 16, "bold")
)
title_label.pack(pady=(0, 20))

# =====================
# 설정 프레임
# =====================
config_frame = ttk.LabelFrame(main, text="설정", padding=15)
config_frame.pack(fill="x", pady=10)


tk.Label(config_frame, text="수집할 헤드라인 선택:").grid(row=0, column=0, sticky="w")
section_combo = ttk.Combobox(config_frame, values=list(SECTION_MAP.keys()), state="readonly", width=40)
section_combo.current(0)
section_combo.grid(row=1, column=0, padx=5, pady= 5)


# 체크박스
extract_var = tk.BooleanVar()
extract_check = tk.Checkbutton(
    config_frame,
    text="파일은 자동 생성, 저장됩니다",
    variable=extract_var
)
extract_check.grid(row=1, column=1, pady=5, padx=40)

# =====================
# CSV 파일 프레임
# =====================
csv_frame = ttk.LabelFrame(main, text="CSV 파일 찾기", padding=15)
csv_frame.pack(fill="x", pady=10)

tk.Label(csv_frame, text="default.csv 파일:").grid(row=0, column=0, sticky="w")

csv_entry = tk.Entry(csv_frame, width=62)
csv_entry.grid(row=1, column=0, pady=5, sticky="w")

csv_btn = tk.Button(csv_frame, text="찾기", width=12, command=open_csv_file)
csv_btn.grid(row=1, column=1, padx=10)

# =====================
# 실행 버튼
# =====================

btn_frame = ttk.LabelFrame(main, text="스크래핑", padding=15)
btn_frame.pack(fill="x", pady=0)

exit_btn = tk.Button(
    btn_frame,
    text="닫기",
    width=12,
    height=1,
    command=exit_program)
exit_btn.pack(side="right", padx=0)


start_btn = tk.Button(
    btn_frame,
    text="스크래핑 시작",
    width=20,
    height=1,
    command=collection
)
start_btn.pack(side="right", padx=20)


# =====================
# 진행 상황 프레임
# =====================
status_frame = ttk.LabelFrame(main, text="진행 상황", padding=15)
status_frame.pack(fill="both", expand=True)

status_label = tk.Label(
    status_frame,
    text="대기 중...",
    anchor="w")
status_label.pack(fill="x", pady=(0, 10))

# 로그 출력 + 스크롤바
log_frame = tk.Frame(status_frame)
log_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(log_frame)
scrollbar.pack(side="right", fill="y")

log_text = tk.Text(
    log_frame,
    wrap="word",
    yscrollcommand=scrollbar.set
)
log_text.insert(tk.END, "헤드라인 수집 시작...\n\n")
log_text.pack(fill="both", expand=True)

scrollbar.config(command=log_text.yview)


root.mainloop()
