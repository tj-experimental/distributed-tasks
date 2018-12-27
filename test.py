# datetime format.
# YYYY-MM-dd-hh:mm:ss

from datetime import datetime

def _parse_datetime(datetime_string, format='%Y-%m-%d-%H:%M:%S'):
    return datetime.strptime(datetime_string, format)


def _get_total_time(start_datetime_string, end_datetime_string):
    start_datetime = _parse_datetime(start_datetime_string)
    end_datetime = _parse_datetime(end_datetime_string)

    return (end_datetime - start_datetime).total_seconds()

def _parse_log_items(start, end):
    print(start, end)
    return _get_total_time(start[-1], end[-1])

def _get_chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]

# log is the file contents as one large string:
def solution(log):
    lines = log.split('\n')
    # Function name, context, Timestamp
    log_information = [v.split(':', maxsplit=2) for v in lines if v]
    functions = set([log_info[0] for log_info in log_information])

    # function_name: {
    #   'maximum_execution_time': '5s',
    #   'minimum_execution_time': '1s',
    #   'average_execution_time': '3s',
    # }

    return_value = {}
    for function in functions:
        func_items = [log_item for log_item in log_information if log_item[0] == function]

        func_calls = [
            _parse_log_items(*log_item)
            for log_item in _get_chunks(
                sorted(
                    func_items,
                    key=lambda item: _parse_datetime(item[-1])
                ),
                2,
            )
        ]
        min_exec_time = min(func_calls)
        max_exec_time = max(func_calls)
        average_exec_time = sum(func_calls) / len(func_calls)

        return_value[function] = {
            'maximum_execution_time': '%.0fm' % (max_exec_time/60),
            'minimum_execution_time': '%.0fm' % (min_exec_time/60),
            'average_execution_time': '%.0fm' % (average_exec_time/60),
        }

    return return_value


if __name__ == '__main__':
    print(solution(open('test.log', 'r').read()))
