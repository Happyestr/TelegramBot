from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import time
import requests

slovar = {'Рим': {'Погода': 'разнообразный',
                  'Достопремечательности': 'хочу',
                  'Пляж': 'не хочу',
                  'Горнолыжный курорт': 'не хочу',
                  'Шопинг': 'хочу',
                  'Отдых': 'неактивный',
                  'Транспорт': 'пешком',
                  'Дети': 'нет'},
          'Сочи': {'Погода': 'солнечный',
                   'Достопремечательности': 'хочу',
                   'Пляж': 'хочу',
                   'Горнолыжный курорт': 'хочу',
                   'Шопинг': 'хочу',
                   'Отдых': 'активный',
                   'Транспорт': 'машина',
                   'Дети': 'да'},
          'Майами': {'Погода': 'солнечный',
                     'Достопремечательности': 'не хочу',
                     'Пляж': 'хочу',
                     'Горнолыжный курорт': 'не хочу',
                     'Шопинг': 'не хочу',
                     'Отдых': 'активный',
                     'Транспорт': 'машина',
                     'Дети': 'да'},
          'Санкт-Петербург': {'Погода': 'дождливый',
                              'Достопремечательности': 'хочу',
                              'Пляж': 'не хочу',
                              'Горнолыжный курорт': 'не хочу',
                              'Шопинг': 'хочу',
                              'Отдых': 'неактивный',
                              'Транспорт': 'пешком',
                              'Дети': 'нет'},
          'Прага': {'Погода': 'разнообразный',
                    'Достопремечательности': 'хочу',
                    'Пляж': 'не хочу',
                    'Горнолыжный курорт': 'не хочу',
                    'Шопинг': 'не хочу',
                    'Отдых': 'неактивный',
                    'Транспорт': 'пешком',
                    'Дети': 'нет'},
          'Анталья': {'Погода': 'солнечный',
                      'Достопремечательности': 'хочу',
                      'Пляж': 'хочу',
                      'Горнолыжный курорт': 'не хочу',
                      'Шопинг': 'хочу',
                      'Отдых': 'неактивный',
                      'Транспорт': 'пешком',
                      'Дети': 'да'},
          'Лондон': {'Погода': 'дождливый',
                     'Достопремечательности': 'хочу',
                     'Пляж': 'не хочу',
                     'Горнолыжный курорт': 'не хочу',
                     'Шопинг': 'хочу',
                     'Отдых': 'неактивный',
                     'Транспорт': 'машина',
                     'Дети': 'да'},

        'Информация': 'Майами – международный город на юго-восточной оконечности Флориды. В городе живет много кубинцев, что особенно заметно на улице Калле-Очо в районе Маленькая Гавана, где открыты традиционные кубинские кафе и сигарные лавки.',
        'Картинка': 'https://ltdfoto.ru/image/ZaDKC'},
    'Санкт-Петербург': {
        'Информация': 'Санкт-Петербург – русский портовый город на побережье Балтийского моря, который в течение двух веков служил столицей Российской империи.',
        'Картинка': 'https://ltdfoto.ru/image/Zao5Z'},
    'Прага': {
        'Информация': 'Прага – столица Чехии, раскинувшаяся вдоль обоих берегов реки Влтавы и известная как Город ста шпилей. Сердцем исторического центра города является Староместская площадь.',
        'Картинка': 'https://ltdfoto.ru/image/ZaZnd'},
    'Анталья': {
        'Информация': 'Анталья – курортный город, который славится своей Старой гаванью, где швартуются яхты, и пляжами, окруженными огромными отелями. ',
        'Картинка': 'https://ltdfoto.ru/image/ZaXvu'},
    'Лондон': {
        'Информация': 'Лондон – столица Англии и Соединенного Королевства. История этого современного города уходит во времена римлян. В самом центре Лондона находится здание парламента – Вестминстерский дворец.',
        'Картинка': 'https://ltdfoto.ru/image/Za2as'},
    'Дели': {
        'Информация': 'Дели – национальный столичный округ Индии и агломерация на севере страны. В районе Старого Дели XVII века возвышается символ Индии – величественный Красный форт эпохи моголов.',
        'Картинка': 'https://ltdfoto.ru/image/ZarER'},
    'Дрезден': {
        'Информация': 'Дрезден – столица восточногерманской земли Саксония со знаменитыми художественными музеями и классической архитектурой реконструированного старого города.',
        'Картинка': 'https://ltdfoto.ru/image/Za1nw'},
    'Париж': {
        'Информация': 'Столица Франции Париж – один из главных европейских городов и мировой центр культуры, искусства, моды и гастрономии.',
        'Картинка': 'https://ltdfoto.ru/image/ZazE7'},
    'Шамони': {
        'Информация': 'Шамони – курортный город во Франции недалеко от границы со Швейцарией и Италией.',
        'Картинка': 'https://ltdfoto.ru/image/Za7BH'},
    'Осло': {
        'Информация': 'Осло – столица Норвегии, расположенная на южном побережье страны у северной оконечности Осло-фьорда. Город известен своими парками и музеями.',
        'Картинка': 'https://ltdfoto.ru/image/ZaNDB'},
    'Богота': {
        'Информация': 'Богота – столица Колумбии, крупный мегаполис, расположенный высоко над уровнем моря',
        'Картинка': 'https://ltdfoto.ru/image/ZagRS'},
    'Каир': {
        'Информация': 'Каир – многолюдная столица Египта на реке Нил. Сердце города – площадь Тахрир, на которой расположен огромный Египетский музей с мумиями фараонов и позолоченными деревянными статуями Тутанхамона.',
        'Картинка': 'https://ltdfoto.ru/image/ZafdU'},
    'Инсбрук': {
        'Информация': 'Инсбрук – это город в Австрии, столица федеральной земли Тироль. Город расположен в Альпах и знаменит среди любителей зимних видов спорта.',
        'Картинка': 'https://ltdfoto.ru/image/Za65G'},
    'Барселона': {
        'Информация': 'Барселона – столица автономной области Каталония. Этот многонациональный город знаменит своей архитектурой и искусством.',
        'Картинка': 'https://ltdfoto.ru/image/ZadKp'},
    'Вена': {
        'Информация': 'Вена – столица Австрии, расположена в восточной части страны на реке Дунай. В культурное и интеллектуальное наследие города внесли вклад такие известные жители, как В.А. Моцарт, Л. Бетховен и З. Фрейд. ',
        'Картинка': 'https://ltdfoto.ru/image/ZaCSk'},
    'Орландо': {
        'Информация': 'Орландо – город в центральной Флориде, где работает более десятка тематических парков. Визитная карточка города – центр развлечений "Дисней Уорлд" с парками "Волшебное королевство" и "Эпкот" и двумя аквапарками.',
        'Картинка': 'https://ltdfoto.ru/image/ZaLRr'},
    'Багамы': {
        'Информация': 'Багамские острова – это архипелаг в Атлантическом океане, в состав которого входит более 700 коралловых островов. Среди них есть как необитаемые, так и заселенные острова со множеством отелей.',
        'Картинка': 'https://ltdfoto.ru/image/ZapZo'},
    'Венеция': {
        'Информация': 'Венеция – столица одноименной области на севере Италии. Город расположен на более чем 100 небольших островах в лагуне Адриатического моря. Здесь совсем нет дорог, движение происходит только по каналам.',
        'Картинка': 'https://ltdfoto.ru/image/ZaVaL'},
}

slovar_counts = {'Рим': 0,
                 'Сочи': 0,
                 'Майами': 0,
                 'Санкт-Петербург': 0,
                 'Прага': 0,
                 'Анталья': 0,
                 'Лондон': 0,
                 'Дели': 0,
                 'Дрезден': 0,
                 'Париж': 0,
                 'Шамони': 0,
                 'Осло': 0,
                 'Богота': 0,
                 'Каир': 0,
                 'Инсбрук': 0,
                 'Барселона': 0,
                 'Вена': 0,
                 'Орландо': 0,
                 'Багамы': 0,
                 'Венеция': 0,
                 }

keyboard_start = [["/start"]]
markup_start = ReplyKeyboardMarkup(keyboard_start, one_time_keyboard=True)

keyboard_weather = [["Дождливый", "Снежный"],
                    ["Разнообразный", "Солнечный"]]
markup_weather = ReplyKeyboardMarkup(keyboard_weather, one_time_keyboard=True)

keyboard_attractions = [["Хочу", "Не хочу"]]
markup_attractions = ReplyKeyboardMarkup(keyboard_attractions, one_time_keyboard=True)

keyboard_beach = [["Хочу", "Не хочу"]]
markup_beach = ReplyKeyboardMarkup(keyboard_beach, one_time_keyboard=False)

keyboard_ski_resort = [["Хочу", "Не хочу"]]
markup_ski_resort = ReplyKeyboardMarkup(keyboard_ski_resort, one_time_keyboard=True)

keyboard_shopping = [["Хочу", "Не хочу"]]
markup_shopping = ReplyKeyboardMarkup(keyboard_shopping, one_time_keyboard=False)

keyboard_type_of_recreation = [["Активный", "Неактивный"]]
markup_type_of_recreation = ReplyKeyboardMarkup(keyboard_type_of_recreation, one_time_keyboard=True)

keyboard_transport = [["Пешком", "Велосипед"],
                      ["Скутер", "Машина"],
                      ["Лодка", "Самолёт"]]
markup_transport = ReplyKeyboardMarkup(keyboard_transport, one_time_keyboard=True)

keyboard_children = [["Да", "Нет"]]
markup_children = ReplyKeyboardMarkup(keyboard_children, one_time_keyboard=True)


def clearspis():
    for i in slovar_counts:
        slovar_counts[i] = 0


def start(update, context):
    clearspis()
    update.message.reply_text(
        "Здравствуйте! Я - бот помощник. Я задам вам несколько вопросов и, исходя из ответов, выберу вам страну для отдыха. Для начала, выберите климат.",
        reply_markup=markup_weather)
    return 1


def help(update, context):
    update.message.reply_text(
        "Для начала нажмите кнопку start", reply_markup=markup_start)


def attractions_question(update, context):
    response = update.message.text
    response = response.lower()
    for i in slovar:
        if slovar[i]['Погода'] == response:
            slovar_counts[i] += 1
    update.message.reply_text(
        "Хотели бы Вы посещать достопримечательности во время вашей поездки?", reply_markup=markup_attractions)
    return 2


def beach_question(update, context):
    response = update.message.text
    response = response.lower()
    for i in slovar:
        if slovar[i]['Достопремечательности'] == response:
            slovar_counts[i] += 1
    update.message.reply_text(
        "Хотели бы Вы посещать пляж во время вашей поездки?", reply_markup=markup_beach)
    return 3


def ski_resort_question(update, context):
    response = update.message.text
    response = response.lower()
    for i in slovar:
        if slovar[i]['Пляж'] == response:
            slovar_counts[i] += 1
    update.message.reply_text(
        "Хотели бы Вы посещать горнолыжный курорт во время вашей поездки?", reply_markup=markup_ski_resort)
    return 4


def shopping_question(update, context):
    response = update.message.text
    response = response.lower()
    for i in slovar:
        if slovar[i]['Горнолыжный курорт'] == response:
            slovar_counts[i] += 1
    update.message.reply_text(
        "Планируете ли Вы ходить на шопинг во время вашей поездки?", reply_markup=markup_shopping)
    return 5


def type_of_recreation_question(update, context):
    response = update.message.text
    response = response.lower()
    for i in slovar:
        if slovar[i]['Шопинг'] == response:
            slovar_counts[i] += 1
    update.message.reply_text(
        "Какой вид отдыха вам предпочтительние?", reply_markup=markup_type_of_recreation)
    return 6


def transport_question(update, context):
    response = update.message.text
    response = response.lower()
    for i in slovar:
        if slovar[i]['Отдых'] == response:
            slovar_counts[i] += 1
    update.message.reply_text(
        "На чём планируете передвигаться по городу?", reply_markup=markup_transport)
    return 7


def children_question(update, context):
    response = update.message.text
    response = response.lower()
    for i in slovar:
        if slovar[i]['Транспорт'] == response:
            slovar_counts[i] += 1
    update.message.reply_text(
        "Поедите ли Вы с детьми?", reply_markup=markup_children)
    return 8


def result(update, context):
    response = update.message.text
    response = response.lower()
    for i in slovar:
        if slovar[i]['Дети'] == response:
            slovar_counts[i] += 1
    list_out_of_slovar = list(slovar_counts.items())
    list_out_of_slovar.sort(key=lambda x: x[1], reverse=True)
    city = list_out_of_slovar[0][0]
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": city
    })
    toponym = response.json()["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    delta = '0.05'
    spn = ",".join([delta, delta])
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"
    update.message.reply_text(f"""Как мне кажется, Вам подойдёт: {city} \n \n {slovar_result[city]['Информация']}""")
    context.bot.send_photo(
        update.message.chat_id,
        static_api_request
    )
    context.bot.send_photo(
        update.message.chat_id,
        slovar_result[city]['Картинка']
    )
    return 9


def stop(update, context):
    update.message.reply_text("Ну ладно(", reply_markup=markup_start)


def data(update, context):
    update.message.reply_text(time.asctime(time.localtime())[:11] + time.asctime(time.localtime())[20:])


def nowtime(update, context):
    update.message.reply_text(time.asctime(time.localtime())[11:20])


def main():
    updater = Updater('1776554257:AAHksnNJpdJmzoy60ZVziefcQLSQxh_cNW0', use_context=True)

    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, attractions_question, pass_user_data=True)],
            2: [MessageHandler(Filters.text, beach_question, pass_user_data=True)],
            3: [MessageHandler(Filters.text, ski_resort_question, pass_user_data=True)],
            4: [MessageHandler(Filters.text, shopping_question, pass_user_data=True)],
            5: [MessageHandler(Filters.text, type_of_recreation_question, pass_user_data=True)],
            6: [MessageHandler(Filters.text, transport_question, pass_user_data=True)],
            7: [MessageHandler(Filters.text, children_question, pass_user_data=True)],
            8: [MessageHandler(Filters.text, result, pass_user_data=True)],
            9: [MessageHandler(Filters.text, start)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("time", nowtime))
    dp.add_handler(CommandHandler("data", data))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
