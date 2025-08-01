# 민원 RAG 문서 수집 및 전처리 레포지토리

## 개요

이 레포지토리는 주민등록등본, 동사무소 위치, 무더위쉼터와 같은 **자주 묻는 민원 질문에 대응하는 챗봇**을 위한 RAG(Retrieval-Augmented Generation) 문서를 수집, 정제, 분할, 벡터화하기 위한 파이프라인을 포함합니다.

## 목표

- 공공기관에서 제공하는 신뢰성 높은 데이터를 수집
- RAG 시스템이 활용 가능한 `.txt` 기반 문서로 변환
- OpenAI 또는 FAISS 등의 벡터 DB에 업로드할 수 있도록 분할 및 구조화
- 민원 챗봇이 정확하고 근거 기반의 응답을 할 수 있도록 지원

---

## 문서 수집 대상

| 주제 | 출처 | 형식 |
|------|------|------|
| 주민등록등본 발급 | 정부24, 행정안전부 | HTML, PDF |
| 동주민센터 위치 | 공공데이터포털 | CSV, XML |
| 무더위 쉼터 정보 | 공공데이터포털, 지자체 | CSV |
| 민원 FAQ | 정부24, 국민권익위 | HTML, JSON |

→ 상세 출처 및 링크: [`docs/data_sources.md`](./docs/data_sources.md)

---

## 프로젝트 구조

```

rag-gov-bot/
├── docs/
│   ├── raw/                  # 원본 수집 문서 (csv, html, pdf 등)
│   ├── cleaned/              # 정제된 txt 문서
│   ├── chunked/              # RAG용으로 분할된 txt
├── crawler/                  # 웹 크롤러 및 데이터 수집기
├── preprocess/               # 문서 정제 및 텍스트 분할기
├── upload/                   # OpenAI 등 벡터DB 업로드 스크립트
├── eval/                     # 테스트 쿼리 및 검색 성능 평가
├── .env.example              # API 키 등 환경 변수 템플릿
└── README.md

````

---

## 사용 방법

### 1. 웹 데이터 수집

```bash
python crawler/gov24_faq_crawler.py
````

→ 결과: `docs/cleaned/gov24_faq.txt`

### 2. CSV 파일 → 텍스트 문서로 변환

```bash
python preprocess/convert_shelter_csv_to_txt.py
```

→ 결과: `docs/cleaned/shelters.txt`

### 3. 문서 Chunk 분할 (RAG용)

```bash
python preprocess/chunk_splitter.py --input docs/cleaned --output docs/chunked --chunk_size 512
```

```
