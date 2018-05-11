import math
from objects import glob
from common.constants import mods

VERSION = 4
ORDER = 4

# Loads the achievement length on load
LENGTH = 0

ACHIEVEMENT_BASE = {
	"name": "{name}",
	"description": "{description}",
	"icon": "all-intro-{mod}"
}

ACHIEVEMENT_KEYS = {
	"name": [
		"Finality",
		"Perfectionist",
		"Rock Around The Clock",
		"Time And A Half",
		"Sweet Rave Party",
		"Blindsight",
		"Are You Afraid Of The Dark?",
		"Dial It Right Back",
		"Risk Averse",
		"Slowboat",
		"Burned Out"
	],
	"description": [
		"High stakes, no regrets.",
		"Accept nothing but the best.",
		"You can't stop the rock.",
		"Having a right ol' time. One and a half of them, almost.",
		"Founded in the fine tradition of changing things that were just fine as they were.",
		"I can see just perfectly.",
		"Harder than it looks, probably because it's hard to look.",
		"Sometimes you just want to take it easy.",
		"Safety nets are fun!",
		"You got there. Eventually.",
		"One cannot always spin to win."
	],
	"mod": [
		"suddendeath",
		"perfect",
		"hardrock",
		"doubletime",
		"nightcore",
		"hidden",
		"flashlight",
		"easy",
		"nofail",
		"halftime",
		"spunout"
	]
}

# For every itteration index gets increased, while mode and mode_2 gets increased every 4 itterations
ACHIEVEMENT_STRUCT = {
	"name": 1,
	"description": 1,
	"mod": 1
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
	return check(score.mods)

def check(m):
	achievement_ids = []

	# Yes I am braindead atm and dont want to think about it...
	if m & mods.SUDDENDEATH > 0:
		achievement_ids += [0]
	if m & mods.PERFECT > 0:
		achievement_ids += [1]
	if m & mods.HARDROCK > 0:
		achievement_ids += [2]
	if m & mods.DOUBLETIME > 0:
		achievement_ids += [3]
	if m & mods.NIGHTCORE > 0:
		achievement_ids += [4]
	if m & mods.HIDDEN > 0:
		achievement_ids += [5]
	if m & mods.FLASHLIGHT > 0:
		achievement_ids += [6]
	if m & mods.EASY > 0:
		achievement_ids += [7]
	if m & mods.NOFAIL > 0:
		achievement_ids += [8]
	if m & mods.HALFTIME > 0:
		achievement_ids += [9]
	if m & mods.SPUNOUT > 0:
		achievement_ids += [10]

	return achievement_ids

def update(userID):
	achievement_ids = []

	entries = glob.db.fetchAll("SELECT mods FROM scores WHERE userid = %s GROUP BY mods", [userID])
	for entry in entries:
		achievement_ids += check(entry["mods"])

	return achievement_ids
