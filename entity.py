from typing import Tuple
import tile_types
import copy
import numpy as np

class Entity:
    """A generic object to describe tetris entities"""
    def __init__(self, x: int, y: int, tile_type: int, bounds: Tuple[int, int], parameters):
        self.x, self.y, self.tile_type, self.bounds = x, y, tile_type, bounds
        self.core, self.rel_map = [], []
        if len(parameters): 
            self.parameters = parameters.copy()
        else: self.parameters = np.full(bounds, False, order='F')
        self.orientation = 0
        self.moveable = True
        self.dimen = 0
        self.life_span = 0
        #None, ----, |__, |^^^, [], _|-, -|_, _|_ 
        total_types = ([], [[0, 0], [1, 0], [2, 0], [3, 0]], [[0, 0], [0, 1], [1, 1], [2, 1]],
            [[0, 1], [0, 0], [1, 0], [2, 0]], [[0, 0], [0, 1], [1, 0], [1, 1]],
            [[0, 1], [1, 1], [1, 0], [2, 0]], [[0, 0], [1, 0], [1, 1], [2, 1]],
            [[1, 0], [0, 1], [1, 1], [2, 1]])
        self.core_lists = [0, 0, 1, 1, 0, 1, 2, 2]
        self.tiles = total_types[tile_type]
        self.prev_set_move = []
        self.prev_set_rot = []
        self.tried_rotate = False
        if tile_type:
            self.core = self.tiles[self.core_lists[tile_type]]
            self.rel_maps = self.gen_all_relative_points()
        for coord in self.tiles:
            coord[0]+=self.x
            coord[1]+=self.y

    def move(self, dx: int, dy: int) -> bool:
        """Move the entity a given amount, returning whether the entity should still be moveable or not"""
        self.prev_set_move = copy.deepcopy(self.tiles)
        if self.moveable and self.check_bounds(self.tiles, dx, dy):
            self.life_span += 1
            for coord in self.tiles:
                coord[0]+=dx
                coord[1]+=dy
        else:
            if dy: self.moveable = False
        return(self.moveable)
    
    def rotate(self, dir=-1, round = 0):
        """Rotate in a more efficient way, switching directions works now!"""
        if round < 4:
            round += 1
            if self.orientation < 3 and dir==1 or (dir==-1 and self.orientation > 0): self.orientation+=dir
            elif dir==-1 and self.orientation == 0: self.orientation = 3
            else: self.orientation = 0
            new_coords = []
            for x in range(4):
                new_coords.append(self.core[:])
            for coord_change in range(4):
                new_coords[coord_change][0]+=(self.rel_maps[self.orientation][coord_change][0])
                new_coords[coord_change][1]+=(self.rel_maps[self.orientation][coord_change][1])
            if self.check_bounds(new_coords, 0, 0):
                self.prev_set_rot = copy.deepcopy(self.tiles)
                self.tiles = new_coords
                self.core = self.tiles[self.core_lists[self.tile_type]]
            else: self.rotate(dir=dir, round=round)
        
                
    def gen_points_relative_core(self):
        """Taking a normal core map, return a list of adjustments needed to be done to the core
        to get the same coords back. Helps with rotation showbiz"""
        output = []
        for coord in self.tiles:
            output.append([coord[0]-self.core[0], coord[1]-self.core[1]])
        return(output)

    def gen_all_relative_points(self):
        """Generate relative core maps for all 4 orientations, starting with 0 and going counter-clockwise"""
        initial = self.gen_points_relative_core()
        total = [initial, [], [], []]
        for coord in initial:
            total[1].append([coord[1], -1*coord[0]])
        for coord in initial:
            total[2].append([coord[0]*-1, coord[1]*-1])
        for coord in initial:
            total[3].append([-1*coord[1], coord[0]])
        return(total)

    def check_bounds(self, coords, dx, dy):
        """Check if every tile is within bounds, and not violating the parameters
        of the entity, which is generally the fill values for other entity tiles"""
        count = 0
        for coord in coords:
            if coord[0]+dx >= 0 and coord[0]+dx < self.bounds[0] and (
                coord[1]+dy >= 0 and coord[1]+dy < self.bounds[1]) and (
                    not self.parameters[coord[0]+dx, coord[1]+dy]
                ): count += 1
        if count == 4:
            return True
        return False

    def update_parameters(self, parameter):
        """Self-explanatory, update the parameter list used for collisions for this entity"""
        self.parameters = parameter

    def move_as_far_as_possible(self, dx = 0, dy = 1):
        """Move until the entity hits something, recursively"""
        if self.check_bounds(self.tiles, dx, dy):
            for coord in self.tiles:
                self.life_span += 1
                coord[0] += dx
                coord[1] += dy
            self.move_as_far_as_possible(dx = dx, dy = dy)