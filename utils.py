import glob

def load_achievements():
    glob.ACHIEVEMENTS_VERSION = 1

def unlock_achievements(score, beatmap, user_data):
    return -1

def achievements_response(id):
    #Achievement structure is:
    #"+".join([name/load, title, subtitle])
    return ""