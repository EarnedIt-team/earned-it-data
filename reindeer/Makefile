# Reindeer Project Makefile
.PHONY: help run check format lint test test-cov clean install dev-setup

# 기본 타겟
help: ## 도움말 표시
	@echo "사용 가능한 명령어:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 개발 환경
install: ## 의존성 설치
	uv sync

dev-setup: install ## 개발 환경 초기 설정
	uv run pre-commit install
	@echo "✅ 개발 환경 설정 완료"
	@echo "💡 .env 파일을 생성하고 환경변수를 설정해주세요"

# 서버 실행
run: ## 개발 서버 실행
	uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000

run-prod: ## 프로덕션 서버 실행
	uv run uvicorn app.app:app --host 0.0.0.0 --port 8000

# 코드 품질
format: ## 코드 포맷팅 (black + isort)
	uv run black .
	uv run isort .
	@echo "✅ 코드 포맷팅 완료"

lint: ## 린팅 검사 (flake8 + mypy)
	uv run flake8 .
	uv run mypy .
	@echo "✅ 린팅 검사 완료"

# 테스트
test: ## 단위 테스트 실행
	uv run pytest tests/unit/ -v

test-integration: ## 통합 테스트 실행
	uv run pytest tests/integration/ -v

test-all: ## 모든 테스트 실행
	uv run pytest -v

test-cov: ## 커버리지 포함 테스트 실행
	uv run pytest --cov=app --cov=browser --cov-report=html --cov-report=term-missing
	@echo "📊 커버리지 리포트: htmlcov/index.html"

# 종합 검사
check: format lint test ## 모든 검사 실행 (CI/CD용)
	@echo "🎉 모든 검사 통과!"

# 정리
clean: ## 임시 파일 정리
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "🧹 정리 완료"

# 의존성 관리
deps-update: ## 의존성 업데이트
	uv sync --upgrade

deps-add: ## 새 의존성 추가 (예: make deps-add PACKAGE=requests)
	uv add $(PACKAGE)

# 개발 유틸리티
shell: ## Python REPL 실행
	uv run python

api-docs: ## API 문서 서버 실행 (별도 터미널에서)
	@echo "🚀 API 문서: http://localhost:8000/docs"
	@echo "🚀 ReDoc: http://localhost:8000/redoc"

# Docker (향후 사용)
docker-build: ## Docker 이미지 빌드
	docker build -t reindeer:latest .

docker-run: ## Docker 컨테이너 실행
	docker run -p 8000:8000 reindeer:latest