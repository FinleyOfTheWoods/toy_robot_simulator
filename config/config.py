import yaml

import logging
logger = logging.getLogger(__name__)

class Config:
    """
    Config class loads configuration from config.yaml and manages application settings.

    This class reads the YAML configuration file, validates the settings, and provides
    access to simulation parameters such as logging level, simulation area, and robot
    starting position.

    Attributes:
        config_file (str): Path to the configuration file. Defaults to 'config.yaml'.
        logging_level (int): The logging level for the application.
        simulation_area (tuple[int, int]): The dimensions of the simulation area as (width, height).
        start_position (tuple[int, int, str]): The robot's starting position as (x, y, direction).
    """
    config_file = 'config.yaml'
    logging_level = logging.INFO
    simulation_area: tuple[int, int] = None
    start_position: tuple[int, int, str] = None

    @classmethod
    def check_config(cls, simulation_area: tuple[int, int], start_position: tuple[int, int, str]) -> None:
        """
        Validate the configuration parameters.

        Ensures that simulation_area and start_position are properly set and have
        the correct types.

        Args:
            simulation_area (tuple[int, int]): The total area that the robot can move within.
            start_position (tuple[int, int, str]): The start position of the robot as (x, y, direction).

        Raises:
            Exception: If simulation_area is None or not a tuple.
            Exception: If start_position is None or not a tuple.
        """
        logging.debug(
            f'Checking config. simulation_area: {simulation_area} type: {type(simulation_area)}, start_position: {start_position} type: {type(start_position)}')

        if simulation_area is None:
            raise Exception("Invalid config. Simulation area is not set.")
        if not isinstance(simulation_area, tuple):
            raise Exception("Invalid config. Simulation area is not of type tuple[int, int]")

        if start_position is None:
            raise Exception("Invalid config. Start position is not set")
        if not isinstance(start_position, tuple):
            raise Exception("Invalid config. Start position is not of type tuple[int, int, str]")
        logging.debug('Config is valid.')
        return None

    @classmethod
    def set_logging_level(cls, level: str) -> None:
        """
        Set the logging level for the application based on the configuration.

        Converts a string logging level (e.g., 'DEBUG', 'INFO') to the corresponding
        logging constant and applies it to the root logger.

        Args:
            level (str): The logging level as a string ('DEBUG', 'INFO', 'WARNING', 'ERROR').
                        Defaults to 'INFO' if an unrecognized value is provided.
        """
        match level:
            case 'DEBUG':
                cls.logging_level = logging.DEBUG
            case 'INFO':
                cls.logging_level = logging.INFO
            case 'WARNING':
                cls.logging_level = logging.WARNING
            case 'ERROR':
                cls.logging_level = logging.ERROR
            case _:
                cls.logging_level = logging.INFO
        logging.getLogger().setLevel(level=cls.logging_level)

    def __init__(self) -> None:
        """
        Initialise the Config by loading and parsing the YAML configuration file.

        Reads config.yaml, extracts simulation_area and start_position, validates
        the configuration, and sets the logging level.

        Raises:
            Exception: If configuration validation fails.
            yaml.YAMLError: If there's an error whilst parsing the YAML file.

        Note:
            The application will exit with code 1 if configuration loading or validation fails.
        """
        with open(self.config_file) as stream:
            try:
                logging.info('Loading config from YAML file. ')
                config = yaml.safe_load(stream)

                self.set_logging_level(config['logging_level'])

                simulation_area_config = config['simulation_area']

                simulation_area = (
                    simulation_area_config['x'],
                    simulation_area_config['y']
                )

                start_position_config = config['start_position']
                start_position = (
                    start_position_config['x'],
                    start_position_config['y'],
                    start_position_config['direction']
                )
                try:
                    self.check_config(simulation_area, start_position)
                except Exception as e:
                    logger.error('Failed to load config. Exiting...')
                    logger.error(e)
                    exit(1)

                self.simulation_area = simulation_area
                self.start_position = start_position
                logging.debug(f'Config set to logging level: {self.logging_level}, simulation_area: {self.simulation_area}, start_position: {self.start_position}')
            except yaml.YAMLError as yaml_e:
                logger.error('Error whilst loading config file. Exiting...')
                logger.error(yaml_e)
                exit(1)
