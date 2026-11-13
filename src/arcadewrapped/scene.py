"""Gestionnaire de scène / niveau."""

from pathlib import Path

import arcade

from .entity import Entity


class Scene:
    COLLISION_LAYER_NAMES = {"collision", "collisions", "collided"}

    def __init__(self) -> None:
        self.entities: list[Entity] = []
        self.tile_map: arcade.TileMap | None = None
        self._tilemap_scene: arcade.Scene | None = None
        self._collision_layers: tuple[str, ...] = ()

    def add(self, entity: Entity) -> Entity:
        self.entities.append(entity)
        return entity

    def load_tilemap(
        self,
        path: str | Path,
        scaling: float = 1.0,
        layer_options: dict[str, dict[str, object]] | None = None,
        collision_layers: tuple[str, ...] | None = None,
    ) -> arcade.TileMap:
        """Charge une map Tiled TMX et prépare ses couches pour le rendu."""
        tile_map = arcade.load_tilemap(
            path,
            scaling=scaling,
            layer_options=layer_options,
        )
        available_layers = set(tile_map.sprite_lists)
        if collision_layers is None:
            collision_layers = tuple(
                name
                for name in tile_map.sprite_lists
                if name.casefold() in self.COLLISION_LAYER_NAMES
                or name.casefold().startswith("c_")
            )
        missing_layers = set(collision_layers) - available_layers
        if missing_layers:
            names = ", ".join(sorted(missing_layers))
            raise ValueError(f"Unknown Tiled collision layer(s): {names}")

        tilemap_scene = arcade.Scene.from_tilemap(tile_map)
        self.tile_map = tile_map
        self._tilemap_scene = tilemap_scene
        self._collision_layers = collision_layers
        return tile_map

    def remove(self, entity: Entity) -> None:
        if entity in self.entities:
            self.entities.remove(entity)

    def on_enter(self) -> None:
        """Appelé lors du passage à cette scène."""

    def on_exit(self) -> None:
        """Appelé lorsque l'on quitte cette scène."""

    def update(self, dt: float) -> None:
        for entity in self.entities:
            entity.update(dt)

    def move(self, entity: Entity, dx: float, dy: float) -> bool:
        """Déplace une entité en la bloquant sur les couches de collision."""
        if self.tile_map is None or not self._collision_layers:
            entity.x += dx
            entity.y += dy
            return False

        collided = self._move_axis(entity, dx, horizontal=True)
        collided = self._move_axis(entity, dy, horizontal=False) or collided
        return collided

    def _move_axis(self, entity: Entity, distance: float, horizontal: bool) -> bool:
        if distance == 0:
            return False

        collided = False
        half_width = entity.width / 2
        half_height = entity.height / 2
        original_position = entity.x if horizontal else entity.y
        target_position = original_position + distance

        for layer_name in self._collision_layers:
            for tile in self.tile_map.sprite_lists[layer_name]:
                if horizontal:
                    overlaps_other_axis = (
                        entity.y - half_height < tile.center_y + tile.height / 2
                        and entity.y + half_height > tile.center_y - tile.height / 2
                    )
                    if not overlaps_other_axis:
                        continue

                    tile_left = tile.center_x - tile.width / 2
                    tile_right = tile.center_x + tile.width / 2
                    current_left = original_position - half_width
                    current_right = original_position + half_width
                    target_left = target_position - half_width
                    target_right = target_position + half_width

                    if distance > 0 and current_right <= tile_left < target_right:
                        target_position = min(target_position, tile_left - half_width)
                        collided = True
                    elif distance < 0 and target_left < tile_right <= current_left:
                        target_position = max(target_position, tile_right + half_width)
                        collided = True
                else:
                    overlaps_other_axis = (
                        entity.x - half_width < tile.center_x + tile.width / 2
                        and entity.x + half_width > tile.center_x - tile.width / 2
                    )
                    if not overlaps_other_axis:
                        continue

                    tile_bottom = tile.center_y - tile.height / 2
                    tile_top = tile.center_y + tile.height / 2
                    current_bottom = original_position - half_height
                    current_top = original_position + half_height
                    target_bottom = target_position - half_height
                    target_top = target_position + half_height

                    if distance > 0 and current_top <= tile_bottom < target_top:
                        target_position = min(target_position, tile_bottom - half_height)
                        collided = True
                    elif distance < 0 and target_bottom < tile_top <= current_bottom:
                        target_position = max(target_position, tile_top + half_height)
                        collided = True

        if horizontal:
            entity.x = target_position
        else:
            entity.y = target_position
        return collided

    def draw(self) -> None:
        if self._tilemap_scene is not None:
            map_layers = [
                name
                for name in self.tile_map.sprite_lists
            ]
            for layer_name in map_layers:
                self._tilemap_scene.draw([layer_name])
                for entity in self.entities:
                    if entity.render_layer == layer_name:
                        entity.draw()

            entities = [
                entity for entity in self.entities
                if entity.render_layer not in map_layers
            ]
        else:
            entities = self.entities

        for entity in entities:
            entity.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        pass

    def on_key_release(self, key: int, modifiers: int) -> None:
        pass
