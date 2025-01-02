import inspect
from typing import Any
from pedant_killer.database.database import database_logger


class CoreMethod:
    @staticmethod
    def checking_for_empty_attributes(**kwargs: Any) -> [dict[Any, Any] | None]:
        sorted_dictionary = {key: value for key, value in kwargs.items() if value is not None}

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name

        if not sorted_dictionary:
            database_logger.info(f'В метод {caller_name} не переданы аргументы')
            return None

        database_logger.info(f'В метод {caller_name} передано {len(sorted_dictionary)} аргументов')
        return sorted_dictionary

    @staticmethod
    def checking_correctness_identifier(*values: Any) -> bool:
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name

        if not all(isinstance(identifier, int) and identifier > 0 for identifier in values):
            database_logger.error(f'Некорректный идентификатор: {values} переданный в функцию {caller_name}')
            return False

        return True

    @staticmethod
    def checking_correctness_type_str(*values: Any) -> bool:
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name
        result = all(isinstance(value, str) for value in values)

        if not result:
            database_logger.info(f'Некорректные данные: {values} переданные в функцию {caller_name}')
            return False

        return True

    @staticmethod
    def checking_correctness_type_int(*values: Any) -> bool:
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name
        result = all(isinstance(value, int) for value in values)

        if not result:
            database_logger.info(f'Некорректные данные: {values} переданные в функцию {caller_name}')
            return False

        return True
