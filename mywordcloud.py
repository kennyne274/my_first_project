# 같은 폴더 안에 동일한 이름의 마스크 파일이 있어야 함(주의)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from PIL import ImageTk
import os
from datetime import datetime

# 마스크 폰트
FONT_MAP = {
    "맑은 고딕": "C:/Windows/Fonts/malgun.ttf",
    "굴림": "C:/Windows/Fonts/gulim.ttc",
    "바탕": "C:/Windows/Fonts/batang.ttc",
    "한컴고딕": "C:/Windows/Fonts/Hancom Gothic Bold.ttf",
    "Arial": "C:/Windows/Fonts/arial.ttf",
    "Times New Roman": "C:/Windows/Fonts/times.ttf",
    "Verdana":"C:/Windows/Fonts/verdana.ttf"
}

wc_image_original = None   # 원본 (저장용)
wc_image_preview = None    # 축소본 (미리보기용)


def word_cloud():
    # 워드 클라우드 생성
    def make_cloud():
        global wc_image_or
       
        selection = mask_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "마스크를 선택하세요!")
            return

        mask_name = mask_listbox.get(selection[0])
        mask_path = f"{mask_name}.png"

        if not os.path.exists(mask_path):
            messagebox.showerror("오류", "마스크 이미지가 없습니다.")
            return

        my_words = text.get(1.0, tk.END).strip()
        if not my_words:
            messagebox.showwarning("경고", "텍스트를 입력하세요!")
            return

        mask = np.array(Image.open(mask_path))
        colors = color_combo.get()
        contour_color = line_combo.get()
        font_name = size_combo.get()
        font_path = FONT_MAP.get(font_name)

        if not font_path or not os.path.exists(font_path):
            messagebox.showerror("오류", "선택한 글꼴 파일을 찾을 수 없습니다.")
            return

        wc = WordCloud(
            font_path=font_path,
            background_color="white",
            mask=mask,
            colormap=colors,
            contour_width=2,               # 마스크 테두리 설정
            contour_color=contour_color,
            max_words=200,
            random_state=42
        )

        wordcloud = wc.generate(my_words)

        # PIL 이미지 생성
        wc_image_or = wordcloud.to_image()
        wc_image = wc_image_or.resize((480, 340), Image.LANCZOS)

        wc_tk = ImageTk.PhotoImage(wc_image)

        #  Canvas 초기화
        preview_canvas.delete("all")

        #  Canvas에 이미지 삽입
        preview_canvas.create_image(
            250, 180,           # 캔버스 중앙 좌표
            image=wc_tk,

        )

        # 참조 유지 
        preview_canvas.image = wc_tk


    # 마우스 우 클릭으로 복사
    def paste_on_right_click(event):
        try:
            text.insert(tk.INSERT, root.clipboard_get())
        except tk.TclError:
            pass

    # 텍스트 박스 지움
    def delete():
        text.delete(1.0, tk.END)

    def save_image():
        global wc_image_or
        now = datetime.now()
        filename = now.strftime("wordcloud_%Y%m%d_%H%M%S.png")

        if wc_image_or is None:
            messagebox.showwarning("경고", "먼저 워드클라우드를 생성하세요!")
            return

        save_path = os.path.join(os.getcwd(), filename)

        if os.path.exists(save_path):
            if not messagebox.askyesno("확인", "이미 파일이 존재합니다. 덮어쓸까요?"):
                return

        wc_image_or.save(save_path)
        messagebox.showinfo("완료", "원본 해상도로 저장되었습니다.")



    root = tk.Tk()
    root.title("워드클라우드 생성기 - Tkinter")
    root.geometry("820x520")
    root.resizable(False, False)

    # =========================
    # 좌측 
    # =========================
    left_frame = tk.LabelFrame(root, text="원하는 마스크를 고르세요")
    left_frame.place(x=10, y=10, width=260, height=400)

    mask_listbox = tk.Listbox(left_frame)
    mask_listbox.place(x=10, y=10, width=235, height=150)

    templates = [
        "heart",
        "apple_mask",
        "twitter",
        "leaf",
        "cloud3",
        "cloud5",
        "korea_mask"
    ]

    for t in templates:
        mask_listbox.insert(tk.END, t)

    words = "**워드 클라우드로 생성할 텍스트를 입력하세요"
    text = tk.Text(left_frame, width=33, height=14, font=("맑은 고딕", 10), wrap="word")
    text.bind("<Button-3>", paste_on_right_click)
    text.insert(1.0, words)
    my_words = text.get(1.0, tk.END)
    text.place(x=10, y=180)

    # =========================
    # 우측 미리보기 
    # =========================
    preview_frame = tk.LabelFrame(root, text="미리보기")
    preview_frame.place(x=280, y=10, width=520, height=400)

    preview_canvas = tk.Canvas(
        preview_frame,
        bg="white",
        relief="sunken",
        bd=1,
        width=500, 
        height=360
    )

    preview_canvas.place(x=10, y=10)

    # =========================
    # 하단
    # =========================
    option_frame = tk.Frame(root)
    option_frame.place(x=10, y=420, width=790, height=50)
    
    embed_check = tk.Checkbutton(
        option_frame,
        text="파일명은 자동 생성됩니다"
    )
    embed_check.place(x=10, y=10)
   
    tk.Label(option_frame, text="색상:").place(x=200, y=12)
    colors = ["Set1", "Set2", "Set3", "Pastel1", "Pastel2","hot", 
            "cool", "rainbow", "spring", "summer", "autumn", "winter", 
            "Blues", "Greens", "Oranges", "Reds", "Purples", "Greys"]
    color_combo = ttk.Combobox(
        option_frame,
        values=colors,
        state="readonly",
        width=12
    )
    color_combo.place(x=240, y=10)
    color_combo.set("summer")

    tk.Label(option_frame, text="테두리색:").place(x=380, y=12)
    line_colors = ["red", "green", "blue", "pink", "black", "navy", "yellow", "brown", "orange"]
    line_combo = ttk.Combobox(
        option_frame,
        values=line_colors ,
        state="readonly",
        width=12
    )
    line_combo.set("green")
    line_combo.place(x=450, y=10)
   

    tk.Label(option_frame, text="글꼴선택:").place(x=580, y=12)

    size_combo = ttk.Combobox(
    option_frame,
    values=list(FONT_MAP.keys()),
    state="readonly",
    width=14
    )
    size_combo.set("맑은 고딕")
    size_combo.place(x=650, y=10)


    # =========================
    # 버튼 
    # =========================
    btn_frame = tk.Frame(root)
    btn_frame.place(x=430, y=470, width=370, height=40)

    create_btn = tk.Button(btn_frame, text="생성(R)", width=10, command=make_cloud)
    create_btn.place(x=0, y=5)

    open_btn = tk.Button(btn_frame, text="지우기", width=10, command=delete)
    open_btn.place(x=90, y=5)

    recent_btn = tk.Button(btn_frame, text="저장", width=10, command=save_image)
    recent_btn.place(x=180, y=5)

    close_btn = tk.Button(btn_frame, text="닫기", width=10, command=root.destroy)
    close_btn.place(x=270, y=5)

    root.mainloop()

try:
    word_cloud()
except Exception as e:
    messagebox.showerror("에러", str(e))
