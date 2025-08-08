import os
import json
import pandas as pd
from openai import OpenAI
from typing import List, Dict, Any

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def upload_csv_to_vector_store(csv_path: str, vector_store_id: str = None) -> str:
    """CSV 파일을 텍스트로 변환하여 OpenAI Vector Store에 업로드"""
    try:
        # 벡터 스토어 생성 (ID가 없는 경우)
        if not vector_store_id:
            vector_store = client.vector_stores.create(
                name=f"dong_data_{os.path.basename(csv_path)}"
            )
            vector_store_id = vector_store.id
            print(f"새 벡터 스토어 생성: {vector_store_id}")
        
        # CSV를 텍스트 형태로 변환
        df = pd.read_csv(csv_path)
        
        # 각 행을 자연어 문장으로 변환
        text_content = []
        for _, row in df.iterrows():
            if '주소' in row and '주민센터명' in row:
                line = f"{row['주민센터명']}는 {row['주소']}에 위치하고 있습니다."
                if '전화' in row:
                    line += f" 전화번호는 {row['전화']}입니다."
                if '위도' in row and '경도' in row:
                    line += f" 좌표는 위도 {row['위도']}, 경도 {row['경도']}입니다."
                text_content.append(line)
        
        # 임시 텍스트 파일 생성
        temp_txt_path = csv_path.replace('.csv', '_converted.txt')
        with open(temp_txt_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(text_content))
        
        # 텍스트 파일 업로드
        with open(temp_txt_path, 'rb') as file:
            file_obj = client.files.create(
                file=file,
                purpose='assistants'
            )
        
        # 벡터 스토어에 파일 추가
        vector_store_file = client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_obj.id
        )
        
        # 임시 파일 삭제
        os.remove(temp_txt_path)
        
        print(f"CSV 파일 변환 및 업로드 완료: {csv_path}")
        print(f"파일 ID: {file_obj.id}")
        print(f"벡터 스토어 ID: {vector_store_id}")
        
        return vector_store_id
        
    except Exception as e:
        print(f"CSV 업로드 중 오류: {e}")
        return None

def upload_text_to_vector_store(text_path: str, vector_store_id: str = None) -> str:
    """텍스트 파일을 OpenAI Vector Store에 업로드"""
    try:
        # 벡터 스토어 생성 (ID가 없는 경우)
        if not vector_store_id:
            vector_store = client.vector_stores.create(
                name=f"text_data_{os.path.basename(text_path)}"
            )
            vector_store_id = vector_store.id
            print(f"새 벡터 스토어 생성: {vector_store_id}")
        
        # 파일 업로드
        with open(text_path, 'rb') as file:
            file_obj = client.files.create(
                file=file,
                purpose='assistants'
            )
        
        # 벡터 스토어에 파일 추가
        vector_store_file = client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_obj.id
        )
        
        print(f"텍스트 파일 업로드 완료: {text_path}")
        print(f"파일 ID: {file_obj.id}")
        print(f"벡터 스토어 ID: {vector_store_id}")
        
        return vector_store_id
        
    except Exception as e:
        print(f"텍스트 업로드 중 오류: {e}")
        return None

def upload_json_to_vector_store(json_path: str, vector_store_id: str = None) -> str:
    """JSON 파일을 OpenAI Vector Store에 업로드"""
    try:
        # 벡터 스토어 생성 (ID가 없는 경우)
        if not vector_store_id:
            vector_store = client.vector_stores.create(
                name=f"json_data_{os.path.basename(json_path)}"
            )
            vector_store_id = vector_store.id
            print(f"새 벡터 스토어 생성: {vector_store_id}")
        
        # 파일 업로드
        with open(json_path, 'rb') as file:
            file_obj = client.files.create(
                file=file,
                purpose='assistants'
            )
        
        # 벡터 스토어에 파일 추가
        vector_store_file = client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_obj.id
        )
        
        print(f"JSON 파일 업로드 완료: {json_path}")
        print(f"파일 ID: {file_obj.id}")
        print(f"벡터 스토어 ID: {vector_store_id}")
        
        return vector_store_id
        
    except Exception as e:
        print(f"JSON 업로드 중 오류: {e}")
        return None

def main():
    """cleaned 폴더의 모든 파일을 OpenAI Vector Store에 업로드"""
    cleaned_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "cleaned")
    
    # 환경 변수 확인
    if not os.getenv('OPENAI_API_KEY'):
        print("OPENAI_API_KEY 환경 변수를 설정해주세요.")
        return
    
    # 통합 벡터 스토어 생성
    vector_store = client.vector_stores.create(
        name="team1_rag_documents"
    )
    vector_store_id = vector_store.id
    print(f"통합 벡터 스토어 생성: {vector_store_id}")
    
    uploaded_files = []
    
    # cleaned 폴더의 모든 파일 처리
    for filename in os.listdir(cleaned_folder):
        file_path = os.path.join(cleaned_folder, filename)
        
        if filename.endswith('.csv'):
            result = upload_csv_to_vector_store(file_path, vector_store_id)
            if result:
                uploaded_files.append(filename)
                
        elif filename.endswith('.txt'):
            result = upload_text_to_vector_store(file_path, vector_store_id)
            if result:
                uploaded_files.append(filename)
                
        elif filename.endswith('.json'):
            result = upload_json_to_vector_store(file_path, vector_store_id)
            if result:
                uploaded_files.append(filename)
    
    # 업로드 결과 출력
    print("\n=== 업로드 완료 ===")
    print(f"벡터 스토어 ID: {vector_store_id}")
    print(f"업로드된 파일 수: {len(uploaded_files)}")
    print("업로드된 파일들:")
    for file in uploaded_files:
        print(f"  - {file}")
    
    # 결과를 JSON으로 저장
    result_data = {
        "vector_store_id": vector_store_id,
        "uploaded_files": uploaded_files,
        "upload_timestamp": pd.Timestamp.now().isoformat()
    }
    
    with open("upload_result.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print("\n업로드 결과가 upload_result.json에 저장되었습니다.")

if __name__ == "__main__":
    main()