from typing import Dict, List

from src.config import configs


def validate_interval_settings(interval_settings: Dict[str, int]):
    required_keys = ['pomodoro', 'short_break', 'long_break', 'intervals']
    check_if_all_keys_exist(interval_settings, required_keys)
    max_val = configs['PARAMETER']['MAX_INTERVAL_SETTINGS_VALUE']
    for key in required_keys:
        if interval_settings[key] and (0 >= interval_settings[key] > max_val):
            raise ValueError(f'interval_setting {key} out of bounds.')


def check_if_all_keys_exist(dictionary: Dict, keys: List[str]):
    for key in keys:
        try:
            dictionary[key]
        except KeyError:
            raise KeyError(f'Dictionary does not contain key: {key}')
