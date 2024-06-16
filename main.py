import argparse
from webagent import WebAgent
import mylog
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

if __name__ == "__main__":
    config = Config()
    mylog.setup_logging()

    logger = mylog.getLogger(__name__)
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