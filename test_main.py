import unittest
from unittest.mock import patch, mock_open
import json
import os
import io

# Import the classes to test
from main import Profile, ProfileManager, QuizGenerator

class TestProfile(unittest.TestCase):

    def test_profile_init(self):
        profile = Profile("test_user")
        self.assertEqual(profile.nickname, "test_user")
        self.assertEqual(profile.score, 0)
        self.assertEqual(profile.quiz_attempts, 0)
        self.assertFalse(profile.active)

    def test_update_score(self):
        profile = Profile("test_user")
        profile.update_score(10)
        self.assertEqual(profile.score, 10)
        self.assertEqual(profile.quiz_attempts, 1)

class TestProfileManager(unittest.TestCase):

    def setUp(self):
        self.profile_manager = ProfileManager()
        self.test_file_name = "test_profiles.json"
        self.test_profiles = [{"nickname": "test_user", "score": 20, "quiz_attempts": 2}]

    def tearDown(self):
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def test_load_profiles(self):
        mock_file = io.StringIO(json.dumps(self.test_profiles))
        with patch("builtins.open", new_callable=mock_open, read_data=mock_file.read()):
            self.profile_manager.load_profiles(self.test_file_name)
        self.assertEqual(len(self.profile_manager.profiles), 1)
        self.assertEqual(self.profile_manager.profiles[0].nickname, "test_user")

    def test_add_profile(self):
        self.profile_manager.add_profile("test_user")
        self.assertEqual(len(self.profile_manager.profiles), 1)
        self.assertEqual(self.profile_manager.profiles[0].nickname, "test_user")
        self.assertTrue(self.profile_manager.add_profile("new_user"))
        self.assertEqual(len(self.profile_manager.profiles), 2)
        self.assertFalse(self.profile_manager.add_profile("test_user"))

class TestQuizGenerator(unittest.TestCase):

    def setUp(self):
        self.quiz_generator = QuizGenerator()

    def test_handle_profile(self):
        with patch("builtins.input", side_effect=["test_user"]):
            self.quiz_generator.handle_profile()
        self.assertEqual(self.quiz_generator.active_profile.nickname, "test_user")

    def test_create_quiz(self):
        with patch("builtins.input", side_effect=["Test Quiz", "1", "Question 1", "Option 1", "Option 2", "Option 3", "Option 4", "Option 1"]):
            self.quiz_generator.active_profile = Profile("test_user")
            self.quiz_generator.create_quiz()
        self.assertTrue("Test Quiz" in self.quiz_generator.categories)

if __name__ == "__main__":
    unittest.main()
