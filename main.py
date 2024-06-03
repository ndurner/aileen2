import argparse

def handle_command_line_args():
    parser = argparse.ArgumentParser(description="AI Task Agent")
    parser.add_argument('--task', type=str, help='Task to be executed')
    args = parser.parse_args()
    if args.task:
        print(f"Received task via command line: {args.task}")

if __name__ == "__main__":
    handle_command_line_args()
