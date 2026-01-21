import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

qr_pil_image = None

# QR 코드 생성
def generate_qr():
    global qr_pil_image

    url = input_text.get("1.0", "end").strip()
    if not url:
        messagebox.showerror("Error", "URL을 입력하세요!")
        return
    qr_color = color_combo.get()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=qr_color, back_color='white')
    img = img.resize((200, 200), Image.LANCZOS)  # 수정된 부분
    img_tk = ImageTk.PhotoImage(img)

    qr_image_label.config(image=img_tk)
    qr_image_label.image = img_tk

    qr_pil_image = qr.make_image(
    fill_color=qr_color,
    back_color="white")

#QR 이미지 저장 
def save_qr():
    if qr_pil_image is None:
        messagebox.showwarning("경고", "먼저 QR 코드를 생성하세요!")
        return

    filename = file_entry.get().strip()
    filename = filename.replace(".png", "").replace(".jpg", "")

    if not filename:
        messagebox.showwarning("경고", "파일명을 입력하세요!")
        return
    try:
        file_type = file_combo.get()

        if file_type == "PNG":
            qr_pil_image.save(f"{filename}.png")
        elif file_type == "JPG":
            qr_pil_image.convert("RGB").save(f"{filename}.jpg")

        messagebox.showinfo("완료", "QR 코드가 저장되었습니다!")
    except Exception:
        messagebox.showerror("오류", "QR 코드가 저장 실패")

# 텍스트 박스 지움
def delete():
    input_text.delete(1.0, tk.END)
    qr_image_label.config(image="")
   
root = tk.Tk()
root.title("QR코드 생성기")
root.geometry("560x600")
root.resizable(False, False)



name_label = tk.Label(root,text="나만의 QR 코드 만들기>>", fg="green")
name_label.place(x=380, y=10)


input_frame = tk.LabelFrame(root, text="생성할 QR코드 내용 입력", padx=10, pady=10)
input_frame.place(x=10, y=40, width=540, height=150)

# 안내 문구
info_label = tk.Label(input_frame,text="* URL 또는 텍스트 내용 입력")
info_label.place(x=5, y=5)


readme_btn = tk.Button(input_frame, text="닫기", width=10, command=root.destroy)
readme_btn.place(x=430, y=0)

# 텍스트 입력창
input_text = tk.Text(input_frame)
input_text.place(x=5, y=30, width=510, height=85)


file_frame = tk.LabelFrame(root, text="저장할 QR코드 파일명 :", padx=10, pady=10)
file_frame.place(x=10, y=200, width=540, height=60)

file_entry = tk.Entry(file_frame)
file_entry.place(x=5, y=5, width=510)

# 예시 텍스트
example_label = tk.Label(root, text="* 파일명 예시) my_qr01", fg="gray")
example_label.place(x=20, y=265)

save_btn = tk.Button(root, text="파일 저장", width=10, command=save_qr)
save_btn.place(x=450, y=265)

# qr 이미지 생성 프레임
qr_frame = tk.LabelFrame(root, text="생성된 QR 코드", width=240, height=250)
qr_frame.place(x=20, y=300)

# 프레임 크기 고정 
qr_frame.pack_propagate(False)

# QR 이미지 출력 라벨 (프레임 안)
qr_image_label = tk.Label(qr_frame)
qr_image_label.place(relx=0.5, rely=0.5, anchor="center")

# QR 생성 버튼
generate_btn = tk.Button(root, text="QR코드 생성",width=15, command=generate_qr)
generate_btn.place(x=300, y=320)

close_btn = tk.Button(root, text="지우기", width=13, command=delete)
close_btn.place(x=430, y=320)

tk.Label(root,text="QR 코드 색상 선택").place(x=300, y=375)

color_combo = ttk.Combobox(
    root,
    values=["black", "blue", "red", "green", "purple", "hotpink", "navy", "teal"],
    state="readonly",
    width=18
)
color_combo.place(x=300, y=400)
color_combo.set("black")

tk.Label(root, text="저장 형식").place(x=300, y=440)

file_combo = ttk.Combobox(
    root,
    values=["PNG", "JPG"],
    state="readonly",
    width=18
)
file_combo.place(x=300, y=465)
file_combo.set("PNG")

root.mainloop()
