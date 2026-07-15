@echo off
echo ===================================================
echo   [Firebase Hosting] Tzuyang Food Map Deployment
echo ===================================================
echo.

:: 1. firebase CLI 존재 여부 점검
where firebase >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Firebase CLI (firebase-tools)가 설치되어 있지 않습니다.
    echo npm install -g firebase-tools 명령어를 실행하여 설치해 주세요.
    pause
    exit /b 1
)

:: 2. Firebase 로그인 상태 점검 및 시도
echo [INFO] Firebase 로그인 상태를 확인합니다...
call firebase login

:: 3. 프로젝트 초기 선택 안내
echo.
echo [INFO] 사용 가능한 Firebase 프로젝트 목록을 불러옵니다...
call firebase projects:list
echo.
echo ===================================================
echo  원하는 프로젝트 ID를 복사하여 아래에 입력하세요.
echo  (새 프로젝트 생성이 필요한 경우 파이어베이스 콘솔이나 
echo   firebase projects:create 명령을 활용해 주십시오.)
echo ===================================================
set /p PROJ_ID="배포 프로젝트 ID 입력: "

if "%PROJ_ID%"=="" (
    echo [ERROR] 프로젝트 ID가 비어 있어 배포를 취소합니다.
    pause
    exit /b 1
)

:: 4. 프로젝트 바인딩 및 배포
echo [INFO] 배포 타겟 프로젝트를 %PROJ_ID% 로 지정합니다...
call firebase use %PROJ_ID%

echo [INFO] Firebase Hosting 배포를 개시합니다...
call firebase deploy --only hosting

echo.
echo [SUCCESS] 배포 완료! 생성된 호스팅 URL로 접속해 보세요.
pause
