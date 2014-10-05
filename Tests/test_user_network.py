import sys
import os
sys.path.append(os.path.abspath(__file__)+"/..")

import unittest
from user import User
from user_network import UserNetwork, NonExistentUserError, DuplicateUserError

__author__ = 'Phillip Lemons'


class TestUserNetwork(unittest.TestCase):

    @staticmethod
    def assertAllInfected(users, version):
        for u in users:
            if u.version != version:
                raise AssertionError(u.name + " is not infected.")

    @staticmethod
    def assertAllNotInfected(users, version):
        # NOTE: this assumes that each user was not already infected with version in
        # a previous infection
        for u in users:
            if u.version == version:
                raise AssertionError(u.name + " is infected.")

    def case_1_setup(self):
        A = User("A", 1)
        B = User("B", 1)
        C = User("C", 1)
        D = User("D", 1)
        E = User("E", 1)
        F = User("F", 1)
        G = User("G", 1)
        H = User("H", 1)
        I = User("I", 1)
        J = User("J", 1)

        A.add_student(B)
        A.add_student(C)
        A.add_student(D)
        B.add_student(E)
        B.add_student(F)
        C.add_student(F)
        D.add_student(G)

        J.add_coach(H)
        J.add_coach(I)

        network = UserNetwork()
        network.add_user(A)
        network.add_user(B)
        network.add_user(C)
        network.add_user(D)
        network.add_user(E)
        network.add_user(F)
        network.add_user(G)
        network.add_user(H)
        network.add_user(I)
        network.add_user(J)

        return {"A": A, "B": B, "C": C, "D": D, "E": E, "F": F, "G": G,
                "H": H, "I": I, "J": J}, network

    def test_add_user(self):
        """
        Tests adding a user to a network.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)

        network = UserNetwork()
        network.add_user(u1)
        self.assertEqual(len(network.users), 1)
        self.assertTrue(u1 in network.users)

        network.add_user(u2)
        self.assertEqual(len(network.users), 2)
        self.assertTrue(u1 in network.users)
        self.assertTrue(u2 in network.users)

    def test_add_duplicate_user(self):
        """
        Tests adding a user twice will throw an error.
        """
        u1 = User("u1", 1)
        network = UserNetwork()
        network.add_user(u1)
        self.assertRaises(DuplicateUserError, network.add_user, u1)

    def test_remove_user(self):
        """
        Tests removing a user from a network.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)

        network = UserNetwork()
        network.add_user(u1)
        network.add_user(u2)

        network.remove_user(u1)
        self.assertEqual(len(network.users), 1)
        self.assertTrue(u2 in network.users)
        self.assertFalse(u1 in network.users)

        network.remove_user(u2)
        self.assertEqual(len(network.users), 0)
        self.assertFalse(u2 in network.users)
        self.assertFalse(u1 in network.users)

    def test_double_remove_user(self):
        """
        Tests double removing a user will throw an error.
        """
        u1 = User("u1", 1)
        network = UserNetwork()
        network.add_user(u1)
        network.remove_user(u1)
        self.assertRaises(NonExistentUserError, network.remove_user, u1)

    def test_basic_total_infection(self):
        """
        Basic test of the total infection algorithm. There are 3 users such that user 1 coaches
        user 2 and user 2 coaches user 3. All of the users should be infected.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u3", 1)
        u1.add_student(u2)
        u2.add_student(u3)

        network = UserNetwork()
        network.add_user(u1)
        network.add_user(u2)
        network.add_user(u3)

        network.total_infection(u1, 2)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 2)
        self.assertEqual(u3.version, 2)

        network.total_infection(u2, 3)
        self.assertEqual(u1.version, 3)
        self.assertEqual(u2.version, 3)
        self.assertEqual(u3.version, 3)

        network.total_infection(u2, 4)
        self.assertEqual(u1.version, 4)
        self.assertEqual(u2.version, 4)
        self.assertEqual(u3.version, 4)

    def test_unconnected_total_infection(self):
        """
        Tests the total infection algorithm with 3 unconnected users.
        Each time the algorithm is called, only one user should be infected.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u3", 1)

        network = UserNetwork()
        network.add_user(u1)
        network.add_user(u2)
        network.add_user(u3)

        network.total_infection(u1, 2)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 1)
        self.assertEqual(u3.version, 1)

        network.total_infection(u2, 3)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 3)
        self.assertEqual(u3.version, 1)

        network.total_infection(u3, 4)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 3)
        self.assertEqual(u3.version, 4)

    def test_some_connected_total_infection(self):
        """
        Tests total infection of a network where only some of the users are connected to each other.
        Each time the algorithm is called, only one connected portion of the network should be infected.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u3", 1)
        u4 = User("u4", 1)
        u5 = User("u5", 1)
        u6 = User("u6", 1)

        u1.add_student(u2)
        u1.add_student(u3)
        u2.add_student(u4)

        u5.add_student(u6)

        network = UserNetwork()
        network.add_user(u1)
        network.add_user(u2)
        network.add_user(u3)
        network.add_user(u4)
        network.add_user(u5)
        network.add_user(u6)

        network.total_infection(u1, 2)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 2)
        self.assertEqual(u3.version, 2)
        self.assertEqual(u4.version, 2)
        self.assertEqual(u5.version, 1)
        self.assertEqual(u6.version, 1)

        network.total_infection(u2, 3)
        self.assertEqual(u1.version, 3)
        self.assertEqual(u2.version, 3)
        self.assertEqual(u3.version, 3)
        self.assertEqual(u4.version, 3)
        self.assertEqual(u5.version, 1)
        self.assertEqual(u6.version, 1)

        network.total_infection(u4, 4)
        self.assertEqual(u1.version, 4)
        self.assertEqual(u2.version, 4)
        self.assertEqual(u3.version, 4)
        self.assertEqual(u4.version, 4)
        self.assertEqual(u5.version, 1)
        self.assertEqual(u6.version, 1)

        network.total_infection(u5, 5)
        self.assertEqual(u1.version, 4)
        self.assertEqual(u2.version, 4)
        self.assertEqual(u3.version, 4)
        self.assertEqual(u4.version, 4)
        self.assertEqual(u5.version, 5)
        self.assertEqual(u6.version, 5)

    def test_case_1_total_infection(self):
        u_dict, network = self.case_1_setup()
        group_1 = [u_dict['A'], u_dict['B'], u_dict['C'], u_dict['D'], u_dict['E'],
                    u_dict['F'], u_dict['G']]
        group_2 = [u_dict['H'], u_dict['I'], u_dict['J']]

        network.total_infection(u_dict['A'], 2)
        self.assertAllInfected(group_1, 2)
        self.assertAllNotInfected(group_2, 2)

        network.total_infection(u_dict['F'], 3)
        self.assertAllInfected(group_1, 3)
        self.assertAllNotInfected(group_2, 3)

        network.total_infection(u_dict['J'], 4)
        self.assertAllInfected(group_2, 4)
        self.assertAllNotInfected(group_1, 4)

    def test_basic_limited_infection(self):
        """
        Tests the limited infection algorithm on a network of 3 users such that user 1 coaches user 2 and
        user 2 coaches user 3.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u3", 1)
        u1.add_student(u2)
        u2.add_student(u3)

        network = UserNetwork()
        network.add_user(u1)
        network.add_user(u2)
        network.add_user(u3)

        network.limited_infection(u1, 2, 2)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 2)
        self.assertEqual(u3.version, 1)

        network.limited_infection(u2, 2, 3)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 3)
        self.assertEqual(u3.version, 3)

        # Make sure it finds user w/ most infected students
        network.limited_infection(u3, 2, 4)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 4)
        self.assertEqual(u3.version, 4)

    def test_unconnected_limited_infection(self):
        """
        Tests the limited infection algorithm with a group of 3 unconnected users.
        """
        u1 = User("u1", 1)
        u2 = User("u2", 1)
        u3 = User("u3", 1)

        network = UserNetwork()
        network.add_user(u1)
        network.add_user(u2)
        network.add_user(u3)

        network.limited_infection(u1, 3, 2)
        self.assertEqual(u1.version, 2)
        self.assertEqual(u2.version, 2)
        self.assertEqual(u3.version, 2)

        network.limited_infection(u2, 3, 3)
        self.assertEqual(u1.version, 3)
        self.assertEqual(u2.version, 3)
        self.assertEqual(u3.version, 3)

        network.limited_infection(u3, 3, 4)
        self.assertEqual(u1.version, 4)
        self.assertEqual(u2.version, 4)
        self.assertEqual(u3.version, 4)

        network.limited_infection(u2, 2, 5)
        self.assertEqual(u2.version, 5)
        # One or other but not both
        self.assertNotEqual(u1.version, u3.version)
        self.assertTrue(u1.version == 5 or u3.version == 5)

    def test_case_1_limited_infection(self):
        """
        Limited infection for test case 1. For a visual representation of the users in test case 1 see
        TestCase1.png. For each section of the test you can see what users are infected and what users are
        uninfected by looking at the infected and uninfected lists.
        """
        u_dict, network = self.case_1_setup()

        network.limited_infection(u_dict["A"], 3, 2)
        infected = [u_dict[u] for u in ["A", "B", "C", "D"]]
        uninfected = [u_dict[u] for u in ["E", "F", "G", "H", "I", "J"]]
        self.assertAllInfected(infected, 2)
        self.assertAllNotInfected(uninfected, 2)

        network.limited_infection(u_dict["A"], 4, 3)
        infected = [u_dict[u] for u in ["A", "B", "C", "D"]]
        uninfected = [u_dict[u] for u in ["E", "F", "G", "H", "I", "J"]]
        self.assertAllInfected(infected, 3)
        self.assertAllNotInfected(uninfected, 3)

        network.limited_infection(u_dict["F"], 3, 4)
        infected = [u_dict[u] for u in ["F", "B", "E"]]
        uninfected = [u_dict[u] for u in ["A", "C", "D", "G", "H", "I", "J"]]
        self.assertAllInfected(infected, 4)
        self.assertAllNotInfected(uninfected, 4)

        network.limited_infection(u_dict["H"], 1, 5)
        infected = [u_dict[u] for u in ["H", "J"]]
        uninfected = [u_dict[u] for u in ["I", "A", "B", "C", "D", "E", "F", "G"]]
        self.assertAllInfected(infected, 5)
        self.assertAllNotInfected(uninfected, 5)

        network.limited_infection(u_dict["H"], 3, 6)
        infected = [u_dict[u] for u in ["H", "I", "J"]]
        uninfected = [u_dict[u] for u in ["A", "B", "C", "D", "E", "F", "G"]]
        self.assertAllInfected(infected, 6)
        self.assertAllNotInfected(uninfected, 6)

        network.limited_infection(u_dict["F"], 2, 7)
        infected = [u_dict[u] for u in ["F", "C"]]
        uninfected = [u_dict[u] for u in ["A", "B", "D", "E", "G", "H", "I", "J"]]
        self.assertAllInfected(infected, 7)
        self.assertAllNotInfected(uninfected, 7)

        network.limited_infection(u_dict["F"], 2, 8)
        network.limited_infection(u_dict["E"], 2, 8)
        network.limited_infection(u_dict["G"], 2, 8)
        infected = [u_dict[u] for u in ["A", "F", "C", "B", "D", "E", "G"]]
        uninfected = [u_dict[u] for u in ["H", "I", "J"]]
        self.assertAllInfected(infected, 8)
        self.assertAllNotInfected(uninfected, 8)

    def test_case_1_limited_infection_too_many(self):
        """
        Tests limited infection when given a number higher than the number of users in the network.
        This should infect every user.
        """
        u_dict, network = self.case_1_setup()

        # Test when we want to infect more users than we have
        network.limited_infection(u_dict["A"], 12, 2)
        infected = [u_dict[u] for u in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]]
        self.assertAllInfected(infected, 2)