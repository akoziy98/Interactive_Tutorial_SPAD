import task_2_2
import math


def test_get_square_number():
    a_list = [10, 10.5555, -10]
    true_return = [get_square_number(el) for el in a_list]
    check_return = [task_2_2.get_square_number(el) for el in a_list]

    if check_return[0] is None:
        assert False, "You don't solve this task"
    else:
        assert true_return == check_return, (
            f"test set: {a_list}. "
            f"True return: {true_return}. "
            f"Your return: {check_return}")


def test_hello_function():
    names_list = ["Alice", "Ivan", "Alice and Ivan"]
    true_return = [hello_function(el) for el in names_list]
    check_return = [task_2_2.hello_function(el) for el in names_list]

    if check_return[0] is None:
        assert False, "You don't solve this task"
    else:
        assert true_return == check_return, (
            f"test set: {names_list}. "
            f"True return: {true_return}. "
            f"Your return: {check_return}")


def test_area_rectangular_room():
    length_list = [10, -10, 10.1231]
    width_list = [5, 5, 5.1235443]

    true_return = [area_rectangular_room(length_list[i], width_list[i])
                   for i in range(len(length_list))]
    check_return = [task_2_2.area_rectangular_room(length_list[i], width_list[i])
                    for i in range(len(length_list))]

    if check_return[0] is None:
        assert False, "You don't solve this task"
    else:
        assert true_return == check_return, (
            f"test set: length = {length_list}, width = {width_list}. "
            f"True return: {true_return}. "
            f"Your return: {check_return}")


def test_compound_interest():
    value_list = [1000, 10, 1000.1231]
    a_list = [0.1, 0.143214, 0.13]

    true_return = [compound_interest(value_list[i], a_list[i]) for i in range(len(value_list))]
    check_return = [task_2_2.compound_interest(value_list[i], a_list[i]) for i in range(len(value_list))]

    if check_return[0] is None:
        assert False, "You don't solve this task"
    else:
        assert true_return == check_return, (
            f"test set: values = {value_list}, a = {a_list}. "
            f"True return: {true_return}. "
            f"Your return: {check_return}")


def test_earth_distance_between_points():
    t1_list = [100, 10, 1000.1231]
    t2_list = [13.2, 53.12, 178.2]
    g1_list = [43.23, 23.21, 12.6]
    g2_list = [31.11, 11.76, 66.321]


    true_return = [earth_distance_between_points(t1_list[i], t2_list[i], g1_list[i], g2_list[i])
                   for i in range(len(t1_list))]
    check_return = [task_2_2.earth_distance_between_points(t1_list[i], t2_list[i], g1_list[i], g2_list[i])
                    for i in range(len(t1_list))]

    if check_return[0] is None:
        assert False, "You don't solve this task"
    else:
        assert true_return == check_return, (
            f"test set: t1 = {t1_list}, t2 = {t2_list}, g1 = {g1_list}, g2 = {g2_list}. "
            f"True return: {true_return}. "
            f"Your return: {check_return}")


def test_free_fall_time():
    v_list = [0, 10, -10]
    h_list = [10, 50, 100]

    true_return = [free_fall_time(v_list[i], h_list[i]) for i in range(len(h_list))]
    check_return = [task_2_2.free_fall_time(v_list[i], h_list[i]) for i in range(len(h_list))]

    if check_return[0] is None:
        assert False, "You don't solve this task"
    else:
        assert true_return == check_return, (
            f"test set: v_list = {v_list}, h_list = {h_list}. "
            f"True return: {true_return}. "
            f"Your return: {check_return}")


def test_sum_of_digits():
    number = [3141, 1001, 9932]
    true_return = [sum_of_digits(el) for el in number]
    check_return = [task_2_2.sum_of_digits(el) for el in number]

    if check_return[0] is None:
        assert False, "You don't solve this task"
    else:
        assert true_return == check_return, (
            f"test set: {number}. "
            f"True return: {true_return}. "
            f"Your return: {check_return}")


def test_yesterday_bread():
    cost_list = [100, 150.5431, 1000.1231]
    a_list = [0.132, 0.1232, 0.1782]
    n_list = [10, 5, 100]


    true_return = [yesterday_bread(cost_list[i], a_list[i], n_list[i])
                   for i in range(len(cost_list))]
    check_return = [task_2_2.yesterday_bread(cost_list[i], a_list[i], n_list[i])
                    for i in range(len(cost_list))]

    if check_return[0] is None:
        assert False, "You don't solve this task"
    else:
        assert true_return == check_return, (
            f"test set: cost = {cost_list}, a = {a_list}, n = {n_list}. "
            f"True return: {true_return}. "
            f"Your return: {check_return}")



#Function defining section
def get_square_number(a : float) -> float:
    # TODO: реалзиуйте возведение числа a в квадрат
    a_square = a * a
    return round(a_square, 2)


def hello_function(name : str) -> str:
    #TODO: реализуйте приветствие человека с именеем name. Пример ожидаемый выход: "Hello name, glad to see you!"
    hello_str = f"Hello {name}, glad to see you!"
    return hello_str


def area_rectangular_room(length : float, width : float) -> float:
    #TODO: реализуйте вычисление площади комнаты с параметрами length и width
    return round(length * width, 1)


def compound_interest(value : float, a : float) -> float:
    #TODO: реалзизуйте вычисление сложного процента
    n = [1, 2, 3]
    money = [round(value * (1 + a) ** (el), 2) for el in n]
    return money


def earth_distance_between_points(t1: float, g1: float, t2 : float, g2 : float) -> float:
    #TODO: Найдите расстояние между точками с координатами (t1, g1) и (t2, g2) на поверхности земли
    R = 6371.01
    return round(R * (math.acos( math.sin(math.radians(t1)) * math.sin(math.radians(t2)) +
                           math.cos(math.radians(t1)) * math.cos(math.radians(t2)) *
                           math.cos(math.radians(g1 - g2)))), 2)


def free_fall_time(v : float, h : float) -> float:
    #TODO: Найдите время до соприкосновения объекта с землей
    G = 9.8
    return round((-v + math.sqrt(v ** 2 + 2 * G * h)) / G, 2)


def sum_of_digits(number : int) -> int:
    #TODO: вычислите сумму цифр четырехзначного числа number
    number_str = str(number)
    dig_count = 0
    for el in number_str:
        dig_count += int(el)
    return dig_count


def yesterday_bread(cost : float, a : float, n : float) -> [float, float, float, float]:
    #TODO:  Функция должна возвращать три величины: обычная цена за буханку,
    # цена со скидкой, общая стоимость приобретенного хлеба, если бы скидки не было
    # и общая стоимость приобретенного хлеба с учетом скидки.
    return [round(cost), round(cost * (1 - a)), round(cost * n), round((1 - a) * cost * n)]