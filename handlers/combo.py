import math
from objects import glob

VERSION = 1
ORDER = 1

# Loads the achievement length on load
LENGTH = 0

ACHIEVEMENT_BASE = {
	"name": "{index} Combo (osu!{mode_2})",
	"description": "{index} big ones! You're moving up in the world!",
	"icon": "{mode}-combo-{index}"
}

ACHIEVEMENT_KEYS = {
	"index": [500, 750, 1000, 2000],
	"mode_2": ["std", "taiko", "ctb", "mania"],
	"mode": ["osu", "taiko", "ctb", "mania"]
}

# For every itteration index gets increased, while mode and mode_2 gets increased every 4 itterations
ACHIEVEMENT_STRUCT = {
	"index": 1,
	"mode": 4,
	"mode_2": 4
}

ACHIEVEMENTS = []

def load():
	global LENGTH
	for struct in ACHIEVEMENT_STRUCT:
		LENGTH = max(LENGTH, len(ACHIEVEMENT_KEYS[struct]) * ACHIEVEMENT_STRUCT[struct])
	
	entry = {x:0 for x in ACHIEVEMENT_STRUCT}
	for i in range(LENGTH):
		for struct in ACHIEVEMENT_STRUCT:
			entry[struct] = math.floor(i / ACHIEVEMENT_STRUCT[struct]) % len(ACHIEVEMENT_KEYS[struct])
		format_data = {x:ACHIEVEMENT_KEYS[x][entry[x]] for x in ACHIEVEMENT_KEYS}
		ACHIEVEMENTS.append({x: ACHIEVEMENT_BASE[x].format_map(format_data) for x in ACHIEVEMENT_BASE})

def handle(mode, score, beatmap, user_data):
	return check(mode, score.maxCombo)

def check(mode, max_combo):
	achievement_ids = []
	indexies = [x for x in ACHIEVEMENT_KEYS["index"] if x <= max_combo]

	for index in indexies:
		achievement_ids.append(index + mode * 4)

	return achievement_ids

def update(userID):
	achievement_ids = []

	entries = glob.db.fetchAll("SELECT MAX(max_combo) AS max_combo, play_mode FROM scores WHERE userid = %s AND completed >= 2 GROUP BY play_mode", [userID])
	for entry in entries:
		achievement_ids += check(entry["play_mode"], entry["max_combo"])

	return achievement_ids
