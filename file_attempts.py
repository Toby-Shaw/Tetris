import tcod
import os
def access_file_tile_sheet(filename):
    try:
        return tcod.tileset.load_tilesheet(filename, 32, 8, tcod.tileset.CHARMAP_TCOD)
    except:
        return tcod.tileset.load_tilesheet("_internal/" + filename, 32, 8, tcod.tileset.CHARMAP_TCOD)
    
def access_txt(filename, type):
    if os.path.exists(filename):
        return open(filename, type)
    else:
        return open("_internal/"+filename, type)