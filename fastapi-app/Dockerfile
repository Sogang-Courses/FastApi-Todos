# Python 3.9 베이스 이미지 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 필요한 소스만 복사
COPY . .

# non-root 사용자 생성
RUN useradd -m appuser

# 사용자 전환
USER appuser

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]