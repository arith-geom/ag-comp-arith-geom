import yaml

data_file = "_data/members.yml"

with open(data_file, "r") as f:
    data = yaml.safe_load(f)

if data and "sections" in data:
    for section in data["sections"]:
        if "members" in section:
            for member in section["members"]:
                if "email" in member:
                    del member["email"]

with open(data_file, "w") as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print("Removed email fields from _data/members.yml")
