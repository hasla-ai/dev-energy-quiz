def display_menu():
    print("\n" + "="*30)
    print("   증기기관 퀴즈 프로그램")
    print("="*30)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록 보기")
    print("4. 점수 확인")
    print("5. 퀴즈 삭제")
    print("6. 기록 히스토리")
    print("7. 종료")
    print("="*30)

def main():
    while True:
        display_menu()
    ## input().strip(): 사용자 입력 앞뒤의 공백을 제거하여 오타로 인한 오류를 방지합니다.    
        choice = input("원하는 기능의 번호를 입력하세요: ").strip()
# Placeholder: 구현 예정. print 문으로 어떤 기능이 실행될지 표시만
        if choice == '1':
            print("\n[알림] 퀴즈 풀기 기능을 시작합니다. (구현 예정)")
        elif choice == '2':
            print("\n[알림] 퀴즈 추가 모드입니다. (구현 예정)")
        elif choice == '3':
            print("\n[알림] 저장된 퀴즈 목록을 불러옵니다. (구현 예정)")
        elif choice == '4':
            print("\n[알림] 현재까지의 점수를 확인합니다. (구현 예정)")
        elif choice == '5':
            print("\n[알림] 퀴즈 삭제 모드입니다. (구현 예정)")
        elif choice == '6':
            print("\n[알림] 학습 기록 히스토리를 출력합니다. (구현 예정)")
        elif choice == '7':
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        else:
            # 잘못된 입력(숫자가 아니거나 범위를 벗어난 경우) 처리
            print("\n[오류] 잘못된 입력입니다. 1번부터 7번 사이의 숫자를 입력해주세요.")

if __name__ == "__main__":
    main()