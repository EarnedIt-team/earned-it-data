#!/bin/bash

# Airflow 시작 스크립트
echo "Airflow 시작 중..."

# 필요한 폴더 생성
mkdir -p logs dags plugins

# 권한 설정
chmod +x start.sh

# Poetry lock 파일 생성 (없는 경우)
if [ ! -f "poetry.lock" ]; then
    echo "Poetry lock 파일 생성 중..."
    poetry lock
fi

# Docker 이미지 빌드 및 Airflow 실행
echo "Docker 이미지 빌드 및 Airflow 시작 중..."
docker-compose build
docker-compose up -d

echo "Airflow가 시작되었습니다!"
echo "웹 UI: http://localhost:8080"
echo "사용자명: airflow"
echo "비밀번호: airflow"
echo ""
echo "상태 확인: docker-compose ps"
echo "로그 확인: docker-compose logs -f"
echo "중지: docker-compose down"
echo ""
echo "Poetry 명령어:"
echo "  의존성 추가: poetry add <package>"
echo "  개발 의존성 추가: poetry add --group dev <package>"
echo "  의존성 제거: poetry remove <package>" 