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

def json_write_line(obj, output_file):
	out_string = json.dumps(obj, ensure_ascii=False)
	with open(output_file, 'a') as file:
		file.write(out_string + '\n')

def json_read_lines(input_file, key):
	obj = {}
	with open(input_file) as file:
		for line in file:
			line_obj = json.loads(line.strip())
			key_value = line_obj[key]
			del line_obj[key]
			obj[key_value] = line_obj
	return obj
