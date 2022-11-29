from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap
from tcod import event as ev
from copy import deepcopy

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """ 
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        engine.stats.write_high_score()
        raise SystemExit()

class MovementAction(Action):
    def __init__(self, dx: int, dy: int, far=False):
        super().__init__()
        self.far = far
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        if not self.far:
            entity.move(self.dx, self.dy)
        else: 
            entity.prev_set = deepcopy(entity.tiles)
            entity.move_as_far_as_possible()

class MouseAction(Action):
    def __init__(self, event, context, gamemap: GameMap):
        super().__init__()
        context.convert_event(event)
        self.tile_pos = event.tile
        self.gamemap = gamemap

    def perform(self, engine: Engine, entity: Entity) -> None:
        pass

class RotateAction(Action):
    def __init__(self, dir = -1):
        self.dir = dir
    def perform(self, engine: Engine, entity: Entity) -> None:
        entity.rotate(dir = self.dir)