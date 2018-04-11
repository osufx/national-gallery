from .handlers import comboHandler

"""
class Achivement(object):
	url			= None
	title		= None
	subtitle	= None
	
	def __init__(self, url):
		pass
"""


""" LEFTOVERS (Part of ACHIVEMENT pre structure)
"500": {
	"title": "500 Combo (osu!std)",
	"subtitle": "500 big ones! You're moving up in the world!",
	"callback": comboHandler
},
"750": {
	"title": "750 Combo (osu!std)",
	"subtitle": "750 big ones! You're moving up in the world!",
	"callback": comboHandler
}
"""

ACHIVEMENTS = {
	1: {
		"osu": {
			"combo": comboHandler
		},
		"taiko": {

		},
		"fruits": {

		},
		"mania": {

		},
		"all": {

		}
	}
}
