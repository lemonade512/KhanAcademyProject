import sys
import os
sys.path.append(os.path.abspath(__file__)+"/..")

import unittest
from user import User, DuplicateCoachError, DuplicateStudentError, MissingStudentError, MissingCoachError

__author__ = 'Phillip Lemons'


class TestUser(unittest.TestCase):

    def test_user_add_single_coach(self):
        """
        Tests adding a single coach to a user's coaches
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_coach(u2)
        self.assertEqual(len(u1.coaches), 1)
        self.assertTrue(u2 in u1.coaches)

        self.assertEqual(len(u2.students), 1)
        self.assertTrue(u1 in u2.students)

    def test_user_add_multiple_coaches(self):
        """
        Tests adding multiple coaches to a user's coaches
        """
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
        """
        Tests that an error is raised when duplicate coaches are added
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_coach(u2)
        self.assertRaises(DuplicateCoachError, u1.add_coach, u2)

        self.assertEqual(len(u1.coaches), 1)
        self.assertTrue(u2 in u1.coaches)

        self.assertEqual(len(u2.students), 1)
        self.assertTrue(u1 in u2.students)

    def test_user_add_single_student(self):
        """
        Tests adding a single student to a user's students.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_student(u2)

        self.assertEqual(len(u1.students), 1)
        self.assertTrue(u2 in u1.students)

        self.assertEqual(len(u2.coaches), 1)
        self.assertTrue(u1 in u2.coaches)

    def test_user_add_multiple_students(self):
        """
        Tests adding multiple students to a user's students
        """
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
        """
        Tests that an error is raised when duplicate students are added
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_student(u2)
        self.assertRaises(DuplicateStudentError, u1.add_student, u2)

        self.assertEqual(len(u1.students), 1)
        self.assertTrue(u2 in u1.students)

        self.assertEqual(len(u2.coaches), 1)
        self.assertTrue(u1 in u2.coaches)

    def test_user_remove_single_student(self):
        """
        Tests removing a student from a user's students
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_student(u2)
        u1.remove_student(u2)

        self.assertEqual(len(u1.students), 0)
        self.assertFalse(u2 in u1.students)

        self.assertEqual(len(u2.coaches), 0)
        self.assertFalse(u1 in u2.coaches)

    def test_user_remove_multiple_students_same_name(self):
        """
        Tests removing students with the same name
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u2", 1)
        u1.add_student(u2)
        u1.add_student(u3)

        u1.remove_student(u2)
        self.assertEqual(len(u1.students), 1)
        self.assertTrue(u3 in u1.students)
        self.assertFalse(u2 in u1.students)
        self.assertTrue(u1 in u3.coaches)
        self.assertFalse(u1 in u2.coaches)

        u1.remove_student(u3)
        self.assertEqual(len(u1.students), 0)
        self.assertFalse(u3 in u1.students)
        self.assertFalse(u2 in u1.students)
        self.assertFalse(u1 in u3.coaches)
        self.assertFalse(u1 in u2.coaches)

    def test_user_double_remove_student(self):
        """
        Tests that an error is raised when double removing a student
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_student(u2)
        u1.remove_student(u2)
        self.assertRaises(MissingStudentError, u1.remove_student, u2)

        self.assertEqual(len(u1.students), 0)
        self.assertFalse(u2 in u1.students)
        self.assertFalse(u1 in u2.coaches)

    def test_user_remove_single_coach(self):
        """
        Tests removing a coach from a user's coaches
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_coach(u2)
        u1.remove_coach(u2)

        self.assertEqual(len(u1.coaches), 0)
        self.assertFalse(u2 in u1.coaches)
        self.assertFalse(u1 in u2.students)

    def test_user_remove_multiple_coaches_same_name(self):
        """
        Tests removing multiple coaches with the same name
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u2", 1)
        u1.add_coach(u2)
        u1.add_coach(u3)

        u1.remove_coach(u2)
        self.assertEqual(len(u1.coaches), 1)
        self.assertFalse(u2 in u1.coaches)
        self.assertTrue(u3 in u1.coaches)
        self.assertFalse(u1 in u2.students)
        self.assertTrue(u1 in u3.students)

    def test_user_double_remove_coach(self):
        """
        Tests that an error is raised when double removing a coach
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u1.add_coach(u2)
        u1.remove_coach(u2)
        self.assertRaises(MissingCoachError, u1.remove_coach, u2)

        self.assertEqual(len(u1.coaches), 0)
        self.assertFalse(u1 in u2.students)
        self.assertFalse(u2 in u1.coaches)

    def test_user_num_infected_students(self):
        """
        Tests the calculation of the number of infected students of a user.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 2)
        u3 = User("u3", 2)
        u4 = User("u4", 1)
        u1.add_student(u2)
        u1.add_student(u3)
        u1.add_student(u4)

        num_infected = u1.num_infected_students(2)
        self.assertEqual(len(u1.students), 3)
        self.assertEqual(num_infected, 2)

        num_infected = u1.num_infected_students(1)
        self.assertEqual(num_infected, 1)