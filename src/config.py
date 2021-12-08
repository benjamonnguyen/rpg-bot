import yaml
import logging


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


configs = read_yaml('../config.yaml')

logging.info('Loaded config file for {} environment.'.format(configs['APP']['ENVIRONMENT']))
