from typing import Generic, TypeVar, Optional, List, Dict, Tuple

T = TypeVar('T')

# ==================== ООП РЕАЛИЗАЦИЯ ====================

class Queue(Generic[T]):
    """Очередь FIFO (First-In-First-Out) - ООП стиль"""
    
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def enqueue(self, item: T) -> None:
        """Добавить элемент в конец очереди"""
        self.items.append(item)
    
    def dequeue(self) -> Optional[T]:
        """Удалить и вернуть первый элемент"""
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def peek(self) -> Optional[T]:
        """Посмотреть первый элемент без удаления"""
        if self.is_empty():
            return None
        return self.items[0]
    
    def is_empty(self) -> bool:
        """Проверить, пуста ли очередь"""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Получить размер очереди"""
        return len(self.items)
    
    def __str__(self) -> str:
        return f"Queue({self.items})"


class Stack(Generic[T]):
    """Стек LIFO (Last-In-First-Out) - ООП стиль"""
    
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        """Добавить элемент на вершину стека"""
        self.items.append(item)
    
    def pop(self) -> Optional[T]:
        """Удалить и вернуть верхний элемент"""
        if self.is_empty():
            return None
        return self.items.pop()
    
    def peek(self) -> Optional[T]:
        """Посмотреть верхний элемент без удаления"""
        if self.is_empty():
            return None
        return self.items[-1]
    
    def is_empty(self) -> bool:
        """Проверить, пуст ли стек"""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Получить размер стека"""
        return len(self.items)
    
    def __str__(self) -> str:
        return f"Stack({self.items})"


# ==================== ФУНКЦИОНАЛЬНАЯ РЕАЛИЗАЦИЯ ====================

# Типы данных для функционального стиля
QueueDict = Dict[str, List[T]]
StackDict = Dict[str, List[T]]

# ---------- Функции для работы с очередью ----------

def create_queue() -> QueueDict[T]:
    """Создать новую пустую очередь - функциональный стиль"""
    return {"items": []}

def queue_enqueue(queue: QueueDict[T], item: T) -> QueueDict[T]:
    """Добавить элемент в конец очереди"""
    new_items = queue["items"].copy()  # Создаем копию для иммутабельности
    new_items.append(item)
    return {"items": new_items}

def queue_dequeue(queue: QueueDict[T]) -> Tuple[Optional[T], QueueDict[T]]:
    """Удалить и вернуть первый элемент из очереди"""
    if len(queue["items"]) == 0:
        return None, queue
    
    new_items = queue["items"].copy()
    item = new_items.pop(0)
    return item, {"items": new_items}

def queue_peek(queue: QueueDict[T]) -> Optional[T]:
    """Посмотреть первый элемент без удаления"""
    if len(queue["items"]) == 0:
        return None
    return queue["items"][0]

def queue_is_empty(queue: QueueDict[T]) -> bool:
    """Проверить, пуста ли очередь"""
    return len(queue["items"]) == 0

def queue_size(queue: QueueDict[T]) -> int:
    """Получить размер очереди"""
    return len(queue["items"])

def queue_to_string(queue: QueueDict[T]) -> str:
    """Представить очередь в виде строки"""
    return f"Queue({queue['items']})"

# ---------- Функции для работы со стеком ----------

def create_stack() -> StackDict[T]:
    """Создать новый пустой стек - функциональный стиль"""
    return {"items": []}

def stack_push(stack: StackDict[T], item: T) -> StackDict[T]:
    """Добавить элемент на вершину стека"""
    new_items = stack["items"].copy()  # Создаем копию для иммутабельности
    new_items.append(item)
    return {"items": new_items}

def stack_pop(stack: StackDict[T]) -> Tuple[Optional[T], StackDict[T]]:
    """Удалить и вернуть верхний элемент стека"""
    if len(stack["items"]) == 0:
        return None, stack
    
    new_items = stack["items"].copy()
    item = new_items.pop()
    return item, {"items": new_items}

def stack_peek(stack: StackDict[T]) -> Optional[T]:
    """Посмотреть верхний элемент без удаления"""
    if len(stack["items"]) == 0:
        return None
    return stack["items"][-1]

def stack_is_empty(stack: StackDict[T]) -> bool:
    """Проверить, пуст ли стек"""
    return len(stack["items"]) == 0

def stack_size(stack: StackDict[T]) -> int:
    """Получить размер стека"""
    return len(stack["items"])

def stack_to_string(stack: StackDict[T]) -> str:
    """Представить стек в виде строки"""
    return f"Stack({stack['items']})"


# ==================== ДЕМОНСТРАЦИЯ И СРАВНЕНИЕ ====================

def print_separator(title: str) -> None:
    """Напечатать разделитель"""
    print("\n" + "="*50)
    print(f" {title} ")
    print("="*50)

def demonstrate_oop() -> None:
    """Демонстрация ООП подхода"""
    print_separator("ООП ПОДХОД")
    
    print("1. ОЧЕРЕДЬ (FIFO):")
    q = Queue[int]()
    print(f"Создана пустая очередь: {q}")
    print(f"Очередь пуста? {q.is_empty()}")
    
    # Добавляем элементы
    for i in [10, 20, 30]:
        q.enqueue(i)
        print(f"Добавили {i}: {q}")
    
    print(f"\nПервый элемент (peek): {q.peek()}")
    print(f"Размер очереди: {q.size()}")
    
    # Извлекаем элементы
    print("\nИзвлечение элементов:")
    while not q.is_empty():
        item = q.dequeue()
        print(f"Извлекли {item}: {q}")
    
    print("\n2. СТЕК (LIFO):")
    s = Stack[str]()
    print(f"Создан пустой стек: {s}")
    
    # Добавляем элементы
    for char in ['A', 'B', 'C']:
        s.push(char)
        print(f"Добавили '{char}': {s}")
    
    print(f"\nВерхний элемент (peek): {s.peek()}")
    print(f"Размер стека: {s.size()}")
    
    # Извлекаем элементы
    print("\nИзвлечение элементов:")
    while not s.is_empty():
        item = s.pop()
        print(f"Извлекли '{item}': {s}")

def demonstrate_functional() -> None:
    """Демонстрация функционального подхода"""
    print_separator("ФУНКЦИОНАЛЬНЫЙ ПОДХОД")
    
    print("1. ОЧЕРЕДЬ (FIFO):")
    q = create_queue()
    print(f"Создана пустая очередь: {queue_to_string(q)}")
    print(f"Очередь пуста? {queue_is_empty(q)}")
    
    # Добавляем элементы (создаем новые очереди)
    q = queue_enqueue(q, 10)
    print(f"Добавили 10: {queue_to_string(q)}")
    q = queue_enqueue(q, 20)
    print(f"Добавили 20: {queue_to_string(q)}")
    q = queue_enqueue(q, 30)
    print(f"Добавили 30: {queue_to_string(q)}")
    
    print(f"\nПервый элемент (peek): {queue_peek(q)}")
    print(f"Размер очереди: {queue_size(q)}")
    
    # Извлекаем элементы
    print("\nИзвлечение элементов:")
    while not queue_is_empty(q):
        item, q = queue_dequeue(q)
        print(f"Извлекли {item}: {queue_to_string(q)}")
    
    print("\n2. СТЕК (LIFO):")
    s = create_stack()
    print(f"Создан пустой стек: {stack_to_string(s)}")
    
    # Добавляем элементы
    s = stack_push(s, 'X')
    print(f"Добавили 'X': {stack_to_string(s)}")
    s = stack_push(s, 'Y')
    print(f"Добавили 'Y': {stack_to_string(s)}")
    s = stack_push(s, 'Z')
    print(f"Добавили 'Z': {stack_to_string(s)}")
    
    print(f"\nВерхний элемент (peek): {stack_peek(s)}")
    print(f"Размер стека: {stack_size(s)}")
    
    # Извлекаем элементы
    print("\nИзвлечение элементов:")
    while not stack_is_empty(s):
        item, s = stack_pop(s)
        print(f"Извлекли '{item}': {stack_to_string(s)}")

def compare_approaches() -> None:
    """Сравнение двух подходов на одном примере"""
    print_separator("СРАВНЕНИЕ ПОДХОДОВ")
    
    data = [1, 2, 3, 4, 5]
    
    print("Задача: добавить числа [1, 2, 3, 4, 5] и извлечь три элемента")
    
    # ООП подход
    print("\n--- ООП подход ---")
    oop_queue = Queue[int]()
    for num in data:
        oop_queue.enqueue(num)
    print(f"После добавления всех чисел: {oop_queue}")
    
    results = []
    for _ in range(3):
        results.append(oop_queue.dequeue())
    print(f"Извлекли три элемента: {results}")
    print(f"Осталось в очереди: {oop_queue}")
    
    # Функциональный подход
    print("\n--- Функциональный подход ---")
    fp_queue = create_queue()
    for num in data:
        fp_queue = queue_enqueue(fp_queue, num)
    print(f"После добавления всех чисел: {queue_to_string(fp_queue)}")
    
    results = []
    current_queue = fp_queue
    for _ in range(3):
        item, current_queue = queue_dequeue(current_queue)
        results.append(item)
    print(f"Извлекли три элемента: {results}")
    print(f"Осталось в очереди: {queue_to_string(current_queue)}")
    
    print("\n" + "-"*40)
    print("КЛЮЧЕВЫЕ ОТЛИЧИЯ:")
    print("-"*40)
    print("1. ООП: методы работают с объектом (изменяют его состояние)")
    print("2. ФП: функции возвращают новые структуры (старые не меняются)")
    print("3. ООП: queue.enqueue(5) - добавляет в существующую очередь")
    print("4. ФП: queue = queue_enqueue(queue, 5) - создает новую очередь")
    print("5. ООП: естественная инкапсуляция (данные внутри объекта)")
    print("6. ФП: данные явно передаются в функции")


   

def main() -> None:
    """Главная функция программы"""
    print("ЛАБОРАТОРНАЯ РАБОТА: РЕАЛИЗАЦИЯ QUEUE И STACK")
    print("В ООП И ФУНКЦИОНАЛЬНОМ СТИЛЕ")
    
    demonstrate_oop()
    demonstrate_functional()
    compare_approaches()
    
    print_separator("ЗАВЕРШЕНИЕ")
    print("Программа демонстрирует разницу между:")
    print("1. ООП - с классами, методами и состоянием объектов")
    print("2. Функциональным стилем - с функциями и иммутабельными данными")

if __name__ == "__main__":
    main()
1