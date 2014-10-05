from random import choice
from user import User

__author__ = 'Phillip Lemons'


class DuplicateUserError(Exception):
    pass


class NonExistentUserError(Exception):
    pass


class UserNetwork:
    def __init__(self):
        self.users = list()

    @staticmethod
    def total_infection(user, version):
        """
        Total infection that uses a breadth-first algorithm to infect all users in a connected section of a network.

        :param user: Starting user to infect
        :type user: User
        :param version: What version to infect users with
        :return: None
        """
        frontier = [user] + [s for s in user.students] + [c for c in user.coaches]
        discovered = []
        while len(frontier) > 0:
            # Take first user from frontier
            curr_user = frontier.pop(0)
            # Add the user to discovered users
            discovered.append(curr_user)
            # Add that user's connections to frontier (if not discovered)
            frontier += [s for s in curr_user.students if s not in discovered]
            frontier += [c for c in curr_user.coaches if c not in discovered]
            # Infect the user
            curr_user.version = version

    def infect_all(self, version):
        """
        Infects all users

        :param version: what to infect each user with
        :return: None
        """
        for user in self.users:
            user.version = version

    def limited_infection(self, user, target_num, version):
        """
        Limited infection attempts to infect a target number of users with a version. The algorithm will first
        infect the given user and their students. Then, the algorithm will search for the user with the most infected
        students. If there are multiple users with the same number of infected students the algorithm will choose the
        user that has a number of un-infected students closest to the target number.

        :param user: Starting user to infect
        :type user: User
        :param target_num: Target number of infections
        :type target_num: int
        :param version: version to infect students with
        """
        num_infected = 0

        # Checks to make sure we don't have a target_num greater than number of uninfected users
        uninfected = [u for u in self.users if u.version != version]
        if target_num > len(uninfected):
            self.infect_all(version)

        while num_infected < target_num:
            # Infect the given user first
            if user.version != version:
                user.version = version
                num_infected += 1

            # Infect the uninfected students of user
            uninfected_students = [s for s in user.students if s.version != version]
            for student in uninfected_students:
                student.version = version
                num_infected += 1

            # Find the next user to infect
            user = self.find_best_user(target_num - num_infected, version)

            # If there is no best user we have infected everyone
            if user is None:
                break

    def find_best_user(self, target_num, version):
        """
        Finds the user that should be infected next or a random one if there is no best user. If there are no
        more users to infect, the method returns None.

        :param target_num: Target number of infections
        :type target_num: int
        :param version: What to infect the user with
        :return: best user to infect next or None if no uninfected users
        """
        # List of tuples (user, num_infected_students)
        best_user_list = [(u, u.num_infected_students(version)) for u in self.users
                          # Filters out users that are not infected and have no infected students
                          if u.num_infected_students(version) != len(u.students) or u.version != version]

        if len(best_user_list) == 0:
            # No one has any uninfected students so return random user w/ uninfected students
            uninfected_users = [u for u in self.users if u.version != version]
            if len(uninfected_users) == 0:
                # No more users to infect
                return None
            rand_user = choice(uninfected_users)
            return rand_user

        # Find all of the users with the max number of infected students
        most_infected = [(u, c) for u, c in best_user_list if c == max([count for _, count in best_user_list])]
        
        # Of the users in most_infected, pick one with uninfected closest to target_num
        best_user = None
        best_uninfected_count = None
        for user, infected_count in most_infected:
            # If user is not infected, subtract 1 from infected_count
            if user.version != version:
                infected_count -= 1

            # target_delta represents how close infecting this user will bring us to our target
            target_delta = abs((len(user.students) - infected_count) - target_num)

            if target_delta < best_uninfected_count or best_uninfected_count is None:
                best_uninfected_count = target_delta
                best_user = user

        return best_user

    def add_user(self, user):
        """
        Will add a user to the user_list. Note: this will not recursively add
        so you must explicitly add every single user.

        :param user: Who you want to add to the network.
        :return: None
        """
        if user in self.users:
            raise DuplicateUserError(user.name + " is already in the network!")
        self.users.append(user)

    def remove_user(self, user):
        """
        Will remove a user from the network. Note: like add_user this does not
        recursively remove users

        :param user: Who you want to remove from the network.
        :return: None
        """
        if user not in self.users:
            raise NonExistentUserError(user.name + " is not in the network!")
        self.users.remove(user)
