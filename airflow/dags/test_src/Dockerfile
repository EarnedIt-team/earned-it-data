FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome 설치
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install poetry==1.7.1

# Poetry 설정 (가상환경 비활성화)
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# 의존성 파일 복사
COPY pyproject.toml poetry.lock* ./

# 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-root \
    && rm -rf $POETRY_CACHE_DIR

# 소스 코드 복사
COPY . .

# 실행 권한 설정
RUN chmod +x main.py

# 환경 변수 설정
ENV DISPLAY=:99
ENV PYTHONPATH=/app

# 기본 명령어
CMD ["python", "main.py"] 