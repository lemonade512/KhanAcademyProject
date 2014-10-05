__author__ = 'Phillip Lemons'


class DuplicateStudentError(Exception):
    pass


class DuplicateCoachError(Exception):
    pass


class MissingStudentError(Exception):
    pass


class MissingCoachError(Exception):
    pass


class User:

    def __init__(self, name, version, coaches=None, students=None):
        """
        Constructor for the User class.

        :param name: User's name
        :param version: what version the user currently has
        :param coaches: coaches of the user
        :type coaches: list
        :param students: students of the user
        :type students: list
        """
        if coaches is None:
            self.coaches = list()
        else:
            self.coaches = coaches

        if students is None:
            self.students = list()
        else:
            self.students = students

        self.version = version
        self.name = name

    def __repr__(self):
        string = "(User: " + str(self.name)
        string += "  Coaches: " + str([c.name for c in self.coaches])
        string += "  Students: " + str([s.name for s in self.students]) + ")"
        return string

    def add_student(self, other):
        """
        Adds a student to self.students making. Also adds self to other.coaches.

        :param other: User that is a student of self
        :type other: User
        :return: None
        :raises: DuplicateStudentError
        """
        if other in self.students:
            raise DuplicateStudentError(other.name + " is already a student of " + self.name)
        other.coaches.append(self)
        self.students.append(other)

    def add_coach(self, other):
        """
        Add coach to self.coaches

        :param other: coach to add
        :type other: User
        :return: None
        :raises: DuplicateCoachError
        """
        if other in self.coaches:
            raise DuplicateCoachError(other.name + " is already a coach of " + self.name)
        other.students.append(self)
        self.coaches.append(other)

    def remove_student(self, other):
        """
        Removes student from self.students

        :param other: student to remove
        :type other: User
        :return: None
        :raises: MissingStudentError
        """
        if other not in self.students:
            raise MissingStudentError(other.name + " is not a student of " + self.name)
        other.coaches.remove(self)
        self.students.remove(other)

    def remove_coach(self, other):
        """
        Removes coach from self.coaches

        :param other: coach to be removed
        :type other: User
        :return: None
        :raises: MissionCoachError
        """
        if other not in self.coaches:
            raise MissingCoachError(other.name + " is not a coach of " + self.name)
        other.students.remove(self)
        self.coaches.remove(other)

    def num_infected_students(self, version):
        """
        Finds how many users are infected with version.

        :rtype: int
        :param version: Specifies version of infected users
        :return: number of users infected with version
        """
        return len([s for s in self.students if s.version == version])