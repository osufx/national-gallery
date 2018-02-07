import glob

def load_achievements():
    glob.ACHIEVEMENTS_VERSION = 1

def unlock_achievements(score, beatmap, user_data):
    return