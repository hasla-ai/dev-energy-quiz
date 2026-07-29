import json
import os
import random

SCORE_FILE = "score.json"

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

# 기본 데이터
DEFAULT_QUIZ_DATA = [
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
]

class QuizGame:
    def __init__(self):
        self.quiz_file = "quizzes.json"
        self.score_file = "score.json"
        self.quizzes = self.load_quizzes()

    # 데이터 관리
    def load_quizzes(self):
        if not os.path.exists(self.quiz_file):
            print("\n[안내] 데이터 파일이 없어 기본 데이터를 로드합니다.")
            return DEFAULT_QUIZ_DATA.copy()
        try:
            with open(self.quiz_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [Quiz(d['question'], d['choices'], d['answer']) for d in data]
        except (json.JSONDecodeError, IOError, KeyError):
            print("\n[오류] 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
            return DEFAULT_QUIZ_DATA.copy()

    def save_quizzes(self):
        with open(self.quiz_file, 'w', encoding='utf-8') as f:
            json.dump([q.to_dict() for q in self.quizzes], f, ensure_ascii=False, indent=4)

    def load_high_score(self):
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
            except (json.JSONDecodeError, IOError):
                return 0
        return 0

    def save_high_score(self, score):
        with open(self.score_file, 'w', encoding='utf-8') as f:
            json.dump({"high_score": score}, f, ensure_ascii=False, indent=4)

    # 유틸
    def get_safe_input(self, prompt, min_val=1, max_val=7):
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
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("[오류] 내용을 입력해주세요.")

    # 게임 기능
    def play_quiz(self):
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return
        print(f"\n>>> 총 {len(self.quizzes)}문제를 시작합니다!")
        score = 0
        pool = list(self.quizzes)
        random.shuffle(pool)
        for i, quiz in enumerate(pool, 1):
            quiz.display_quiz(i)
            user_choice = self.get_safe_input("정답 번호 입력: ", 1, 4)
            if quiz.check_answer(user_choice):
                print("=> 정답입니다! ✨")
                score += 1
            else:
                print(f"=> 오답입니다. (정답: {quiz.answer})")
        print("\n" + "="*30)
        print(f"학습 종료! 최종 점수: {score} / {len(self.quizzes)}")
        print(f"정답률: {(score/len(self.quizzes))*100:.1f}%")
        print("="*30)
        # 최고점 저장
        high = self.load_high_score()
        if score > high:
            print("새로운 최고 기록입니다! 저장합니다.")
            self.save_high_score(score)

    def add_quiz(self):
        print("\n--- 새로운 퀴즈 추가 ---")
        question = self.get_non_empty_string("문제 내용을 입력하세요: ")
        choices = []
        for i in range(1,5):
            choices.append(self.get_non_empty_string(f"선택지 {i}번을 입력하세요: "))
        answer = self.get_safe_input("정답 번호를 입력하세요 (1~4): ", 1, 4)
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_quizzes()
        print("\n[성공] 새로운 퀴즈가 추가되었습니다!")

    def delete_quiz(self):
        if not self.quizzes:
            print("\n[알림] 삭제할 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return
        self.list_quizzes()
        delete_index = self.get_safe_input("삭제할 퀴즈 번호 입력: ", 1, len(self.quizzes))
        confirm = input(f"정말로 '{self.quizzes[delete_index-1].question}' 문제를 삭제하시겠습니까? (y/n): ").strip().lower()
        if confirm == 'y':
            removed = self.quizzes.pop(delete_index-1)
            self.save_quizzes()
            print(f"\n[성공] '{removed.question}' 문제가 삭제되었습니다.")
        else:
            print("\n[취소] 퀴즈 삭제가 취소되었습니다.")

    def list_quizzes(self):
        print("\n--- 등록된 퀴즈 목록 ---")
        if not self.quizzes:
            print("[알림] 현재 등록된 퀴즈가 없습니다. 새로운 퀴즈를 추가해보세요!")
            return
        for i, quiz in enumerate(self.quizzes,1):
            print(f"{i}. {quiz.question} (정답: {quiz.answer}번)")
        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 등록되어 있습니다.")

    def show_high_score(self):
        high_score = self.load_high_score()
        print("\n" + "="*30)
        if high_score == 0:
            print("아직 기록이 없습니다. 첫 퀴즈를 풀어보세요!")
        else:
            print(f"현재 최고 기록: {high_score}점 🏆")
        print("="*30)

    def display_menu(self):
        print("\n" + "="*30)
        print("   증기기관 퀴즈 프로그램")
        print("="*30)
        print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 목록 보기")
        print("4. 점수 확인  5. 퀴즈 삭제  6. 히스토리")
        print("7. 종료")
        print("="*30)

    def run(self):
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
                    self.show_high_score()
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


if __name__ == "__main__":
    game = QuizGame()
    game.run()
