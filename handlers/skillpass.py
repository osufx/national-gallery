from common.constants import gameModes as Mode

VERSION = 2

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
	"callback": skill_pass,
	"achievement": {
		"uid": "skill-pass-{mode}-{index}",
		"name": "{name}",
		"description": "{description}",
		"icon": "{mode}-skill-pass-{index}",
		"replacements": {
			"index": [1, 2, 3, 4, 5, 6, 7, 8],
			"mode": ["osu", "taiko", "ctb", "mania"],
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
	}
}

def skill_pass(mode, score, beatmap):
	achievement_ids = []
	# No need to check if correct mode is passed as we accept every

	mode_2 = mode.replace("osu", "std")
	stars = beatmap["stars" + mode_2.title()]

	indexies = [x for x in TABLE[1].achievement.replacements.index if x == stars]

	for index in indexies:
		uid = TABLE[1].achievement.uid.format(mode=mode, index=index)
		achievement_ids.append(BINDINGS[uid])

	return achievement_ids
