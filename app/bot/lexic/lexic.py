# Меню бота
MAIN_MENU_RU: dict[str, str] = {
    '/start': 'Запуск бота',
    '/help': 'Информация о возможностях бота'
    # '/weather_in_location': 'Погода по местоположению',
    # '/get_weather': 'Погода по времени...'
}

# Текстовый ответ на кнопки меню
MENU_ANS_RU: dict[str, str] = {
    '/start': 'hi!',
    '/help': 'В этом чате ты можешь узнать прогноз погоды '
        'в текущий момент/ на целый день/ на неделю. Вот мои команды:\n\n'
        '/start_weather — отправить погоду сейчас/сегодня/на неделю',
    '/unexpected_message': 'unknown bla-bla'
}

# Запрос и обработка геопозиции
WEATHER_RU: dict[str, str] = {
    'req_loc_txt': 'Для определения погоды требуются данные о вашем местоположении.',
    'req_loc_btn': 'Отправить геопозицию',
    'other_loc_btn': 'Определить вручную',
    'other_loc': 'Введите название города...',
    'got_loc': 'Геопозиция получена',
    'pick_dur': 'Смотрим погоду...',
    'weather_ask': 'Щас-щас, секундочку...'
}

WEATHER_LOC_BTN: dict[str, str] = {
    'ask_city': 'Определить вручную',
    'ask_location': 'Отправить геопозицию'
}

WEATHER_DURATION_BTN: dict[str, str] = {
    'current': 'Сейчас',
    'today': 'Сегодня',
    'week': 'На неделю'
}
