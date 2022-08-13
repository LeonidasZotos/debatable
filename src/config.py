import yaml

with open("settings.yaml", "r") as f:
    settings = yaml.load(f, Loader=yaml.FullLoader)