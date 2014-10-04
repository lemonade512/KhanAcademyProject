from random import choice

__author__ = 'Phillip Lemons'


class UserNetwork:
    def __init__(self):
        self.users = list()

    @staticmethod
    def total_infection(user, version):
        # Create a frontier of users
        # TODO: this does not work for circular relationships. Maybe use an ordered set?
        frontier = [user] + [s for s in user.students] + [c for c in user.coaches]
        # Create empty list of discovered users
        discovered = []
        # While frontier is not empty
        while len(frontier) > 0:
            # Take first user from frontier
            curr_user = frontier[0]
            # Add the user to discovered users
            discovered.append(curr_user)
            # Add that user's connections to frontier (if not discovered)
            frontier += [s for s in curr_user.students if s not in discovered]
            frontier += [c for c in curr_user.coaches if c not in discovered]
            # Infect the user
            curr_user.version = version
            del frontier[0]

    def limited_infection(self, user, target_num, version):
        num_infected = 0

        # Checks to make sure we don't have a target_num greater than number of uninfected users
        uninfected = [u for u in self.users if u.version != version]
        if target_num > len(uninfected):
            print "Target num is too high! Infecting all users..."
            target_num = len(uninfected)
            # TODO Should I make a faster function to just infect everyone?

        while num_infected < target_num:
            # If user not infected
            if user.version != version:
                # Infect user
                user.version = version
                # Add 1 to num
                num_infected += 1

            # For uninfected student in user.students
            uninfected_students = [s for s in user.students if s.version != version]
            for student in uninfected_students:
                # Infect student
                student.version = version
                # Add 1 to num
                num_infected += 1

            # (Find user with most infected students AND uninfected closest to target num) OR random user
            user = self.find_best_user(target_num - num_infected, version)

            # If there is no best user we have infected everyone
            if user is None:
                break

    #TODO this function needs improvement
    def find_best_user(self, target_num, version):
        """
        Finds the user that should be infected next. Or a random one if there is no best user.
        :param target_num:
        :param version:
        :return: best user to infect next (for limited infection)
        """
        # List of tuples where tuple is (user, num_infected_students)
        best_user_list = [(u, u.num_infected_students(version)) for u in self.users
                          if u.num_infected_students(version) != len(u.students) or u.version != version]

        if len(best_user_list) == 0:
            # No one has any uninfected students so return random user w/ uninfected students
            uninfected_users = [u for u in self.users if u.version != version]
            if len(uninfected_users) == 0:
                return None
            rand_user = choice(uninfected_users)
            return rand_user

        # Find all of the users with the max infected students
        most_infected = [(u, c) for u, c in best_user_list if c == max([count for _, count in best_user_list])]
        # Of the users in most_infected, pick one with uninfected closest to target_num
        best_user = None
        best_uninfected_count = None
        for user, count in most_infected:
            # If user is not infected, subtract 1 from count
            if user.version != version:
                count -= 1

            target_delta = abs((len(user.students) - count) - target_num)

            if target_delta < best_uninfected_count or best_uninfected_count is None:
                best_uninfected_count = target_delta
                best_user = user

        return best_user

    def add_user(self, user):
        """
        Will add a user to the user_list. Note: this will not recursively add
        so you must explicitly add every single user.

        :param user: user to add
        :return:
        """
        if user in self.users:
            print "User already in network!"
            return
        self.users.append(user)

    def remove_user(self, user):
        """
        Will remove a user from the network. Note: like add_user this does not
        recursively remove users

        :param user:
        :return:
        """
        if user not in self.users:
            print "User is not in network!"
            return
        self.users.remove(user)