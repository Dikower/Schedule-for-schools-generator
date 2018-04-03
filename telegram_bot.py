import os

try:
    import time
except:
    try:
        os.system("pip install time")
        import time
    except:
        print("Не удалось установить time.")

try:
    from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
    from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
except:
    try:
        os.system("pip install python-telegram-bot")
        from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
        from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
    except:
        print("Не удалось установить telegram.")

try:
    import re
except:
    try:
        os.system("pip install re")
        import re
    except:
        print("Не удалось установить re.")

try:
    import json
except:
    try:
        os.system("pip install json")
        import json
    except:
        print("Не удалось установить json.")

reply_keyboard = [['/Расписание_на_завтра', '/Расписание_на_сегодня'],
                  ['/Время', '/Помощь'],
                  ['/Закрыть_клавиатуру']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(bot, update):
    update.message.reply_text('Я бот, выдающий расписания.\nДля начала введи "/Поменять_класс XX". Вместо XX - твой класс.',
                              reply_markup=markup)


def helper(bot, update):
    update.message.reply_text(
        'В мой функционал входят три основные команды: выдать расписание на сегодня, либо на завтра и показать время. Также есть возможность поменять класс, чтобы узнавать расписание для выбранного класса.\nДля этого введи "/Поменять_класс XX". Вместо XX - свой класс.')


def give_time(bot, update):
    update.message.reply_text(time.asctime().split()[-2])


def give_scheudle_today(bot, update, chat_data):
    if 'class' in chat_data:
        try:
            with open("scheudle.json", encoding="utf8") as file:
                scheudle = json.loads(file.read().strip())
            day = time.strftime('%A')
            week = {"Sunday": "Воскресенье", "Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда", "Thursday": "Четверг", "Friday": "Пятница", "Saturday": "Суббота"}
            if week[day] in scheudle:
                if chat_data['class'] in scheudle[week[day]]:
                    print(True)

                    update.message.reply_text("Рассписание на сегодня ({0}) для {1} класса.".format(week[day], chat_data['class']))
                    for num, obj in enumerate(scheudle[week[day]][chat_data['class']]):
                        update.message.reply_text(str(num+1)+'. ' + obj)
                else:
                    update.message.reply_text("Рассписание на сегодня ({0}) для {1} класса отсутствует.".format(week[day], chat_data['class']))
            else:
                update.message.reply_text("Рассписание на сегодня ({}) отсутствует.".format(week[day]))

        except FileNotFoundError:
            update.message.reply_text("Расписание отсутствует.")

    else:
        update.message.reply_text('Cначала нужно добавить себя в класс. Пример правильного ввода:\n/Поменять_класс 1А\n(буква кириллицей).')


def give_scheudle_tomorrow(bot, update, chat_data):
    if 'class' in chat_data:
        try:
            with open("scheudle.json", encoding="utf8") as file:
                scheudle = json.loads(file.read().strip())

            day = time.strftime('%A')
            next_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            number = next_days.index(day)

            if number == 6:
                day = next_days[0]
            else:
                day = next_days[number+1]

            week = {"Sunday": "Воскресенье", "Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда",
                    "Thursday": "Четверг", "Friday": "Пятница", "Saturday": "Суббота"}

            if week[day] in scheudle:
                if chat_data['class'] in scheudle[week[day]]:
                    update.message.reply_text(
                        "Рассписание на завтра ({0}) для {1} класса.".format(week[day], chat_data['class']))
                    for num, obj in enumerate(scheudle[week[day]][chat_data['class']]):
                        update.message.reply_text(str(num + 1) + '. ' + obj)
                else:
                    print(chat_data['class'], scheudle[week[day]])
                    print(chat_data['class'] in scheudle[week[day]])

                    update.message.reply_text(
                        "Рассписание на завтра ({0}) для {1} класса отсутствует.".format(week[day],
                                                                                          chat_data['class']))
            else:
                update.message.reply_text("Рассписание на завтра ({}) отсутствует.".format(week[day]))

        except FileNotFoundError:
            update.message.reply_text("Расписание отсутствует.")

    else:
        update.message.reply_text('Сначала нужно добавить себя в класс. Для этого введи: \n/Поменять_класс XX. Вместо XX - твой класс.')


def close_keyboard(bot, update):
    update.message.reply_text("Закрываю", reply_markup=ReplyKeyboardRemove())


def change_class(bot, update, args, chat_data):
    if len(args[0]) >= 2:
        if args[0][:-1].isdigit() and ord(args[0][-1]) in range(ord('А'), ord('я')+1):
            chat_data['class'] = args[0].strip()
            update.message.reply_text('Теперь ты в {} классе.'.format(args[0]))
            print(chat_data)
        else:
            update.message.reply_text(
                'Неправильно введен класс! Пример правильного ввода:\n/Поменять_класс 1А\n(буква кириллицей).')

    else:
        update.message.reply_text(
            'Неправильно введен класс! Пример правильного ввода:\n/Поменять_класс 1А\n(буква кириллицей).')


def Telegram_bot():
    updater = Updater("598818758:AAFKUTQ2CwW7RJsWqHFF2nKUnsDsl5bgrgo")

    dp = updater.dispatcher

    # dp.add_handler(CommandHandler("start", start, pass_chat_data=True))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("Время", give_time))
    dp.add_handler(CommandHandler("Закрыть_клавиатуру", close_keyboard))
    dp.add_handler(CommandHandler("Помощь", helper))
    dp.add_handler(CommandHandler("Расписание_на_завтра", give_scheudle_tomorrow, pass_chat_data=True))
    dp.add_handler(CommandHandler("Расписание_на_сегодня", give_scheudle_today, pass_chat_data=True))
    dp.add_handler(CommandHandler("Поменять_класс", change_class, pass_chat_data=True, pass_args=True))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    Telegram_bot()