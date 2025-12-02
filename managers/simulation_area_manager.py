import logging
logger = logging.getLogger(__name__)


class SimulationAreaManager:
    """
    SimulationAreaManager handles the simulation area boundaries.

    This class manages the dimensions of the table/area that the robot can move within,
    ensuring the robot stays within valid boundaries.

    Attributes:
        simulation_area (tuple[int, int]): The dimensions (width, height) of the simulation area.
    """
    simulation_area: tuple[int, int] = None

    def __init__(self, simulation_area: tuple[int, int] = None):
        """
        Initialise the SimulationAreaManager with the specified area dimensions.

        Args:
            simulation_area (tuple[int, int], optional): The total area that the robot can move within.
                                                         Must be a tuple of (width, height).

        Raises:
            Exception: If simulation_area is None or not properly configured in config.yaml.
        """
        logger.debug(f'Simulation area set to: {simulation_area}, type: {type(simulation_area)}')
        if simulation_area is None:
            logger.error('simulation_area is None.')
            raise Exception("Simulation area has not been set. Check config.yaml")
        self.set_simulation_area(simulation_area[0], simulation_area[1])

    def set_simulation_area(self, x: int, y: int):
        """
        Set the simulation area dimensions.

        Args:
            x (int): The width (x-coordinate) of the simulation area.
            y (int): The height (y-coordinate) of the simulation area.
        """
        logging.debug(f'Setting simulation area to: {x}, {y}')
        self.simulation_area = (x, y)

    def get_simulation_area(self):
        """
        Get the current simulation area dimensions.

        Returns:
            tuple[int, int]: The simulation area as (width, height).

        Raises:
            Exception: If simulation_area is None or not properly set.
        """
        if self.simulation_area is not None:
            logging.debug(f'Returning simulation area: {self.simulation_area}')
            return self.simulation_area
        logger.error('simulation_area is None.')
        raise Exception("Simulation area not set. Ensure config.yaml has been loaded.")
