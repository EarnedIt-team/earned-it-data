# Airflow Docker Compose 관리를 위한 Makefile
# 사용법: make <command>

# 기본 명령어
.PHONY: help start stop restart status logs logs-git clean build

# 도움말 (기본 명령어)
help:
	@echo "🚀 Airflow Docker Compose 관리 명령어"
	@echo "=================================="
	@echo "make start       - Airflow 서버 시작"
	@echo "make stop        - Airflow 서버 중지"
	@echo "make restart     - Airflow 서버 재시작"
	@echo "make status      - 서비스 상태 확인"
	@echo "make logs        - 전체 로그 확인"
	@echo "make logs-git    - Git-sync 로그 확인"
	@echo "make logs-web    - 웹서버 로그 확인"
	@echo "make logs-sch    - 스케줄러 로그 확인"
	@echo "make build       - 이미지 빌드 후 시작"
	@echo "make clean       - 모든 컨테이너/볼륨 정리"
	@echo "make reset       - 완전 초기화 (데이터 삭제)"
	@echo ""
	@echo "🔧 고급 명령어"
	@echo "make exec-web    - 웹서버 컨테이너 접속"
	@echo "make exec-sch    - 스케줄러 컨테이너 접속"
	@echo "make sync-check  - Git 동기화 상태 확인"
	@echo "make env-check   - 환경변수 확인"

# 서버 시작
start:
	@echo "🚀 Airflow 서버를 시작합니다..."
	sudo docker-compose up -d
	@echo "✅ 서버가 시작되었습니다!"
	@echo "🌐 웹 UI: http://localhost:8080"
	@echo "👤 사용자명: airflow | 비밀번호: airflow"

# 서버 중지
stop:
	@echo "🛑 Airflow 서버를 중지합니다..."
	sudo docker-compose down
	@echo "✅ 서버가 중지되었습니다!"

# 서버 재시작
restart:
	@echo "🔄 Airflow 서버를 재시작합니다..."
	sudo docker-compose down
	sudo docker-compose up -d
	@echo "✅ 서버가 재시작되었습니다!"
	@echo "🌐 웹 UI: http://localhost:8080"

# 서비스 상태 확인
status:
	@echo "📊 Airflow 서비스 상태:"
	sudo docker-compose ps

# 전체 로그 확인
logs:
	@echo "📋 전체 로그를 확인합니다..."
	sudo docker-compose logs

# Git-sync 로그 확인
logs-git:
	@echo "📋 Git-sync 로그를 확인합니다..."
	sudo docker-compose logs git-sync

# 웹서버 로그 확인
logs-web:
	@echo "📋 웹서버 로그를 확인합니다..."
	sudo docker-compose logs airflow-webserver

# 스케줄러 로그 확인
logs-sch:
	@echo "📋 스케줄러 로그를 확인합니다..."
	sudo docker-compose logs airflow-scheduler

# 이미지 빌드 후 시작
build:
	@echo "🔨 Docker 이미지를 빌드하고 서버를 시작합니다..."
	sudo docker-compose build
	sudo docker-compose up -d
	@echo "✅ 빌드 완료 및 서버 시작됨!"

# 컨테이너 정리 (볼륨 유지)
clean:
	@echo "🧹 컨테이너를 정리합니다..."
	sudo docker-compose down
	sudo docker system prune -f
	@echo "✅ 정리 완료!"

# 완전 초기화 (데이터베이스 포함)
reset:
	@echo "⚠️  완전 초기화를 진행합니다 (모든 데이터 삭제)..."
	@read -p "정말 진행하시겠습니까? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		sudo docker-compose down -v; \
		sudo docker system prune -f; \
		echo "✅ 완전 초기화 완료!"; \
	else \
		echo "❌ 취소되었습니다."; \
	fi

# 웹서버 컨테이너 접속
exec-web:
	@echo "🖥️  웹서버 컨테이너에 접속합니다..."
	sudo docker-compose exec airflow-webserver bash

# 스케줄러 컨테이너 접속
exec-sch:
	@echo "🖥️  스케줄러 컨테이너에 접속합니다..."
	sudo docker-compose exec airflow-scheduler bash

# Git 동기화 상태 확인
sync-check:
	@echo "🔄 Git 동기화 상태를 확인합니다..."
	@echo "마지막 Git-sync 로그:"
	sudo docker-compose logs --tail=10 git-sync

# 환경변수 확인
env-check:
	@echo "⚙️  현재 환경변수 설정:"
	@echo "Airflow 사용자: $$(grep _AIRFLOW_WWW_USER_USERNAME .env | cut -d'=' -f2)"
	@echo "Git 레포지토리: $$(grep GIT_SYNC_REPO .env | cut -d'=' -f2)"
	@echo "Git 브랜치: $$(grep GIT_SYNC_BRANCH .env | cut -d'=' -f2)"
	@echo "동기화 간격: $$(grep GIT_SYNC_WAIT .env | cut -d'=' -f2)초"

# 실시간 로그 모니터링
logs-follow:
	@echo "📋 실시간 로그를 모니터링합니다 (Ctrl+C로 종료)..."
	sudo docker-compose logs -f

# Git-sync 실시간 로그
logs-git-follow:
	@echo "📋 Git-sync 실시간 로그를 모니터링합니다 (Ctrl+C로 종료)..."
	sudo docker-compose logs -f git-sync

# 포트 확인
port-check:
	@echo "🔍 포트 사용 상태:"
	@echo "Airflow 웹서버 (8080):"
	@sudo netstat -tlnp | grep :8080 || echo "포트 8080이 사용되지 않음"
	@echo "PostgreSQL (5432):"
	@sudo netstat -tlnp | grep :5432 || echo "포트 5432가 사용되지 않음"

# 빠른 재시작 (git-sync만)
restart-git:
	@echo "🔄 Git-sync만 재시작합니다..."
	sudo docker-compose restart git-sync
	@echo "✅ Git-sync가 재시작되었습니다!"

# 개발 모드 (로그 출력하며 실행)
dev:
	@echo "🛠️  개발 모드로 실행합니다..."
	sudo docker-compose up

# 기본 타겟을 help로 설정
.DEFAULT_GOAL := help 