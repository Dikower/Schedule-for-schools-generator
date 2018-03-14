# Первая группа тестов
# class_list1 = ["Алгебра", "Алгебра", "Физ-ра", "История", "Английский", "Информатика"]
# class_list2 = ["Алгебра", "Алгебра", "Физ-ра", "История", "Английский", "Информатика"]

# Вторая группа тестов
# class_list1 = ["Алгебра", "Алгебра","Aлгебра"]
# class_list2 = ["Русский"]

# Третья группа тестов
# class_list1 = ["Алгебра", "Русский","Aлгебра"]
# class_list2 = ["Алгебра", "Литература","Русский"]

# Четвертая группа тестов
# classes = {"1": ["Алгебра", "Русский", "Aлгебра"], "2": ["Алгебра", "Литература", "Русский"], "3": ["Литература", "Русский"]}

# Пятая группа тестов
inp = {"1": ["Алгебра", "Русский", "Алгебра"], "2": ["Алгебра", "Литература", "Русский"], "3": ["Литература", "Русский"], "4": ["Музыка", "Физра", "Английский", "Алгебра", "Русский", "Литература"]}

# inp = {"1": ["Алгебра", "Русский","Литература", "Литература"], "2": ["Алгебра", "Литература", "Русский"], "3": ["Литература", "Русский", "Литература", "Алгебра"]}
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
            print("Unable to make")
            print(classes)
            print(sorted_lessons)
            print(current_lessons)
            break
    time += 1
print("-"*100)
for i in sorted_lessons:
    print(sorted_lessons[i])
