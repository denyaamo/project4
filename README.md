# Main idea and why.
1. At work we often play Kahoot, however sometimes we face issues with creating quizes, since platform limits its usage for corporates, and it costs.
2. Considering that I'm studying web development, here I starting my journey to creating simple version of Kahoot for myself and my colleagues.
3. However, since web development itself has not been started yet, i would create micro-version of quiz/kahoot using python.

# Functionallity and how app will work
1. Program will have profiles, hardcoded quizes, possibility to create own quiz and leader board.
2. Program will prompt user to insert a nickname that would be considered as profile(if such profile has been created before the program wont create same profile, you will be acting on behalf of profile that has been created before(hopefully by you). No passwords or any other security will be created due to low-skill of developer.
3. First option would be something like '1. Hardcoded quiz', that would have couple of quizez(called category), each of category will have 10 questions. After completing 10 questions the app will give you an output of your score out of 10 questions, and the program will update your score in profile file, that has been created when you created a profile(initial score set to 0). These point will be used to create a leaderboard.
4. Second option would be something like '1. Create you own quiz', that would prompt user to name a quiz(category name), then it would prompt user for question, options and correct answer. Minimum amount of questions would be 5. (Main thing is that the user cant play the quiz created by himself, since knowing all answers would affect a score and leader board. Say no to cheaters.)
5. Third option would be the leader board that will calculate how much questions user answered, how much correct answers and it will calculate the place of a user based on ratio correct answers/total answered.
6. Fourth option would be exiting the program.
