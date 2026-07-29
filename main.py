import json
import os
import random
from typing import Any

# ==========================================
# 1. 데이터 모델 클래스 (기존 동일)
# ==========================================
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display_quiz(self, index):
        print(f"\n[문제 {index}] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_choice):
        return self.answer == user_choice

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

# ==========================================
# 2. 퀴즈 게임 전체를 관리하는 메인 클래스
# ==========================================
class QuizGame:
    def __init__(self):
    # 상수 및 설정값
        # 1. 파일 경로를 하나로 통합
        self.state_file = "state.json"
            
        # 2. 데이터를 한 번에 로드
        state_data = self.load_state()    
                
        # 3. 로드된 데이터를 속성에 할당
        self.quizzes = state_data["quizzes"]
        self.best_score = state_data["best_score"]
    
# ------------------------------------------
# 데이터 입출력 관련 메서드
# ------------------------------------------

    def load_state(self):
        """파일에서 퀴즈와 점수를 한 번에 불러옵니다."""
 
        # 파일이 없을 때 사용할 기본 데이터 (최소 스키마 준수)
        DEFAULT_QUIZ_DATA = {
            "quizzes":      [
            Quiz(
                "증기기관에 대한 설명으로 가장 옳지 않은 것은?",
                [
                    "열에너지를 기계적 에너지로 변환하는 장치이다.",
                    "물이 끓을 때 발생하는 수증기의 팽창 압력을 이용한다.",
                    "산업 혁명의 원동력이 되었다.",
                    "화석 연료를 전혀 사용하지 않는 친환경 기관이다.",
                ],
                4,
            ),
            Quiz(
                "증기기관의 작동 원리와 가장 깊은 관련이 있는 물리적 법칙은?",
                ["질량 보존의 법칙", "열역학 제2법칙", "관성의 법칙", "옴의 법칙"],
                2,
            ),    
            Quiz(
                "현대적 의미의 실용적인 증기기관을 최초로 발명한 사람은?",
                ["토머스 뉴커먼", "제임스 와트", "토머스 세이버리", "리처드 트레비식"],
                2,
            ),       
            Quiz(
                "증기기관의 효율을 높이기 위해 제임스 와트가 고안한 장치는?",
                ["증기 터빈", "증기 팽창기", "증기 응축기", "증기 압력계"],
                3,
            ),
            Quiz(
                "증기기관이 산업 혁명에 미친 영향으로 가장 적절한 것은?",
                [
                    "농업 생산량 감소",
                    "수공업 중심의 경제 체제 강화",
                    "대량 생산과 공장제 기계 공업 발전",
                    "교통 수단의 전면적 퇴보",
                ],
                3,
            ),  
        ],
        "best_score": 0
        }
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # List Comprehension & Dictionary Unpacking
                quizzes: list[Quiz[Any, Any, Any]] = [Quiz(**q) for q in data.get("quizzes", [])]             
                best_score = data.get('best_score', 0)
                return {
                    "quizzes": quizzes, "best_score": best_score
                }                    
            else:
                print("\n[안내] 데이터 파일이 없어 기본 데이터를 로드합니다.")
                return DEFAULT_QUIZ_DATA 
        except (json.JSONDecodeError, IOError):
            print(f"\n[경고] {self.state_file} 읽기 오류! 기본 데이터를 사용합니다.")
            return DEFAULT_QUIZ_DATA 

    def save_state(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장합니다."""
        try:
            # Quiz 객체 리스트를 다시 저장 가능한 딕셔너리 형태로 변환
            quiz_data = [q.to_dict() for q in self.quizzes]

            # 저장할 데이터 구조 (스키마 유지)
            data_to_save = {
                "quizzes": quiz_data,
                "best_score": self.best_score
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
                # indent=4로 보기 좋게 저장, ensure_ascii=False로 한글 깨짐 방지
        except IOError as e:
            print(f"퀴즈 저장 중 오류 발생: {e}")

# ------------------------------------------
# 유틸리티 입력 메서드
# ------------------------------------------

    def get_safe_input(self, prompt, min_val=1, max_val=7):
        """사용자 입력을 안전하게 처리합니다."""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print(">> 입력이 비어 있습니다. 번호를 입력해주세요.")
                    continue
                choice = int(user_input)
                if min_val <= choice <= max_val:
                    return choice
                else:
                    print(f">> {min_val}~{max_val} 사이의 숫자를 입력해주세요.")
            except ValueError:
                print(">> 잘못된 입력입니다. '숫자'만 입력 가능합니다.")

    def get_non_empty_string(self, prompt):
        """비어 있지 않은 문자열을 입력받습니다."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("[오류] 내용을 입력해주세요.")

# ------------------------------------------
# 메뉴별 주요 실행 기능 (기존 함수들 -> 클래스 메서드 변환)
# ------------------------------------------
    def play_quiz(self):
        """1. 퀴즈 풀기"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return
        print(f"\n>>> 총 {len(self.quizzes)}문제를 시작합니다!")
        score = 0
        pool = list(self.quizzes)
        random.shuffle(pool)
        for i, quiz in enumerate(pool, 1):
            # 1. 문제 출력 (Quiz 클래스의 메서드 사용!)
            quiz.display_quiz(i)
            user_choice = self.get_safe_input("정답 번호 입력: ", 1, 4)

            # 2. 정답 확인 (Quiz 클래스의 메서드 사용!)
            if quiz.check_answer(user_choice):
                print("=> 정답입니다! ✨")
                score += 1
            else:
                print(f"=> 오답입니다. (정답: {quiz.answer})")

        print("\n" + "="*30)
        print(f"학습 종료! 맞힌 개수: {score} / {len(self.quizzes)}")

        # 1. 현재 게임의 백분율 점수 계산 (0으로 나누기 방지 포함)
        score = (score / len(self.quizzes)) * 100 if self.quizzes else 0
                
        #변수 없이 직접 계산하여 출력(소수점 1자리까지 표시)
        if self.quizzes:
            print(f"최종점수: {score}점")
        print("="*30)
        # 최고점 저장
        if score > self.best_score:
            print("새로운 최고 기록입니다! 저장합니다.")
            self.best_score = score
            # 데이터가 변할 때마다 저장!
            self.save_state() 

    def add_quiz(self):
        """2. 퀴즈 추가"""
        print("\n--- 새로운 퀴즈 추가 ---")
        question = self.get_non_empty_string("문제 내용을 입력하세요: ")
        choices = []
        for i in range(1,5):
            choices.append(self.get_non_empty_string(f"선택지 {i}번을 입력하세요: "))
        answer = self.get_safe_input("정답 번호를 입력하세요 (1~4): ", 1, 4)
        # 새로운 Quiz 객체 추가    
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        # 데이터가 변할 때마다 저장!
        self.save_state()
        print("\n[성공] 새로운 퀴즈가 추가되었습니다!")


    def delete_quiz(self):
        if not self.quizzes:
            print("\n[알림] 삭제할 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return
        self.list_quizzes()
        # 안전하게 번호 입력 받기
        delete_index = self.get_safe_input("삭제할 퀴즈 번호 입력: ", 1, len(self.quizzes))
        # 삭제 대상 확인
        target_quiz = self.quizzes[delete_index - 1]
        confirm = input(f"정말로 '{target_quiz.question}' 문제를 삭제하시겠습니까? (y/n): ").strip().lower()

        if confirm == 'y':
            # 1. 메모리에서 삭제
            removed = self.quizzes.pop(delete_index-1)
            # 2. 변경된 상태를 파일에 저장 (실제 데이터가 변했을 때만!)
            self.save_state()
            print(f"\n[성공] '{removed.question}' 문제가 삭제되었습니다.")
        else:
            print("\n[취소] 퀴즈 삭제가 취소되었습니다.")

    def list_quizzes(self):
        """3. 목록 보기"""
        print("\n--- 등록된 퀴즈 목록 ---")
        if not self.quizzes:
            print("[알림] 현재 등록된 퀴즈가 없습니다. 새로운 퀴즈를 추가해보세요!")
            return
        for i, quiz in enumerate(self.quizzes,1):
            print(f"{i}. {quiz.question} (정답: {quiz.answer}번)")
        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 등록되어 있습니다.")

    def show_best_score(self):
        """4. 점수 확인"""
        print("\n" + "="*30)
        if self.best_score == 0:
            print("아직 기록이 없습니다. 첫 퀴즈를 풀어보세요!")
        else:
            print(f"현재 최고 기록: {self.best_score}점 🏆")
        print("="*30)

    def display_menu(self):
        """메뉴 출력"""
        print("\n" + "="*30)
        print("   증기기관 퀴즈 프로그램")
        print("="*30)
        print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 목록 보기")
        print("4. 점수 확인  5. 퀴즈 삭제  6. 히스토리")
        print("7. 종료")
        print("="*30)

    def run(self):
        """프로그램 실행 메인 루프"""
        try:
            while True:
                self.display_menu()
                choice = self.get_safe_input("선택: ", 1, 7)
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    self.delete_quiz()
                elif choice == 6:
                    print("\n[기능] 히스토리 확인 (다음 단계에서 구현)")
                elif choice == 7:
                    print("\n프로그램을 안전하게 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n[경고] 사용자에 의해 프로그램이 중단되었습니다.")
        finally:
            print("이용해 주셔서 감사합니다.")

# ==========================================
# 3. 메인 실행부 (단 2줄로 단순화)
# ==========================================
if __name__ == "__main__":
    game = QuizGame()
    game.run()
