import yaml


def readYML(path):
    #print(f"[READ-YML] READING {path}")
    with open(path) as stream:
        try:
            data = yaml.safe_load(stream)
            return data 
        except yaml.YAMLError as exc:
            print(exc)