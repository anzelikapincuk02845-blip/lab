# ==================== ООП-СТИЛЬ ====================

class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
    
    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Матрицы должны быть одного размера")
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            result.append(row)
        return Matrix(result)
    
    def __mul__(self, other):
        # Умножение на скаляр
        if isinstance(other, (int, float)):
            result = []
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    row.append(self.data[i][j] * other)
                result.append(row)
            return Matrix(result)
        
        # Умножение матриц
        elif isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("Количество столбцов первой матрицы должно совпадать с количеством строк второй матрицы")
            
            result = []
            for i in range(self.rows):
                row = []
                for j in range(other.cols):
                    sum_val = 0
                    for k in range(self.cols):
                        sum_val += self.data[i][k] * other.data[k][j]
                    row.append(sum_val)
                result.append(row)
            return Matrix(result)
        
        else:
            raise TypeError("Неподдерживаемый тип операнда")
    
    def transpose(self):
        result = []
        for j in range(self.cols):
            row = []
            for i in range(self.rows):
                row.append(self.data[i][j])
            result.append(row)
        return Matrix(result)
    
    def determinant(self):
        if self.rows != self.cols:
            raise ValueError("Матрица должна быть квадратной")
        
        # Базовый случай для матрицы 1x1
        if self.rows == 1:
            return self.data[0][0]
        
        # Базовый случай для матрицы 2x2
        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        
        det = 0
        # Разложение по первой строке
        for j in range(self.cols):
            # Создаем минор
            minor = []
            for i in range(1, self.rows):
                row = []
                for k in range(self.cols):
                    if k != j:
                        row.append(self.data[i][k])
                minor.append(row)
            
            minor_matrix = Matrix(minor)
            det += ((-1) ** j) * self.data[0][j] * minor_matrix.determinant()
        
        return det
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.data])
    
    def __repr__(self):
        return f"Matrix({self.data})"


# ==================== ФУНКЦИОНАЛЬНЫЙ СТИЛЬ ====================

def create_matrix(data):
    """Создает матрицу из списка списков"""
    return data

def matrix_rows(matrix):
    """Возвращает количество строк матрицы"""
    return len(matrix)

def matrix_cols(matrix):
    """Возвращает количество столбцов матрицы"""
    return len(matrix[0]) if matrix else 0

def matrix_add(m1, m2):
    """Сложение матриц"""
    if matrix_rows(m1) != matrix_rows(m2) or matrix_cols(m1) != matrix_cols(m2):
        raise ValueError("Матрицы должны быть одного размера")
    
    result = []
    for i in range(matrix_rows(m1)):
        row = []
        for j in range(matrix_cols(m1)):
            row.append(m1[i][j] + m2[i][j])
        result.append(row)
    return result

def matrix_multiply(m1, m2):
    """Умножение матриц"""
    if matrix_cols(m1) != matrix_rows(m2):
        raise ValueError("Количество столбцов первой матрицы должно совпадать с количеством строк второй матрицы")
    
    result = []
    for i in range(matrix_rows(m1)):
        row = []
        for j in range(matrix_cols(m2)):
            sum_val = 0
            for k in range(matrix_cols(m1)):
                sum_val += m1[i][k] * m2[k][j]
            row.append(sum_val)
        result.append(row)
    return result

def scalar_multiply(matrix, scalar):
    """Умножение матрицы на скаляр"""
    result = []
    for i in range(matrix_rows(matrix)):
        row = []
        for j in range(matrix_cols(matrix)):
            row.append(matrix[i][j] * scalar)
        result.append(row)
    return result

def transpose(matrix):
    """Транспонирование матрицы"""
    result = []
    for j in range(matrix_cols(matrix)):
        row = []
        for i in range(matrix_rows(matrix)):
            row.append(matrix[i][j])
        result.append(row)
    return result

def determinant(matrix):
    """Вычисление определителя матрицы"""
    if matrix_rows(matrix) != matrix_cols(matrix):
        raise ValueError("Матрица должна быть квадратной")
    
    n = matrix_rows(matrix)
    
    # Базовый случай для матрицы 1x1
    if n == 1:
        return matrix[0][0]
    
    # Базовый случай для матрицы 2x2
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    # Разложение по первой строке
    for j in range(n):
        # Создаем минор
        minor = []
        for i in range(1, n):
            row = []
            for k in range(n):
                if k != j:
                    row.append(matrix[i][k])
            minor.append(row)
        
        det += ((-1) ** j) * matrix[0][j] * determinant(minor)
    
    return det

def print_matrix(matrix):
    """Печать матрицы"""
    for row in matrix:
        print(' '.join(map(str, row)))


# ==================== ТЕСТИРОВАНИЕ ОБОИХ СТИЛЕЙ ====================

def test_oop_style():
    print("=== ТЕСТИРОВАНИЕ ООП-СТИЛЯ ===")
    m1 = Matrix([[1, 2], [2, 3]])
    m2 = Matrix([[2, 5], [7, 9]])
    
    print("Матрица m1:")
    print(m1)
    print("\nМатрица m2:")
    print(m2)
    
    m3 = m1 + m2
    print("\nm1 + m2:")
    print(m3)
    
    m4 = m1 * m2
    print("\nm1 * m2:")
    print(m4)
    
    m5 = m1.transpose()
    print("\nТранспонированная m1:")
    print(m5)
    
    m6 = m1 * 3
    print("\nm1 * 3:")
    print(m6)
    
    det = m1.determinant()
    print(f"\nОпределитель m1: {det}")
    
    return m1, m2, m3, m4, m5, m6, det

def test_functional_style():
    print("\n\n=== ТЕСТИРОВАНИЕ ФУНКЦИОНАЛЬНОГО СТИЛЯ ===")
    m1 = create_matrix([[1, 2], [2, 3]])
    m2 = create_matrix([[2, 5], [7, 9]])
    
    print("Матрица m1:")
    print_matrix(m1)
    print("\nМатрица m2:")
    print_matrix(m2)
    
    m3 = matrix_add(m1, m2)
    print("\nm1 + m2:")
    print_matrix(m3)
    
    m4 = matrix_multiply(m1, m2)
    print("\nm1 * m2:")
    print_matrix(m4)
    
    m5 = transpose(m1)
    print("\nТранспонированная m1:")
    print_matrix(m5)
    
    m6 = scalar_multiply(m1, 3)
    print("\nm1 * 3:")
    print_matrix(m6)
    
    det = determinant(m1)
    print(f"\nОпределитель m1: {det}")
    
    return m1, m2, m3, m4, m5, m6, det

def compare_results(oop_results, func_results):
    print("\n\n=== СРАВНЕНИЕ РЕЗУЛЬТАТОВ ===")
    
    # Извлекаем результаты из кортежей
    oop_m1, oop_m2, oop_m3, oop_m4, oop_m5, oop_m6, oop_det = oop_results
    func_m1, func_m2, func_m3, func_m4, func_m5, func_m6, func_det = func_results
    
    # Сравниваем каждую операцию
    print("1. Сложение матриц:")
    print(f"   ООП-результат: {oop_m3.data}")
    print(f"   Функциональный результат: {func_m3}")
    print(f"   Результаты совпадают: {oop_m3.data == func_m3}")
    
    print("\n2. Умножение матриц:")
    print(f"   ООП-результат: {oop_m4.data}")
    print(f"   Функциональный результат: {func_m4}")
    print(f"   Результаты совпадают: {oop_m4.data == func_m4}")
    
    print("\n3. Транспонирование:")
    print(f"   ООП-результат: {oop_m5.data}")
    print(f"   Функциональный результат: {func_m5}")
    print(f"   Результаты совпадают: {oop_m5.data == func_m5}")
    
    print("\n4. Умножение на скаляр:")
    print(f"   ООП-результат: {oop_m6.data}")
    print(f"   Функциональный результат: {func_m6}")
    print(f"   Результаты совпадают: {oop_m6.data == func_m6}")
    
    print("\n5. Определитель:")
    print(f"   ООП-результат: {oop_det}")
    print(f"   Функциональный результат: {func_det}")
    print(f"   Результаты совпадают: {oop_det == func_det}")

def main():
    print("=" * 50)
    print("Лабораторная работа 2: Матрицы")
    print("Реализация в ООП и функциональном стиле")
    print("=" * 50)
    
    # Тестируем ООП-стиль
    oop_results = test_oop_style()
    
    # Тестируем функциональный стиль
    func_results = test_functional_style()
    
    # Сравниваем результаты
    compare_results(oop_results, func_results)
    
    # Дополнительный пример с матрицами 3x3
    print("\n\n" + "=" * 50)
    print("ДОПОЛНИТЕЛЬНЫЙ ПРИМЕР (матрицы 3x3):")
    print("=" * 50)
    
    # ООП-стиль
    print("\nООП-стиль:")
    m1_oop = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    m2_oop = Matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
    print(f"Матрица 1:\n{m1_oop}")
    print(f"\nМатрица 2:\n{m2_oop}")
    print(f"\nСумма:\n{m1_oop + m2_oop}")
    print(f"\nПроизведение:\n{m1_oop * m2_oop}")
    print(f"\nОпределитель матрицы 1: {m1_oop.determinant()}")
    
    # Функциональный стиль
    print("\nФункциональный стиль:")
    m1_func = create_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    m2_func = create_matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
    print("Матрица 1:")
    print_matrix(m1_func)
    print("\nМатрица 2:")
    print_matrix(m2_func)
    print("\nСумма:")
    print_matrix(matrix_add(m1_func, m2_func))
    print("\nПроизведение:")
    print_matrix(matrix_multiply(m1_func, m2_func))
    print(f"\nОпределитель матрицы 1: {determinant(m1_func)}")

if __name__ == "__main__":
    main()