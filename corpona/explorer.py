import collections

class Node(object):
	"""docstring for Node"""
	def __init__(self, type):
		super(Node, self).__init__()
		self.types = set()
		self.type_freqs = {}
		self.type = type
		self.children = {}
		self.children_l = []

	def add_child(self, child, path, key, t=dict):
		c = self.find(path)
		return c._add_child(child, key,t)

	def _add_child(self, child, key,t):
		if t == dict:
			if key not in self.children:
				self.children[key] = []
			self.children[key].append(child)
			return len(self.children[key])-1
		else:
			if len(self.children)-1 < key:
				self.children_l.append([])
			self.children_l[key].append(child)
			return len(self.children_l[key]) -1
	def _add_type(self, t):
		if t not in self.types:
			self.types.add(t)
			self.type_freqs[t] = 0
		self.type_freqs[t] += 1

	def find(self, jpath):
		if len(jpath) == 0:
			return self
		if jpath[0] is list:
			return self.children[jpath[1]].find(jpath[2:])
		else:
			return self.children[jpath[0]].find(jpath[1:])



def map_structure(dictionary):
	current_map = Node(type(dictionary))
	return _map(dictionary, current_map, [])

def _map(dictionary, current_map, jpath):
	if isinstance(dictionary, collections.abc.Mapping):
		#dictionary
		for key in dictionary:
			index = current_map.add_child(Node(type(dictionary[key])), jpath, key)
			_map(dictionary[key], current_map, jpath + [key])
	elif isinstance(dictionary, collections.abc.Iterable):
		#list
		for i, item in enumerate(dictionary):
			index = current_map.add_child(Node(list), jpath, i, list)
	else:
		current_map.add_child(Node(type(dictionary)), jpath)

def find_child(data, path, default_value=None, explicit_list=False):
	next_list = False
	for i, folder in enumerate(path):
		if next_list:
			next_list = False
			try:
				data = data[i]
			except:
				return default_value
		if isinstance(data, collections.abc.Mapping):
			#dictionary
			try:
				data = data[folder]
			except:
				return default_value
		elif isinstance(data, collections.abc.Iterable) and not explicit_list:
			#list
			r = []
			for x in data:
				res = find_in_path(x, path[i:])
				if res is not None:
					r.append(res)
			if len(r) == 0:
				return [default_value]
			else:
				return r
		elif isinstance(data, collections.abc.Iterable) and explicit_list and folder is list:
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

			
def _add_node_to_path(data, path, node):




