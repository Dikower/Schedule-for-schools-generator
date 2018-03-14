import sys
import json
import easygui
import re

def generator(day):
    pass

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
                            generator(day_name)
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
            base.write(re.sub("'", '"',str(week)))

        with open("classes.json", "w", encoding="utf8") as classes_file:
            classes_file.write(re.sub("'", '"', str(classes)))

interface()
# load_base()
# msg = "Enter your personal information"
# title = "Credit Card Application"
# fieldNames = ["Name","Street Address","City","State","ZipCode"]
# fieldValues = []  # we start with blanks for the values
# fieldValues = easygui.multenterbox(msg,title, fieldNames)

# print(fieldValues)