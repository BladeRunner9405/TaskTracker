import sys

from src.TaskTracker.Processes import CancelProcessException, ChooseProfileProcess, MainMenuProcess, \
    GetCurrProfileProcess, UserProfileProcess, TaskProcess, BackPackSolutionProcess
import os

CURR_PROFILE = None


def main_menu(actions, actions_for_authorized):
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Главное меню". Возвращает пользователя в главное меню.
    Параметры нужны для того, чтобы процесс главного меню знал, какие методы могут быть доступны для пользователя
    :param actions:
    :param actions_for_authorized:
    :return request - запрос пользователя:
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Добро пожаловать в консольное приложение TaskTracker!")
    curr_process = MainMenuProcess(CURR_PROFILE, list(actions.keys()), list(actions_for_authorized.keys()))
    return curr_process.start_process()


def create_profile():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Создать профиль". Запускает процесс создания профиля
    :return:
    """
    global CURR_PROFILE
    CURR_PROFILE = UserProfileProcess().start_creating_process()


def choose_profile():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Выбрать профиль". Запускает процесс выбора профиля
    :return:
    """
    global CURR_PROFILE
    CURR_PROFILE = ChooseProfileProcess().start_process()


def my_profile():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Мой профиль". Запускает процесс показа информации о профиле
    :return:
    """
    global CURR_PROFILE
    GetCurrProfileProcess(CURR_PROFILE).start_process()


def edit_profile():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Изменить профиль". Запускает процесс редактирования профиля
    :return:
    """
    global CURR_PROFILE
    UserProfileProcess(CURR_PROFILE).start_editing_process()


def create_task():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Создать задачу". Запускает процесс создания задачи
    :return:
    """
    global CURR_PROFILE
    if not CURR_PROFILE:
        print("Для этого нужно выбрать профиль. Чтобы выбрать профиль, введите \"Выбрать профиль\"")
    else:
        TaskProcess(CURR_PROFILE).start_creating_process()


def solve_bock_pack_task():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Составить план-ориентир". Запускает процесс составления и показа плана-ориентира
    :return:
    """
    BackPackSolutionProcess(CURR_PROFILE).start_process()


def edit_task():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Изменить задачу". Запускает процесс выбора и изменения задачи
    :return:
    """
    global CURR_PROFILE
    if not CURR_PROFILE:
        print("Для этого нужно выбрать профиль. Чтобы выбрать профиль, введите \"Выбрать профиль\"")
    else:
        TaskProcess(CURR_PROFILE).start_edit_process()


def delete_task():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Удалить задачу". Запускает процесс выбора удаления задачи
    :return:
    """
    global CURR_PROFILE
    TaskProcess(CURR_PROFILE).start_deleting_task_process()


def show_tasks():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Просмотреть задачи". Запускает процесс показа задач
    :return:
    """
    global CURR_PROFILE
    if not CURR_PROFILE:
        print("Для этого нужно выбрать профиль. Чтобы выбрать профиль, введите \"Выбрать профиль\"")
    else:
        TaskProcess(CURR_PROFILE).show_tasks()


def end_work():
    """
    Специальный метод, который вызывается, когда пользователь выбирает вариант "Завершение работы". Завершает работу приложения
    :return:
    """
    global CURR_PROFILE
    sys.exit()


ACTIONS = {"Создать профиль": create_profile,
           "Выбрать профиль": choose_profile,
           "Завершение работы": end_work}

ACTIONS_FOR_AUTHORIZED = {
    "Мой профиль": my_profile,
    "Изменить профиль": choose_profile,
    "Создать задачу": create_task,
    "Изменить задачу:": edit_task,
    "Удалить задачу:": delete_task,
    "Просмотреть задачи": show_tasks,
    "Составить план-ориентир": solve_bock_pack_task,
}

ALL_ACTIONS = ACTIONS | ACTIONS_FOR_AUTHORIZED
if __name__ == "__main__":
    while True:
        try:
            request = main_menu(ACTIONS, ACTIONS_FOR_AUTHORIZED)

            if request in ALL_ACTIONS:
                ALL_ACTIONS[request]()

        except CancelProcessException:
            continue
