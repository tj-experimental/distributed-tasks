# datetime format.
# YYYY-MM-dd-hh:mm:ss
from collections import defaultdict
from datetime import datetime

def _parse_datetime(datetime_string, format='%Y-%m-%d-%H:%M:%S'):
    return datetime.strptime(datetime_string, format)


def _get_total_time(start_datetime_string, end_datetime_string):
    start_datetime = _parse_datetime(start_datetime_string)
    end_datetime = _parse_datetime(end_datetime_string)

    return (end_datetime - start_datetime).total_seconds()

def _parse_log_items(start, end):
    return (
        _get_total_time(start.split(':', maxsplit=2)[-1], end.split(':', maxsplit=2)[-1])
    )

def _get_chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]

# log is the file contents as one large string:
def solution(log):
    stats = defaultdict(list)
    lines = sorted(log.splitlines(), key=lambda item: item.split(':', maxsplit=2)[0])
    # Function name, context, Timestamp
    log_information = [
        (log_item[0], _parse_log_items(*log_item)) for log_item in
        _get_chunks(lines, size=2)
    ]

    for func_name, duration in log_information:
        stats[func_name].append(duration)

    # function_name: {
    #   'maximum_execution_time': '5s',
    #   'minimum_execution_time': '1s',
    #   'average_execution_time': '3s',
    # }

    return_value = {}
    for func_name, values in stats.items():
        min_exec_time = min(values)
        max_exec_time = max(values)
        average_exec_time = sum(values) / len(values)

        return_value[func_name] = {
            'maximum_execution_time': '%.0fm' % (max_exec_time/60),
            'minimum_execution_time': '%.0fm' % (min_exec_time/60),
            'average_execution_time': '%.0fm' % (average_exec_time/60),
        }

    return return_value


if __name__ == '__main__':
    print(solution(open('test.log', 'r').read()))
