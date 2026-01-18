from reports import report_all_children, report_by_group, report_needs_treatment
from records import load_children, save_children, generate_sample_data
from file_operations import *


def confirm_save(children):
    """Запрашивает подтверждение на сохранение изменений"""
    while True:
        confirm = input("\n-- Сохранить изменения в базе данных? (да/нет): ").lower()
        if confirm in ['да', 'д', 'yes', 'y']:
            save_children(data_filename, children)
            print("Изменения успешно сохранены")
            return True
        elif confirm in ['нет', 'н', 'no', 'n']:
            print("Изменения не сохранены")
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'")


def navigation_menu(children=None, changes_made=False):
    """Меню навигации с возможностью возврата или выхода"""
    while True:
        print("\n1. Вернуться в предыдущее меню")
        print("0. Выйти из программы")
        choice = input("Выберите действие (1,0): ").strip()
        if choice == '1':
            if changes_made and children is not None:
                if confirm_save(children):
                    return True
                else:
                    return False
            return True
        elif choice == '0':
            if changes_made and children is not None:
                confirm_save(children)
            print("\nСпасибо за использование программы! До свидания!")
            exit(0)

        else:
            print("Некорректный выбор. Введите 1 или 0")


def reports_submenu(children):
    """Подменю для формирования отчетов"""
    while True:
        print_header("ФОРМИРОВАНИЕ ОТЧЕТОВ")
        print("1. Полный список всех детей (по количеству здоровых заключений)")
        print("2. Список детей заданной группы")
        print("3. Список детей, нуждающихся в лечении")
        print("4. Вернуться в главное меню")
        print("0. Выйти из программы")
        print("=" * 60)
        choice = input("Выберите тип отчета (1-4,0): ").strip()
        if choice == '1':
            sorted_children = report_all_children(children.copy())
            display_children(sorted_children,
                             "ОТЧЕТ 1\nПолный список воспитанников, отсортированный по количеству здоровых "
                             "заключений\n(сначала идут дети со всеми здоровыми заключениями)")
            navigation_menu()
        elif choice == '2':
            group = input("\nВведите название группы (младшая/средняя/старшая): ").strip().lower()
            if group in ["младшая", "средняя", "старшая"]:
                sorted_children = report_by_group(children.copy(), group)
                if sorted_children:
                    display_children(sorted_children,
                                     f"ОТЧЕТ 2\nСписок воспитанников группы '{group}', "
                                     "отсортированный по дате рождения")
                else:
                    print(f"\nВ группе '{group}' нет воспитанников")
            else:
                print("\nНекорректное название группы. Выберите: младшая, средняя или старшая")
            navigation_menu()
        elif choice == '3':
            treatment_children = report_needs_treatment(children.copy())
            if treatment_children:
                display_children(treatment_children,
                                 "ОТЧЕТ 3\nСписок воспитанников, нуждающихся в лечении, отсортированный по группе и "
                                 "фамилии")
            else:
                print("\nНет воспитанников, нуждающихся в лечении")
            navigation_menu()
        elif choice == '4':
            break
        elif choice == '0':
            print("\nСпасибо за использование программы! До свидания!")
            exit(0)
        else:
            print("Некорректный выбор. Введите число от 1 до 4 или 0")


def management_submenu(children):
    """Подменю для управления данными воспитанников"""
    current_children = children.copy()
    changes_occurred = False
    while True:
        print_header("УПРАВЛЕНИЕ ДАННЫМИ ВОСПИТАННИКОВ")
        print("1. Добавить нового воспитанника")
        print("2. Редактировать данные воспитанника")
        print("3. Удалить воспитанника")
        print("4. Вернуться в главное меню")
        print("0. Выйти из программы")
        print("=" * 60)
        choice = input("Выберите действие (1-4,0): ").strip()
        if choice == '1':
            new_children = add_child(current_children)
            if new_children != current_children:
                changes_occurred = True
                current_children = new_children
            navigation_menu()
        elif choice == '2':
            new_children = edit_child(current_children)
            if new_children != current_children:
                changes_occurred = True
                current_children = new_children
            navigation_menu()
        elif choice == '3':
            new_children = remove_child(current_children)
            if new_children != current_children:
                changes_occurred = True
                current_children = new_children
                if not current_children:
                    return current_children, True
            navigation_menu()
        elif choice == '4':
            if changes_occurred:
                if confirm_save(current_children):
                    return current_children, True
                else:
                    return children, False
            return current_children, changes_occurred
        elif choice == '0':
            if changes_occurred:
                confirm_save(current_children)
            print("\nСпасибо за использование программы! До свидания!")
            exit(0)
        else:
            print("Некорректный выбор. Введите число от 1 до 4 или 0")


def empty_database_menu():
    """Меню для работы с пустой базой данных"""
    children = []
    while True:
        print_header("УЧЁТ РЕЗУЛЬТАТОВ ДИСПАНСЕРИЗАЦИИ")
        print("База данных воспитанников пуста\n")
        print("1. Создать демонстрационные данные (25 записей)")
        print("2. Добавить первого воспитанника вручную")
        print("0. Выйти из программы")
        print("=" * 60)
        choice = input("Выберите действие (1-2,0): ").strip()
        if choice == '1':
            children = generate_sample_data()
            save_children(data_filename, children)
            print("\nДемонстрационные данные успешно созданы и сохранены в файл")
            return children
        elif choice == '2':
            children = add_child(children)
            save_children(data_filename, children)
            print("\nДанные воспитанника успешно сохранены в файл")
            return children
        elif choice == '0':
            print("\nСпасибо за использование программы! До свидания!")
            exit(0)
        else:
            print("Некорректный выбор. Введите число от 1 до 2 или 0")


def main_menu(children):
    """Главное меню программы"""
    while True:
        print_header("УЧЁТ РЕЗУЛЬТАТОВ ДИСПАНСЕРИЗАЦИИ")
        print("1. Показать всех воспитанников")
        print("2. Сформировать отчет")
        print("3. Управление данными (добавить/редактировать/удалить)")
        print("0. Выйти из программы")
        print("=" * 60)
        choice = input("Выберите действие (1-3,0): ").strip()
        if choice == '1':
            display_children(children, "СПИСОК ВСЕХ ВОСПИТАННИКОВ")
            navigation_menu()
        elif choice == '2':
            reports_submenu(children)
        elif choice == '3':
            children, _ = management_submenu(children)
        elif choice == '0':
            print("\nСпасибо за использование программы! До свидания!")
            exit(0)
        else:
            print("Некорректный выбор. Введите число от 1 до 3 или 0")


data_filename = "database.txt"


def program_entry():
    """Точка входа в программу"""
    print_header("ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ УЧЁТА ДИСПАНСЕРИЗАЦИИ")
    print("Программа загружает данные из файла...")
    children = load_children(data_filename)
    if children is False:
        print("\nФайл базы данных не найден. Будет создана новая база.")
        children = empty_database_menu()
    elif children is None:
        print("\nОшибка формата данных в файле. Будет создана новая база.")
        children = empty_database_menu()
    elif not children:
        print("\nФайл базы данных пуст. Необходимо добавить данные.")
        children = empty_database_menu()
    main_menu(children)


if __name__ == "__main__":
    program_entry()
