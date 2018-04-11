import glob
from . import achivement
from common.ripple import userUtils, scoreUtils

def load_achievements():
    glob.ACHIEVEMENTS_VERSION = 1

def unlock_achivements_gamemode(score, beatmap, user_data, gamemode):
	pass
	#ach = achivement.ACHIVEMENTS[gamemode]
	#for type in ach:
		#for index in ach[type]:
			 
def unlock_achievements_scan(userID, version):
	"""Scan specific version for past achivements they should have unlocked
	
	Arguments:
		userID {int} -- User id of a player
		version {int} -- Achivement version to scan
	"""
	achivements = []

	ach = achivement.ACHIVEMENTS[version]
	for gamemode in ach.values():
		for callback in ach[gamemode].keys():
			achivements += callback.scan(gamemode, userID)
	
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
	scan = [v for v in achivement.ACHIVEMENTS.keys() if v > version]
	for v in scan:
		achivements += unlock_achievements_scan(userID, v)

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
	if gamemode_name == "std":
		gamemode_name = "osu"

	# Check if user should run achivement recheck
	user_version = userUtils.getAchievementsVersion(userID)
	if user_version < glob.ACHIEVEMENTS_VERSION:
		achivements += unlock_achievements_update(userID, user_version)

	for version in achivement.ACHIVEMENTS.values():
		for callback in version[gamemode_name]:
			callback.handle(gamemode_name, score)

	return achivements

def achievements_response(achivements):
    #Achievement structure is:
    #"+".join([name/load, title, subtitle])

	return ""

# Just a test
# return "taiko-skill-fc-3+Test medal+Hia/taiko-skill-fc-1+More of them+yay"