# Python 3.9 베이스 이미지 사용
FROM python:3.9

# 필요한 소스만 복사
WORKDIR /app

# non-root 사용자 생성
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd -m appuser \
    && chown -R appuser:appuser /app

# 사용자 전환
USER appuser

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]