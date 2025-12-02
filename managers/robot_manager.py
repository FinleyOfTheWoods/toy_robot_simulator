import logging

from config import config

logger = logging.getLogger(__name__)

from managers.location_manager import LocationManager

class RobotManager:
    """
    RobotManager class orchestrates the robot controls such as movement and rotation.

    Attributes:
        location_manager (LocationManager): Manages the robot's location and movement logic.
    """

    location_manager = None
    def __init__(self, location_manager: LocationManager) -> None:
        """
        Initialise the RobotManager with a LocationManager instance.

        Args:
            location_manager (LocationManager): The location manager to control robot position.
        """
        self.location_manager = location_manager

    def move_robot(self) -> str:
        """
        Move the robot a set number of units in its current facing direction.

        Returns:
            str: A message indicating the robot moved and its new location.
        """
        if not self.location_manager.is_placed():
            return 'Robot not placed. Please place robot before moving.'
        if self.location_manager.move_robot(self.location_manager.location_facing, 1):
            return f'Robot moved. Location: {self.location_manager.location_x}, {self.location_manager.location_y}, facing {self.location_manager.location_facing}'
        return 'Robot movement failed. Stopped moving. See logs for more details.'

    def turn_robot(self, rotation: str) -> str:
        """
        Turn the robot 90 degrees in the specified direction.

        Args:
            rotation (str): The rotation direction ('LEFT' or 'RIGHT').

        Returns:
            str: A message indicating the robot's new facing direction.
        """
        logger.debug(f'Turning robot {rotation}. current facing: {self.location_manager.location_facing}')
        if self.location_manager.update_rotation(rotation):
            logger.debug(f'Robot now facing: {self.location_manager.location_facing}')
            return f'Robot is now facing {self.location_manager.location_facing}'
        return f'Failed to rotate to {rotation}. Robot is still facing {self.location_manager.location_facing}.'

    def place_robot(self, location: tuple[int, int, str]) -> str:
        """
        Place the robot at the specified location and direction.

        Args:
            location (tuple[int, int, str]): A tuple containing (x, y, direction).

        Returns:
            str: A message confirming the robot placement.
        """
        if self.location_manager.set_start_position(location):
            return f'Robot placed successfully at {location}.'
        return f'Robot placed at default location.'

    def report_robot_location(self) -> str:
        """
        Report the current location and facing direction of the robot.

        Returns:
            str: A formatted string with the robot's position in format:
                 '(x,y,direction)'
        """
        return self.location_manager.to_string()