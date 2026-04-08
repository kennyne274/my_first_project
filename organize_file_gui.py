import shutil
from pathlib import Path
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
                    shutil.move(str(file), str(dest))
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
                shutil.move(str(file), str(dest))
                log_box.insert(tk.END, f"[기타] {file.name}\n")
                log_box.see(tk.END)
                moved += 1
            except Exception as e:
                log_box.insert(tk.END, f"[실패] {file.name} - {e}\n")
                skipped += 1

    log_box.insert(tk.END, f"\n완료: {moved}개 이동 / 실패: {skipped}개\n")


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


# GUI 생성
root = tk.Tk()
root.title("파일 자동 정리 프로그램")
root.geometry("600x500")

# 폴더 선택
frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=60)
entry.pack(side=tk.LEFT, padx=10, pady=10, ipady=6)

btn_select = tk.Button(frame, text="폴더 선택", command=lambda: select_folder(entry), padx=10, pady=5)
btn_select.pack(side=tk.LEFT)

# 실행 버튼
btn_run = tk.Button(root, text="정리 시작", command=lambda: run_program(entry, log_box), pady=5, width=12)
btn_run.pack(pady=10)

# 로그 출력
log_box = scrolledtext.ScrolledText(root, width=70, height=20)
log_box.pack()

root.mainloop()
