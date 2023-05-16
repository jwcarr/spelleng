import json

class SetEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, set):
			return list(obj)
		return json.JSONEncoder.default(self, obj)

def json_write(obj, output_file):
	with open(output_file, 'w') as file:
		json.dump(obj, file, indent='\t', ensure_ascii=False, cls=SetEncoder)

def json_read(input_file):
	with open(input_file) as file:
		data = json.load(file)
	return data