import unittest

from managers.location_manager import LocationManager
from managers.robot_manager import RobotManager

class TestRobotSimulator(unittest.TestCase):
    """
    Test cases for the robot simulator.
    Tests three scenarios specified in the README.
    """

    def setUp(self):
        """
        setUp method to instantiate LocationManager, SimulationAreaManager and RobotManager before each test method.
        """
        self.simulation_area = (5, 5)
        self.default_start_position = (0, 0, 'NORTH')

    def _create_robot(self):
        location_manager = LocationManager(self.simulation_area, self.default_start_position)
        return RobotManager(location_manager)

    def test_case_place_move_report(self):
        """
        Test case A: PLACE 0,0,NORTH; MOVE; REPORT
        Expected result: (0,1,NORTH)
        """
        robot = self._create_robot()

        # Place 0,0,NORTH
        robot.place_robot((0, 0, 'NORTH'))
        # Move robot
        robot.move_robot()
        # Report robot position
        result = robot.report_robot_location()

        self.assertEqual(result, '(0,1,NORTH)', f'Expected "(0,1,NORTH)", got {result} instead."')

    def test_case_place_left_report(self):
        """
        Test case B: PLACE 0,0,NORTH; LEFT; REPORT
        Exported result: (0,0,WEST)
        """
        robot = self._create_robot()
        # Place 0,0,NORTH
        robot.place_robot((0, 0, 'NORTH'))
        # Turn robot left
        robot.turn_robot('LEFT')
        # Report robot position
        result = robot.report_robot_location()

        self.assertEqual(result, '(0,0,WEST)', f'Expected "(0,0,WEST)", got {result} instead."')

    def test_case_place_move_move_left_move_report(self):
        """
        Test case C: PLACE 1,2,EAST; MOVE; MOVE; LEFT; MOVE; REPORT
        Expected result: (3,3,NORTH)
        """
        robot = self._create_robot()
        # Place robot at (1,2,EAST)
        robot.place_robot((1, 2, 'EAST'))
        # Move the robot twice
        robot.move_robot()
        robot.move_robot()
        # Turn the robot left
        robot.turn_robot('LEFT')
        # Move the robot once
        robot.move_robot()
        # Report robot position
        result = robot.report_robot_location()

        self.assertEqual(result, '(3,3,NORTH)', f'Expected "(3,3,NORTH)", got {result} instead."')
