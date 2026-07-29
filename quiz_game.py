import json
import os
import random

class QuizGame:
    def __init__(self):
        self.file_path = "state.json"
        self.data = self.load_state()

    def load_state(self):
        if not os.path.exists(self.file_path):
            print("[오류] 데이터 파일이 없습니다. generate_data.py를 먼저 실행하세요.")
            return {"quizzes": [], "high_score": 0, "history": []}
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"quizzes": [], "high_score": 0, "history": []}

    def save_state(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print("\n[저장 완료]")

    def read_int(self, prompt, min_val, max_val):
        while True:
            try:
                val = input(prompt).strip()
                num = int(val)
                if min_val <= num <= max_val: return num
                print(f"{min_val}~{max_val} 사이 입력!")
            except ValueError: print("숫자만 입력!")

    def show_menu(self):
        print(f"\n=== 증기기관 퀴즈 (총 {len(self.data['quizzes'])}문제 로드됨) ===")
        print("1. 퀴즈 풀기 (10문제 랜덤) | 2. 추가 | 3. 목록 | 4. 최고점수 | 5. 삭제 | 6. 히스토리 | 0. 종료")

    def play_quiz(self):
        if len(self.data["quizzes"]) < 10:
            print("최소 10문제 이상의 퀴즈가 필요합니다.")
            return
        
        # 300개 중 10개를 랜덤하게 뽑음
        current_quizzes = random.sample(self.data["quizzes"], 10)
        score = 0
        
        print("\n--- 랜덤 10문제 시작 ---")
        for i, q_item in enumerate(current_quizzes, 1):
            ans = input(f"[{i}/10] {q_item['q']} -> ").strip()
            if ans == q_item['a']:
                print("정답!"); score += 1
            else:
                print(f"오답! 정답은: {q_item['a']}")
        
        print(f"\n이번 판 점수: {score}/10")
        self.data["history"].append(f"10문제 중 {score}개 정답")
        if score > self.data["high_score"]:
            self.data["high_score"] = score
            print("⭐ 최고 기록 경신! ⭐")

    def list_quiz(self):
        print(f"\n--- 퀴즈 목록 (처음 10개만 표시) ---")
        for i, q in enumerate(self.data["quizzes"][:10], 1):
            print(f"{i}. {q['q']} (정답: {q['a']})")
        print(f"... 외 {len(self.data['quizzes'])-10}개 더 있음")

    def add_quiz(self):
        q = input("문제: ").strip(); a = input("정답: ").strip()
        if q and a: self.data["quizzes"].append({"q": q, "a": a})

    def delete_quiz(self):
        idx = self.read_int("삭제할 번호(1~): ", 1, len(self.data["quizzes"])) - 1
        del self.data["quizzes"][idx]

    def show_score(self):
        print(f"\n최고 점수: {self.data['high_score']}/10")

    def show_history(self):
        for h in self.data["history"][-5:]: print(h)

def main():
    game = QuizGame()
    while True:
        game.show_menu()
        choice = game.read_int("선택: ", 0, 6)
        if choice == 1: game.play_quiz()
        elif choice == 2: game.add_quiz()
        elif choice == 3: game.list_quiz()
        elif choice == 4: game.show_score()
        elif choice == 5: game.delete_quiz()
        elif choice == 6: game.show_history()
        elif choice == 0: game.save_state(); break

if __name__ == "__main__":
    main()