from typing import Iterable, Any
from tcod import libtcodpy
from tcod.context import Context
from tcod.console import Console
from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap
import time
from random import randint
from numpy import swapaxes

class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, active: Entity, interval: int, mult: int,
        stats):
        self.event_handler, self.game_map, self.active = event_handler, game_map, active
        self.interval = interval
        self.multiplier = mult
        self.prev_proc = time.time()
        self.stats = stats
        self.random_start(randint(1, 7))

    def handle_events(self, events: Iterable[Any]) -> None:
        count = 0
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None: 
                continue
            action.perform(self, self.active)
            count += 1
        if not count: self.increment_active()
        
    def render(self, console: Console, context: Context):
        self.console = console
        self.game_map.render(console)
        context.present(console)
        console.clear()

    def increment_active(self):
        """If the interval has passed, attempt to move the active entity. If this
        fails, write out high scores and end the game if the entity never managed to move
        at all. Otherwise, increment the score, check rows for full ones, and lower the interval
        by the multiplier value. Then create a new random entity to be the new active one."""
        if time.time()-self.prev_proc>self.interval:
            self.prev_proc = time.time()
            if not self.active.move(0, 1):
                if not self.active.life_span: 
                    self.stats.write_high_score()
                    raise SystemExit
                self.stats.increment_score()
                self.check_rows()
                if self.interval > 0.6: self.interval = self.interval*(1-self.multiplier/100)
                elif self.interval > 0.4: self.interval = self.interval*(1-self.multiplier/150)
                else: self.interval = self.interval*(1-(self.multiplier)/250)
                self.new_active_ent()

    def new_active_ent(self):
        """Create a new random entity type at a random top x position, and add it 
        to the entity list."""
        new_ent = Entity(self.num, 0, self.tile_type, self.game_map.dims, self.game_map.full)
        self.game_map.entities.update(set(((new_ent),)))
        self.active = new_ent
        self.random_start(self.tile_type)

    def check_rows(self):
        """Swap axes for easy rows_org access, do a recursive check, then redo all game_map elements based
        on entity values"""
        rows_org = swapaxes(self.game_map.full, 0, 1)
        self.rows_del = 0
        for row in range(len(rows_org)-1, -1, -1):
            self.constant_row_check(rows_org, row)
        # For one row: 4 pts, then 12, then 24, then 40
        increment = 2*self.rows_del*(self.rows_del+1)
        for x in range(increment):
            self.stats.increment_score()
        self.game_map.full_redo()

    def random_start(self, prev):
        self.tile_type = randint(1, 7)
        if self.tile_type == prev: self.random_start(prev)
        if self.tile_type==1: self.num = randint(0, 11)
        else: self.num = randint(0, 12)

    def constant_row_check(self, rows_org, row):
        """If a full row is found, delete it, move entities fully down, and then check the row again"""
        if all(rows_org[row]):
            rows_org = self.del_row_check_continue(row)
            self.constant_row_check(rows_org, row)

    def del_row_check_continue(self, row):
        """Delete all entity tiles in a given row,
        then move all appropriate entities down, and redo all game_map tiles and fill values
        to ensure future accuracy. Then run through every entity by tile left to right, down to up,
        and attempt to shift them once based the entire entities freedom of movement.
        Return an updated row_swapped version of game_map.fill to ensure recursive accuracy."""
        self.rows_del += 1
        for scalar in range(len(self.game_map.tiles)): 
            for entity in self.game_map.entities:
                if [scalar, row] in entity.tiles:
                    entity.tiles.remove([scalar, row])
        self.game_map.move_down_one(row)
        self.game_map.full_redo()
        for column in range(self.game_map.dims[0]):
            for row_num in range(self.game_map.dims[1], -1, -1):
                for entity in self.game_map.entities:
                    if [column, row_num] in entity.tiles:
                        entity.update_parameters(self.game_map.full)
                        entity.move_as_far_as_possible()
        return(swapaxes(self.game_map.full, 0, 1))

    def print_scores(self, offset, s_height, s_width):
        top_strings = self.signal_ent_future()
        self.console.print(0, offset-1, top_strings[0], (0, 0, 100), (0, 0, 255))
        self.console.print(self.num, offset-1, top_strings[1], (200, 200, 250), (0, 0, 255))
        self.console.print(self.num+1, offset-1, top_strings[2], (0, 0, 100), (0, 0, 255))
        self.console.print(0, s_height-1, '^^^^^^^^^^^^^^^^', (0, 0, 100), (0, 0, 255))
        self.console.print(s_width//2, 0, f'Tetris', (255, 255, 255), (0, 0, 0), alignment = libtcodpy.CENTER)
        self.console.print(0, 1, f'Score:{self.stats.score}', (255, 255, 255), (0, 0, 0))
        self.console.print(0,2,
            f'Top:{self.stats.high_score[0]},{self.stats.high_score[1]},{self.stats.high_score[2]}',
            (255, 255, 255), (0, 0, 0))

    def signal_ent_future(self):
        base = '<><><><><><><><'
        return([base[:self.num], base[self.num], base[self.num+1:]])
