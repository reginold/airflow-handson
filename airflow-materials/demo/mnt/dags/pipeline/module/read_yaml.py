import yaml

YAML_FILE = "/usr/local/airflow/dags/config/param.yaml"


def read_yaml():
    """Read the conig yaml file
    Raises:
        exc: raise NotFoundFile error

    Returns:
        [yaml]: loaded yaml file
    """
    # read the config yaml
    with open(YAML_FILE, "r") as config:
        try:
            config_file = yaml.safe_load(config)
        except yaml.YAMLError as exc:
            raise exc

    return config_file
