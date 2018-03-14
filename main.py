import sys
import json
import easygui
import re
import xlsxwriter
import copy
import os


def generator(classes_inp, hours, cabinets, day_name):
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

    current_hours = copy.deepcopy(hours)
    to_write = {}
    for one_class in sorted_lessons.keys():
        for teacher in sorted_lessons[one_class]:
            if teacher != "":
                for subject in current_hours[one_class]:
                    if classes_inp[one_class][subject] == teacher and current_hours[one_class][subject] > 0:
                        to_write[one_class] = to_write.get(one_class, []) + [subject + " " + cabinets[teacher]]
                        current_hours[one_class][subject] -= 1
            else:
                to_write[one_class] = to_write.get(one_class, []) + [""]

    # print(to_write)
    # for i in to_write:
    #     print(to_write[i])
    keys = sorted(list(to_write.keys()), key=lambda x: (int(x[:-1]), x[-1]))
    try:
        workbook = xlsxwriter.Workbook(day_name+".xlsx")
    except:
        os.remove(day_name+".xlsx")
        workbook = xlsxwriter.Workbook(day_name+".xlsx")

    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, day_name)
    try:
        max_lenght = len(max(to_write.values(), key=len))
    except ValueError:
        max_lenght = 0
    # print(max_lenght)
    # print(keys)
    string = 0
    col = 0
    for one_class in range(len(keys)):
        worksheet.write(string * max_lenght + 1, one_class, keys[one_class])
        objects = to_write[keys[one_class]]
        # print(objects)
        for object in range(1, len(objects) + 1):
            worksheet.write(string * max_lenght + 1 + object, one_class, objects[object-1])

    workbook.close()


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
        with open("cabinets.json", "r", encoding="utf8") as json_file:
            cabinet = json.loads(json_file.read().strip("\n"))
    except FileNotFoundError:
        with open("cabinets.json", "w", encoding="utf8") as json_file:
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
    choices = ["Классы", "Дни", "Выбрать кабинеты для учителей.", "Руководство(Обязательно к прочтению!)"]
    choice = easygui.buttonbox(msg, title=title, choices=choices)
    if choice is None:
        sys.exit(0)
    return choice


def week_screen():
    title = "Мененджер расписаний"
    msg = "Выберите день недели, в котором хотите задать количество часов для классов по определенным предметам."
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


def edit_class(curr, class_name):
    title = "Мененджер расписаний"
    msg = "Выберите, что хотите сделать."
    choices = ["Поменять учителей", "Удалить", "Cancel"]
    choice = easygui.buttonbox(msg, title=title, choices=choices)
    if choice is None:
        sys.exit(0)
    return choice


def edit_day(classes):
    title = "Мененджер расписаний"
    msg = "Если вы уже назначили во всех классах количество часов, можно сгенерировать расписание.\nЕсли нет, то выберите класс и назначте предметы.\nЕсли вы не назначите часы для класса, то он не будет учитываться при генерации."
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


def make_cabinets(classes):
    teachers = []
    for key in classes.keys():
        for teacher in classes[key].values():
            if teacher not in teachers:
                teachers.append(teacher)
    title = "Мененджер расписаний"
    msg = "Впишите номера кабинетов, закрепленных за учителями."
    field_names = sorted(teachers)
    field_values = []  # we start with blanks for the values
    field_values = easygui.multenterbox(msg, title, field_names)
    if field_values is None:
        return None
    return {field_names[i]: field_values[i] for i in range(len(field_values))}


def lessons_view_screen(curr, class_name):
    title = "Мененджер расписаний"
    msg = class_name
    easygui.textbox(msg, title, "\n".join([i+": "+curr[i] for i in curr.keys()]))


def interface():
    week = load_base()
    classes = load_classes()
    cabinets = load_cabinets()

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
                            generator(classes, week[day_name], cabinets, day_name)
                            msg = "Готово, расписание сохранено под именем {}.xlsx".format(day_name)
                            easygui.msgbox(msg, title="Готово!")
                            break
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
                                    classes[n_class] = objects_with_teachers
                                    break
                                break
                else:
                    changer = edit_class(classes[classes_mode], classes_mode)
                    if changer == "Cancel":
                        continue
                    elif changer == "Поменять учителей":
                        objects_with_teachers = add_teachers(list(classes[classes_mode].keys()), classes_mode)
                        if objects_with_teachers is not None:
                            classes[classes_mode] = objects_with_teachers
                            continue
                        else:
                            break

                    elif changer == "Удалить":
                        classes.pop(classes_mode)
                        for d in week.keys():
                            if classes_mode in week[d].keys():
                                week[d].pop(classes_mode)
        elif mode == "Выбрать кабинеты для учителей." and len(classes.values()) != 0:
            try_cabinets = make_cabinets(classes)
            if try_cabinets is not None:
                cabinets = try_cabinets
        elif len(classes.values()) == 0 and mode == "Выбрать кабинеты для учителей.":
            easygui.msgbox("Создайте сначала класс и распределите учителей по предметам, нажав на кнопку Классы.")

        elif mode == "Руководство(Обязательно к прочтению!)":
            easygui.msgbox("Кнопка класс перенесет вас в раздел создания и редактирования класса, если хотите поменять список предметов у выбранного класса, выберите класс и нажмите OK. В любом разделе кнопка Cancel вернет вас в предыдущий раздел.")

        with open("base.json", "w", encoding="utf8") as base:
            base.write(re.sub("'", '"', str(week)))

        with open("classes.json", "w", encoding="utf8") as classes_file:
            classes_file.write(re.sub("'", '"', str(classes)))

        with open("cabinets.json", "w", encoding="utf8") as cabinets_file:
            cabinets_file.write(re.sub("'", '"', str(cabinets)))


if __name__ == '__main__':
    interface()
