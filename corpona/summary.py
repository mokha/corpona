from collections import defaultdict
from tqdm import tqdm

def strtype(v): return str(type(v).__name__)


def summarize(data, show_progress=True):
    summary = defaultdict(list)
    _t = tqdm
    if show_progress is False:
        _t = list
    if isinstance(data, dict):
        for k, v in _t(data.items()):
            _v = summarize(v, show_progress=False)
            summary[k] = _v
    elif isinstance(data, str):
        return [strtype(data), ]
    elif isinstance(data, list):
        for v in _t(data):
            _v = summarize(v, show_progress=False)
            for __v in _v:
                if __v not in summary[strtype(v)]:
                    summary[strtype(v)].append(__v)
    else:
        return [strtype(data), ]

    return [dict(summary), ]
