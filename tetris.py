import tcod
from input_handlers import EventHandler
from engine import Engine
from entity import Entity
from game_map import GameMap
from random import randint, choice
from game_stats import Gamestats

def main():
    s_width = 15
    s_height = 20
    g_width = 15
    g_height = 15

    tileset = tcod.tileset.load_tilesheet("randomimage.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    entities = []
    tile_type = choice([1, 2, 3, 4, 7])
    if tile_type==1: num = randint(0, 11)
    else: num = randint(0, 12)
    entities.append(Entity(num, 0, tile_type, [g_width, g_height], []))
    offset = 4
    game_map = GameMap(g_width, g_height, offset, entities)
    stats = Gamestats()

    context = tcod.context.new(
        x=400,
        y=40,
        width = 700,
        height = 840,
        columns = g_width,
        rows = g_height,
        tileset=tileset,
        title = "Tetris",
        vsync=True)

    event_handler = EventHandler(game_map, context, stats)
    engine = Engine(event_handler = event_handler, game_map = game_map, active = entities[0],
        interval = 0.8, mult = 3, stats=stats)
    root_console = tcod.console.Console(s_width, s_height, order='F')
    while True:
        engine.render(console=root_console, context=context)
        events = tcod.event.get()
        engine.handle_events(events)
        engine.print_scores(offset, s_height, s_width)
                
if __name__ == '__main__':
    main()