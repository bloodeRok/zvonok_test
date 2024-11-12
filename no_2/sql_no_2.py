class Solution:
    def __row_is_valid(self, row: list[str]) -> bool:
        """
        Проверяет корректность строки с данными о сотруднике и часах работы.

        :param row: Список строк, в последнем элементы содержащем кол-во часов.
         До часов идут некоторые части ФИО.
        :return: True, если строка валидна (содержит хотя бы два элемента: имя
         и последний элемент — число), иначе False.
        """
        if len(row) < 2:
            print(f"Невалидная строка: {' '.join(row)}")
            return False

        if not row[-1].isdigit():
            print(f"Невалидное кол-во часов в строке: {' '.join(row)}")
            return False

        return True

    def print_workers_statistic(self, string: str) -> None:
        """
        Собирает и выводит статистику по рабочим часам сотрудников в формате:
                 - Имя сотрудника
                 - Перечень отработанных часов
                 - Общая сумма отработанных часов

        :param string: Текст, где каждая строка содержит имя сотрудника и число,
         представляющее отработанные часы.
        :return: None.
        """
        workers = {}
        for row in string.split("\n"):
            splitted_row = row.split(" ")

            if not self.__row_is_valid(row=splitted_row):
                continue

            name, hours = ' '.join(splitted_row[:-1]), splitted_row[-1]
            workers.setdefault(name, []).append(int(hours))

        for worker_name, worker_hours in workers.items():
            hours_str = ", ".join(map(str, worker_hours))
            print(f"{worker_name}: {hours_str}; sum: {sum(worker_hours)}")


test_string = """Андрей 9
Василий 11
Артём
Не написал тут часы
Роман 7
X Æ A-12 45
Иван Петров 3
Андрей 6
Роман 11"""

Solution().print_workers_statistic(string=test_string)
