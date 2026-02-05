# 네이버 IT/과학 뉴스 제목 10개를 추출하여 워드 클리우드로 시각화하는 코드
# pip install requests beautifulsoup4 wordcloud matplotlib <= 코드를 실행 하기전에 설차

import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. 네이버 IT/과학 뉴스 URL
url = "https://news.naver.com/section/105"


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


    # 3. 제목들을 하나의 문자열로 합치기
text = " ".join(titles)

print("워드클라우드 원본 텍스트")
print(text)
# 4. 워드클라우드 생성 (기본 버전, 마스크 없음)
wordcloud = WordCloud(
    font_path="malgun.ttf",   # 한글 폰트 (Windows)
    width=800,
    height=500,
    max_words=100,  # 최대 단어 수
    relative_scaling=0.5,
    max_font_size=110,
    colormap="spring",
    background_color="white"
).generate(text)

# 5. 시각화
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("wordcloud.png", dpi=300)
plt.show()
