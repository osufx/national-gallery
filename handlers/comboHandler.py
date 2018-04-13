def handle(mode, score):
	"""Handles achivements targetted the user's combo.
	
	Arguments:
		mode {string} -- osu! gamemode type
		score {Score} -- Score data of the finished play
	
	Returns:
		Array -- List of unlocked achivements
	"""
	achivements = []

	if score.maxCombo > 500:
		achivements.append(
			{
				"title": "500 Combo osu!{}".format("""gamemode name"""),
				"subtitle": "500 big ones! You're moving up in the world!",
				"icon": ""
			}
		)

	return achivements


def scan(mode, userID):
	pass