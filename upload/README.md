# OpenAI Vector Store 업로드

cleaned 폴더의 파일들을 OpenAI Vector Store에 업로드하는 스크립트입니다.

## 사용법

1. OpenAI API 키 설정:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. 스크립트 실행:
```bash
python upload_to_openai.py
```

## 업로드되는 파일들

- `dong_data.csv`: 주민센터 정보 데이터
- `gov_faq_등본.txt`: 정부24 FAQ 텍스트
- `rag_docs.json`: RAG 문서 JSON 데이터

## 결과

- 모든 파일이 하나의 통합 벡터 스토어에 업로드됩니다
- 업로드 결과는 `upload_result.json`에 저장됩니다
- 벡터 스토어 ID와 업로드된 파일 목록이 기록됩니다