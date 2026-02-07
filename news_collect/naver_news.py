# 네이버 IT/과학 뉴스 제목 10개를 추출하여 워드 클리우드로 시각화하는 코드
# pip install requests beautifulsoup4 wordcloud matplotlib <= 코드를 실행 하기전에 설차

import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime

now = datetime.now().strftime("%Y%m%d_%H%M")


# 네이버 뉴스 url
# 정치 "https://news.naver.com/section/100"
# 경제 "https://news.naver.com/section/101"
# 사회 "https://news.naver.com/section/102" 
# 생활 문화 "https://news.naver.com/section/103"
# 세계 "https://news.naver.com/section/104"
# IT/과학 "https://news.naver.com/section/105"

url_map = {
    1: "100",
    2: "101",
    3: "102",
    4: "103",
    5: "104",
    6: "105"
}

print("원하는 뉴스의 번호를 선택하세요")
print("""
      1 : 정치
      2 : 경제
      3 : 사회
      4 : 생활 문화
      5 : 세계
      6 : IT/과학 """)

while True:
    try:
        choice = int(input("원하는 뉴스의 번호를 입력하세요(숫자만!) : "))
    except ValueError:
        print("숫자만 입력하세요")
        continue


    if choice in url_map:
        url = f"https://news.naver.com/section/{url_map[choice]}"
        break  
    else:
        print("1~6 사이의 숫자를 입력하세요")
        continue

   

# 2. 페이지 요청
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0"
})

titles = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # 기사 제목 선택 (상위 10개)
    headlines = soup.select(".sa_text_title")[:10]

    for headline in headlines:
        title = headline.get_text().strip()
        titles.append(title)

else:
    print("뉴스 페이지 가져오기 실패")
    exit()

    # 3. 제목들을 하나의 문자열로 합치기
text = " ".join(titles)

print("워드클라우드 원본 텍스트")
print(text)

with open(f"news_{now}.txt", "a", encoding="utf-8") as f:
    f.write(text)

# 4. 워드클라우드 생성 (기본 버전, 마스크 없음)
wordcloud = WordCloud(
    font_path="malgun.ttf",   # 한글 폰트 (Windows)
    # font_path='/System/Library/Fonts/AppleGothic.ttf',  # Mac
    # font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf',  # Linux
    width=800,
    height=500,
    max_words=100,  # 최대 단어 수
    max_font_size=120,
    colormap="winter",
    background_color="aliceblue"
).generate(text)

# 5. 시각화
plt.figure(figsize=(8, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(f"wordcloud_{now}.png", dpi=300)
plt.show()
