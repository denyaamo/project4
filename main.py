import sys
import random
import json

class Profile:
    def __init__(self, nickname):
        self.nickname = nickname
        self.score = 0
        self.quiz_attempts = 0
        self.active = False

    def update_score(self, score):
        self.score += score
        self.quiz_attempts += 1

    def to_dict(self):
        return {"nickname": self.nickname, "score": self.score, "quiz_attempts": self.quiz_attempts}

    @staticmethod
    def from_dict(data):
        profile = Profile(data["nickname"])
        profile.score = data.get("score", 0)
        profile.quiz_attempts = data.get("quiz_attempts", 0)
        return profile
    
    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        if not value.strip():
            raise ValueError("Nickname cannot be blank.")
        self._nickname = value


class ProfileManager:
    def __init__(self):
        self.profiles = []

    def load_profiles(self, file_name="profiles.json"):
        try:
            with open(file_name, 'r') as file:
                profiles_data = json.load(file)
                self.profiles = [Profile.from_dict(profile) for profile in profiles_data]
        except FileNotFoundError:
            pass

    def save_profiles(self, file_name="profiles.json"):
        with open(file_name, 'w') as file:
            json.dump([profile.to_dict() for profile in self.profiles], file, indent=4)

    def add_profile(self, nickname):
        if not self.get_profile(nickname):
            self.profiles.append(Profile(nickname))
            self.save_profiles()
            return True
        else:
            return False

    def get_profile(self, nickname):
        for profile in self.profiles:
            if profile.nickname == nickname:
                return profile
        return None

    def update_profile_score(self, nickname, score):
        profile = self.get_profile(nickname)
        if profile:
            profile.update_score(score)
            self.save_profiles()

    def display_leaderboard(self):
        sorted_profiles = sorted(self.profiles, key=lambda x: x.score, reverse=True)
        print("Leaderboard:")
        for idx, profile in enumerate(sorted_profiles, start=1):
            print(f"{idx}. {profile.nickname}: {profile.score} points out of {profile.quiz_attempts} quiz attempts, ratio: {profile.score/10:.2f}")



class QuizGenerator:
    def __init__(self):
        self.categories = {}
        self.profile_manager = ProfileManager()
        self.active_profile = None

    def load_data(self):
        try:
            with open("categories.json", 'r') as file:
                self.categories = json.load(file)
        except FileNotFoundError:
            print("Questions file not found.")

    def start(self):
        self.profile_manager.load_profiles()
        self.load_data()
        print("Welcome to the Quiz Generator!")
        self.handle_profile()

    def handle_profile(self):
        while True:

            nickname = input("Enter your nickname: ")
            if not nickname:
                print ("Nickname cannot be blank.")
                continue
            profile = self.profile_manager.get_profile(nickname)
            if profile:
                print(f"Welcome back, {profile.nickname}!")
                self.active_profile = profile
            else:
                if self.profile_manager.add_profile(nickname):
                    print(f"Profile {nickname} created successfully!")
                    self.active_profile = self.profile_manager.get_profile(nickname)
            self.active_profile.active = True

            if profile is None:
                self.profile_manager.save_profiles()
            break
    def create_quiz(self):
        quiz_name = input("Enter a name for your quiz: ")
        if not quiz_name:
            print ("Quiz name cannot be blank")
            return
        self.categories[quiz_name] = {
            "creator": self.active_profile.nickname,
            "questions": []
        }

        num_questions = input("How many questions would you like to add? ")
        while not num_questions.isdigit() or int(num_questions) < 1:
            print("Invalid input. Please enter a positive integer.")
            num_questions = input("How many questions would you like to add? ")

        num_questions = int(num_questions)

        for i in range(num_questions):
            question = input(f"Enter question {i+1}: ")
            options = [input(f"Enter option {j+1}: ") for j in range(4)]  # 4 options per question
            correct_answer = input("Enter the correct answer: ")
            self.categories[quiz_name]["questions"].append({
                "question": question,
                "options": options,
                "answer": correct_answer
            })

        with open("categories.json", 'w') as file:
            json.dump(self.categories, file, indent=4)

        print(f"Quiz '{quiz_name}' created successfully!")

    def delete_quiz(self):
        print("Your Quizzes:")
        for quiz_name, quiz_data in self.categories.items():
            if isinstance(quiz_data, dict) and quiz_data["creator"] == self.active_profile.nickname:
                print(f"- {quiz_name}")

        quiz_name = input("Enter the name of the quiz you want to delete: ")
        if not quiz_name:
            print("Quiz name cannot be blank.")
            return

        if quiz_name not in self.categories:
            print("Quiz not found.")
            return

        if self.categories[quiz_name]["creator"] != self.active_profile.nickname:
            print("You can only delete quizzes that you created.")
            return

        del self.categories[quiz_name]

        with open("categories.json", 'w') as file:
            json.dump(self.categories, file, indent=4)

        print(f"Quiz '{quiz_name}' deleted successfully!")


    def start_quiz_menu(self):
        
        print(f"Welcome, {self.active_profile.nickname}!")

        while True:
            self.display_categories()
            category = input("Choose a category: ")
            if not category:
                print ("Category cannot be blank.")
                continue
            if category in self.categories:
                category_data = self.categories[category]
                if isinstance(category_data, dict):  # If the category data is a dictionary (for quizzes created inside the app)
                    if category_data["creator"] == self.active_profile.nickname:
                        print("You cannot start a quiz that you created. Please choose another category.")
                        continue
                    questions = category_data["questions"]
                else:  # If the category data is a list (for hardcoded quizzes)
                    questions = category_data
                num_questions = min(10, len(questions))  # Fixed to 10 questions per category or less if there are not enough questions
                quiz_questions = random.sample(questions, num_questions)
                score = self.present_quiz(quiz_questions)
                self.active_profile.update_score(score)
                self.profile_manager.save_profiles()  # Update profiles.json
                print(f"Your score: {score} out of {num_questions}")
                break  # Exit the loop if a valid category is chosen
            else:
                print("Invalid category. Please choose a valid category.")
                    

    def present_quiz(self, quiz_questions):
        score = 0
        for idx, question in enumerate(quiz_questions, start=1):
            print(f"Question {idx}: {question['question']}")
            for i, option in enumerate(question['options'], start=1):
                print(f"{i}. {option}")
            user_answer = input("Enter your choice: ").strip()
            if user_answer.lower() == question['answer'].lower():
                print("Correct!")
                score += 1
            else:
                print("Incorrect!")
        return score

    def display_categories(self):
        print("Available Categories:")
        for category in self.categories.keys():
            print(f"- {category}")

def main():
    quiz_generator = QuizGenerator()
    quiz_generator.start()

    while True:
        print("\nMain Menu:")
        print("1. Start Quiz")
        print("2. Create Your Own Quiz")
        print("3. Delete Your Quiz")
        print("4. Display Leaderboard")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            quiz_generator.start_quiz_menu()
        elif choice == "2":
            quiz_generator.create_quiz()
        elif choice == "3":
            quiz_generator.delete_quiz()
        elif choice == "4":
            quiz_generator.profile_manager.display_leaderboard()
        elif choice == "5":
            print("Exiting program.")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Program.")