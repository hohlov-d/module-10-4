from threading import Thread
import queue
import time
from random import randint


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(randint(3, 10))


class Cafe:
    def __init__(self, *args):
        self.queve = queue.Queue()
        self.tables = args

    def guest_arrival(self, *args):
        guests = args
        for i in guests:
            flag = True
            for j in self.tables:
                if j.guest is None:
                    j.guest = i
                    i.start()
                    print(f'{i.name} сел(-а) за стол номер {j.number}')
                    flag = False
                    break
            if flag:
                self.queve.put(i)
                print(f'{i.name} в очереди')

    def discuss_guests(self):
        while not self.queve.empty() or any(j.guest is not None for j in self.tables):
            for j in self.tables:
                if j.guest is not None and j.guest.is_alive():
                    print(f'{j.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {j.number} свободен')
                    j.guest = None
                if not self.queve.empty():
                    j.guest = self.queve.get()
                    print(f'{j.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {j.number}>')
                    j.guest.start()


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
