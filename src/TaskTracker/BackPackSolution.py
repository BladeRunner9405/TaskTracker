from datetime import datetime, timedelta
from collections import namedtuple
from functools import lru_cache


class BackPackSolution:
    """
    Класс, который решает задачу о рюкзаке
    """

    def __init__(self, tasks, free_time_schedule, final_date):
        self.tasks = tasks
        self.free_time_schedule = free_time_schedule
        self.final_date = final_date

    def calculate_free_time(self, end_date):
        """
        Вычисляет количество доступного времени у пользователя между сегодняшним днём и датой end_date
        :param end_date:
        :return total_free_time:
        """
        start_date = datetime.today().date()

        total_free_time = 0
        current_date = start_date

        while current_date <= end_date:
            day_of_week = current_date.weekday()
            free_hours = self.free_time_schedule.get(day_of_week, 0)  # Получаем часы для текущего дня недели
            total_free_time += free_hours
            current_date += timedelta(days=1)

        return total_free_time

    def solve_problem(self, tasks, time_remains):
        """
        Метод, решающий задачу о рюкзаке для задач tasks и доступным временем time_remains
        :param tasks:
        :param time_remains:
        :return result - решение задачи о рюкзаке, оптимальный выбор:
        """
        Item = namedtuple('Item', 'Task_name utility_value weight_value deadline')
        items = []
        for i in range(len(tasks)):
            items.append(Item(*tasks[i]))

        capacity = time_remains  # max weight we can put into the knapsack

        @lru_cache(maxsize=None)  # cache all calls
        def best_value(n, w_limit):
            """
            Метод, который позволяет решать задачу о рюкзаке с помощью динамического программирования. Выбирает, добавлять ли n-ый элемент в рюкзак, или нет
            :param n:
            :param w_limit:
            :return max value для n элементов с w_limit:
            """
            if n == 0:  # no items
                return 0  # zero value
            elif items[n - 1].weight_value > w_limit:
                # new item is heavier than the current weight limit
                return best_value(n - 1, w_limit)  # don't include new item
            else:
                return max(  # max of with and without the new item
                    best_value(n - 1, w_limit),  # without
                    best_value(n - 1, w_limit - items[n - 1].weight_value)
                    + items[n - 1].utility_value)  # with the new item

        result = []
        weight_limit = capacity
        for i in reversed(range(len(items))):
            if best_value(i + 1, weight_limit) > best_value(i, weight_limit):
                # better with the i-th item
                result.append(items[i])  # include it in the result
                weight_limit -= items[i].weight_value
        return result

    def solution(self, time_remains=None):
        """
        Метод, который запускает решение задачи о рюкзаке. Так как метод solve_problem не гарантирует, что ответ будет
        корректный (так как в него на вход поступают задачи, дедлайн которых раньше, чем final_date). Метод обрабатывает результат solve_problem,
        и удаляет те задачи, которые были выбраны, но которые никак не получается решить. Метод оставляет выбранные задачи, которые можно решить,
        и запускает снова solve_problem. Аналогично обрабатывает результат. Процесс повторяется до тех пор,
        пока solve_problem хотя-бы что-то возвращает.
        :param time_remains:
        :return can_be_done - оптимальный выбор задач:
        """
        if time_remains is None:
            time_remains = self.calculate_free_time(self.final_date)
        result = sorted(self.solve_problem(self.tasks, time_remains), key=lambda x: x.utility_value / x.weight_value,
                        reverse=True)
        if len(result) == 0:
            return []

        can_be_done = []
        can_not_be_done = []
        for task in result:
            time_to_do_task = self.calculate_free_time(datetime.strptime(task.deadline, '%d.%m.%Y').date())
            if time_remains - task.weight_value >= 0 and task.weight_value <= time_to_do_task:
                time_remains -= task.weight_value
                can_be_done.append(task)
            else:
                can_not_be_done.append(task.Task_name)

        new_tasks = []
        for elem in self.tasks:
            if not (elem in can_not_be_done or elem in can_be_done):
                new_tasks.append(elem)
        self.tasks = new_tasks
        return can_be_done + self.solution(time_remains)
