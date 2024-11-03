from threading import Thread, Lock
from random import randint
from time import sleep
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    lock = Lock()
    queue = Queue()

    def __init__(self, *tables):
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            self.lock.acquire()
            assigned = False
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    table.guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    assigned = True
                    break
            if not assigned:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')
            self.lock.release()

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None

            for table in self.tables:
                if self.queue.empty():
                    break
                if table.guest is None:
                    guest = self.queue.get()
                    table.guest = guest
                    print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    table.guest.start()


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
                'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
