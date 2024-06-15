import argparse
from webagent import WebAgent
import logging
from config import Config

def handle_command_line_args() -> dict:
    """
    Handle commandline args. Return agent task (or None)
    """

    parser = argparse.ArgumentParser(description="AI Task Agent")
    parser.add_argument('--task', type=str, help='Task to be executed')
    parser.add_argument('--profile-id', type=str, help='User profile ID to use')
    args = parser.parse_args()
    if args.task:
        print(f"Received task via command line: {args.task}")
    
    return {"task": args.task,
            "profile_id": args.profile_id}

def setup_logging(config: dict):
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
    config = Config()
    setup_logging(config.get_logging_config())
    logger = logging.getLogger(__name__)

    logger.info("Starting application")

    dict = handle_command_line_args()
    task = dict.get("task")
    profile_id = dict.get("profile_id")
    if not profile_id:
        profile_id = next(iter(config.user_profiles))
    profile = config.user_profiles[profile_id]

    if task:
        agent = WebAgent()
        agent.start(task, profile)