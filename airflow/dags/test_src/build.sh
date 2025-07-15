#!/bin/bash

# 다나와 크롤링 Docker 이미지 빌드 스크립트

echo "다나와 크롤링 Docker 이미지 빌드 시작..."

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# Poetry lock 파일 생성 (없는 경우)
if [ ! -f "poetry.lock" ]; then
    echo "Poetry lock 파일 생성 중..."
    poetry lock
fi

# Docker 이미지 빌드
echo "Docker 이미지 빌드 중..."
docker build -t danawa-crawling:latest .

# 빌드 결과 확인
if [ $? -eq 0 ]; then
    echo "✅ Docker 이미지 빌드 완료!"
    echo "이미지 정보:"
    docker images danawa-crawling:latest
    echo ""
    echo "테스트 실행:"
    echo "docker run --rm danawa-crawling:latest"
else
    echo "❌ Docker 이미지 빌드 실패!"
    exit 1
fi 