import re
from datetime import datetime, timedelta

def _parse_timestamp(timestamp):
    return datetime.strptime(timestamp, '%H:%M:%S,%f')

def process(content: str):
    entries = content.strip().split('\n\n')
    result = []
    previous_end_time = None

    for entry in entries:
        lines = entry.split('\n')
        if len(lines) >= 3:
            time_range = lines[1]
            start_time_str, end_time_str = time_range.split(' --> ')
            start_time = _parse_timestamp(start_time_str)
            end_time = _parse_timestamp(end_time_str)

            if previous_end_time and (start_time - previous_end_time).total_seconds() > 3:
                result.append('\n')

            payload = ' '.join(lines[2:])
            result.append(payload.strip())
            previous_end_time = end_time

    return '\n'.join(result)
