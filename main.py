import sys
import json
import easygui
import re
import xlsxwriter


def generator(classes_inp, hours, day):
    # inp = {"1": ["Алгебра", "Русский", "Алгебра"], "2": ["Алгебра", "Литература", "Русский"],
    #        "3": ["Литература", "Русский"], "4": ["Музыка", "Физра", "Английский", "Алгебра", "Русский", "Литература"]}

    # inp = {"1": ["Алгебра", "Русский","Литература", "Литература"], "2": ["Алгебра", "Литература", "Русский"], "3": ["Литература", "Русский", "Литература", "Алгебра"]}
    cls = hours.keys()
    inp = {}
    for one_class in hours.keys():
        for object in hours[one_class]:
            inp[one_class] = inp.get(one_class, []) + [classes_inp[one_class][object]]
    # print(inp)
    # print(classes)
    # print(hours)
    values = [j for i in inp.values() for j in i]
    amount = {}

    for value in values:
        amount[value] = amount.get(value, 0) + 1

    classes = {key: sorted(inp[key], key=lambda x: amount[x], reverse=True) for key in inp.keys()}
    sorted_lessons = {i: [] for i in classes.keys()}
    lesson = 0
    time = 0

    while len(classes.values()) != 0:
        to_del = []
        for key in classes.keys():
            if len(classes[key]) == 0:
                to_del.append(key)
        for key in to_del:
            classes.pop(key)

        if len(classes.keys()) == 0:
            break

        list_to_choose = sorted(list(set(classes.keys()).intersection(set(sorted_lessons.keys()))),
                                key=lambda x: len(sorted_lessons[x]))
        min_sorted_lessons = []

        for el in list_to_choose:
            if len(sorted_lessons[list_to_choose[0]]) != len(sorted_lessons[el]):
                break
            min_sorted_lessons.append(el)

        min_sorted_lessons = sorted(min_sorted_lessons, key=lambda x: len(classes[x]))
        min_lessons = []

        for el in min_sorted_lessons:
            if len(classes[min_sorted_lessons[0]]) != len(classes[el]):
                break
            min_lessons.append(el)

        weights = {key: sum(amount[i] for i in classes[key]) for key in min_lessons}
        # print(weights)
        chosen_class = max(weights.keys(), key=lambda x: weights[x])
        # print(chosen_class)
        lesson = len(sorted_lessons[chosen_class])
        max_lessons = max([len(sorted_lessons[i]) for i in sorted_lessons.keys()])

        # print(time)
        # print(classes)
        # print(sorted_lessons)
        # print("-" * 100)

        if max_lessons == lesson:
            sorted_lessons[chosen_class].append(classes[chosen_class].pop(0))
        else:
            r = True
            current_lessons = [sorted_lessons[i][lesson] for i in sorted_lessons.keys()
                               if len(sorted_lessons[i]) - 1 == lesson]
            for l in range(len(classes[chosen_class])):
                if classes[chosen_class][l] not in current_lessons:
                    r = False
                    sorted_lessons[chosen_class].append(classes[chosen_class].pop(l))
                    break
            if r:
                sorted_lessons[chosen_class].append("")
                print("Unable to make")
                print(classes)
                print(sorted_lessons)
                print(current_lessons)

        time += 1

    current_hours = hours.copy()
    to_write = {}
    print(sorted_lessons)
    for one_class in sorted_lessons.keys():
        for teacher in sorted_lessons[one_class]:
            if teacher != "":
                for subject in current_hours[one_class]:
                    if classes_inp[one_class][subject] == teacher and current_hours[one_class][subject] > 0:
                        to_write[one_class] = to_write.get(one_class, []) + [subject]
                        current_hours[one_class][subject] -= 1
            else:
                to_write[one_class] = to_write.get(one_class, []) + [""]
    # print(to_write)
    # for i in to_write:
    #     print(to_write[i])


def load_base():
    try:
        with open("base.json", "r", encoding="utf8") as base:
            week = json.loads(base.read().strip("\n"))
    except FileNotFoundError:
        json_style = '{"Понедельник":{},"Вторник":{},"Среда":{},"Четверг":{},"Пятница":{},"Суббота":{}}'
        with open("base.json", "w", encoding="utf8") as base:
            base.write(json_style)
        week = json.loads(json_style)
    finally:
        return week


def load_cabinets():
    try:
        with open("cabinet.json", "r", encoding="utf8") as json_file:
            cabinet = json.loads(json_file.read().strip("\n"))
    except FileNotFoundError:
        with open("cabinet.json", "w", encoding="utf8") as json_file:
            json_file.write("{}")
        cabinet = {}
    finally:
        return cabinet


def load_classes():
    try:
        with open("classes.json", "r", encoding="utf8") as json_file:
            classes = json.loads(json_file.read().strip("\n"))
    except FileNotFoundError:
        with open("classes.json", "w", encoding="utf8") as json_file:
            json_file.write("{}")
        classes = {}
    finally:
        return classes


def start_screen():
    title = "Мененджер расписаний"
    msg = "Выберите режим работы. Если вы первый раз запустили данную программу, выберите сначала кнопку Классы."
    choices = ["Классы", "Дни", "Руководство(Обязательно к прочтению!)"]
    choice = easygui.buttonbox(msg, title=title, choices=choices)
    if choice is None:
        sys.exit(0)
    return choice


def week_screen():
    title = "Мененджер расписаний"
    msg = "Выберите день недели. В котором хотите задать количество часов для классов по определенным предметам."
    choices = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    choice = easygui.choicebox(msg, title, choices)
    return choice


def classes_screen(classes):
    title = "Мененджер расписаний"
    msg = "Это раздел создания и настройки классов, чтобы выйти из него нажмите Cancel."
    choices = list(classes.keys()) + ["Добавить класс.", ""]
    choice = easygui.choicebox(msg, title, choices)
    return choice


def add_objects(curr):
    title = "Мененджер расписаний"
    msg = "Выберите предметы для данного класса: " + curr
    choices = ["Алгебра", "Русский язык", "Литература", "Геометрия", "Физика", "Информатика", "Биология", "Химия",
               "Обществознание", "История", "Физкультура", "Иностранный язык", "ОБЖ", "География", "Труд", "Астрономия",
               "Экономика", "Экология", "Право"]
    choice = easygui.multchoicebox(msg, title, choices)
    return choice


def new_class():
    while True:
        title = "Мененджер расписаний"
        msg = "Впишите информацию во все поля."
        field_names = ["Номер класса(год обучения)", "Буква"]
        field_values = []  # we start with blanks for the values
        field_values = easygui.multenterbox(msg, title, field_names)
        errors = []
        if field_values is None:
            return None

        try:
            test = int(field_values[0])
        except ValueError:
            errors.append("Нужно ввести цифру!")
        finally:
            test = len(field_values[1])
            if test != 1 or not field_values[1].isalpha():
                errors.append("Нужно ввести одну букву! (без кавычек)")

        if len(errors) == 0:
            break
        easygui.msgbox('\n'.join(errors))
    field_values[1] = field_values[1].upper()
    return "".join(field_values)


def add_teachers(objects, curr):
    while True:
        title = "Мененджер расписаний"
        msg = "Впишите имена учителей для {}, если имена в будут совпадать, то программа воспримет как одного и того же учителя.\nМожно ставить цифры, фамилии, отличительные черты для каждого учителя.".format(curr)
        field_names = objects
        field_values = []  # we start with blanks for the values
        field_values = easygui.multenterbox(msg, title, field_names)
        if field_values is None:
            break
        if len(field_values) != len(field_names):
            continue
        return {field_names[i]: field_values[i] for i in range(len(field_names))}


def edit_class():
    title = "Мененджер расписаний"
    msg = "Выберите, что хотите сделать."
    choices = ["Выбрать предметы", "Удалить", "Cancel"]
    choice = easygui.buttonbox(msg, title=title, choices=choices)
    if choice is None:
        sys.exit(0)
    return choice


def edit_day(classes):
    title = "Мененджер расписаний"
    msg = "Если вы уже назначили во всех классах количество часов, можно сгенерировать расписание.\nЕсли нет, то выберите класс и назначте предметы."
    choices = list(classes.keys())
    if len(choices) > 0:
        choices.insert(0, "Сгенерировать расписание.")
    else:
        choices = ["Сначала нужно создать классы.", ""]

    choice = easygui.choicebox(msg, title, choices)
    return choice


def choose_objects(classes, curr):
    title = "Мененджер расписаний"
    msg = "Выберите предметы, которые будут в этот день, для данного класса: " + curr
    choices = classes[curr]
    choice = easygui.multchoicebox(msg, title, choices)
    return choice


def make_hours(objects, curr):
    title = "Мененджер расписаний"
    msg = "Впишите колличество часов в этот день для {} класса, если ничего не впишете, то будет выставлен 1 час".format(curr)
    field_names = objects
    field_values = []  # we start with blanks for the values
    field_values = easygui.multenterbox(msg, title, field_names)
    if field_values is None:
        return None
    for value in range(len(field_values)):
        try:
            if field_values[value] != "":
                field_values[value] = int(field_values[value])
            else:
                field_values[value] = 1
        except ValueError:
            field_values[value] = 1
    return {field_names[i]: field_values[i] for i in range(len(field_values))}


def interface():
    week = load_base()
    classes = load_classes()
    while True:
        mode = start_screen()
        if mode == "Дни":
            while True:
                day_name = week_screen()
                if day_name is None:
                    break
                else:
                    while True:
                        do = edit_day(classes)
                        if do is None or do == "Сначала нужно создать классы." or do == "":
                            break
                        elif do == "Сгенерировать расписание.":
                            generator(classes, week[day_name], day_name)
                            msg = "Готово, расписание сохранено под именем {}.xlsx".format(day_name)
                            easygui.msgbox(msg, title="Готово!")
                        else:
                            while True:
                                objects = choose_objects(classes, do)
                                if objects is None:
                                    break
                                else:
                                    hours = make_hours(objects, do)
                                    if hours is None:
                                        continue
                                    else:
                                        week[day_name][do] = hours
                                    break

        elif mode == "Классы":
            while True:
                classes_mode = classes_screen(classes)
                if classes_mode is None:
                    break
                elif classes_mode == "Добавить класс.":
                    n_class = new_class()
                    if n_class is None:
                        continue
                    else:
                        while True:
                            objects = add_objects(n_class)
                            if objects is None or len(objects) == 0:
                                break
                            else:
                                while True:
                                    objects_with_teachers = add_teachers(objects, n_class)
                                    if objects_with_teachers is None:
                                        break
                                    else:
                                        classes[n_class] = objects_with_teachers
                                        break
                                break
                else:
                    changer = edit_class()
                    if changer == "Cancel":
                        continue
                    elif changer == "Выбрать предметы":
                                objects = add_objects(classes_mode)
                                objects_with_teachers = add_teachers(objects, classes_mode)
                                classes[classes_mode] = objects_with_teachers
                                # break
                    elif changer == "Удалить":
                        classes.pop(classes_mode)
        elif mode == "Руководство(Обязательно к прочтению!)":
            easygui.msgbox("Кнопка класс перенесет вас в раздел создания и редактирования класса, если хотите поменять список предметов у выбранного класса, выберите класс и нажмите OK. В любом разделе кнопка Cancel вернет вас в предыдущий раздел.")

        with open("base.json", "w", encoding="utf8") as base:
            base.write(re.sub("'", '"', str(week)))

        with open("classes.json", "w", encoding="utf8") as classes_file:
            classes_file.write(re.sub("'", '"', str(classes)))


interface()
