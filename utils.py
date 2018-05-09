from objects import glob
from common.ripple import userUtils, scoreUtils

glob.achievementHandlers = {}
from . handlers import *

def load_achievements():
	"""Load all the achivements from the sql server into glob.achievementClasses,
	and sets glob.ACHIEVEMENTS_VERSION to the highest version number in our achievement list.
	"""
	achivements = glob.db.fetchAll("SELECT id, name, description, icon, version FROM achievements ORDER BY id ASC;")
	for achivement in achivements:
		keys = achivement["icon"].split("-")

		# TODO: Set version as part of the first few keys in the keychain

		# Change osu keyword to std in first key
		keys[0].replace("osu", "std")

		if keys[0] not in glob.achievementClasses:
			glob.achievementClasses[keys[0]] = {}
		if keys[1] not in glob.achievementClasses[keys[0]]:
			glob.achievementClasses[keys[0]][keys[1]] = []
		glob.achievementClasses[keys[0]][keys[1]].append(achivement)

		# Set the achivement version as the newest achivement version number if higher then the old value
		glob.ACHIEVEMENTS_VERSION = max(glob.ACHIEVEMENTS_VERSION, achivement["version"])

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
			#for entry in handle_val:
			achivements += glob.achievementHandlers[handle].scan(mode, userID)
	
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

	# Check if user should get new achivement
	"""
	for version in achivement.ACHIVEMENTS.values():
		for callback in version[gamemode_name]:
			achivements += callback.handle(gamemode_name, score)
	"""
	print("2")

	return achivements

def achievements_response(achivements):
    #Achievement structure is:
    #"+".join([name/load, title, subtitle])

	return ""

# Just a test
# return "taiko-skill-fc-3+Test medal+Hia/taiko-skill-fc-1+More of them+yay"