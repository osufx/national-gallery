from os.path import dirname, basename, isfile
import glob
import importlib

SQL_STRING = """
CREATE TABLE IF NOT EXISTS `achievements` (
  `id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `description` varchar(128) NOT NULL,
  `icon` varchar(32) NOT NULL,
  `version` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
INSERT INTO achievements (id, name, description, icon, version) VALUES
"""

module_list = glob.glob("handlers/*.py")
module_list = [basename(f)[:-3] for f in module_list if isfile(f) and not f.endswith("__init__.py")]
#							^ cat face

modules = []
for module in module_list:
	modules.append(importlib.import_module("handlers." + module))

modules = sorted(modules, key=lambda k: k.ORDER)

index = 0
for module in modules:
	achievement = module.TABLE.achievement
	uniq = achievement.unique
	rep = achievement.replacements

	length = 1
	for x in [rep[y] for y in uniq]:
		length *= len(x)

	rep_map = {x:[rep] for x in rep}

	for i in range(length):
		index += 1
		name = achievement.name.format_map({

		})
		#SQL_STRING += "({}, '{}', '{}', '{}', {})".format(index, )
		#SQL_STRING += len(rep.index) * len(rep.mode)

print(SQL_STRING)