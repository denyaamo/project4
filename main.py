import sys
import random
import json

class Profile:
    def __init__(self, nickname):
        self.nickname = nickname
        self.score = 0
        self.active = False

    def update_score(self, score):
        self.score += score

    def to_dict(self):
        return {"nickname": self.nickname, "score": self.score}

    @staticmethod
    def from_dict(data):
        profile = Profile(data["nickname"])
        profile.score = data.get("score", 0)
        return profile

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
            print(f"{idx}. {profile.nickname}: {profile.score} points")

class FootballQuizGenerator:
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
        print("Welcome to the Football Quiz Generator!")
        self.handle_profile()

    def handle_profile(self):
        nickname = input("Enter your nickname: ")
        profile = self.profile_manager.get_profile(nickname)
        if profile:
            print(f"Welcome back, {profile.nickname}!")
            self.active_profile = profile
        else:
            if self.profile_manager.add_profile(nickname):
                print(f"Profile {nickname} created successfully!")
                self.active_profile = self.profile_manager.get_profile(nickname)
            else:
                print("Profile already exists. Logging in...")
                self.active_profile = self.profile_manager.get_profile(nickname)

        # Set the active profile as active
        self.active_profile.active = True

        # Save profiles only if a new profile is created or an existing profile is logged in
        if profile is None:
            self.profile_manager.save_profiles()



    def start_quiz_menu(self):
        if not self.active_profile:
            print("No active profile. Please create or log in to a profile first.")
            return

        print(f"Welcome, {self.active_profile.nickname}!")

        while True:
            self.display_categories()
            category = input("Choose a category: ")
            if category in self.categories:
                num_questions = 10  # Fixed to 10 questions per category
                quiz_questions = random.sample(self.categories[category], num_questions)
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
    quiz_generator = FootballQuizGenerator()
    quiz_generator.start()

    while True:
        print("\nMain Menu:")
        print("1. Start Quiz")
        print("2. Display Leaderboard")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            quiz_generator.start_quiz_menu()
        elif choice == "2":
            quiz_generator.profile_manager.display_leaderboard()
        elif choice == "3":
            print("Exiting program.")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()

