from typing import Tuple
import numpy as np

graphic_dt = np.dtype(
    [   
        ("ch", np.int32),  #Unicode
        ("fg", "3B"),   #Foreground
        ('bg', "3B"),   #Background
    ]
)

tile_dt = np.dtype(
    [
        ('ent_id', np.int32),
        ('desig', np.int32),
        ('light', graphic_dt)
    ]
)

def new_tile(
    *, desig: np.int32, light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
    ) -> np.ndarray:
    """Helper Function to make a tile with associated attributes"""
    return np.array((0, desig, light), dtype=tile_dt)

SHROUD = np.array((ord('|'), (55, 55, 55), (0, 0, 0)), dtype=graphic_dt)

empty = new_tile(
    desig = 0,
    light=(ord(' '), (255, 255, 255), (255, 255, 255))
)
long = new_tile(
    desig = 1,
    light=(ord('-'), (255, 255, 255), (173, 216, 230))
)
back_l = new_tile(
    desig = 2,
    light=(ord(')'), (255, 255, 255), (0, 0, 139))
)
front_l = new_tile(
    desig = 3, 
    light=(ord('('), (255, 255, 255), (255, 128, 0))
    )
square = new_tile(
    desig = 4,
    light=(ord('o'), (255, 255, 255), (255, 255, 0))
    )
sqig = new_tile(
    desig = 5,
    light=(ord('%'), (255, 255, 255), (0, 255, 0))
    )
back_sqig = new_tile(
    desig = 6,
    light=(ord('&'), (255, 255, 255), (255, 0, 0))
    )
point = new_tile(
    desig = 7,
    light=(ord('^'), (255, 255, 255), (102, 0 , 204))
    )
tile_type_list = [empty, long, back_l, front_l, square, sqig, back_sqig, point]