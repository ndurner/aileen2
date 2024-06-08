import argparse
from webagent import WebAgent
import logging
from config import Config

def handle_command_line_args() -> str:
    """
    Handle commandline args. Return agent task (or None)
    """

    parser = argparse.ArgumentParser(description="AI Task Agent")
    parser.add_argument('--task', type=str, help='Task to be executed')
    args = parser.parse_args()
    if args.task:
        print(f"Received task via command line: {args.task}")
    
    return args.task

def setup_logging():
    config = Config().get_logging_config()
    logging.basicConfig(
        level=logging.getLevelName(config['level']),
        format=config['format'],
        datefmt=config['datefmt'],
        filename=config['filename'],
        filemode=config['filemode']
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(config['format'])
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting application")

    task = handle_command_line_args()
    if task:
        agent = WebAgent()
        agent.start(task)