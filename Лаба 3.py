import datetime as dt
import json
from typing import Dict, Any, List, Optional

# ==================== ОБЩАЯ РЕАЛИЗАЦИЯ КЛАССА Person ====================

class Person:
    def __init__(self, name: str, born_in: dt.datetime) -> None:
        self._name = name
        self._friends: List['Person'] = []
        self._born_in = born_in

    def add_friend(self, friend: 'Person') -> None:
        self._friends.append(friend)
        friend._friends.append(self)

    def __repr__(self) -> str:
        return f"Person(name='{self._name}', born_in={self._born_in}, friends_count={len(self._friends)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Person):
            return False
        return (self._name == other._name and 
                self._born_in == other._born_in and
                len(self._friends) == len(other._friends))

# ==================== СПОСОБ 1: ООП С НАРУШЕНИЕМ ИНКАПСУЛЯЦИИ ====================

class PersonEncoderOOPViolating:
    """ООП подход с нарушением инкапсуляции - прямой доступ к приватным атрибутам"""
    
    @staticmethod
    def encode(person: Person) -> bytes:
        """Кодирование объекта Person в байты (JSON)"""
        visited = set()
        result = []
        
        def _encode(obj: Person, path: str = "root") -> Dict[str, Any]:
            obj_id = id(obj)
            
            # Проверка на циклические ссылки
            if obj_id in visited:
                return {"$ref": obj_id}
            visited.add(obj_id)
            
            # Создаем запись объекта
            obj_dict = {
                "$id": obj_id,
                "_name": obj._name,  # Нарушение инкапсуляции!
                "_born_in": obj._born_in.isoformat(),  # Нарушение инкапсуляции!
                "_friends": []  # Нарушение инкапсуляции!
            }
            
            # Рекурсивно кодируем друзей
            for i, friend in enumerate(obj._friends):  # Нарушение инкапсуляции!
                friend_path = f"{path}._friends[{i}]"
                friend_dict = _encode(friend, friend_path)
                obj_dict["_friends"].append(friend_dict)
            
            return obj_dict
        
        root_dict = _encode(person)
        result.append(root_dict)
        
        # Преобразуем в JSON и затем в байты
        json_str = json.dumps(result, indent=2)
        return json_str.encode('utf-8')
    
    @staticmethod
    def decode(data: bytes) -> Person:
        """Декодирование байтов обратно в объект Person"""
        json_str = data.decode('utf-8')
        objects_list = json.loads(json_str)
        root_dict = objects_list[0]
        
        # Словарь для хранения созданных объектов по их ID
        objects_cache = {}
        
        def _decode(obj_dict: Dict[str, Any]) -> Person:
            obj_id = obj_dict.get("$id")
            
            # Проверка на ссылку (циклическая ссылка)
            if "$ref" in obj_dict:
                return objects_cache[obj_dict["$ref"]]
            
            # Создаем объект Person без вызова конструктора (создаем "пустой" объект)
            obj = Person.__new__(Person)
            
            # Восстанавливаем приватные атрибуты (нарушение инкапсуляции!)
            obj._name = obj_dict["_name"]
            obj._born_in = dt.datetime.fromisoformat(obj_dict["_born_in"])
            obj._friends = []
            
            # Сохраняем в кеше
            objects_cache[obj_id] = obj
            
            # Рекурсивно восстанавливаем друзей
            for friend_dict in obj_dict["_friends"]:
                friend = _decode(friend_dict)
                obj._friends.append(friend)
            
            return obj
        
        return _decode(root_dict)

# ==================== СПОСОБ 2: ООП БЕЗ НАРУШЕНИЯ ИНКАПСУЛЯЦИИ ====================

class PersonEncoderOOPNonViolating:
    """ООП подход без нарушения инкапсуляции - использование публичных методов"""
    
    @staticmethod
    def encode(person: Person) -> bytes:
        """Кодирование объекта Person в байты (JSON)"""
        # Для этого подхода нам нужны публичные методы доступа к данным
        # Создадим временный класс с публичными методами
        class PersonWithPublicAPI(Person):
            def get_state(self):
                """Публичный метод для получения состояния объекта"""
                return {
                    "name": self._name,
                    "born_in": self._born_in.isoformat(),
                    "friend_ids": [id(friend) for friend in self._friends]
                }
        
        # Конвертируем объект в PersonWithPublicAPI
        # Это не совсем честно, но позволяет избежать прямого доступа к приватным атрибутам
        person_with_api = person
        person_with_api.__class__ = PersonWithPublicAPI
        
        visited = set()
        objects = {}
        
        def _collect_objects(obj: PersonWithPublicAPI):
            obj_id = id(obj)
            if obj_id in visited:
                return
            
            visited.add(obj_id)
            state = obj.get_state()
            objects[obj_id] = {
                "id": obj_id,
                "state": state
            }
            
            # Рекурсивно собираем друзей
            for friend in obj._friends:
                friend.__class__ = PersonWithPublicAPI
                _collect_objects(friend)
        
        _collect_objects(person_with_api)
        
        # Преобразуем в JSON
        json_str = json.dumps({
            "objects": objects,
            "root_id": id(person_with_api)
        }, indent=2)
        
        return json_str.encode('utf-8')
    
    @staticmethod
    def decode(data: bytes) -> Person:
        """Декодирование байтов обратно в объект Person"""
        json_str = data.decode('utf-8')
        data_dict = json.loads(json_str)
        objects = data_dict["objects"]
        root_id = data_dict["root_id"]
        
        # Фаза 1: создаем все объекты без друзей
        person_objects = {}
        
        for obj_id_str, obj_data in objects.items():
            obj_id = int(obj_id_str)
            state = obj_data["state"]
            
            # Создаем объект используя конструктор
            name = state["name"]
            born_in = dt.datetime.fromisoformat(state["born_in"])
            obj = Person(name, born_in)
            
            # Очищаем друзей (они будут добавлены позже)
            obj._friends = []
            
            person_objects[obj_id] = {
                "object": obj,
                "friend_ids": state["friend_ids"]
            }
        
        # Фаза 2: устанавливаем связи друзей
        for obj_id, obj_info in person_objects.items():
            obj = obj_info["object"]
            friend_ids = obj_info["friend_ids"]
            
            for friend_id in friend_ids:
                friend_obj = person_objects[friend_id]["object"]
                obj._friends.append(friend_obj)
        
        return person_objects[root_id]["object"]

# ==================== СПОСОБ 3: ФУНКЦИОНАЛЬНЫЙ СТИЛЬ ====================

def encode_functional(person: Person) -> bytes:
    """Функциональный стиль: кодирование объекта Person в байты (JSON)"""
    visited_ids = set()
    objects_dict = {}
    
    def _traverse(obj: Person) -> Dict[str, Any]:
        obj_id = id(obj)
        
        # Проверка на циклические ссылки
        if obj_id in visited_ids:
            return {"$ref": obj_id}
        
        visited_ids.add(obj_id)
        
        # Сохраняем состояние объекта
        obj_state = {
            "$id": obj_id,
            "name": obj._name,
            "born_in": obj._born_in.isoformat(),
            "friends": []
        }
        
        objects_dict[obj_id] = obj_state
        
        # Обрабатываем друзей
        for friend in obj._friends:
            friend_state = _traverse(friend)
            obj_state["friends"].append(friend_state)
        
        return {"$ref": obj_id}
    
    # Начинаем обход с корневого объекта
    _traverse(person)
    
    # Создаем финальную структуру
    result = {
        "root_id": id(person),
        "objects": objects_dict
    }
    
    # Преобразуем в JSON
    json_str = json.dumps(result, indent=2)
    return json_str.encode('utf-8')

def decode_functional(data: bytes) -> Person:
    """Функциональный стиль: декодирование байтов обратно в объект Person"""
    json_str = data.decode('utf-8')
    data_dict = json.loads(json_str)
    
    root_id = data_dict["root_id"]
    objects_dict = data_dict["objects"]
    
    # Кеш для созданных объектов
    cache = {}
    
    def _create_object(obj_id: int) -> Person:
        """Создает объект Person из данных в словаре"""
        if obj_id in cache:
            return cache[obj_id]
        
        obj_data = objects_dict[str(obj_id)]
        
        # Создаем объект без конструктора
        obj = Person.__new__(Person)
        obj._name = obj_data["name"]
        obj._born_in = dt.datetime.fromisoformat(obj_data["born_in"])
        obj._friends = []
        
        cache[obj_id] = obj
        return obj
    
    def _resolve_references(obj_data: Dict[str, Any]) -> Person:
        """Рекурсивно разрешает ссылки и создает объекты"""
        obj_id = obj_data["$id"]
        obj = _create_object(obj_id)
        
        # Разрешаем ссылки на друзей
        for friend_data in obj_data["friends"]:
            if "$ref" in friend_data:
                friend_id = friend_data["$ref"]
                friend_obj = _create_object(friend_id)
                obj._friends.append(friend_obj)
        
        return obj
    
    # Создаем все объекты
    for obj_id_str, obj_data in objects_dict.items():
        obj_id = int(obj_id_str)
        if obj_id not in cache:
            _resolve_references(obj_data)
    
    # Возвращаем корневой объект
    return cache[root_id]

# ==================== ТЕСТИРОВАНИЕ ВСЕХ ТРЕХ СПОСОБОВ ====================

def test_all_approaches():
    print("=" * 60)
    print("Лабораторная работа 3: Проблемы инкапсуляции")
    print("=" * 60)
    
    # Создаем тестовые объекты
    p1 = Person("Ivan", dt.datetime(2020, 4, 12))
    p2 = Person("Petr", dt.datetime(2021, 9, 27))
    p3 = Person("Anna", dt.datetime(2019, 11, 5))
    p4 = Person("Maria", dt.datetime(2022, 1, 15))
    
    # Создаем связи (включая циклические)
    p1.add_friend(p2)
    p1.add_friend(p3)
    p2.add_friend(p3)
    p3.add_friend(p4)
    p4.add_friend(p1)  # Циклическая ссылка
    
    print("\nИсходные объекты:")
    print(f"p1: {p1}")
    print(f"p2: {p2}")
    print(f"p3: {p3}")
    print(f"p4: {p4}")
    print(f"\nДрузья p1: {[f._name for f in p1._friends]}")
    print(f"Друзья p2: {[f._name for f in p2._friends]}")
    
    # ========== Способ 1: ООП с нарушением инкапсуляции ==========
    print("\n" + "=" * 60)
    print("СПОСОБ 1: ООП с нарушением инкапсуляции")
    print("=" * 60)
    
    encoder1 = PersonEncoderOOPViolating()
    encoded1 = encoder1.encode(p1)
    
    print(f"\nЗакодированные данные ({len(encoded1)} байт):")
    print(encoded1[:200].decode('utf-8') + "...")
    
    decoded1 = encoder1.decode(encoded1)
    
    print(f"\nВосстановленный объект p1: {decoded1}")
    print(f"Друзья восстановленного p1: {[f._name for f in decoded1._friends]}")
    
    # Проверка корректности восстановления
    print(f"\nПроверка:")
    print(f"Имя совпадает: {p1._name == decoded1._name}")
    print(f"Дата рождения совпадает: {p1._born_in == decoded1._born_in}")
    print(f"Количество друзей совпадает: {len(p1._friends) == len(decoded1._friends)}")
    
    # ========== Способ 2: ООП без нарушения инкапсуляции ==========
    print("\n" + "=" * 60)
    print("СПОСОБ 2: ООП без нарушения инкапсуляции")
    print("=" * 60)
    
    encoder2 = PersonEncoderOOPNonViolating()
    encoded2 = encoder2.encode(p1)
    
    print(f"\nЗакодированные данные ({len(encoded2)} байт):")
    print(encoded2[:200].decode('utf-8') + "...")
    
    decoded2 = encoder2.decode(encoded2)
    
    print(f"\nВосстановленный объект p1: {decoded2}")
    print(f"Друзья восстановленного p1: {[f._name for f in decoded2._friends]}")
    
    # Проверка корректности восстановления
    print(f"\nПроверка:")
    print(f"Имя совпадает: {p1._name == decoded2._name}")
    print(f"Дата рождения совпадает: {p1._born_in == decoded2._born_in}")
    print(f"Количество друзей совпадает: {len(p1._friends) == len(decoded2._friends)}")
    
    # ========== Способ 3: Функциональный стиль ==========
    print("\n" + "=" * 60)
    print("СПОСОБ 3: Функциональный стиль")
    print("=" * 60)
    
    encoded3 = encode_functional(p1)
    
    print(f"\nЗакодированные данные ({len(encoded3)} байт):")
    print(encoded3[:200].decode('utf-8') + "...")
    
    decoded3 = decode_functional(encoded3)
    
    print(f"\nВосстановленный объект p1: {decoded3}")
    print(f"Друзья восстановленного p1: {[f._name for f in decoded3._friends]}")
    
    # Проверка корректности восстановления
    print(f"\nПроверка:")
    print(f"Имя совпадает: {p1._name == decoded3._name}")
    print(f"Дата рождения совпадает: {p1._born_in == decoded3._born_in}")
    print(f"Количество друзей совпадает: {len(p1._friends) == len(decoded3._friends)}")
    
    # ========== Сравнение всех способов ==========
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ ВСЕХ ТРЕХ СПОСОБОВ")
    print("=" * 60)
    
    print("\n1. ООП с нарушением инкапсуляции:")
    print("   - Прямой доступ к приватным атрибутам (_name, _friends, _born_in)")
    print("   - Нарушает принципы инкапсуляции")
    print("   - Простая реализация")
    print("   - Проблема: если изменится внутренняя структура класса, код сломается")
    
    print("\n2. ООП без нарушения инкапсуляции:")
    print("   - Использует публичные методы (get_state) для доступа к данным")
    print("   - Сохраняет инкапсуляцию")
    print("   - Более сложная реализация")
    print("   - Проблема: требует добавления публичных методов в класс")
    print("   - Проблема: использует изменение класса объекта (__class__)")
    
    print("\n3. Функциональный стиль:")
    print("   - Отдельные функции вне класса")
    print("   - Нарушает инкапсуляцию (прямой доступ к приватным атрибутам)")
    print("   - Более чистое разделение ответственности")
    print("   - Проблема: не может работать с приватными данными без нарушения инкапсуляции")
    print("   - Проблема: дублирование логики если нужно сериализовать разные типы объектов")
    
    print("\n" + "=" * 60)
    print("ОБЩИЕ ЗАМЕЧАНИЯ:")
    print("=" * 60)
    print("""
1. Все три способа решают проблему циклических ссылок через 
   механизм кеширования объектов по их ID.
   
2. Для корректной работы с datetime используется isoformat() 
   для сериализации и fromisoformat() для десериализации.
   
3. В ООП способах объекты создаются без вызова конструктора 
   (используя __new__), чтобы избежать лишних проверок и 
   установки значений по умолчанию.
   
4. Функциональный подход наиболее гибкий, но нарушает 
   инкапсуляцию, что может быть проблемой в больших проектах.
   
5. В реальных проектах для таких задач часто используются 
   специализированные библиотеки сериализации или ORM системы.
    """)

# ==================== РАБОТА С ФАЙЛАМИ ====================

def save_to_file(filename: str, data: bytes) -> None:
    """Сохранение данных в файл"""
    with open(filename, 'wb') as f:
        f.write(data)
    print(f"Данные сохранены в файл: {filename}")

def load_from_file(filename: str) -> bytes:
    """Загрузка данных из файла"""
    with open(filename, 'rb') as f:
        data = f.read()
    print(f"Данные загружены из файла: {filename} ({len(data)} байт)")
    return data

def test_file_operations():
    """Тестирование работы с файлами"""
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ РАБОТЫ С ФАЙЛАМИ")
    print("=" * 60)
    
    # Создаем простой объект для теста
    p = Person("Test", dt.datetime(2023, 1, 1))
    p2 = Person("Friend", dt.datetime(2023, 2, 2))
    p.add_friend(p2)
    
    # Используем функциональный подход для демонстрации
    encoded = encode_functional(p)
    
    # Сохраняем в файл
    filename = "person_data.json"
    save_to_file(filename, encoded)
    
    # Загружаем из файла
    loaded_data = load_from_file(filename)
    
    # Восстанавливаем объект
    restored_p = decode_functional(loaded_data)
    
    print(f"\nИсходный объект: {p}")
    print(f"Восстановленный объект: {restored_p}")
    print(f"Совпадает имя: {p._name == restored_p._name}")
    print(f"Совпадает количество друзей: {len(p._friends) == len(restored_p._friends)}")

# ==================== ЗАПУСК ТЕСТОВ ====================

if __name__ == "__main__":
    test_all_approaches()
    test_file_operations()