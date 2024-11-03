import sys

from src.TaskTracker.Processes import CancelProcessException, ChooseProfileProcess, MainMenuProcess, \
    GetCurrProfileProcess, UserProfileProcess, TaskProcess, BackPackSolutionProcess
import os

CURR_PROFILE = None


def main_menu(actions, actions_for_authorized):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Добро пожаловать в консольное приложение TaskTracker!")
    curr_process = MainMenuProcess(CURR_PROFILE, list(actions.keys()), list(actions_for_authorized.keys()))
    return curr_process.start_process()


def create_profile():
    global CURR_PROFILE
    CURR_PROFILE = UserProfileProcess().start_creating_process()


def choose_profile():
    global CURR_PROFILE
    CURR_PROFILE = ChooseProfileProcess().start_process()


def my_profile():
    global CURR_PROFILE
    GetCurrProfileProcess(CURR_PROFILE).start_process()


def edit_profile():
    global CURR_PROFILE
    UserProfileProcess(CURR_PROFILE).start_editing_process()


def create_task():
    global CURR_PROFILE
    if not CURR_PROFILE:
        print("Для этого нужно выбрать профиль. Чтобы выбрать профиль, введите \"Выбрать профиль\"")
    else:
        TaskProcess(CURR_PROFILE).start_creating_process()


def solve_bock_pack_task():
    BackPackSolutionProcess(CURR_PROFILE).start_process()


def edit_task():
    global CURR_PROFILE
    if not CURR_PROFILE:
        print("Для этого нужно выбрать профиль. Чтобы выбрать профиль, введите \"Выбрать профиль\"")
    else:
        TaskProcess(CURR_PROFILE).start_edit_process()


def delete_task():
    global CURR_PROFILE
    TaskProcess(CURR_PROFILE).start_deleting_task_process()


def show_tasks():
    global CURR_PROFILE
    if not CURR_PROFILE:
        print("Для этого нужно выбрать профиль. Чтобы выбрать профиль, введите \"Выбрать профиль\"")
    else:
        TaskProcess(CURR_PROFILE).show_tasks()


def backpack_solution():
    pass


def end_work():
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
