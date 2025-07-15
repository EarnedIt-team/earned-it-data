from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

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
    'test_dag',
    default_args=default_args,
    description='test DAG',
    schedule_interval=timedelta(hours=6),  # 6시간마다 실행
    catchup=False,
    tags=['test', 'python'],
)

# Docker 이미지 빌드
build_task = BashOperator(
    task_id='test_task',
    bash_command='''
        echo "=== test task 시작 ==="
        
        # 경로 디버깅
        echo "DAGs 루트 경로 확인:"
        ls -la /opt/airflow/dags/
        
        # danawa_crawling 경로 찾기
        TEST_PATH=""
        if [ -d "/opt/airflow/dags/test_src" ]; then
            TEST_PATH="/opt/airflow/dags/test_src"
        elif [ -d "/opt/airflow/dags/airflow/dags/test_src" ]; then
            TEST_PATH="/opt/airflow/dags/airflow/dags/test_src"
        else
            echo "ERROR: test_src 경로를 찾을 수 없습니다"
            find /opt/airflow/dags -name "test_src" -type d
            exit 1
        fi
        
        echo "test_src 경로: $TEST_PATH"
        cd $TEST_PATH
        
        # 현재 경로 확인
        echo "현재 경로: $(pwd)"
        echo "파일 목록:"
        ls -la
        
        # Docker 이미지 빌드
        echo "Docker 이미지 빌드 중..."
        docker build -t test:{{ ds_nodash }} -t test:latest .
        
        echo "빌드 완료!"
        docker images test:latest
    ''',
    dag=dag,
)

# 크롤링 실행
test_task = BashOperator(
    task_id='run_test',
    bash_command='''
        echo "=== test 실행 시작 ==="
        
        # 고유한 컨테이너 이름 생성
        CONTAINER_NAME="test_{{ ds_nodash }}_{{ ts_nodash }}"
        
        echo "컨테이너 이름: $CONTAINER_NAME"
        echo "실행 시간: {{ ts }}"
        
        # Docker 컨테이너로 크롤링 실행
        docker run --rm \
            --name $CONTAINER_NAME \
            --env RUN_DATE="{{ ds }}" \
            --env EXECUTION_TIME="{{ ts }}" \
            test:{{ ds_nodash }}
        
        echo "test 완료!"
    ''',
    dag=dag,
)

# 이미지 정리
cleanup_image_task = BashOperator(
    task_id='cleanup_old_images',
    bash_command='''
        echo "=== 오래된 Docker 이미지 정리 ==="
        
        # 7일 이상 된 test 이미지 정리 (latest 제외)
        docker image prune -f --filter "label=test" --filter "until=168h" || true
        
        echo "이미지 정리 완료!"
        docker images test
    ''',
    dag=dag,
)

# 태스크 의존성 설정
build_task >> test_task >> cleanup_image_task 