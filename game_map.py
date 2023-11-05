from __future__ import annotations
import numpy as np
from tcod.console import Console

import tile_types

from typing import Iterable
from entity import Entity

class GameMap:
    def __init__(self, width:int, height:int, offset: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.ofs = offset
        self.dims = (self.width, self.height)
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.empty, order="F")
        self.full = np.full((width, height), fill_value=False, order='F')

    def render(self, console: Console) -> None:
        """If a tile is visible, draw with "light" colors, otherwise draw with SHROUD"""
        console.rgb[0:self.width, (self.ofs):(self.height+self.ofs)] = np.select(
            condlist = [self.full],
            choicelist = [self.tiles['light']],
            default = tile_types.SHROUD
        )
        for entity in self.entities:
            if entity.moveable:
                for prev_tile in entity.prev_set_move:
                    self.full[prev_tile[0], prev_tile[1]] = False
                    self.tiles[prev_tile[0], prev_tile[1]] = tile_types.empty
                for prev_tile in entity.prev_set_rot:
                    self.full[prev_tile[0], prev_tile[1]] = False
                    self.tiles[prev_tile[0], prev_tile[1]] = tile_types.empty
                for tile in entity.tiles:
                        self.full[tile[0], tile[1]] = True
                        self.tiles[tile[0], tile[1]] = tile_types.tile_type_list[entity.tile_type]

    def full_redo(self):
        """Based on entity data, completely redo self.tiles and self.full to reflect it."""
        self.tiles = np.full(self.dims, fill_value=tile_types.empty, order="F")
        self.full = np.full(self.dims, fill_value=False, order='F')
        for entity in self.entities:
            for tile in entity.tiles:
                self.full[tile[0], tile[1]] = True
                self.tiles[tile[0], tile[1]] = tile_types.tile_type_list[entity.tile_type]

    def move_down_one(self, row):
        """For every entity, move them down one if they are above the given row"""
        for entity in self.entities:
            for tile in entity.tiles:
                if tile[1] < row:
                    tile[1] += 1
                


