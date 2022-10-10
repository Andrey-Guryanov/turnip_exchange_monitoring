import yaml
import os.path

def load_settings(settings_path='settings.yaml'):
    if not os.path.exists(settings_path):
        settings_path=f'../{settings_path}'
    with open(settings_path) as file_settings:
        settings = yaml.load(file_settings, Loader=yaml.FullLoader)
    return settings
