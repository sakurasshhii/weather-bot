# Кнопки общего меню
MAIN_MENU_RU: dict[str, str] = {
    '/start': 'Запуск бота',
    '/help': 'Информация о возможностях бота',
    '/weather_in_location': 'Погода по местоположению',
    '/get_weather': 'Погода по времени...'
}

# Текстовый ответ на кнопки общего меню
MENU_ANS_RU: dict[str, str] = {
    '/start': 'hi!',
    '/help': 'i cant help myself either...',
    '/get_weather': 'Выберите временной промежуток:',
    '/unexpected_message': 'unknown bla-bla'
}

# Запрос и обработка геопозиции
WEATHER_RU: dict[str, str] = {
    'req_loc_txt': 'Для определения погоды требуются данные о вашем местоположении.',
    'req_loc_btn': 'Отправить геопозицию',
    'other_loc_btn': 'Определить вручную',
    'other_loc': 'Введите название города...'
}

WEATHER_LOC: dict[str, str] = {
    'req_loc_txt': 'Для определения погоды требуются данные о вашем местоположении.',
    'req_loc_btn': 'Отправить геопозицию'
}

WEATHER_DURATION: dict[str, str] = {
    'current': 'Сейчас',
    'today': 'Сегодня',
    'week': 'На неделю'
}