import argparse
import logging

from config.config import Config
from managers.location_manager import LocationManager
from managers.robot_manager import RobotManager
from managers.simulation_area_manager import SimulationAreaManager

if __name__ == '__main__':
    # Set the initial logging level to the default of INFO
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)



    # Allows the logging level to be set via command line argument. to enable early debugging before config is loaded.
    parser = argparse.ArgumentParser(description='Toy robot simulator.')
    parser.add_argument('--log-level', help='Set logging level. Default is INFO (overrides config.yaml).', default='INFO')
    args = parser.parse_args()
    if args.log_level is not None:
        level = getattr(logging, args.log_level.upper())
        logging.getLogger().setLevel(level=level)

    logger.info('Starting simulation...')


    # Load config from the YAML file.
    config = Config()
    logger.info(f'Logging level set to: {config.logging_level}')

    # Load simulation area from config, this is the total area that the robot can move within.
    simulation_manager = SimulationAreaManager(config.simulation_area)
    logger.info(f'Simulation area set to: {simulation_manager.get_simulation_area()}')


    # Load the start position from config, this is the position the robot starts at.
    location_manager = LocationManager(simulation_manager.get_simulation_area())

    # Initialise RobotManager.
    robot_manager = RobotManager(location_manager)

    # List of available commands for application to use, presented to user on start up or when HELP command is given.
    available_commands = 'Available commands: PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT | STOP | HELP'

    # Start of user input monitoring. Listening for commands.
    print('Toy Robot Simulation')
    print(available_commands)
    print("-" * 70)


    # Command loop. Runs application until the STOP command is given or KeyboardInterrupt is received.
    running = True
    while running:
        try:
            command = input("> ").strip().upper()
            if not command:
                continue

            if command == 'STOP':
                running = False
                logger.info('Exiting simulation...')
                print(f'Robots final location: {robot_manager.report_robot_location()}')
                print('Exiting simulation...')
                break
            elif command.startswith('PLACE'):
                # NB: Currently only supports PLACE X,Y,F (no spaces between values).
                # Would require additional logic to handle commands with spaces.
                logger.debug('Processing PLACE command...')
                print('Processing PLACE command...')
                try:
                    parts = command.split()
                    if len(parts) != 2:
                        raise Exception('Invalid PLACE command. Please provide X,Y,F coordinates separated by commas.')
                    coords = parts[1].split(',')
                    if len(coords) != 3:
                        raise Exception('Invalid PLACE command. Please provide X,Y,F coordinates separated by commas.')
                    x, y, direction = coords
                    print(location_manager.set_start_position((int(x), int(y), direction)))
                except Exception as e:
                    logger.error(f'Error whilst processing PLACE command: {e}')
                    print(e)
                    continue
            elif command == 'REPORT':
                logger.debug('Processing REPORT command...')
                print('Processing REPORT command...')
                print(robot_manager.report_robot_location())
            elif command == 'LEFT':
                logger.debug('Processing LEFT command...')
                print('Processing LEFT command...')
                print(robot_manager.turn_robot('LEFT'))
            elif command == 'RIGHT':
                logger.debug('Processing RIGHT command...')
                print('Processing RIGHT command...')
                print(robot_manager.turn_robot('RIGHT'))
            elif command == 'MOVE':
                logger.debug('Processing MOVE command...')
                print('Processing MOVE command...')
                print(robot_manager.move_robot())
            elif command == 'HELP':
                logger.debug('Processing HELP command...')
                print(available_commands)
            else:
                logger.warning(f'Unknown command: {command}')
                print(f'Unknown command: {command}. {available_commands}')
        except EOFError:
            # Handles EOFError when user presses Ctrl+D (Unix) or Ctrl+Z (windows).
            running = False
            logger.info('Exiting simulation...')
        except KeyboardInterrupt:
            # Handles KeyboardInterrupt when user presses Ctrl+C.
            running = False
            print('\nKeyboard interrupt received. Exiting simulation...')
        except Exception as e:
            # Handles any other unexpected error.
            print('\nReceived unexpected error. Please see logs for more details. Exiting simulation...')
            logger.error(f'Error whilst processing. Exiting simulation...')
            logger.error(e)
            exit(1)
    print('Simulation complete.')
    logger.info('Simulation complete.')
