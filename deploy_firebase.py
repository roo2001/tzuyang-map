import subprocess
import sys
import shutil

def run_cmd(cmd_list, shell=True):
    try:
        result = subprocess.run(cmd_list, shell=shell, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Command failed: {' '.join(cmd_list)}")
        print(f"Error Details: {e}")
        return False

def main():
    print("===================================================")
    print("   [Firebase Hosting] Tzuyang Food Map Deployment")
    print("===================================================")
    print()

    # 1. npx 존재 여부 확인
    if not shutil.which("npx"):
        print("[ERROR] Node.js 및 npm (npx)이 설치되어 있지 않습니다.")
        print("Node.js를 먼저 설치해 주셔야 Firebase Hosting 배포가 가능합니다.")
        sys.exit(1)

    # 2. Firebase 로그인 상태 확인 및 로그인 창 호출
    print("[INFO] npx -y firebase-tools login 세션을 확인/수행합니다...")
    if not run_cmd(["npx", "-y", "firebase-tools", "login"]):
        print("[ERROR] Firebase 로그인 과정 중 오류가 발생했습니다.")
        sys.exit(1)

    # 3. 프로젝트 리스트 검색
    print("\n[INFO] 사용 가능한 Firebase 프로젝트 목록을 조회합니다...")
    run_cmd(["npx", "-y", "firebase-tools", "projects:list"])

    print("\n" + "=" * 55)
    print("  원하는 Firebase 프로젝트 ID를 복사하여 아래에 입력하세요.")
    print("  (프로젝트가 없다면 https://console.firebase.google.com/ 에서 생성 가능)")
    print("=" * 55)
    
    try:
        project_id = input("배포 프로젝트 ID 입력: ").strip()
    except KeyboardInterrupt:
        print("\n[INFO] 사용자에 의해 배포가 취소되었습니다.")
        sys.exit(0)

    if not project_id:
        print("[ERROR] 프로젝트 ID가 입력되지 않아 배포를 중단합니다.")
        sys.exit(1)

    # 4. 프로젝트 설정 바인딩
    print(f"\n[INFO] 배포 타겟 프로젝트를 '{project_id}' 로 변경합니다...")
    if not run_cmd(["npx", "-y", "firebase-tools", "use", project_id]):
        print("[ERROR] 프로젝트 바인딩에 실패했습니다. 올바른 프로젝트 ID인지 확인해 주십시오.")
        sys.exit(1)

    # 5. 최종 배포 구동
    print("\n[INFO] Firebase Hosting 배포를 시작합니다...")
    if run_cmd(["npx", "-y", "firebase-tools", "deploy", "--only", "hosting"]):
        print(f"\n[SUCCESS] 배포 완료! https://{project_id}.web.app 으로 전 세계 어디서든 무설치 앱(PWA) 설치 및 접속이 가능합니다.")
    else:
        print("\n[ERROR] 배포 도중 에러가 발생했습니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()
