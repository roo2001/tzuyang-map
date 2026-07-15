@echo off
title 쯔양 맛집 지도 로컬 서버 실행기 (Port: 8085)
echo ========================================================
echo   쯔양 맛집 지도 로컬 서버 구동기 (M.A.G)
echo   접속 주소: http://localhost:8085/tzuyang_food_map.html
echo ========================================================
echo.

:: 쯔양 맛집 시각화 폴더 경로로 이동
cd /d "F:\Antigravity\Antigravity_data\workspace\01_작업_진행\122_쯔양_맛집_지도_시각화"

:: 1초 대기 후 브라우저 열기
timeout /t 1 /nobreak > nul
start http://localhost:8085/tzuyang_food_map.html

:: 파이썬 간이 HTTP 웹서버 구동 (8085 포트)
python -m http.server 8085
