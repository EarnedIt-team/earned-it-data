#!/usr/bin/env python3
"""
다나와 전체 카테고리 크롤링 메인 실행 파일
"""

import os
import sys
from datetime import datetime

# src 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """메인 실행 함수"""
    # Airflow에서 전달받은 환경변수
    run_date = os.getenv('RUN_DATE', 'Unknown')
    execution_time = os.getenv('EXECUTION_TIME', 'Unknown')
    
    print("=" * 80)
    print("🕷️  test 시작!")
    print(f"📅 실행 날짜: {run_date}")
    print(f"⏰ 실행 시간: {execution_time}")
    print(f"🐍 Python 환경: {sys.version}")
    print(f"🏠 작업 디렉토리: {os.getcwd()}")
    print("=" * 80)
    
    print("test 완료!")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
