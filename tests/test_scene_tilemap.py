from pathlib import Path
from types import SimpleNamespace

import arcade
import pytest

from arcadewrapped import Entity, Scene


MAP_PATH = Path(__file__).parent / "maps" / "gameart2d-desert.tmx"


def test_scene_loads_tmx_layers_and_applies_scaling() -> None:
    scene = Scene()

    tile_map = scene.load_tilemap(MAP_PATH, scaling=0.5)

    assert scene.tile_map is tile_map
    assert tile_map.width == 120
    assert tile_map.height == 18
    assert set(tile_map.sprite_lists) == {"background", "entities", "c_ground"}
    assert tile_map.sprite_lists["background"][0].width == 64
    assert scene._collision_layers == ("c_ground",)


def test_scene_move_stops_entity_at_collision_tiles() -> None:
    scene = Scene()
    collision_tile = SimpleNamespace(
        center_x=128,
        center_y=64,
        width=128,
        height=128,
    )
    scene.tile_map = SimpleNamespace(
        sprite_lists={"SolidTiles": [collision_tile]}
    )
    scene._collision_layers = ("SolidTiles",)
    player = Entity(x=128, y=200)
    player.width = 32
    player.height = 32

    collided = scene.move(player, dx=0, dy=-100)

    assert collided
    assert player.y == 144


def test_scene_move_allows_motion_without_collision() -> None:
    scene = Scene()
    player = Entity(x=128, y=200)

    collided = scene.move(player, dx=0, dy=10)

    assert not collided
    assert player.y == 210


def test_scene_uses_collision_layers_named_in_code() -> None:
    scene = Scene()

    tile_map = scene.load_tilemap(MAP_PATH, collision_layers=("background",))

    assert scene.tile_map is tile_map
    assert scene._collision_layers == ("background",)


def test_scene_detects_collision_layers_by_tiled_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tile_map = SimpleNamespace(
        sprite_lists={
            "Background": [],
            "Collided": [],
            "Collision": [],
            "c_Walls": [],
            "C_Platforms": [],
            "Decorations": [],
        }
    )
    tilemap_scene = object()
    monkeypatch.setattr(arcade, "load_tilemap", lambda *args, **kwargs: tile_map)
    monkeypatch.setattr(
        arcade.Scene,
        "from_tilemap",
        lambda loaded_tile_map: tilemap_scene,
    )
    scene = Scene()

    scene.load_tilemap("unused.tmx")

    assert scene._collision_layers == (
        "Collided",
        "Collision",
        "c_Walls",
        "C_Platforms",
    )


def test_scene_rejects_unknown_collision_layer_names() -> None:
    scene = Scene()

    with pytest.raises(ValueError, match="Unknown Tiled collision layer"):
        scene.load_tilemap(MAP_PATH, collision_layers=("SolidTiles",))


def test_scene_draws_entities_after_their_named_map_layer() -> None:
    events: list[str] = []

    class DrawProbe(Entity):
        def draw(self) -> None:
            events.append(f"entity:{self.render_layer}")

    class TileMapScene:
        def draw(self, names: list[str]) -> None:
            events.append(f"map:{names[0]}")

    scene = Scene()
    scene.tile_map = SimpleNamespace(
        sprite_lists={
            "background": [],
            "foreground": [],
            "collided": [],
        }
    )
    scene._tilemap_scene = TileMapScene()
    scene._collision_layers = ("collided",)
    scene.add(DrawProbe(render_layer="background"))
    scene.add(DrawProbe(render_layer="entities"))

    scene.draw()

    assert events == [
        "map:background",
        "entity:background",
        "map:foreground",
        "map:collided",
        "entity:entities",
    ]
