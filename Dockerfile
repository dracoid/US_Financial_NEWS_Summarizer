FROM python:3.10-slim

# 작업 디렉토리
WORKDIR /app

# 전체 복사
COPY . /app

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 기본 실행 명령
CMD ["python", "run_summarize.py"]
