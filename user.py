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
            self.students = studenst

        self.software_version = version
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

if __name__ == "__main__":
    # Example relationship tree
    #            u5--|
    #            |   |
    #            u1  |
    #           /  \ |
    #         u2   u3-
    #         |
    #        u4
    u1 = User("u1", 1)
    u2 = User("u2", 1)
    u3 = User("u3", 1)
    u4 = User("u4", 1)
    u5 = User("u5", 1)

    u1.add_student(u2)
    u1.add_student(u2)
    u1.add_student(u3)
    u2.add_student(u4)
    u1.add_coach(u5)
    u3.add_student(u5)

    print u1
    print u2
    print u3
    print u4
    print u5