import os 
import requests 
from pathlib import Path 
from gtts import gTTS 
from dotenv import load_dotenv 
 
# 1. [ 환경 변수 로드 ] 
load_dotenv()
MY_TTBKEY = os.getenv('MY_TTBKEY')
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'
 
# 2. [ 최대 100개까지 주제별 도서 데이터를 가져오는 함수 정의 ] 
def fetch_books_by_topic(topic, max_results=100): 
    params = {
        "TTBKey": MY_TTBKEY,
        "Query": topic,
        "QueryType": "Keyword",
        "MaxResults": max_results,
        "start": 1,
        "SearchTarget": "Book",
        "output": "js",
        "Version": "20131101"
    }

    response = requests.get(ALADIN_SEARCH_URL, params=params)
    return response.json()
 
 
# 3. [ 도서 정보를 텍스트 파일로 저장하는 함수 정의 ] 
# 책 정보를 "제목, 저자, 소개" 형식으로 변환하여 txt 파일로 저장 
def save_books_info(books, filename): 
    Path("output").mkdir(exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        for book in books:
            title = book.get("title", "")
            author = book.get("author", "")
            description = book.get("description", "")

            f.write(f"제목: {title}\n")
            f.write(f"저자: {author}\n")
            f.write(f"소개: {description}\n")
            f.write("\n")
 
    print(f"{filename} 파일이 생성되었습니다.") 
 
 
# 5. [ 텍스트 파일을 오디오 파일로 변환하는 함수 정의 ] 
def create_audio_file(text_file, audio_file): 
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()

    tts = gTTS(text=text, lang="ko")
    tts.save(audio_file)
 
    print(f"{audio_file} 파일이 생성되었습니다.") 
 
 
# 6. [ 음악 관련 도서 데이터를 처리하는 함수 정의 ] 
def process_music_books(): 
    # 6.1 [ '음악' 주제의 도서 데이터 수집 ] 
    books = fetch_books_by_topic("음악", 10)["item"]
 
    # 6.2 [ 도서 정보를 텍스트 파일로 저장 ] 
    save_books_info(books, "output/music_books_info.txt")
 
    # 6.3 [ 텍스트 파일을 오디오 파일로 변환 ] 
    create_audio_file("output/music_books_info.txt", "output/music_books.mp3")
 
    print("모든 작업이 완료되었습니다.") 
 
 
# 함수 실행 
if __name__ == '__main__': 
    process_music_books()