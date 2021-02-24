from collections import Counter
from itertools import groupby
from tqdm import tqdm


def strtype(v): return str(type(v).__name__)


class Container:
    def __init__(self, data):
        self.data = data
        self.type = strtype(data)
        self.contains = []
        self.inner_content = []

        if isinstance(data, dict):
            values = data.items()
            self.contains = [(v[0], strtype(v[1]),) for v in values]
            self.inner_content = [Container(v[1]) for v in values if strtype(v[1]) in ['dict', 'list', 'tuple', 'set']]
        elif isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set):
            self.contains = [strtype(v) for v in data]
            self.inner_content = [Container(v) for v in self.data if strtype(v) in ['dict', 'list', 'tuple', 'set']]
        else:  # do nothing
            pass

        self.contains_counter = Counter(self.contains)

    def __repr__(self, depth=0, _indent=4, content_only=False, show_progress=True):
        _output = ''
        if not content_only:
            _output += " " * _indent * depth + f"{self.type}:\n"

        _t = tqdm
        if show_progress is False:
            _t = list

        for k, v in _t(self.contains_counter.items()):
            if isinstance(k, tuple):  # a dictionary
                _k, _type = k
                _output += " " * _indent * (depth + 1) + f"{_k}:"
                if _type in ['dict', 'list', 'tuple', 'set']:
                    _output += "\n" + Container(self.data[_k]).__repr__(depth + 2, content_only=True,
                                                                        show_progress=False)
                else:
                    _output += f" {_type}\n"
            else:
                _output += " " * _indent * (depth + 1) + f"{k}: ({v})\n"
                _inner_containers = [_i for _i in self.inner_content if _i.type == k]
                if len(_inner_containers) > 0:
                    _inner_containers = groupby(sorted(_inner_containers, key=lambda __k: __k.type),
                                                key=lambda __k: __k.type)  # group them based on their type
                    for _k, groups in _inner_containers:
                        # group them based on their content type
                        _inner_inner_containers = groupby(sorted(groups, key=lambda __k: __k.contains),
                                                          key=lambda __k: __k.contains)
                        for __k, __groups in _inner_inner_containers:
                            _data = list(__groups)
                            _output += " " * _indent * (depth + 2) + f"{len(_data)}:\n"
                            _output += _data[0].__repr__(depth=depth + 2, content_only=True, show_progress=False)

        return _output


def summarize(data):
    return Container(data).__repr__(0)
