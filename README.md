# 🦌 Earned-It Data Engine

마포 지역 기반 제품 검색 및 데이터 처리 엔진

## 📋 프로젝트 개요

Earned-It Data는 마포구 지역 상권 분석 및 제품 검색 서비스를 위한 데이터 엔진입니다. 네이버 쇼핑 API를 활용한 실시간 제품 검색과 이미지 처리, 그리고 Airflow를 통한 데이터 파이프라인을 제공합니다.

## 🏗️ 아키텍처

```
earned-it-data/
├── airflow/          # 데이터 파이프라인 (Airflow)
│   ├── dags/         # DAG 정의
│   └── plugins/      # 커스텀 플러그인
└── reindeer/         # 제품 검색 API 서버
    ├── app/          # FastAPI 애플리케이션
    └── browser/      # 헥사고날 아키텍처 기반 비즈니스 로직
```
