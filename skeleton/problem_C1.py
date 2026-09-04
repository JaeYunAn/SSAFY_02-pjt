import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# 1. [ 환경 변수 로드 ]
load_dotenv()
MY_TTBKEY = os.getenv('MY_TTBKEY')
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 2. [ 최대 100개까지 주제별 도서 데이터를 가져오는 함수 정의 ]
def fetch_books_by_topic(topic, max_results=100):
    books = []
    max_per_page = 50
    pages = (max_results + max_per_page - 1) // max_per_page

    for page in range(1, pages + 1):
        params = {
            "TTBKey": MY_TTBKEY,
            "Query": topic,
            "Output": "js",
            "Version": "20131101",
            "MaxResults": max_per_page,
            "Start": page  # 페이지 번호
        }

        response = requests.get(ALADIN_SEARCH_URL, params=params)
        data = response.json()
        items = data.get('item', [])
        books.extend(items)

        if not items:
            break

    return books[:max_results]

# 3. '인공지능' 도서 데이터를 처리하는 함수 정의
def process_ai_books():
    # 3.1 [ '인공지능' 관련 도서 검색 ]
    # fetch_books_by_topic()을 호출하여 '인공지능' 관련 도서를 100개 수집합니다.
    books = fetch_books_by_topic('인공지능', 100)

    # 3.2 [ 수집된 데이터에서 가격 정보가 있는 책 필터링 및 가격순 정렬 ]
    sorted_books = sorted(books, key=lambda x: x.get('priceStandard', 0), reverse=True)

    # 3.3 [ 상위 10개 도서 선택 ]
    top_10_books = sorted_books[:10] 

    # 3.4 [ 상위 10개 도서 정보 출력 ]
    print("가격이 높은 순서대로 상위 10개 도서:")
    for idx, book in enumerate(top_10_books, start=1):
        title = book.get('title', '제목 없음')
        price = book.get('priceStandard', 0)
        print(f"{idx}. 제목: {title}, 가격: {price}원")

    # 3.5 [ JSON 파일로 저장할 데이터 준비 ]
    # output/ai_top10_books.json 파일로 저장
    json_data = []
    for book in top_10_books:
        json_data.append({
            "제목": book.get('title', '제목 없음'),
            "저자": book.get('author', '저자 미상')
        })

    output_folder = Path('output')
    output_folder.mkdir(parents=True, exist_ok=True)
    file_path = output_folder / 'ai_top10_books.json'

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    # 3.6 [ 완료 메시지를 출력 ]
    print(f"'{file_path.name}' 파일이 생성되었습니다.")

# 함수 실행
if __name__ == '__main__':
    process_ai_books()
