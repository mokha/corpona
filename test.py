from corpona import find_child
data = {"key":["list_item", {"key2":"oo"}, {"key2":"bbb"}]}
print(find_child(data, ["key", "key2"]))
print(find_child(data, ["key", "key3"], default_value="ok"))