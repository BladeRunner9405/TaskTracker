class UserProfile:
    days = []

    def __init__(self):
        days = []
        for i in range(7):
            days.append(Day())

    def get_free_time(self, day):
        pass

    def set_free_time(self, day):
        pass


class Day:
    freeTime = 0

    def __init__(self):
        self.freeTime = 0

    def change_free_time(self, new_free_time):
        if type(new_free_time) != float and type(new_free_time) != int:
            raise NameError("Free time amount must be float or int")
        if new_free_time < 0:
            raise NameError("The number must not be negative")
        else:
            self.freeTime = new_free_time
