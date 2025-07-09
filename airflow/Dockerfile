FROM apache/airflow:2.8.0-python3.11

# Poetry 설치를 위한 의존성 및 Docker CLI
USER root
RUN apt-get update && apt-get install -y curl build-essential docker.io

# Docker 그룹에 airflow 사용자 추가 (그룹이 없으면 생성)
RUN groupadd -f docker && usermod -aG docker airflow

# airflow 사용자로 변경
USER airflow

# 작업 디렉토리로 변경
WORKDIR /opt/airflow

# Poetry 설치 (사용자 공간)
RUN pip install --user poetry==1.7.1

# PATH에 Poetry 추가
ENV PATH="/home/airflow/.local/bin:$PATH"

# Poetry 설정 (프로젝트 디렉토리에 가상환경 생성)
RUN poetry config virtualenvs.in-project true
RUN poetry config virtualenvs.path /tmp/venv

# pyproject.toml 복사
COPY --chown=airflow:root pyproject.toml ./

# 의존성 설치 (사용자 공간)
ENV PIP_USER=1
RUN poetry install --only=main --no-root

# 나머지 파일들 복사
COPY --chown=airflow:root . . 