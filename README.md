# corpona
corpona is a library for processing corpora formats (e.g. XML and JSON).

## Examples
### Reading NewsML XML format
```python
from corpona import XML
d = XML.parse_xml('2660341.xml')
print(f"Guid: {d.guid}") # access tag attributes as Python attributes
print(f"Language: {d.attributes['xml:lang']}") # in case of special characters, access them directly

contentMeta = d['contentMeta'][0]
print(f"Urgency: {contentMeta['urgency']}")
print(f"Headline: {contentMeta['headline']}")
print(f"Subject: {contentMeta['subject'][0]['name']}")
print("Genres: {}".format(", ".join(g['name'].text for g in contentMeta['genre'])))
print()
content_body = d['contentSet'][0]['inlineXML'][0]['html'][0]['body'][0]
print("Content: ")
for p in content_body['p']:
    print(p)
```


### Getting a Summary of an XML/JSON

```python
from corpona import XML
from corpona import summarize
from pprint import pprint

d = XML.parse_xml('data.xml', namespaces={'http://www.w3.org/XML/1998/namespace': 'xml', })
pprint(summarize(d), indent=4)

pprint(summarize([
    {'key1': 'hello1', 'key2': 1},
    {'key1': 'hello2', 'key2': 2},
    {'key1': 'hello3', 'key2': 3},
    {'key1': 'hello4', 'key2': 4},
]), indent=4)
```

### Find children


```python
from corpona import find_child

data = {"key":["list_item", {"key2":"oo"}, {"key2":"bbb"}]}
print(find_child(data, ["key", "key2"]))
print(find_child(data, ["key", "key3"], default_value="ok"))

>> ['oo', 'bbb']
>> ['ok']

```