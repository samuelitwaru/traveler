import pprint
import jinja2

models_file_path = "../../models/models.py"
fields_file_path = "../fields.py"
fields_file_temp_path = "fields_file_temp.temp"
res_file_temp_path = "res_file_temp.temp"
res_folder = "../resources"

models_file = open(models_file_path)

resources = {}

current_res = None

for line in models_file:
	if line.startswith("class "):
		res = line.replace("class ", "").replace("(db.Model):", "").replace("(db.Model, UserMixin):","").strip()
		current_res = res
		resources[res] = []

	elif "db.Column" in line:
		attr = { "name": None, "type": None }
		name, desc = line.split(" = ")
		if name.endswith("_id"):
			attr["is_rel"] = True
			attr["name"] = name.replace("_id", "").strip()
			attr["type"] = f"Nested(self.{attr['name']}_fields_min())"
			resources[current_res].append(attr)
		else:
			attr["name"] = name.strip()
			if "db.String" in desc:
				attr["type"] = "String"
			elif "db.Integer" in desc:
				attr["type"] = "Integer"
			elif "db.Boolean" in desc:
				attr["type"] = "Boolean"
			elif "db.Float" in desc:
				attr["type"] = "Float"
			elif "db.DateTime" in desc:
				attr["type"] = "DateTime"
			elif "db.Date" in desc:
				attr["type"] = "DateTime"
			resources[current_res].append(attr)


	elif "db.relationship" in line:
		attr = { "name": None, "type": None }
		name, desc = line.split(" = ")
		attr["is_rel"] = True
		attr["name"] = name.strip()
		rel_field_name_bluh = desc.replace('db.relationship("', "")
		i = rel_field_name_bluh.find('"')
		rel_field_name = rel_field_name_bluh[0:i]
		attr["type"] = f"Nested(self.{rel_field_name.lower()}_fields_min())"
		resources[current_res].append(attr)


# pprint.pprint(resources)

def create_fields_file():
	fields_fh = open(fields_file_path, 'w')
	temp_fh = open(fields_file_temp_path)
	temp = temp_fh.read()
	temp_fh.close()
	output = jinja2.Template(temp).render(resources=resources)
	fields_fh.write(output)
	fields_fh.close()

def create_resources():
	for res in resources:
		res_fh = open(f"{res_folder}/{res.lower()}.py", 'w')
		temp_fh = open(res_file_temp_path)
		temp = temp_fh.read()
		temp_fh.close()
		output = jinja2.Template(temp).render(res=res)
		res_fh.write(output)
		res_fh.close()


create_fields_file()
create_resources()