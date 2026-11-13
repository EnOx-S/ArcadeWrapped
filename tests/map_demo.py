"""Exemple de déplacement d'un joueur sur une map Tiled."""

from pathlib import Path

import arcade

from arcadewrapped import Engine, Entity, Scene


MAP_PATH = Path(__file__).parent / "maps" / "gameart2d-desert.tmx"


class Player(Entity):
    def __init__(self) -> None:
        super().__init__(
            x=128,
            y=200,
            color=arcade.color.AMBER,
            render_layer="entities",
        )
        self.speed = 250.0
        self.width = 32
        self.height = 32


class MapScene(Scene):
    def on_enter(self) -> None:
        self.load_tilemap(MAP_PATH, scaling=1.0)
        self.player = self.add(Player())
        window = arcade.get_window()
        if hasattr(arcade, "Camera2D"):
            self.camera = arcade.Camera2D(
                window=window,
                position=(self.player.x, self.player.y),
            )
        else:
            self.camera = arcade.Camera(window.width, window.height)
        self.pressed_keys: set[int] = set()

    def update(self, dt: float) -> None:
        self.player.vx = 0
        self.player.vy = 0
        if arcade.key.LEFT in self.pressed_keys or arcade.key.A in self.pressed_keys:
            self.player.vx = -self.player.speed
        if arcade.key.RIGHT in self.pressed_keys or arcade.key.D in self.pressed_keys:
            self.player.vx = self.player.speed
        if arcade.key.DOWN in self.pressed_keys or arcade.key.S in self.pressed_keys:
            self.player.vy = -self.player.speed
        if arcade.key.UP in self.pressed_keys or arcade.key.W in self.pressed_keys:
            self.player.vy = self.player.speed

        self.move(self.player, self.player.vx * dt, self.player.vy * dt)
        if hasattr(self.camera, "position"):
            self.camera.position = (self.player.x, self.player.y)
        else:
            self.camera.move_to(
                (
                    self.player.x - arcade.get_window().width / 2,
                    self.player.y - arcade.get_window().height / 2,
                )
            )

    def draw(self) -> None:
        self.camera.use()
        super().draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        self.pressed_keys.add(key)

    def on_key_release(self, key: int, modifiers: int) -> None:
        self.pressed_keys.discard(key)


if __name__ == "__main__":
    game = Engine(width=800, height=600, title="ArcadeWrapped - Tiled map")
    game.switch_scene(MapScene())
    game.run()
