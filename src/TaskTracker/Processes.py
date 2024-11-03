import re
from datetime import datetime

from src.TaskTracker.BackPackSolution import BackPackSolution
from src.TaskTracker.Managers import UserDatabaseManager, TasksDatabaseManager
from prettytable import PrettyTable

DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


class CancelProcessException(Exception):
    def __init__(self, message):
        self.message = message


class Process:
    """
    Класс общий предок для всех процессов
    """

    def start_process(self):
        """
        Метод, вызывающийся, чтобы запустить процесс
        """
        pass

    def cancel_process(self):
        """
        Метод, вызывающийся при завершении процесса
        """
        pass


def get_date(process):
    print("Введите дату:", end=" ")

    date = _get_message(process, True)
    while not is_valid_date(date):
        print("Пожалуйста, введите дату в формате DD.MM.YYYY:", end=" ")
        date = _get_message(process, True)

    return date


def is_valid_date(date_str):
    """
    Проверяет, является ли строка датой в формате DD.MM.YYYY.

    Args:
      date_str: Строка, которую нужно проверить.

    Returns:
      True, если строка является датой в формате DD.MM.YYYY, иначе False.
    """
    pattern = r"^\d{2}\.\d{2}\.\d{4}$"
    if re.match(pattern, date_str):
        day, month, year = map(int, date_str.split('.'))
        # Дополнительная проверка:
        if 1 <= month <= 12 and 1 <= day <= 31:
            return True
    return False


def _get_message(process, not_none=False, only_int=False):
    """
    Метод, специально созданный для того, чтобы в любой момент можно было отменить любой процесс
    :return:
    """

    def repeat():
        print("Пожалуйста, попробуйте ещё раз:", end=" ")
        return _get_message(process, not_none, only_int)

    message = input()
    if message == "Отмена":
        process.cancel_process()
        raise CancelProcessException("Процесс создания профиля был отменён")
    if not_none:
        if not message:
            print("Сейчас ввод не может быть пустым")
            return repeat()

    if only_int:
        try:
            ans = int(message)
            if ans < 0:
                print("Ввод не может быть отрицательным числом.")
                return repeat()
            return ans
        except ValueError:
            print("Пожалуйста, введите положительное целое число, без лишних символов")
            return repeat()
    return message


def get_non_digit_name(process):
    name = _get_message(process, True)
    if name.isdigit():
        print("Ввод не может состоять только из цифр. Пожалуйста, попробуйте другой вариант:", end=" ")
        return get_non_digit_name(process)

    return name


def choose_variant(process, variants):
    for i in range(len(variants)):
        print(f"\t{i + 1}: {variants[i]}")
    print("Ваш выбор:", end=" ")
    res = _get_message(process)
    if res in variants:
        return res
    elif res.isdigit():
        res = int(res) - 1
        if 0 <= res < len(variants):
            return variants[res]
    print("Такого варианта нет в списке. Пожалуйста, выберете вариант из списка")
    return choose_variant(process, variants)


def print_table(head, body):
    table = PrettyTable(head)
    td_data = body[:]

    for elem in td_data:
        table.add_row(elem)

    print(table)


def press_anything_to_continue(process):
    print("Введите что-нибудь для продолжения:", end=" ")
    _get_message(process)


class UserProfileProcess(Process):
    """
    Класс, предназначенный для создания нового профиля
    """

    def __init__(self, profile=None):
        self.profile = profile
        self.database_manager = UserDatabaseManager("my_database.db")

    def get_day(self, i):
        """
        Метод, считывающий и обрабатывающий пользовательский ввод на i-ый день недели
        :param i:
        :return:
        """

        print(f"\t{DAYS[i]}:")
        print("\tЧасов", end=" ")
        hours = _get_message(self, True, True)
        print("\tМинут", end=" ")
        minutes = _get_message(self, True, True)

        if hours * 60 + minutes > 24 * 60:
            print("Введённое вами время превышает количество часов в одном дне")
            return self.get_day(i)

        return hours * 60 + minutes

    def get_week_time(self):
        """
        Метод, считывающий, обрабатывающий и кодирующий общее свободное время пользователя
        :return:
        """
        print(
            "Пожалуйста, введите сколько своего времени вы хотите тратить на выполнение своих задач в каждом из следующих дней:")

        week_time = []  # Массив, где элемент с номером i отвечает, сколько у пользователя свободного времени в i-ый день недели
        for i in range(7):
            week_time.append(self.get_day(i))
            print("\t----------")

        return week_time

    def start_creating_process(self):
        """
        Процесс создания профиля
        :return:
        """
        super().start_process()
        print(
            "Запускается процесс создания профиля. В любой момент вы можете ввести \"Отмена\" для отмены создания профиля.")

        print("Пожалуйста, введите название профиля:", end=" ")
        name = get_non_digit_name(self)
        while not self.database_manager.check_if_profile_exists(name):
            print("Такой профиль уже существует. Пожалуйста, придумайте другое название")
            name = get_non_digit_name(self)
        self.profile = name
        return self.start_editing_process(False)

    def start_editing_process(self, edit=True):
        """
        Процесс изменения профиля
        :return:
        """

        week_times = self.get_week_time()
        if not edit:
            self.database_manager.create_user(self.profile, week_times)
        else:
            self.database_manager.update_user(self.profile, week_times)
        self.database_manager.close()
        print(f"Профиль {self.profile} был успешно сохранён. Переключаемся на него...")
        press_anything_to_continue(self)
        return self.profile

    def cancel_process(self):
        super().cancel_process()
        print("Процесс создания профиля был отменён")
        self.database_manager.close()


class ChooseProfileProcess(Process):
    def start_process(self):
        """
        Процесс выбора профиля пользователя
        :return:
        """
        super().start_process()

        database_manager = UserDatabaseManager("my_database.db")
        profiles = database_manager.get_all_profiles()
        database_manager.close()
        if len(profiles) > 0:
            print("Пожалуйста, выберете профиль из списка:")
            profile = choose_variant(self, profiles)
            print(f"Выбран профиль: {profile}")
            press_anything_to_continue(self)
            return profile
        else:
            print("Пока что профилей нет. Пожалуйста, создайте новый профиль")
            press_anything_to_continue(self)

    def cancel_process(self):
        super().cancel_process()
        print("Процесс выбора профиля был отменён")


class TaskProcess(Process):
    """
    Класс, для создания новых задач
    """

    def __init__(self, curr_profile, task_name=None):
        self.task_name = task_name
        self.curr_profile = curr_profile
        self.database_manager = TasksDatabaseManager("my_database.db")

    def start_creating_process(self):
        """
        Процесс создания задачи
        :return:
        """
        print("Введите названия задачи:", end=" ")

        self.task_name = get_non_digit_name(self)
        while not self.database_manager.check_if_task_exists(self.curr_profile, self.task_name):
            print("Задача с таким названием уже существует. Пожалуйста, придумайте другое название:", end=" ")
            self.task_name = get_non_digit_name(self)

        self.start_detailing_process(False)

    def start_detailing_process(self, edit=True):
        """
        Процесс изменения задачи
        :return:
        """

        print("Введите важность этой задачи в условных единицах, от 1 до 10, где 10-очень важно, 1-совсем не важно:",
              end=" ")
        task_importance = _get_message(self, True, True)
        while task_importance > 10:
            print(f"Ваше число больше 10: {task_importance}")
            print("Попробуйте ещё раз:", end=" ")
            task_importance = _get_message(self, True, True)

        print("Введите, сколько примерно времени займёт полное выполнение этого задания:")
        print("Часов:", end=" ")
        hours = _get_message(self, True, True)
        print("Минут:", end=" ")
        minutes = _get_message(self, True, True)
        print("Введите дедлайн этого задания в формате DD.MM.YYYY")
        deadline = get_date(self)

        task_time_cost = hours * 60 + minutes

        if not edit:
            self.database_manager.save_task(self.curr_profile, self.task_name, task_importance, task_time_cost,
                                            deadline)
        else:
            self.database_manager.update_task(self.curr_profile, self.task_name, task_importance, task_time_cost,
                                              deadline)
        self.database_manager.close()
        print(f"Ваша задача {self.task_name} успешно сохранена")
        press_anything_to_continue(self)

    def start_edit_process(self, stop=True):
        self.show_tasks(False)
        print("Пожалуйста, выберете задачу, которую вы хотите отредактировать:")
        database_manager = TasksDatabaseManager("my_database.db")
        tasks = database_manager.get_all_tasks(self.curr_profile)
        database_manager.close()
        self.task_name = choose_variant(self, list(_[0] for _ in tasks))
        self.start_detailing_process(True)

    def start_deleting_task_process(self):
        self.show_tasks(False)
        print("Пожалуйста, выберете задачу, которую вы хотите удалить:")
        database_manager = TasksDatabaseManager("my_database.db")
        tasks = database_manager.get_all_tasks(self.curr_profile)
        task = choose_variant(self, list(_[0] for _ in tasks))
        database_manager.delete_task(self.curr_profile, task)
        database_manager.close()
        print(f"Задача {task} была успешно удалена")
        press_anything_to_continue(self)

    def show_tasks(self, stop=True):
        database_manager = TasksDatabaseManager("my_database.db")
        tasks = database_manager.get_all_tasks(self.curr_profile)
        database_manager.close()

        for i in range(len(tasks)):
            tasks[i] = [tasks[i][0], tasks[i][1], f"{tasks[i][2] // 60} часов {tasks[i][2] % 60} минут", tasks[i][3]]

        if len(tasks) > 0:
            print_table("Название задачи, Важность задачи, Трудозатратность задачи, Дедлайн".split(', '), tasks)
        else:
            print("У этого профиля пока что нет задач")
        if stop:
            press_anything_to_continue(self)


class MainMenuProcess(Process):
    def __init__(self, curr_profile, variants, variants_for_authorized):
        self.curr_profile = curr_profile
        self.variants = variants
        self.variants_for_authorized = variants_for_authorized

    def start_process(self):
        print("Главное меню. Для отмены любого действия введите слово \"Отмена\"")
        curr_variants = self.variants
        if self.curr_profile is not None:
            curr_variants.extend(self.variants_for_authorized)
        res = choose_variant(self, curr_variants)
        return res


class GetCurrProfileProcess(Process):
    def __init__(self, curr_profile):
        self.curr_profile = curr_profile

    def start_process(self):
        if not self.curr_profile:
            print("Пока что вы не выбрали профиль. Чтобы выбрать профиль, введите \"Выбрать профиль\"")
        else:
            user_db_manager = UserDatabaseManager("my_database.db")
            head = ["Профиль", *DAYS]
            body = [user_db_manager.get_profile_info(self.curr_profile)]
            for i in range(len(body)):
                body[i] = [body[i][0], *list(f"{_ // 60} часов {_ % 60} минут" for _ in body[i][1:])]
            print_table(head, body)
        press_anything_to_continue(self)


def filter_tasks(tasks, cutoff_date):
    filtered_data = []
    cutoff_datetime = datetime.strptime(cutoff_date, '%d.%m.%Y').date()
    min_date = None
    for row in tasks:
        date_str = row[3]
        date = datetime.strptime(date_str, '%d.%m.%Y').date()
        if date < cutoff_datetime:
            filtered_data.append(row)
            if min_date is None or date > min_date:
                min_date = date

    return filtered_data, min_date


class BackPackSolutionProcess(Process):
    def __init__(self, curr_profile):
        self.curr_profile = curr_profile
        self.task_db_manager = TasksDatabaseManager("my_database.db")
        self.user_db_manager = UserDatabaseManager("my_database.db")

    def start_process(self):
        tasks = self.task_db_manager.get_all_tasks(self.curr_profile)
        if len(tasks) == 0:
            print("У вас сейчас нет задач")
        else:
            print("Введите дату, до которой вы хотите решить как можно больше важных задач")
            deadline = get_date(self)
            tasks, deadline = filter_tasks(tasks, deadline)
            if len(tasks) == 0:
                print("К сожалению, у вас нет задач, которые вы полностью успеете выполнить")
            else:
                info = self.user_db_manager.get_profile_info(self.curr_profile)

                free_time_schedule = {}
                for i in range(1, len(info)):
                    free_time_schedule[i - 1] = info[i]

                result = sorted(BackPackSolution(tasks, free_time_schedule, deadline).solution(),
                                key=lambda x: datetime.strptime(x.deadline, '%d.%m.%Y').date())
                data = []
                for i in range(len(result)):
                    data.append([result[i].Task_name, result[i].utility_value,
                                 f"{result[i].weight_value // 60} часов {result[i].weight_value % 60} минут",
                                 result[i].deadline])

                print("Согласно вашему расписанию, вы можете успеть сделать следующие наиболее важные задачи:")
                print_table(["Задача", "Важность", "Время выполнения", "Дедлайн"], data)
                print("Советуем выполнять те задачи из списка, чей дедлайн раньше других")
        press_anything_to_continue(self)
