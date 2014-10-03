import unittest
from user import User

__author__ = 'Phillip Lemons'

#TODO test circular relationships?


class TestUser(unittest.TestCase):

    def test_user_add_single_coach(self):
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_coach(u2)
        self.assertEqual(len(u1.coaches), 1)
        self.assertTrue(u2 in u1.coaches)

        self.assertEqual(len(u2.students), 1)
        self.assertTrue(u1 in u2.students)

    def test_user_add_multiple_coaches(self):
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u3", 1)
        u1.add_coach(u2)
        u1.add_coach(u3)

        self.assertEqual(len(u1.coaches), 2)
        self.assertTrue(u2 in u1.coaches)
        self.assertTrue(u3 in u1.coaches)

        self.assertEqual(len(u2.students), 1)
        self.assertTrue(u1 in u2.students)

        self.assertEqual(len(u3.students), 1)
        self.assertTrue(u1 in u3.students)

    def test_user_add_duplicate_coaches(self):
        #TODO make this test for duplicate coach error
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_coach(u2)
        u1.add_coach(u2)
        u1.add_coach(u2)
        u1.add_coach(u2)

        self.assertEqual(len(u1.coaches), 1)
        self.assertTrue(u2 in u1.coaches)

        self.assertEqual(len(u2.students), 1)
        self.assertTrue(u1 in u2.students)

    def test_user_add_single_student(self):
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_student(u2)

        self.assertEqual(len(u1.students), 1)
        self.assertTrue(u2 in u1.students)

        self.assertEqual(len(u2.coaches), 1)
        self.assertTrue(u1 in u2.coaches)

    def test_user_add_multiple_students(self):
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u3", 1)
        u1.add_student(u2)
        u1.add_student(u3)

        self.assertEqual(len(u1.students), 2)
        self.assertTrue(u2 in u1.students)
        self.assertTrue(u3 in u1.students)

        self.assertEqual(len(u2.coaches), 1)
        self.assertTrue(u1 in u2.coaches)

        self.assertEqual(len(u3.coaches), 1)
        self.assertTrue(u1 in u3.coaches)

    def test_user_add_duplicate_students(self):
        #TODO make this test for duplicate student error
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_student(u2)
        u1.add_student(u2)
        u1.add_student(u2)
        u1.add_student(u2)

        self.assertEqual(len(u1.students), 1)
        self.assertTrue(u2 in u1.students)

        self.assertEqual(len(u2.coaches), 1)
        self.assertTrue(u1 in u2.coaches)