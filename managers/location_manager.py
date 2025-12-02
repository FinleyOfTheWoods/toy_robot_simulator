import logging
logger = logging.getLogger(__name__)



class LocationManager:
    """
    LocationManager handles the location, movement, and rotation of the robot.

    This class manages the robot's position on the table, validates movements to prevent
    the robot from falling off, and handles directional changes (rotation).

    Attributes:
        simulation_area (tuple[int, int]): The dimensions (width, height) of the simulation area.
        location_x (int): The current x-coordinate of the robot.
        location_y (int): The current y-coordinate of the robot.
        location_facing (str): The direction the robot is facing (NORTH, EAST, SOUTH, WEST).
        available_directions (list[str]): Valid directions for robot orientation.
    """

    available_directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']

    def __init__(self, simulation_area: tuple[int, int]) -> None:
        """
        Initialise the LocationManager with a simulation area and starting location.

        Args:
            simulation_area (tuple[int, int]): The dimensions of the table as (width, height).
        """
        self.simulation_area = simulation_area
        self.location_x = None
        self.location_y = None
        self.location_facing = None

    @classmethod
    def check_location(cls, simulation_area, location: tuple) -> bool:
        """
        Check if a location is within the simulation area boundaries.

        This prevents the robot from moving outside the valid table area.

        Args:
            simulation_area (tuple[int, int]): The dimensions of the simulation area.
            location (tuple[int, int]): The location to validate as (x, y).

        Returns:
            bool: True if the location is valid, False otherwise.
        """
        logger.debug(f'Checking location: {location}')
        if location[0] < 0 or location[0] > simulation_area[0] or location[1] < 0 or location[1] > simulation_area[1]:
            logger.warning(f'Location {location} is outside of simulation area {simulation_area}. Rejecting move.')
            return False
        return True

    @classmethod
    def handle_rotation(cls, available_directions: list, rotation: str, current_direction: str = None) -> str:
        """
        Handle the rotation of the robot when LEFT or RIGHT command is given.

        Rotates the robot 90 degrees clockwise (RIGHT) or counter-clockwise (LEFT).

        Args:
            available_directions (list[str]): List of valid direction strings.
            rotation (str): The rotation direction ('LEFT' or 'RIGHT').
            current_direction (str, optional): The robot's current facing direction.

        Returns:
            str: The new direction after rotation.

        Raises:
            Exception: If rotation is not 'LEFT' or 'RIGHT'.
        """
        rotation_factor = 0
        match rotation:
            case 'RIGHT': rotation_factor = 1
            case 'LEFT': rotation_factor = -1
            case _: raise Exception(f'Invalid rotation direction. Must be LEFT or RIGHT. Received: {rotation}')

        logger.debug(f'Requested rotation: {rotation}, Rotation factor set to: {rotation_factor}')
        new_direction = available_directions[(available_directions.index(current_direction) + rotation_factor) % len(available_directions)]
        logger.debug(f'Rotating right. current direction: {current_direction}, new direction: {new_direction}')

        return new_direction

    @classmethod
    def handle_move(cls, current_location: tuple[int, int], direction: str, distance: int = 1) -> tuple[int, int]:
        """
        Calculate the new position after moving in a specified direction.

        This is called when the MOVE command is given. It calculates the new coordinates
        without actually updating the robot's position.

        Args:
            current_location (tuple[int, int]): The current location as (x, y).
            direction (str): The direction to move (NORTH, EAST, SOUTH, WEST).
            distance (int, optional): The distance to move in units. Defaults to 1.

        Returns:
            tuple[int, int]: The new calculated position as (x, y).
        """
        new_x, new_y = current_location
        match direction:
            case 'NORTH':
                new_y += distance
            case 'EAST':
                new_x += distance
            case 'SOUTH':
                new_y -= distance
            case 'WEST':
                new_x -= distance
            case _:
                logger.error(f'Invalid direction: {direction}. Must be one of {cls.available_directions}')
                return current_location
        logger.debug(f'Moving in direction {direction} by {distance} units.')
        return new_x, new_y

    def set_start_position(self, location: tuple[int, int, str] = None) -> bool:
        """
        Set or reset the robot's position (used for PLACE command).

        If no location is provided, defaults to (0, 0, NORTH).

        Args:
            location (tuple[int, int, str], optional): The position as (x, y, direction).
                                                       Defaults to (0, 0, 'NORTH') if None.
        """
        logger.debug('Setting robot start position.')
        if location is not None:
            logger.debug(f'Setting robot start position to: {location}')
            self.location_x, self.location_y = location[0], location[1]
            self.location_facing = location[2]
            return True
        logger.debug('No start position provided.')
        return False

    def update_rotation(self, rotation) -> bool:
        """
        Update the robot's facing direction based on the rotation command.

        Args:
            rotation (str): The rotation direction ('LEFT' or 'RIGHT').
        """
        try:
            logger.debug(f'Updating robot rotation to {rotation}')
            self.location_facing = self.handle_rotation(self.available_directions, rotation, self.location_facing)
            return True
        except Exception as e:
            logger.error(f'Error updating robot rotation: {e}')
            return False


    def move_robot(self, direction: str = None, distance: int = 1) -> bool:
        """
        Move the robot in the specified direction by a given distance.

        Validates the move to ensure the robot stays within the simulation area boundaries.
        If the move causes the robot to fall off, the move is rejected and the robot
        stays in its current position.

        Args:
            direction (str, optional): The direction to move. Should match the robot's current facing.
            distance (int, optional): The number of units to move. Defaults to 1.

        Returns:
            tuple[int, int]: The robot's position after the move attempt as (x, y).
        """
        new_x, new_y = self.handle_move((self.location_x, self.location_y), direction, distance)
        if (new_x, new_y) == (self.location_x, self.location_y):
            logger.warning(f'Robot attempted to move {distance} units in direction {direction} but no change was made. Current location: ({self.location_x},{self.location_y})')
            return False
        logger.debug(f'Robot attempted to move {distance} units in direction {direction}. New location: ({new_x},{new_y})')
        if self.check_location(self.simulation_area, (new_x, new_y)):
            self.location_x, self.location_y = new_x, new_y
            logger.debug(f'Robot moved {distance} units in direction {direction}. New location: ({self.location_x},{self.location_y})')
            return True
        else:
            logger.error(f'Robot attempted to move outside of simulation area ({self.simulation_area}). Current location: ({self.location_x},{self.location_y})')
            return False

    def to_string(self) -> str:
        """
        Report the current location and facing direction of the robot.

        Returns:
            str: A formatted string with the robot's position in format:
                 '(x,y,direction)'
        """
        return f'({self.location_x},{self.location_y},{self.location_facing})'

    def is_placed(self):
        logger.debug(f'Checking if robot is placed. location_x: {self.location_x}, location_y: {self.location_y}: {self.location_x and self.location_y is not None}')
        return self.location_x is not None and self.location_y is not None
