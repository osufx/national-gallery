from objects import glob
from common.ripple import userUtils, scoreUtils
from os.path import dirname, basename, isfile
import glob as _glob
import importlib
import json

def load_achievements():
	"""Load all the achievements from the sql server into glob.achievementClasses,
	and sets glob.ACHIEVEMENTS_VERSION to the highest version number in our achievement list.
	"""

	modules = _glob.glob("secret/achievements/handlers/*.py")
	modules = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")]
	#						^ cat face

	for module in modules:
		module = importlib.import_module("secret.achievements.handlers." + module)
		module.load()
		if module.ORDER in glob.achievementClasses:
			print("!!! FOUND OVERLAPPING ACHIEVEMENT ORDER FOR {}!!!".format(module.ORDER))
			print("Unable to load {} due to {} already loaded in slot {}".format(module.__name__, glob.achievementClasses[module.ORDER].__name__, module.ORDER))
			continue
		glob.achievementClasses[module.ORDER] = module
		glob.ACHIEVEMENTS_VERSION = max(glob.ACHIEVEMENTS_VERSION, module.VERSION)
	
	print("Loaded {} achievements!".format(len(modules)))

def get_achievements_with_version(version):
	"""Return same established achivement list structure but only with the achievements that matches
	the argument passed.
	
	Arguments:
		version {int} -- Version number to scan for
	
	Returns:
		Dict -- Filtered achivement list
	"""
	achievements = {}
	for mode, mode_val in glob.achievementClasses.items():
		if mode not in achievements:
			achievements[mode] = {}
		for handle, handle_val in mode_val.items():
			if handle not in achievements[mode]:
				achievements[mode][handle] = []
			for entry in handle_val:
				if entry["version"] == version:
					achievements[mode][handle].append(entry)
	return achievements

def unlock_achievements_scan(userID, version):
	"""Scan specific version for past achievements they should have unlocked
	
	Arguments:
		userID {int} -- User id of a player
		version {int} -- Achivement version to scan
	"""
	achievements = []

	#ach = achivement.ACHIEVEMENTS[version]
	for mode, mode_val in glob.achievementClasses.items():
		for handle, handle_val in mode_val.items():
			pass
			#for entry in handle_val:
			#achievements += glob.achievementHandlers[handle].scan(mode, userID)
	
	return achievements

def unlock_achievements_update(userID, version):
	"""Scans the user for past achievements they should have unlocked
	
	Arguments:
		userID {int} -- User id of a player
		version {int} -- Last achivement version the player had
	
	Returns:
		Array -- List of achievements
	"""
	achievements = []

	# Scan all past achivement versions from the user's achivement version to the latest
	"""
	scan = [v for v in achivement.ACHIEVEMENTS.keys() if v > version]
	for v in scan:
		achievements += unlock_achievements_scan(userID, v)
	"""
	print("1")

	# Update achivement version for user
	userUtils.updateAchievementsVersion(userID)

	return achievements

def unlock_achievements(score, beatmap, user_data):
	"""Return array of achievements the current play recived
	
	Arguments:
		score {Score} -- Score data recived from replay
		beatmap {Beatmap} -- Played beatmap
		user_data {dict} -- Info about the current player
	
	Returns:
		Array -- List of achievements for the current play
	"""
	achievements = []

	userID = userUtils.getID(score.playerName)
	achieved = glob.redis.get("lets:user_achievement_cache:{}".format(userID))
	if achieved is None:
		# Load from sql database
		achieved = [x["achievement_id"] for x in glob.db.fetchAll("SELECT achievement_id FROM users_achievements WHERE user_id=%s", [userID])]
		glob.redis.set("lets:user_achievement_cache:{}".format(userID), json.dumps(achieved), 1800)
	else:
		achieved = json.loads(achieved.decode("utf-8"))

	# Get current gamemode and change value std to osu
	gamemode_index = score.gameMode

	# Check if user should run achivement recheck
	user_version = userUtils.getAchievementsVersion(userID)
	if user_version < glob.ACHIEVEMENTS_VERSION:
		achievements += unlock_achievements_update(userID, user_version)

	# Check if gameplay should get new achivement
	index = 0
	for handler in glob.achievementClasses.values():
		achievements += [x + index for x in handler.handle(gamemode_index, score, beatmap, user_data)]
		index += handler.LENGTH
	
	# Remove duplicated achievements (incase of unlock_achievements_update adding stuff)
	achievements = list(set(achievements))

	# Remove already achived achievements from list
	achievements = [x for x in achievements if x not in achieved]

	glob.redis.set("lets:user_achievement_cache:{}".format(userID), json.dumps(achieved + achievements), 1800)

	for achievement in achievements:
		userUtils.unlockAchievement(userID, achievement)

	return achievements

def achievements_response(achievements):
	achievement_objects = []

	index = 0
	for handler in glob.achievementClasses.values():
		achievement_objects += [handler.ACHIEVEMENTS[x - index] for x in achievements if len(handler.ACHIEVEMENTS) >= x]
		index += handler.LENGTH

	achievements_packed = []
	for achievement_object in achievement_objects:
		achievements_packed.append("+".join([achievement_object["icon"], achievement_object["name"], achievement_object["description"]]))

	return "/".join(achievements_packed)
