import pandas as pd
import os
import glob
import chardet

# 폴더 경로 설정
folder_path = "./docs"  # 이 부분을 실제 폴더 경로로 수정

# CSV 파일 모두 탐색
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

merged_df = pd.DataFrame()

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result['encoding']

for file in csv_files:
    filename = os.path.basename(file)
    
    # 파일명에서 자치구 추출
    try:
        district = filename.split("_")[1].replace("서울특별시", "").replace(" ", "").strip()
    except IndexError:
        district = "알수없음"

    # 인코딩 자동 감지 후 읽기
    try:
        encoding = detect_encoding(file)
        df = pd.read_csv(file, encoding=encoding)
        df["자치구"] = district
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    except Exception as e:
        print(f"[ERROR] {filename} 읽기 실패: {e}")

# 결과 저장
merged_df.to_csv("merged_dong_center_data.csv", index=False, encoding="utf-8-sig")


df = pd.read_csv("./merged_dong_center_data.csv")

# 주소 관련 컬럼 합치기
address_columns = [col for col in df.columns if ('도로명' in col or '주소' in col or '소재지' in col) and ('지번' not in col)]
df['c주소'] = df[address_columns].astype(str).apply(lambda row: ' '.join(filter(lambda x: x != 'nan', row)), axis=1)

# 위도, 경도 관련 컬럼 합치기
latitude_columns = [col for col in df.columns if '위도' in col]
longitude_columns = [col for col in df.columns if '경도' in col]
df['c위도'] = df[latitude_columns].bfill(axis=1).iloc[:, 0]
df['c경도'] = df[longitude_columns].bfill(axis=1).iloc[:, 0]

# 주민센터명 관련 컬럼 합치기
center_name_columns = [col for col in df.columns if any(x in col for x in ['행정동', '주민센터', '시설명', '기관명', '동주민센터', '주민센터명', '동']) and '상위' not in col]
def normalize_center_name(row):
    for value in row:
        if value and value != 'nan':
            name = str(value).strip()
            return name if name.endswith('주민센터') else name + ' 주민센터'
    return ''

df['c주민센터명'] = df[center_name_columns].astype(str).apply(normalize_center_name, axis=1)

number_columns = [col for col in df.columns if any(x in col for x in '전화')]
df['c전화'] = df[number_columns].astype(str).apply(lambda row: next((x for x in row if x and x != 'nan'), ''), axis=1)

# # 불필요한 원본 컬럼 제거
# columns_to_drop = list(set(address_columns + latitude_columns + longitude_columns + center_name_columns))
# df.drop(columns=columns_to_drop, inplace=True)

# 정리된 결과 저장
cleaned_path = "cleaned_merged_dong_center_data.csv"
df.to_csv(cleaned_path, index=False, encoding="utf-8-sig")

