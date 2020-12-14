# corpona
corpona is a library for processing corpora formats (e.g. XML and JSON).

## Examples
### Reading NewsML XML format
```python
from corpona.xml import XML
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
