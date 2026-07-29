import json
import os
import random
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

# [기본 데이터] 파일이 없거나 손상되었을 때 사용할 데이터 -> 인스턴스화
DDEFAULT_QUIZ_DATA = [
    Quiz("증기기관에 대한 설명으로 가장 옳지 않은 것은?", ["열에너지를 기계적 에너지로 변환하는 장치이다.", "물이 끓을 때 발생하는 수증기의 팽창 압력을 이용한다.", "산업 혁명의 원동력이 되었다.", "화석 연료를 전혀 사용하지 않는 친환경 기관이다."], 4),
    Quiz("증기기관의 작동 원리와 가장 깊은 관련이 있는 물리적 법칙은?", ["질량 보존의 법칙", "열역학 제2법칙", "관성의 법칙", "옴의 법칙"], 2),
    Quiz("현대적 의미의 실용적인 증기기관을 최초로 발명한 사람은?", ["토머스 뉴커먼", "제임스 와트", "토머스 세이버리", "리처드 트레비식"], 2),
    Quiz("다음 중 증기기관의 발달 순서가 올바르게 나열된 것은?", ["뉴커먼 기관 -> 와트 기관 -> 세이버리 기관", "세이버리 기관 -> 뉴커먼 기관 -> 와트 기관", "와트 기관 -> 세이버리 기관 -> 뉴커먼 기관", "뉴커먼 기관 -> 세이버리 기관 -> 와트 기관"], 2),
    Quiz("토머스 뉴커먼이 발명한 증기기관의 주된 용도는?", ["증기선 운항", "증기 기관차 운전", "광산의 지하수 배출", "방직기 구동"], 3),
    Quiz("제임스 와트가 기존 뉴커먼 기관의 단점을 보완하여 발명한 핵심 장치는 무엇인가?", ["증기 압력 조절 밸브", "자동 급수 장치", "피스톤 운동 변환 장치", "분리형 응축기"], 4),
    Quiz("증기기관의 발명으로 인해 가장 크게 변화한 산업 분야는?", ["정보 통신 산업", "항공 우주 산업", "농업 및 수공업", "운송 및 제조업"], 4),
    Quiz("와트의 증기기관은 직선 운동을 회전 운동으로 바꾸는 장치를 도입하여 어떤 산업에 직접적인 기여를 했는가?", ["자동차 산업", "원자력 발전", "면방직 공업 및 공장 자동화", "항공기 제작"], 3),
    Quiz("증기기관을 이용해 세계 최초로 상업적인 증기선을 운항한 사람은 누구인가?", ["로버트 풀턴", "조지 스티븐슨", "올리버 에반스", "윌리엄 머독"], 1),
    Quiz("증기기관의 동력을 이용하여 석탄과 철도를 운반하는 증기 기관차를 최초로 실용화한 인물은?", ["제임스 와트", "조지 스티븐슨", "마이클 패러데이", "니콜라 테슬라"], 2)
]
## JSON 파일은 텍스트(딕셔너리 형태)만 저장할 수 있으므로, Quiz 객체를 바로 저장할 수 없고, 딕셔너리로 변환 후 저장해야 합니다.
def load_data(filename="quizzes.json"):
    """파일에서 데이터를 로드하며, 예외 발생 시 Quiz 객체 리스트를 반환합니다."""
    if not os.path.exists(filename):
        print("\n[안내] 데이터 파일이 없어 기본 데이터를 로드합니다.")
        return DEFAULT_QUIZ_DATA
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
          # return json.load(f)
          # 딕셔너리 리스트를 Quiz 객체 리스트로 변환
          data = json.load(f)
        return [Quiz(d['question'], d['choices'], d['answer']) for d in data_list]
    #except (json.JSONDecodeError, IOError):
    except (json.JSONDecodeError, IOError, KeyError):
        print("\n[오류] 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
        return DEFAULT_QUIZ_DATA

# 퀴즈 추가 기능이 구현될 때 호출할 함수입니다. q.to_dict()를 사용하여 객체를 저장 가능한 형태로 변환합니다.
def save_data(quizzes, filename="quizzes.json"):
    """Quiz 객체 리스트를 JSON 파일로 저장합니다."""
    with open(filename, 'w', encoding='utf-8') as f:
        # 객체를 딕셔너리로 변환하여 저장
        json.dump([q.to_dict() for q in quizzes], f, ensure_ascii=False, indent=4)

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

# 퀴즈 풀기 기능, main 함수에서 이를 호출하도록 수정.
def play_quiz(quizzes):
    """퀴즈 풀기 기능을 수행합니다."""
    # 인스턴스화로 방지한 기능: 리스트가 비어있을 경우 안내 메시지를 출력하고 종료. 
    if not quizzes:
        print("\n[알림] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
        return

    print(f"\n>>> 총 {len(quizzes)}문제를 시작합니다!")
    score = 0
    
# 보너스 기능: 문제를 무작위로 섞어서 매번 다른 순서로 문제를 풀 수 있도록 출제.
    quiz_pool = list(quizzes)
    random.shuffle(quiz_pool)

    for i, quiz in enumerate(quiz_pool, 1):
        quiz.display_quiz(i)
        # 1~4번 선택지 입력 받기
        ## 이전에 만든 get_safe_input 함수를 재사용하여 1~4 이외의 값이나 문자 입력 시 자동으로 재입력을 유도
        user_choice = get_safe_input("정답 번호 입력: ", 1, 4)
        
        if quiz.check_answer(user_choice):
            print("=> 정답입니다! ✨")
            score += 1
        else:
            print(f"=> 오답입니다. (정답: {quiz.answer})")

    # 최종 결과 표시
    print("\n" + "="*30)
    print(f"학습 종료! 최종 점수: {score} / {len(quizzes)}")
    print(f"정답률: {(score/len(quizzes))*100:.1f}%")
    print("="*30)

# 퀴즈 추가 기능 구현
def get_non_empty_string(prompt):
    """공백이 아닌 문자열을 입력받을 때까지 반복합니다."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("[오류] 내용을 입력해주세요.")

def add_quiz(quizzes):
    """새로운 퀴즈를 입력받아 리스트에 추가하고 파일에 저장합니다."""
    print("\n--- 새로운 퀴즈 추가 ---")
    
    # 1. 문제 입력
    question = get_non_empty_string("문제 내용을 입력하세요: ")
    
    # 2. 선택지 4개 입력
    choices = []
    for i in range(1, 5):
        choice = get_non_empty_string(f"선택지 {i}번을 입력하세요: ")
        choices.append(choice)
    
    # 3. 정답 번호 입력 (기존 예외 처리 함수 활용)
    answer = get_safe_input("정답 번호를 입력하세요 (1~4): ", 1, 4)
    ## get_safe_input 재사용: 정답 번호를 입력받을 때 이미 만들어둔 범주형 정수 입력 함수를 사용하여 1~4 사이의 숫자만 받도록 강제합니다.
    
    # 4. Quiz 객체 생성 및 리스트 추가
    new_quiz = Quiz(question, choices, answer)
    quizzes.append(new_quiz)
    
    # 5. 파일에 저장
    ### 데이터 영속성(Persistence): 퀴즈를 리스트에 추가한 즉시 save_data(quizzes)를 호출하여 quizzes.json 파일에 쓰기 작업을 수행합니다. 이제 프로그램을 껐다 켜도 추가한 문제가 유지됩니다.

    try:
        save_data(quizzes)
        print("\n[성공] 퀴즈가 안전하게 저장되었습니다!")
    except Exception as e:
        print(f"\n[오류] 저장 중 문제가 발생했습니다: {e}")

# main 함수 내 메뉴 연결
# elif choice == 2:
#     add_quiz(quizzes)

def list_quizzes(quizzes):
    """저장된 모든 퀴즈의 목록을 번호와 함께 출력합니다."""
    print("\n--- 등록된 퀴즈 목록 ---")
    
    # 1. 퀴즈가 없는 경우 처리
    if not quizzes:
        print("[알림] 현재 등록된 퀴즈가 없습니다. 새로운 퀴즈를 추가해보세요!")
        return

    # 2. 퀴즈 목록 출력: 문제 내용과 정답 번호만 간략히. 리스트 인덱스를 1부터.
    for i, quiz in enumerate(quizzes, 1):
        print(f"{i}. {quiz.question} (정답: {quiz.answer}번)")
    
    print(f"\n총 {len(quizzes)}개의 퀴즈가 등록되어 있습니다.")

# main 함수 내 메뉴 연결
# elif choice == 3:
#     list_quizzes(quizzes)

def main():
    quizzes = load_data()
    
    try:
        while True:
            display_menu()
            choice = get_safe_input("선택: ", 1, 7)

            if choice == 1:
                play_quiz(quizzes) # 퀴즈 풀기 함수 호출
            elif choice == 2:
                print("\n[기능] 퀴즈 추가 (다음 단계에서 구현)")
            # ... (나머지 elif 생략) ...
            elif choice == 7:
                print("\n프로그램을 안전하게 종료합니다.")
                break
                
    except (KeyboardInterrupt, EOFError):
        print("\n\n[경고] 사용자에 의해 프로그램이 중단되었습니다.")
    finally:
        print("이용해 주셔서 감사합니다.")

if __name__ == "__main__":
    main()

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