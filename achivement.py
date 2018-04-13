#from .handlers import comboHandler

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

class Achivement():
	title		= None
	subtitle	= None
	icon		= None

	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)
	
	def format(self, **kwargs):
		for key, value in self.__dict__.items():
			setattr(self, key, value.format(**kwargs))
	
	def getData(self):
		return "{icon}+{title}+{subtitle}".format(**self.__dict__)

# Will most likely have to change this to work differently as it needs to assign a different index for every actual achivement.
# SQL is a posibility...
ACHIVEMENTS = {
	1: {
		"std": [
			#comboHandler
		],
		"taiko": [

		],
		"fruits": [

		],
		"mania": [

		],
		"all": [

		]
	}
}
