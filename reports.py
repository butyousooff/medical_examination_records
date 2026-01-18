def count_healthy_reports(child):
    """Подсчитывает количество заключений 'здоров' у воспитанника"""
    conclusions = child[6:10]
    return sum(1 for conclusion in conclusions if conclusion == "здоров")


def selection_sort(children, key_func, reverse=False):
    """
    Сортировка выбором для списка воспитанников
    children: список записей
    key_func: функция для получения ключа сортировки
    reverse: True для сортировки по убыванию, False для возрастания
    """
    sorted_children = children.copy()
    for i in range(len(sorted_children)):
        extreme_index = i
        for j in range(i + 1, len(sorted_children)):
            current_key = key_func(sorted_children[j])
            extreme_key = key_func(sorted_children[extreme_index])
            if reverse:
                if current_key > extreme_key:
                    extreme_index = j
            else:
                if current_key < extreme_key:
                    extreme_index = j
        if extreme_index != i:
            sorted_children[i], sorted_children[extreme_index] = sorted_children[extreme_index], sorted_children[i]
    return sorted_children


def multi_key_selection_sort(children, key_funcs, reverse_flags):
    """
    Многоуровневая сортировка выбором
    key_funcs: список функций для получения ключей
    reverse_flags: список флагов направления сортировки
    """
    sorted_children = children.copy()
    for i in range(len(sorted_children)):
        extreme_index = i
        for j in range(i + 1, len(sorted_children)):
            for k in range(len(key_funcs)):
                key_func = key_funcs[k]
                reverse = reverse_flags[k]
                current_key = key_func(sorted_children[j])
                extreme_key = key_func(sorted_children[extreme_index])
                if reverse:
                    if current_key > extreme_key:
                        extreme_index = j
                        break
                    elif current_key < extreme_key:
                        break
                else:
                    if current_key < extreme_key:
                        extreme_index = j
                        break
                    elif current_key > extreme_key:
                        break
            else:
                continue
        if extreme_index != i:
            sorted_children[i], sorted_children[extreme_index] = sorted_children[extreme_index], sorted_children[i]
    return sorted_children


def report_all_children(children):
    """Отчет 1: Полный список всех детей"""
    key_funcs = [
        lambda x: count_healthy_reports(x),
        lambda x: x[0].lower()
    ]
    reverse_flags = [True, False]
    return multi_key_selection_sort(children, key_funcs, reverse_flags)


def report_by_group(children, group_name):
    """Отчет 2: Список детей заданной группы"""
    group_children = [child.copy() for child in children if child[5].lower() == group_name.lower()]
    if not group_children:
        return []
    key_funcs = [
        lambda x: x[2],
        lambda x: x[3],
        lambda x: x[4]
    ]
    reverse_flags = [False, False, False]
    return multi_key_selection_sort(group_children, key_funcs, reverse_flags)


def report_needs_treatment(children):
    """Отчет 3: Список детей, нуждающихся в лечении"""
    treatment_children = []
    for child in children:
        conclusions = child[6:10]
        if any(conclusion == "нуждается в лечении" for conclusion in conclusions):
            treatment_children.append(child.copy())
    if not treatment_children:
        return []
    key_funcs = [
        lambda x: x[5].lower(),
        lambda x: x[0].lower()
    ]
    reverse_flags = [False, False]
    return multi_key_selection_sort(treatment_children, key_funcs, reverse_flags)
