from objects import glob
from common.ripple import userUtils, scoreUtils
from os.path import dirname, basename, isfile
import glob as _glob
import importlib

def load_achievements():
	"""Load all the achivements from the sql server into glob.achievementClasses,
	and sets glob.ACHIEVEMENTS_VERSION to the highest version number in our achievement list.
	"""

	modules = _glob.glob("handlers/*.py")
	modules = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")]
	#						^ cat face

	for module in modules:
		module = importlib.import_module("handlers." + module)
		module.load()
		if module.ORDER in glob.achievementClasses:
			print("!!! FOUND OVERLAPPING ACHIEVEMENT ORDER FOR {}!!!".format(module.ORDER))
			print("Unable to load {} due to {} already loaded in slot {}".format(module.__name__, glob.achievementClasses[module.ORDER].__name__, module.ORDER))
			continue
		glob.achievementClasses[module.ORDER] = module
		glob.ACHIEVEMENTS_VERSION = max(glob.ACHIEVEMENTS_VERSION, module.VERSION)
	
	print("Loaded {} achievements!".format(len(modules)))

def get_achievements_with_version(version):
	"""Return same established achivement list structure but only with the achivements that matches
	the argument passed.
	
	Arguments:
		version {int} -- Version number to scan for
	
	Returns:
		Dict -- Filtered achivement list
	"""
	achivements = {}
	for mode, mode_val in glob.achievementClasses.items():
		if mode not in achivements:
			achivements[mode] = {}
		for handle, handle_val in mode_val.items():
			if handle not in achivements[mode]:
				achivements[mode][handle] = []
			for entry in handle_val:
				if entry["version"] == version:
					achivements[mode][handle].append(entry)
	return achivements

def unlock_achievements_scan(userID, version):
	"""Scan specific version for past achivements they should have unlocked
	
	Arguments:
		userID {int} -- User id of a player
		version {int} -- Achivement version to scan
	"""
	achivements = []

	#ach = achivement.ACHIVEMENTS[version]
	for mode, mode_val in glob.achievementClasses.items():
		for handle, handle_val in mode_val.items():
			pass
			#for entry in handle_val:
			#achivements += glob.achievementHandlers[handle].scan(mode, userID)
	
	return achivements

def unlock_achievements_update(userID, version):
	"""Scans the user for past achivements they should have unlocked
	
	Arguments:
		userID {int} -- User id of a player
		version {int} -- Last achivement version the player had
	
	Returns:
		Array -- List of achivements
	"""
	achivements = []

	# Scan all past achivement versions from the user's achivement version to the latest
	"""
	scan = [v for v in achivement.ACHIVEMENTS.keys() if v > version]
	for v in scan:
		achivements += unlock_achievements_scan(userID, v)
	"""
	print("1")

	# Update achivement version for user
	userUtils.updateAchievementsVersion(userID)

	return achivements

def unlock_achievements(score, beatmap, user_data):
	"""Return array of achivements the current play recived
	
	Arguments:
		score {Score} -- Score data recived from replay
		beatmap {Beatmap} -- Played beatmap
		user_data {dict} -- Info about the current player
	
	Returns:
		Array -- List of achivements for the current play
	"""
	achivements = []

	userID = userUtils.getID(score.playerName)

	# Get current gamemode and change value std to osu
	gamemode_index = score.gameMode
	gamemode_name = scoreUtils.readableGameMode(gamemode_index)

	print("version: {}".format(glob.ACHIEVEMENTS_VERSION))

	# Check if user should run achivement recheck
	user_version = userUtils.getAchievementsVersion(userID)
	if user_version < glob.ACHIEVEMENTS_VERSION:
		achivements += unlock_achievements_update(userID, user_version)

	# Check if gameplay should get new achivement
	index = 0
	for handler in glob.achievementClasses.values():
		achivements += [x + index for x in handler.handle(gamemode_index, score, beatmap)]
		index += handler.LENGTH
	
	# TODO: use user_data to remove achievements we already have

	return achivements

def achievements_response(achivements):
    #Achievement structure is:
    #"+".join([name/load, title, subtitle])

	return ""

# Just a test
# return "taiko-skill-fc-3+Test medal+Hia/taiko-skill-fc-1+More of them+yay"