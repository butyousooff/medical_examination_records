def print_header(title):
    """Выводит заголовок в консоли с разделителями"""
    print("\n" * 2)
    print("=" * 120)
    print(f"{title:^120}")
    print("=" * 120)


def display_children(records, title=""):
    """Отображает список воспитанников с форматированием"""
    if not records:
        print("\nВоспитанников не найдено")
        return
    print_header(title)
    print("№   Фамилия        Имя           Группа    Дата рождения   Заключения специалистов")
    print("-- --------------- -------------- --------- --------------- -----------------------")
    for i, record in enumerate(records, 1):
        surname, name, year, month, day, group, neuro, ent, ortho, ocul = record
        birth_date = f"{day:02d}.{month:02d}.{year}"
        healthy_count = 0
        for conclusion in [neuro, ent, ortho, ocul]:
            if conclusion == "здоров":
                healthy_count += 1
        healthy_status = f"{healthy_count} из 4 здоровы"
        surname_display = surname[:12] + ".." if len(surname) > 12 else surname.ljust(12)
        name_display = name[:12] + ".." if len(name) > 12 else name.ljust(12)
        group_display = group[:9] + ".." if len(group) > 9 else group.ljust(9)
        print(f"{i:<3} {surname_display:<15} {name_display:<14} {group_display:<10} {birth_date:<15} {healthy_status}")
    print("-" * 120)
    print(f"Всего воспитанников: {len(records)}")


def add_child(records):
    """Добавляет нового воспитанника в базу"""
    print_header("ДОБАВЛЕНИЕ НОВОГО ВОСПИТАННИКА")
    while True:
        surname = input("Фамилия ребёнка: ").strip()
        if surname:
            break
        print("Фамилия не может быть пустой")
    while True:
        name = input("Имя ребёнка: ").strip()
        if name:
            break
        print("Имя не может быть пустым")
    while True:
        try:
            year = int(input("Год рождения (2010-2020): "))
            if 2010 <= year <= 2020:
                break
            print("Год должен быть в диапазоне от 2010 до 2020")
        except ValueError:
            print("Введите корректное число")
    while True:
        try:
            month = int(input("Месяц рождения (1-12): "))
            if 1 <= month <= 12:
                break
            print("Месяц должен быть в диапазоне от 1 до 12")
        except ValueError:
            print("Введите корректное число")
    while True:
        try:
            day = int(input("День рождения (1-31): "))
            if 1 <= day <= 31:
                break
            print("День должен быть в диапазоне от 1 до 31")
        except ValueError:
            print("Введите корректное число")
    while True:
        group = input("Группа (младшая/средняя/старшая): ").strip().lower()
        if group in ["младшая", "средняя", "старшая"]:
            break
        print("Неверное название группы. Выберите: младшая, средняя, старшая")
    specialists = ["невропатолога", "отоларинголога", "ортопеда", "окулиста"]
    conclusions = []
    print("\nЗаключения специалистов (выберите: здоров или нуждается в лечении)")
    for spec in specialists:
        while True:
            conclusion = input(f"Заключение {spec}: ").strip().lower()
            if conclusion in ["здоров", "нуждается в лечении"]:
                conclusions.append(conclusion)
                break
            print("Некорректное заключение. Введите: здоров или нуждается в лечении")
    new_record = [surname, name, year, month, day, group] + conclusions
    updated_records = records.copy()
    updated_records.append(new_record)
    print(f'\nВоспитанник "{surname} {name}" успешно добавлен в базу')
    return updated_records


def edit_child(records):
    """Редактирует информацию о существующем воспитаннике"""
    if not records:
        print("Нет воспитанников для редактирования")
        return records

    display_children(records, "РЕДАКТИРОВАНИЕ ДАННЫХ ВОСПИТАННИКА")
    while True:
        try:
            choice = int(input(f"\nВыберите номер воспитанника для редактирования (1-{len(records)}): "))
            if 1 <= choice <= len(records):
                break
            print(f"Введите число в диапазоне от 1 до {len(records)}")
        except ValueError:
            print("Введите корректное число")
    updated_records = [record.copy() for record in records]
    child = updated_records[choice - 1]
    original_child = child.copy()
    print(f"\nРедактирование данных для: {child[0]} {child[1]}")
    print("Оставьте поле пустым, чтобы сохранить текущее значение")
    new_surname = input(f"Фамилия [{child[0]}]: ").strip()
    if new_surname:
        child[0] = new_surname
    new_name = input(f"Имя [{child[1]}]: ").strip()
    if new_name:
        child[1] = new_name
    year_input = input(f"Год рождения [{child[2]}]: ").strip()
    if year_input:
        while True:
            try:
                year = int(year_input)
                if 2010 <= year <= 2020:
                    child[2] = year
                    break
                print("Год должен быть в диапазоне от 2010 до 2020")
                year_input = input(f"Год рождения [{child[2]}]: ").strip()
            except ValueError:
                print("Введите корректное число")
                year_input = input(f"Год рождения [{child[2]}]: ").strip()
    month_input = input(f"Месяц рождения [{child[3]}]: ").strip()
    if month_input:
        while True:
            try:
                month = int(month_input)
                if 1 <= month <= 12:
                    child[3] = month
                    break
                print("Месяц должен быть в диапазоне от 1 до 12")
                month_input = input(f"Месяц рождения [{child[3]}]: ").strip()
            except ValueError:
                print("Введите корректное число")
                month_input = input(f"Месяц рождения [{child[3]}]: ").strip()
    day_input = input(f"День рождения [{child[4]}]: ").strip()
    if day_input:
        while True:
            try:
                day = int(day_input)
                if 1 <= day <= 31:
                    child[4] = day
                    break
                print("День должен быть в диапазоне от 1 до 31")
                day_input = input(f"День рождения [{child[4]}]: ").strip()
            except ValueError:
                print("Введите корректное число")
                day_input = input(f"День рождения [{child[4]}]: ").strip()
    group_input = input(f"Группа [{child[5]}]: ").strip().lower()
    if group_input:
        while group_input not in ["младшая", "средняя", "старшая"]:
            print("Неверное название группы. Выберите: младшая, средняя, старшая")
            group_input = input(f"Группа [{child[5]}]: ").strip().lower()
        child[5] = group_input
    specialists = ["невропатолога", "отоларинголога", "ортопеда", "окулиста"]
    for i, spec in enumerate(specialists, 6):
        conclusion_input = input(f"Заключение {spec} [{child[i]}]: ").strip().lower()
        if conclusion_input:
            while conclusion_input not in ["здоров", "нуждается в лечении"]:
                print("Некорректное заключение. Введите: здоров или нуждается в лечении")
                conclusion_input = input(f"Заключение {spec} [{child[i]}]: ").strip().lower()
            child[i] = conclusion_input
    if child == original_child:
        print("\nДанные не были изменены")
        return records
    else:
        print(f'\nДанные воспитанника "{child[0]} {child[1]}" успешно обновлены')
        return updated_records


def remove_child(records):
    """Удаляет воспитанника из базы"""
    if not records:
        print("Нет воспитанников для удаления")
        return records
    print_header("УДАЛЕНИЕ ВОСПИТАННИКА")
    for i, record in enumerate(records, 1):
        print(f"{i:3}. {record[0]} {record[1]} ({record[5]} группа)")
    while True:
        try:
            del_choice = int(input(f"\nВыберите номер воспитанника для удаления (1-{len(records)}): "))
            if 1 <= del_choice <= len(records):
                break
            print(f"Введите число в диапазоне от 1 до {len(records)}")
        except ValueError:
            print("Введите корректное число")
    selected_child = records[del_choice - 1]
    while True:
        confirm = input(
            f'\n-- Вы уверены, что хотите удалить "{selected_child[0]} {selected_child[1]}"? (да/нет): ').lower()
        if confirm in ['да', 'д', 'yes', 'y']:
            updated_records = records.copy()
            removed = updated_records.pop(del_choice - 1)
            print(f'\nВоспитанник "{removed[0]} {removed[1]}" успешно удален из базы')
            print(f"Осталось воспитанников: {len(updated_records)}")
            return updated_records
        elif confirm in ['нет', 'н', 'no', 'n']:
            print("Удаление отменено")
            return records.copy()
        print('Пожалуйста, введите "да" или "нет"')
