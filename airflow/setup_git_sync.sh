#!/bin/bash
# GitHub DAGs 자동 동기화 설정 스크립트

echo "🔧 GitHub DAGs 자동 동기화 설정"
echo "==============================="

# 1. SSH 키 생성 확인
if [ ! -f "./ssh/id_rsa" ]; then
    echo "🔑 SSH 키가 없습니다. 새로 생성하시겠습니까? (y/n)"
    read -r create_key
    
    if [ "$create_key" = "y" ]; then
        echo "📧 GitHub 계정 이메일을 입력하세요:"
        read -r email
        
        echo "🔄 SSH 키 생성 중..."
        ssh-keygen -t rsa -b 4096 -C "$email" -f ./ssh/id_rsa -N ""
        
        chmod 600 ./ssh/id_rsa
        chmod 644 ./ssh/id_rsa.pub
        chmod 700 ./ssh
        
        echo "✅ SSH 키 생성 완료!"
        echo "📋 다음 공개 키를 GitHub에 등록하세요:"
        echo "--------------------------------------------"
        cat ./ssh/id_rsa.pub
        echo "--------------------------------------------"
        echo ""
        echo "🔗 GitHub 설정 방법:"
        echo "1. GitHub → Settings → SSH and GPG keys"
        echo "2. 'New SSH key' 클릭"
        echo "3. 위의 공개 키 내용 붙여넣기"
        echo "4. 'Add SSH key' 클릭"
        echo ""
    fi
fi

# 2. .env 파일 설정
if [ ! -f ".env" ]; then
    echo "🔧 .env 파일을 생성하시겠습니까? (y/n)"
    read -r create_env
    
    if [ "$create_env" = "y" ]; then
        cp env.example .env
        echo "📝 .env 파일이 생성되었습니다."
    fi
fi

# 3. Git 저장소 URL 설정
echo "📁 GitHub 저장소 URL을 입력하세요:"
echo "예: git@github.com:username/repo.git (SSH 방식)"
echo "예: https://github.com/username/repo.git (HTTPS 방식)"
read -r repo_url

if [ -n "$repo_url" ]; then
    # .env 파일에서 GIT_SYNC_REPO 업데이트
    if [ -f ".env" ]; then
        sed -i.bak "s|GIT_SYNC_REPO=.*|GIT_SYNC_REPO=$repo_url|" .env
        rm .env.bak 2>/dev/null || true
        echo "✅ .env 파일이 업데이트되었습니다."
    fi
fi

# 4. 브랜치 설정
echo "🌿 사용할 브랜치를 입력하세요 (기본: main):"
read -r branch
branch=${branch:-main}

if [ -f ".env" ]; then
    sed -i.bak "s|GIT_SYNC_BRANCH=.*|GIT_SYNC_BRANCH=$branch|" .env
    rm .env.bak 2>/dev/null || true
fi

# 5. 동기화 간격 설정
echo "⏰ 동기화 간격을 초 단위로 입력하세요 (기본: 60):"
read -r wait_time
wait_time=${wait_time:-60}

if [ -f ".env" ]; then
    sed -i.bak "s|GIT_SYNC_WAIT=.*|GIT_SYNC_WAIT=$wait_time|" .env
    rm .env.bak 2>/dev/null || true
fi

echo ""
echo "🎉 설정 완료!"
echo "==============="
echo "📁 저장소: $repo_url"
echo "🌿 브랜치: $branch"
echo "⏰ 동기화 간격: ${wait_time}초"
echo ""
echo "🚀 이제 다음 명령어로 Airflow를 시작하세요:"
echo "   ./start.sh"
echo ""
echo "📊 Git 동기화 로그 확인:"
echo "   docker-compose logs -f git-sync" 