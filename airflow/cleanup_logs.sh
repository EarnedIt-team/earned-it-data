#!/bin/bash
# Airflow 로그 정리 스크립트
# 서버 용량 절약을 위한 로그 관리

echo "🧹 Airflow 로그 정리 시작..."

# 3일 이상 된 로그 파일 삭제
find ./logs -type f -name "*.log" -mtime +3 -exec rm -f {} \;

# 빈 로그 디렉토리 삭제 (단, .gitkeep 파일이 있는 경우는 제외)
find ./logs -type d -empty -exec rmdir {} \; 2>/dev/null || true

# Docker 로그 정리 (정지된 컨테이너의 로그)
docker system prune -f --volumes 2>/dev/null || true

# 로그 파일 크기 체크 및 대용량 파일 압축
find ./logs -type f -name "*.log" -size +50M -exec gzip {} \; 2>/dev/null || true

echo "✅ 로그 정리 완료!"
echo "💾 현재 로그 디렉토리 크기:"
du -sh ./logs 2>/dev/null || echo "로그 디렉토리 크기 측정 불가" 