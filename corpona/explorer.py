import collections


def find_child(data, path, default_value=None, explicit_list=False):
	next_list = False
	for i, folder in enumerate(path):
		if next_list:
			next_list = False
			try:
				data = data[i]
			except:
				return default_value
		if type(data) is dict:
			#dictionary
			try:
				data = data[folder]
				if len(path) == i +1:
					return data
			except:
				return default_value
		elif type(data) is list and not explicit_list:
			#list
			r = []
			for x in data:
				res = find_child(x, path[i:])
				if res is not None:
					r.append(res)
			if len(r) == 0:
				return [default_value]
			else:
				return r
		elif type(data) is list and explicit_list and folder is list:
			next_list = True
		else:
			return default_value
	return default_value

def find_parent(data, path, default_value=None, explicit_list=False):
	if explicit_list:
		if path[-2] is list:
			return find_child(data, path[:-2])
		else:
			return find_child(data, path[:-1])
	else:
		return find_child(data, path[:-1])






