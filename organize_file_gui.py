import shutil
from pathlib import Path
from send2trash import send2trash 
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# 확장자 카테고리
categories = {
    'images': {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
    'documents': {'.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.hwpx'},
    'code': {'.py', '.ipynb', '.c', '.html', '.css', '.js'},
    'videos': {'.mp4', '.avi', '.mkv', '.mov'},
    'music': {'.mp3', '.wav', '.flac'},
    'archives': {'.zip', '.rar', '.7z'}
}

# 파일 분류 및 이동 함수
def organize_files(folder_path, log_box):
    source = Path(folder_path)

    if not source.exists():
        messagebox.showerror("오류", "폴더가 존재하지 않습니다.")
        return

    moved = 0
    skipped = 0

    # 폴더 생성
    for category in categories:
        (source / category).mkdir(exist_ok=True)

    for file in source.iterdir():
        if not file.is_file():
            continue

        moved_file = False

        ext = file.suffix.lower()

        for category, exts in categories.items():
            if ext in exts:
                dest = source / category / file.name

                # 이름 충돌 처리
                counter = 1
                while dest.exists():
                    dest = source / category / f"{file.stem} ({counter}){file.suffix}"
                    counter += 1

                try:
                    shutil.move(file, dest)
                    log_box.insert(tk.END, f"[이동] {file.name} → {category}\n")
                    moved += 1
                except Exception as e:
                    log_box.insert(tk.END, f"[실패] {file.name} - {e}\n")
                    skipped += 1

                moved_file = True
                break

                
        if not moved_file:
            other = source / "others"
            other.mkdir(exist_ok=True)

            dest = other / file.name
            try:
                shutil.move(file, dest)
                log_box.insert(tk.END, f"[기타] {file.name}\n")
                moved += 1
            except Exception as e:
                log_box.insert(tk.END, f"[실패] {file.name} - {e}\n")
                skipped += 1

    log_box.insert(tk.END, f"\n완료: {moved}개 이동 / 실패: {skipped}개\n")


# 지정된 경로의 파일과 폴더를 휴지통으로 이동
def move_file_to_trash(folder_path, log_box):
    file_to_trash = 0
    source = Path(folder_path)

    if not source.exists():
        messagebox.showerror("오류", "폴더가 존재하지 않습니다.")
        return
    
    for file in source.iterdir():
        try:
            # 파일이나 심볼릭 링크를 휴지통으로 이동
            if file.is_file():
                send2trash(str(file))
                log_box.insert(tk.END, f"[이동] {file.name} → 휴지통\n")
                file_to_trash += 1

            # 디렉토리를 휴지통으로 이동
            elif file.is_dir():
                send2trash(str(file))
                log_box.insert(tk.END, f"[이동] {file.name} → 휴지통\n")
                file_to_trash += 1
        except Exception as e:
            log_box.insert(tk.END, f"파일 {file}룰 휴지통으로 이동하는데 실패했습니다.\n에러 원인 : {e}")


def select_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)


def run_program(entry, log_box):
    folder = entry.get()
    if not folder:
        messagebox.showwarning("경고", "폴더를 선택하세요.")
        return

    log_box.delete(1.0, tk.END)
    organize_files(folder, log_box)


def del_program(entry, log_box):
    folder = entry.get()
    if not folder:
        messagebox.showwarning("경고", "폴더를 선택하세요.")
        return
    
    confirm = messagebox.askyesno("확인", "정말 삭제하시겠습니까?")
    if not confirm:
        return
    else:
        log_box.delete(1.0, tk.END)
        move_file_to_trash(folder, log_box)
import tkinter as tk
from tkinter import scrolledtext

# --- 기존에 작성하신 함수들 (select_folder, run_program, del_program) 은 이 위에 그대로 두시면 됩니다 ---

# GUI 생성
root = tk.Tk()
root.title("파일 자동 정리 프로그램")
root.geometry("620x520")
root.configure(bg="#2b2b2b") # 세련된 다크 그레이 배경

# 공통 폰트 설정
main_font = ("Malgun Gothic", 10)
btn_font = ("Malgun Gothic", 10, "bold")

# 폴더 선택 프레임
frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(pady=(40, 20))

# 입력창 (Entry) - 테두리 제거 및 색상 반전
entry = tk.Entry(frame, width=55, font=main_font, bg="#3c3f41", fg="#ffffff",
                 insertbackground="#ffffff", relief="flat", highlightthickness=1, highlightcolor="#5c82ff")
entry.pack(side=tk.LEFT, padx=(0, 10), ipady=8)

# 폴더 선택 버튼
btn_select = tk.Button(frame, text="폴더 선택", command=lambda: select_folder(entry),
                       font=btn_font, bg="#4a4d50", fg="#ffffff", activebackground="#5c5f62",
                       activeforeground="#ffffff", relief="flat", padx=15, cursor="hand2")
btn_select.pack(side=tk.LEFT, ipady=4)

# 버튼 프레임
btn_frame = tk.Frame(root, bg="#2b2b2b")
btn_frame.pack(pady=(0, 20))

# 실행 버튼 (시원한 블루 포인트 컬러)
btn_run = tk.Button(btn_frame, text="파일 정리 시작", command=lambda: run_program(entry, log_box),
                    font=btn_font, bg="#5c82ff", fg="#ffffff", activebackground="#4a6bdf",
                    activeforeground="#ffffff", relief="flat", width=18, cursor="hand2")
btn_run.grid(row=0, column=0, padx=10, ipady=6)

# 삭제 버튼 (경고를 의미하는 레드/오렌지 포인트 컬러)
del_btn = tk.Button(btn_frame, text="휴지통으로 이동", command=lambda: del_program(entry, log_box),
                    font=btn_font, bg="#e05252", fg="#ffffff", activebackground="#c44444",
                    activeforeground="#ffffff", relief="flat", width=18, cursor="hand2")
del_btn.grid(row=0, column=1, padx=10, ipady=6)

# 로그 출력 창 - 배경과 어우러지도록 톤 다운
log_box = scrolledtext.ScrolledText(root, width=72, height=18, font=main_font,
                                    bg="#1e1e1e", fg="#cccccc", relief="flat",
                                    padx=10, pady=10, insertbackground="#ffffff")
log_box.pack(pady=(0, 20))

root.mainloop()
