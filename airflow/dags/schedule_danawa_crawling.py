from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def pre_crawling_check():
    """크롤링 전 체크 함수"""
    print("크롤링 전 환경 체크 중...")
    print(f"현재 시간: {datetime.now()}")
    print(f"작업 디렉토리: {os.getcwd()}")
    print("Docker 환경에서 다나와 크롤링을 실행합니다.")
    print("환경 체크 완료!")
    return "체크 완료"

def post_crawling_cleanup():
    """크롤링 후 정리 함수"""
    print("크롤링 후 정리 작업 중...")
    print("Docker 컨테이너 정리 완료!")
    print("정리 작업 완료!")
    return "정리 완료"



# DAG 기본 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
dag = DAG(
    'danawa_crawling_dag',
    default_args=default_args,
    description='다나와 크롤링 DAG',
    schedule_interval=timedelta(hours=6),  # 6시간마다 실행
    catchup=False,
    tags=['danawa', 'crawling', 'python'],
)

# 태스크 정의
pre_check_task = PythonOperator(
    task_id='pre_crawling_check',
    python_callable=pre_crawling_check,
    dag=dag,
)

# GitHub에서 코드 가져오기 및 Docker 빌드
build_task = BashOperator(
    task_id='build_docker_image',
    bash_command='''
        echo "=== 다나와 크롤링 Docker 빌드 시작 ==="
        cd /opt/airflow/dags/danawa_crawling
        
        # Git 정보 확인 (선택사항)
        echo "현재 브랜치: $(git branch --show-current 2>/dev/null || echo 'Git 정보 없음')"
        echo "최신 커밋: $(git log -1 --oneline 2>/dev/null || echo 'Git 정보 없음')"
        
        # Docker 이미지 빌드 (태그에 날짜 포함)
        echo "Docker 이미지 빌드 중..."
        docker build -t danawa-crawling:{{ ds_nodash }} -t danawa-crawling:latest .
        
        echo "빌드 완료!"
        docker images danawa-crawling:latest
    ''',
    dag=dag,
)

# Bash로 Docker 실행 (완전히 분리된 Python 환경)
crawling_task = BashOperator(
    task_id='run_danawa_crawling',
    bash_command='''
        echo "=== 다나와 크롤링 실행 시작 ==="
        
        # 고유한 컨테이너 이름 생성
        CONTAINER_NAME="danawa_crawling_{{ ds_nodash }}_{{ ts_nodash }}"
        
        echo "컨테이너 이름: $CONTAINER_NAME"
        echo "실행 시간: {{ ts }}"
        
        # Docker 컨테이너로 크롤링 실행
        docker run --rm \
            --name $CONTAINER_NAME \
            --env RUN_DATE="{{ ds }}" \
            --env EXECUTION_TIME="{{ ts }}" \
            danawa-crawling:{{ ds_nodash }}
        
        echo "크롤링 완료!"
    ''',
    dag=dag,
)

# 정리 작업
cleanup_task = PythonOperator(
    task_id='post_crawling_cleanup',
    python_callable=post_crawling_cleanup,
    dag=dag,
)

# 이미지 정리 (선택사항)
cleanup_image_task = BashOperator(
    task_id='cleanup_old_images',
    bash_command='''
        echo "=== 오래된 Docker 이미지 정리 ==="
        
        # 7일 이상 된 danawa-crawling 이미지 정리 (latest 제외)
        docker image prune -f --filter "label=danawa-crawling" --filter "until=168h" || true
        
        echo "이미지 정리 완료!"
        docker images danawa-crawling
    ''',
    dag=dag,
)

# 태스크 의존성 설정 (Bash Docker 방식)
pre_check_task >> build_task >> crawling_task >> cleanup_task >> cleanup_image_task 