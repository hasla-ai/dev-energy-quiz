import json
import os

class Quiz: 
    # __init__: 퀴즈 하나가 가져야 할 필수 정보(문제, 4개 선택지, 정답 번호)를 초기화
    def __init__(self, question, choices, answer):
        """
        :param question: 문제 내용 (문자열)
        :param choices: 4개의 선택지 (리스트)
        :param answer: 정답 번호 (1~4 정수)
        """
        self.question = question
        self.choices = choices
        self.answer = answer

    # display_quiz: enumerate를 사용하여 선택지 앞에 1,2,3,4 번호를 자동으로 붙여 출력   
    def display_quiz(self, index):
        """문제를 화면에 출력합니다."""
        print(f"\n[문제 {index}] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    # check_answer: 사용자의 입력값과 정답(self.answer)을 비교하여 True/False를 반환
    def check_answer(self, user_choice):
        """사용자가 입력한 번호가 정답인지 확인합니다."""
        return self.answer == user_choice
    
    # to_dict: 나중에 JSON 파일로 저장할 때 클래스 객체를 바로 저장할 수 없으므로, 딕셔너리로 변환하는 편의 메서드를 추가
    def to_dict(self):
        """데이터 저장을 위해 딕셔너리 형태로 변환합니다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

# 테스트용 예시 데이터 사용법:
# q1 = Quiz("증기기관을 개량한 사람은?", ["뉴커먼", "와트", "에디슨", "테슬라"], 2)
# q1.display_quiz(1)

# [기본 데이터] 파일이 없거나 손상되었을 때 사용할 데이터
DEFAULT_QUIZZES = [
    {"question": "증기기관을 개량하여 산업 혁명을 이끈 사람은?", "answer": "제임스 와트"},
    {"question": "최초의 상업적 증기선을 만든 사람은?", "answer": "로버트 풀턴"}
]

def load_data(filename="quizzes.json"):
    """파일에서 데이터를 로드하며, 예외 발생 시 기본 데이터를 반환합니다."""
    if not os.path.exists(filename):
        print("\n[안내] 데이터 파일이 없어 기본 데이터를 로드합니다.")
        return DEFAULT_QUIZZES
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("\n[오류] 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
        return DEFAULT_QUIZZES

def get_safe_input(prompt, min_val=1, max_val=7):
    """숫자 입력에 대한 모든 예외 처리를 담당하는 함수입니다."""
    while True:
        try:
            user_input = input(prompt).strip() # 1. 공백 제거
            
            if not user_input: # 4. 빈 입력 처리
                print(">> 입력이 비어 있습니다. 번호를 입력해주세요.")
                continue
            
            choice = int(user_input) # 2. 숫자 변환 및 실패 처리
            
            if min_val <= choice <= max_val: # 3. 범위 체크
                return choice
            else:
                print(f">> {min_val}~{max_val} 사이의 숫자를 입력해주세요.")
        
        except ValueError:
            print(">> 잘못된 입력입니다. '숫자'만 입력 가능합니다.")

def display_menu():
    print("\n" + "="*30)
    print("   증기기관 퀴즈 프로그램")
    print("="*30)
    print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 목록 보기")
    print("4. 점수 확인  5. 퀴즈 삭제  6. 히스토리")
    print("7. 종료")
    print("="*30)

def main():
    # 8. 데이터 로드 (파일 부재/손상 대응)
    quizzes = load_data()
    
    try:
        while True:
            display_menu()
            # 안전한 입력 함수 호출
            choice = get_safe_input("선택: ", 1, 7)

            if choice == 1: print("\n[기능] 퀴즈 풀기 시작")
            elif choice == 2: print("\n[기능] 퀴즈 추가")
            elif choice == 3: print(f"\n[목록] 현재 {len(quizzes)}개의 퀴즈가 있습니다.")
            elif choice == 4: print("\n[기능] 점수 확인")
            elif choice == 5: print("\n[기능] 퀴즈 삭제")
            elif choice == 6: print("\n[기능] 히스토리 확인")
            elif choice == 7:
                print("\n프로그램을 안전하게 종료합니다.")
                break
                
    except (KeyboardInterrupt, EOFError): # 5, 6, 7. 강제 종료 처리
        print("\n\n[경고] 사용자에 의해 프로그램이 강제 중단되었습니다.")
        print("[안내] 데이터를 안전하게 저장하고 종료합니다... (저장 로직 미구현)")
    finally:
        print("이용해 주셔서 감사합니다.")

if __name__ == "__main__":
    main()