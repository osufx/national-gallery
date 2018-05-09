from common.constants import gameModes as Mode

VERSION = 3

# Initialize data on lets load
# uid: index (directly from database?)
BINDINGS = {}

TABLE = {
	"mode": [
		Mode.STD,
		Mode.TAIKO,
		Mode.CTB,
		Mode.MANIA
	],
	"count": 32,
	"callback": skill_fc,
	"achievement": {
		"uid": "skill-fc-{mode}-{index}",
		"name": "{name}",
		"description": "{description}",
		"icon": "{mode}-skill-fc-{index}",
		"replacements": {
			"index": [1, 2, 3, 4, 5, 6, 7, 8],
			"mode": ["osu", "taiko", "ctb", "mania"],
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
	}
}

def skill_fc(mode, score, beatmap):
	if not score.fullCombo: # No need to check if the score were not a fullcombo
		return []

	achievement_ids = []

	mode_2 = mode.replace("osu", "std")
	stars = beatmap["stars" + mode_2.title()]

	indexies = [x for x in TABLE[2].achievement.replacements.index if x == stars]

	for index in indexies:
		uid = TABLE[2].achievement.uid.format(mode=mode, index=index)
		achievement_ids.append(BINDINGS[uid])

	return achievement_ids
