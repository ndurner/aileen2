import argparse
from webagent import WebAgent

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

if __name__ == "__main__":
    task = handle_command_line_args()
    if task:
        agent = WebAgent()
        agent.start(task)