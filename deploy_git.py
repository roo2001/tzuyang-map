import subprocess
import sys
import shutil

def run_cmd(cmd_list, shell=True):
    try:
        subprocess.run(cmd_list, shell=shell, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Command failed: {' '.join(cmd_list)}")
        print(f"Error Details: {e}")
        return False

def main():
    # 윈도우 콘솔 한글 처리
    sys.stdout.reconfigure(encoding='utf-8')

    print("===================================================")
    print("   [GitHub Pages] Tzuyang Food Map Git Deployment")
    print("===================================================")
    print()

    # 1. Git 설치 체크
    if not shutil.which("git"):
        print("[ERROR] Git이 설치되어 있지 않거나 시스템 PATH에 등록되지 않았습니다.")
        print("Git을 설치한 뒤 다시 구동해 주십시오.")
        sys.exit(1)

    # 2. 브랜치 main 지정
    print("[INFO] 기본 브랜치를 main으로 설정합니다...")
    run_cmd(["git", "branch", "-M", "main"])

    # 3. 원격 URL 입력
    print("\n" + "=" * 55)
    print("  GitHub에서 새로 생성한 레포지토리 주소를 입력하세요.")
    print("  (예: https://github.com/roo2001/tzuyang-map.git)")
    print("=" * 55)
    
    try:
        repo_url = input("GitHub 저장소 URL 입력: ").strip()
    except KeyboardInterrupt:
        print("\n[INFO] 배포가 취소되었습니다.")
        sys.exit(0)

    if not repo_url:
        print("[ERROR] 저장소 주소가 입력되지 않았습니다.")
        sys.exit(1)

    # 4. 원격 연결 설정
    print("\n[INFO] 원격 저장소 origin 연결을 재설정합니다...")
    run_cmd(["git", "remote", "remove", "origin"])
    if not run_cmd(["git", "remote", "add", "origin", repo_url]):
        print("[ERROR] 원격 저장소 추가에 실패했습니다.")
        sys.exit(1)

    # 5. 자산 재-커밋 확인
    run_cmd(["git", "add", "tzuyang_food_map.html", "tzuyang_restaurants_coords.json", "service-worker.js", "manifest.json", "icon.png"])
    # 로컬 설정이 되어 있으므로 무조건 커밋을 시도함 (변경사항이 없더라도 에러 생략)
    subprocess.run(["git", "commit", "-m", "feat: Release 697-item Tzuyang Food Map Dashboard"], shell=True, capture_output=True)

    # 6. Push
    print("\n[INFO] GitHub로 코드 전송을 시작합니다. 브라우저 로그인 창이 뜨면 승인해 주세요...")
    if run_cmd(["git", "push", "-u", "origin", "main"]):
        print("\n" + "=" * 55)
        print("  [SUCCESS] 깃허브 업로드 성공!")
        print("  ")
        print("  배포를 마감하기 위해 아래 링크로 접속하셔서")
        print("  GitHub Pages 브랜치를 [main]으로 설정해 저장해 주세요!")
        print(f"  * 설정 페이지: {repo_url.replace('.git', '')}/settings/pages")
        print(f"  * 완성 주소  : https://roo2001.github.io/tzuyang-map/tzuyang_food_map.html")
        print("=" * 55)
    else:
        print("[ERROR] GitHub 업로드 도중 오류가 발생했습니다. 권한이나 주소를 점검해 주세요.")
        sys.exit(1)

if __name__ == "__main__":
    main()
