import io
from collections import defaultdict, OrderedDict


class Item(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.text = kwargs.get('text', '').strip()
        _dic = kwargs.get('attributes', None)
        self.attributes = _dic if _dic is not None and isinstance(_dic, dict) else defaultdict(str)

    def filtered_attributes(self, ignore=()):
        return {k: v for k, v in self.attributes.items() if k not in ignore}

    def __repr__(self):
        return self.text

    def __getattr__(self, item):
        item = item.lower()
        return self.attributes.get(item, '')


class XML:
    def __init__(self, *args, **kwargs):
        self.elements = kwargs.pop('elements', [])  # the main holder for all elements

        # set any additional passed keywords
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def odict2item(value):
        if isinstance(value, OrderedDict):
            d = Item()
            for k, v in value.items():
                if isinstance(v, OrderedDict):  # assumes v is also list of pairs
                    d[k.lower()] = d[k] = [XML.odict2item(v)]
                elif isinstance(v, list):
                    d[k.lower()] = d[k] = [XML.odict2item(_v) for _v in v]
                elif isinstance(v, str):
                    if k.startswith('@'):  # an attribute
                        d.attributes[k[1:]] = v
                    elif k.startswith('#'):  # the text element
                        d.text = v
            return d
        elif isinstance(value, str):
            d = Item()
            d.text = value
            return d
        return value

    @staticmethod
    def parse_file(filename):
        import xmltodict
        with io.open(filename, 'r', encoding='utf-8') as fp:
            namespaces = {'http://www.w3.org/XML/1998/namespace': 'xml', }
            x = xmltodict.parse(fp.read(), process_namespaces=True, namespaces=namespaces)
            r = XML.odict2item(x['r'])
            lang = r.attributes.get('xml:lang')
            g_xml = XML(lang=lang)
            g_xml.elements = r['e'] if 'e' in r else []
            return g_xml
