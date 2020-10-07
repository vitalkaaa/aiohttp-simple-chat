import yaml

config_path = 'config/chat.yaml'


def get_config(path):
    with open(path) as f:
        _config = yaml.safe_load(f)
    return _config


config = get_config(config_path)
