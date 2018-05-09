from common.constants import gameModes as Mode

VERSION = 1

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
	"count": 16,
	"callback": combo,
	"achievement": {
		"uid": "combo-{mode}-{index}",
		"name": "{index} Combo (osu!{mode_2})",
		"description": "{index} big ones! You're moving up in the world!",
		"icon": "{mode}-combo-{index}",
		"replacements:": {
			"index": [500, 750, 1000, 2000],
			"mode_2": ["std", "taiko", "ctb", "mania"],
			"mode": ["osu", "taiko", "ctb", "mania"]
		}
	}
}

def combo(mode, score, beatmap):
	achievement_ids = []
	# No need to check if correct mode is passed as we accept every

	indexies = [x for x in TABLE[0].achievement.replacements.index if x <= score.maxCombo]

	for index in indexies:
		uid = TABLE[0].achievement.uid.format(mode=mode, index=index)
		achievement_ids.append(BINDINGS[uid])

	return achievement_ids
