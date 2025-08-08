import pandas as pd

# 데이터 불러오기
df = pd.read_csv("cleaned_merged_dong_center_data.csv", encoding="utf-8")

# 'c'로 시작하는 컬럼만 추출
c_columns = [col for col in df.columns if col.startswith('c')]
df_c_only = df[c_columns]

# 컬럼명에서 'c' 제거
df_c_only.columns = [col[1:] for col in c_columns]

# 저장
df_c_only.to_csv("docs/cleaned/dong_data.csv", index=False, encoding="utf-8-sig")
