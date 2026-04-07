import shutil
from pathlib import 

# 다운로드 폴더 정리기
# 파일 종류별로 자동 분류합니다.
# 폴더 없으면 자동 생성

def get_downloads_folder() -> Path:
    """사용자의 다운로드 폴더 경로 반환"""
    home = Path.home()
    downloads = home / "Downloads" 

    if downloads.exists():
        return downloads
    else:
        raise FileNotFoundError("다운로드 폴더를 찾을 수 없습니다.")
    
def organize_files():  

    # 카테고리별 폴더 매핑
    categories = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.hwpx'],
        'code' : ['.py', 'ipynb', '.c', '.html', '.css', '.js'],
        'videos': ['.mp4', '.avi', '.mkv', '.mov'],
        'music': ['.mp3', '.wav', '.flac'],
        'archives': ['.zip', '.rar', '.7z']
    }

    # 원본 경로 설정 (다운로드 폴더)
    source = get_downloads_folder()
    
    # 카테고리 딕셔너리에서 키와 value를 쌍으로 꺼냄
    for category, exts in categories.items():
        folder = source / category
        folder.mkdir(exist_ok=True)


    moved = 0
    skipped_count = 0

    # 다운로드 폴더 내부 파일을 순회하며 분류 및 이동
    for file in source.iterdir():  
        # 파일이 아니면 건너뜀
        if file.is_file():
            for category, exts in categories.items():
                if file.suffix.lower() in exts:                    
                    dest = source / category / file.name 
                    if not dest.exists():
                        try:
                            shutil.move(file, dest)
                            print(f"{category}로 이동: {file.name}")
                            moved += 1
                        except shutil.Error:
                            print(f"파일 이동 실패 {file.name}")
                            skipped_count += 1
                        except PermissionError:
                            print(f"권한 오류 (건너뜀): {file.name}")
                            skipped_count += 1

                    # 같은 이름의 파일이 폴더 안에 있으면 번호를 붙임        
                    else:               
                        counter = 1
                        original_name = dest.stem
                        ext = dest.suffix
                        while True:
                            new_file = source / category / f"{original_name} ({counter}){ext}"
                            if not new_file.exists():
                                try:
                                    shutil.move(file, new_file)                               
                                    print(f"{category}로 이동: {new_file.name}")
                                    moved += 1
                                except shutil.Error:
                                    print(f"파일 이동 실패 {file.name}")
                                    skipped_count += 1
                                except PermissionError:
                                    print(f"권한 오류, 이동 실패: {file.name}")
                                    skipped_count += 1
                                break
                            
                            counter += 1
               
                    break
            
            # 카테고리에 없는 확장자는 기타 폴더로 이동
            else:  # for-else 구문
                other = source / "others"
                other.mkdir(exist_ok=True)
                shutil.move(file, other / file.name)
                print(f"기타 폴더로 이동: {file.name}")
                moved += 1

    print(f"\n총 {moved}개의 파일을 정리했습니다.")

if __name__ == "__main__":
    organize_files()
