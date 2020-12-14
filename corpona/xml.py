import io
from collections import defaultdict, OrderedDict
from typing import Any


class Item(OrderedDict):
    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text', '').strip()
        _dic = kwargs.pop('attributes', None)
        self.attributes = _dic if _dic is not None and isinstance(_dic, dict) else defaultdict(str)
        super(Item, self).__init__(*args, **kwargs)

    def filtered_attributes(self, ignore=()):
        return {k: v for k, v in self.attributes.items() if k not in ignore}

    def __repr__(self):
        return self.text

    def __getattr__(self, item: str) -> Any:
        return getattr(self, item, self.attributes.get(item.lower(), ''))

    @staticmethod
    def odict2item(value):
        d = Item()

        if isinstance(value, OrderedDict):
            for k, v in value.items():
                k = k.lower()

                if isinstance(v, OrderedDict):  # assumes v is also list of pairs
                    d[k] = [Item.odict2item(v)]
                elif isinstance(v, list):
                    d[k] = [Item.odict2item(_v) for _v in v]
                elif isinstance(v, str):
                    if k.startswith('@'):  # an attribute
                        d.attributes[k[1:]] = v
                    elif k.startswith('#'):  # the text element
                        d.text = v
            return d
        elif isinstance(value, str):
            d.text = value
            return d
        return value


class XML(Item):
    @classmethod
    def parse_xml(cls, filename, namespaces={}):
        import xmltodict
        with io.open(filename, 'r', encoding='utf-8') as fp:
            x = xmltodict.parse(fp.read(), process_namespaces=True if namespaces else False, namespaces=namespaces)

            root_keys = list(x.keys())

            if not root_keys:  # no root
                return cls()

            root = Item.odict2item(x[root_keys[0]])
            return cls(**{**root, **root.__dict__})
