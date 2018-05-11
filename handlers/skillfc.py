import math
from common.ripple import scoreUtils

VERSION = 3
ORDER = 3

# Loads the achievement length on load
LENGTH = 0

ACHIEVEMENT_BASE = {
	"name": "{name}",
	"description": "{description}",
	"icon": "{mode}-skill-fc-{index}"
}

ACHIEVEMENT_KEYS = {
	"index": [1, 2, 3, 4, 5, 6, 7, 8],
	"mode": ["osu", "taiko", "fruits", "mania"],
	"name": [
		"Totality",
		"Keeping Time",
		"Sweet And Sour",
		"Keystruck",
		"Business As Usual",
		"To Your Own Beat",
		"Reaching The Core",
		"Keying In",
		"Building Steam",
		"Big Drums",
		"Clean Platter",
		"Hyperflow",
		"Moving Forward",
		"Adversity Overcome",
		"Between The Rain",
		"Breakthrough",
		"Paradigm Shift",
		"Demonslayer",
		"Addicted",
		"Everything Extra",
		"Anguish Quelled",
		"Rhythm's Call",
		"Quickening",
		"Level Breaker",
		"Never Give Up",
		"Time Everlasting",
		"Supersonic",
		"Step Up",
		"Aberration",
		"The Drummer's Throne",
		"Dashing Scarlet",
		"Behind The Veil"
	],
	"description": [
		"All the notes. Every single one.",
		"Two to go, please.",
		"Hey, this isn't so bad.",
		"Bet you feel good about that.",
		"Surprisingly difficult.",
		"Don't choke.",
		"Excellence is its own reward.",
		"They said it couldn't be done. They were wrong."
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
	if not score.fullCombo: # No need to check if the score were not a fullcombo
		return []

	achievement_ids = []

	mode_str = scoreUtils.readableGameMode(mode)

	mode_2 = mode_str.replace("osu", "std")
	stars = getattr(beatmap, "stars" + mode_2.title())

	indexies = [x for x in ACHIEVEMENT_KEYS["index"] if x == stars]

	for index in indexies:
		achievement_ids.append(mode + index * 4)

	return achievement_ids
