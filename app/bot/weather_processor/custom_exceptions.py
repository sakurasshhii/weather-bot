class WeatherException(Exception):
    def __init__(self, name, *args: object) -> None:
        self._name = name
        self._args = args

    def __str__(self) -> str:
        txt = f'Произошла ошибка во время выполнения функции {self._name}'
        if self._args:
            txt += f'; {self._args.__repr__()}'
        return txt
