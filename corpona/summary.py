from collections import defaultdict


def strtype(v): return str(type(v).__name__)


def summarize(data):
    summary = defaultdict(list)

    if isinstance(data, dict):
        for k, v in data.items():
            _v = summarize(v)
            summary[k] = _v
    elif isinstance(data, str):
        return [strtype(data), ]
    elif isinstance(data, list):
        for v in data:
            _v = summarize(v)
            for __v in _v:
                if __v not in summary[strtype(v)]:
                    summary[strtype(v)].append(__v)
    else:
        return [strtype(data), ]

    return [dict(summary), ]
