__author__ = 'Phillip Lemons'
# TODO add remove_student and remove_coach


class User:
    def __init__(self, name, version, coaches=None, students=None):
        '''
        :param version: integer of the version (could be float too)
        :param coaches: a list of coaches for the user
        :param students: a list of students for the user
        '''
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
        string = "User: " + str(self.name) + "\n"
        string += "\tCoaches: " + str([c.name for c in self.coaches]) + "\n"
        string += "\tStudents: " + str([s.name for s in self.students])
        return string

    def add_student(self, other):
        if other in self.students:
            print other.name + " is already a student of " + self.name
            return
        other.coaches.append(self)
        self.students.append(other)

    def add_coach(self, other):
        if other in self.coaches:
            print other.name + " is already a coach of " + self.name
            return
        other.students.append(self)
        self.coaches.append(other)

    def remove_student(self, other):
        if other not in self.students:
            print other.name + " is not a student of " + self.name
            return
        other.coaches.remove(self)
        self.students.remove(other)

    def remove_coach(self, other):
        if other not in self.coaches:
            print other.name + " is not a coach of " + self.name
            return
        other.students.remove(self)
        self.coaches.remove(other)

    def num_infected_students(self, version):
        """
        :param version: version we are infecting with
        :return: number of students without version
        """
        return len([s for s in self.students if s.version == version])