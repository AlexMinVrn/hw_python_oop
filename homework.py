from dataclasses import asdict, dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> None:
        """Напечатать информационное сообщение о тренировке."""
        return (self.MESSAGE.format(**asdict(self)))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Method is implemented in children')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_COEF_CALORIE_1: float = 18
    RUN_COEF_CALORIE_2: float = 20
    H_IN_MIN: float = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return (
            (
                self.RUN_COEF_CALORIE_1 * self.get_mean_speed()
                - self.RUN_COEF_CALORIE_2
            )
            * self.weight / self.M_IN_KM * self.duration * self.H_IN_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SW_COEF_CALORIE_1: float = 0.035
    SW_COEF_CALORIE_2: float = 0.029
    H_IN_MIN: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        return (
            (
                self.SW_COEF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.SW_COEF_CALORIE_2
                * self.weight
            )
            * self.duration * self.H_IN_MIN
        )


class Swimming(Training):
    """Тренировка: плавание."""
    SWIM_COEF_CALORIE_1: float = 1.1
    SWIM_COEF_CALORIE_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        return (
            (
                self.get_mean_speed() + self.SWIM_COEF_CALORIE_1
            )
            * self.SWIM_COEF_CALORIE_2 * self.weight
        )


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in training_dict:
        raise KeyError(f'{workout_type} - Такой тренировки не существует')
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
