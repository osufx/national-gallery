import math
from common.ripple import scoreUtils

VERSION = 2
ORDER = 2

# Loads the achievement length on load
LENGTH = 0

ACHIEVEMENT_BASE = {
	"name": "{name}",
	"description": "{description}",
	"icon": "{mode}-skill-pass-{index}"
}

ACHIEVEMENT_KEYS = {
	"index": [1, 2, 3, 4, 5, 6, 7, 8],
	"mode": ["osu", "taiko", "fruits", "mania"],
	"name": [
		"Rising Star",
		"My First Don",
		"A Slice Of Life",
		"First Steps",
		"Constellation Prize",
		"Katsu Katsu Katsu",
		"Dashing Ever Forward",
		"No Normal Player",
		"Building Confidence",
		"Not Even Trying",
		"Zesty Disposition",
		"Impulse Drive",
		"Insanity Approaches",
		"Face Your Demons",
		"Hyperdash ON!",
		"Hyperspeed",
		"These Clarion Skies",
		"The Demon Within",
		"It's Raining Fruit",
		"Ever Onwards",
		"Above and Beyond",
		"Drumbreaker",
		"Fruit Ninja",
		"Another Surpassed",
		"Supremacy",
		"The Godfather",
		"Dreamcatcher",
		"Extra Credit",
		"Absolution",
		"Rhythm Incarnate",
		"Lord of the Catch",
		"Maniac"
	],
	"description": [
		"Can't go forward without the first steps.",
		"Definitely not a consolation prize. Now things start getting hard!",
		"Oh, you've SO got this.",
		"You're not twitching, you're just ready.",
		"Everything seems so clear now.",
		"A cut above the rest.",
		"All marvel before your prowess.",
		"My god, you're full of stars!"
	]
}

# For every itteration index gets increased, while mode and mode_2 gets increased every 4 itterations
ACHIEVEMENT_STRUCT = {
	"name": 1,
	"mode": 1,
	"index": 4,
	"description": 4
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
	achievement_ids = []

	mode_str = scoreUtils.readableGameMode(mode)

	mode_2 = mode_str.replace("osu", "std")
	stars = getattr(beatmap, "stars" + mode_2.title())

	indexies = [x for x in ACHIEVEMENT_KEYS["index"] if x == math.floor(stars)]

	for index in indexies:
		achievement_ids.append(mode + index * 4)

	return achievement_ids

def update(userID):
	pass
