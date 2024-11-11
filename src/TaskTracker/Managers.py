from src.TaskTracker.SQLiteDatabase import SQLiteDatabase

WEEK_DAYS = "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday".split(', ')
TASKS_HEADS = "Importance, Time, Deadline".split(', ')


class UserManager:
    pass


class UserDatabaseManager:
    """
    Класс, который манипулирует таблицей Users с помощью SQLiteDatabase
    """

    def __init__(self, db_file):
        self.database = SQLiteDatabase(db_file)

        self.database.create_table("Users", "Name", *WEEK_DAYS)

    def create_user(self, name, week_times):
        """
        Метод, сохраняющий нового пользователя в базу данных
        :param name:
        :param week_times:
        :return:
        """
        if self.database is not None:
            self.database.insert_data("Users", name, *week_times)

    def update_user(self, name, week_times):
        """
        Метод, сохраняющий изменения пользователя в базу данных
        :param name:
        :param week_times:
        :return:
        """
        if self.database is not None:
            self.database.update_data("Users", "Name", name, WEEK_DAYS, week_times)

    def check_if_profile_exists(self, profile):
        """
        Метод, проверяющий, существует ли такой профиль в базе данных
        :param profile:
        :return True/False:
        """
        if self.database.fetch_one("Users", f"Name = \"{profile}\"") is not None:
            return False
        return True

    def get_all_profiles(self):
        """
        Метод, возвращающий все профили
        :return profiles:
        """
        profiles = list(_[0] for _ in self.database.get_column("Users", "Name"))
        return profiles

    def get_profile_info(self, profile):
        """
        Метод, возвращающий информацию о профиле
        :param profile:
        :return profile_info - информация о профиле profile:
        """
        profile_info = self.database.fetch_one("Users", f"Name = \"{profile}\"")
        return profile_info

    def close(self):
        """
        Метод, который прерывает соединение с базой данных
        :return:
        """
        self.database.close()


class TasksDatabaseManager:
    """
    Класс, который манипулирует таблицей Tasks с помощью SQLiteDatabase
    """

    def __init__(self, db_file):
        self.database = SQLiteDatabase(db_file)
        self.database.create_table("Tasks", "Profile", "Task", *TASKS_HEADS)

    def save_task(self, profile, task_name, task_importance, task_time_cost, deadline):
        """
        Метод, сохраняющий новую задачу в базу данных
        :param profile:
        :param task_name:
        :param task_importance:
        :param task_time_cost:
        :return:
        """
        if self.database is not None:
            self.database.insert_data("Tasks", profile, task_name, task_importance, task_time_cost, deadline)

    def update_task(self, profile, task_name, task_importance, task_time_cost, deadline):
        """
        Метод, который редактирует задачу
        :param profile:
        :param task_name:
        :param task_importance:
        :param task_time_cost:
        :param deadline:
        :return:
        """
        if self.database is not None:
            self.database.update_data("Tasks", "Profile", profile, TASKS_HEADS,
                                      [task_importance, task_time_cost, deadline],
                                      "Task", task_name)

    def delete_task(self, profile, task_name):
        """
        Метод, который удалят задачу
        :param profile:
        :param task_name:
        :return:
        """
        if self.database is not None:
            self.database.delete_data("Tasks", "Profile", profile, "Task", task_name)

    def check_if_task_exists(self, profile, task_name):
        """
        Метод, проверяющий, существует ли у пользователя задача с таким названием
        :param profile:
        :param task_name:
        :return False/True:
        """
        if self.database.fetch_one("Tasks", f"Profile = \"{profile}\" AND Task = \"{task_name}\"") is not None:
            return False
        return True

    def get_all_tasks(self, profile):
        """
        Метод, получающий все задачи профиля
        :param profile:
        :return tasks - все задачи пользователя profile:
        """
        tasks = list(_[1:] for _ in self.database.fetch_all("Tasks", f"Profile = \"{profile}\""))
        return tasks

    def close(self):
        """
        Метод, который прерывает соединение с базой данных
        :return:
        """
        self.database.close()
