"""Moteur principal et boucle applicative."""

import arcade

from .scene import Scene

class Engine(arcade.Window):
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "ArcadeWrapped Game",
        bg_color: tuple[int, int, int] = (20, 24, 30),
    ):
        super().__init__(width, height, title)
        self.bg_color = bg_color
        self.current_scene: Scene | None = None
        arcade.set_background_color(self.bg_color)

    def switch_scene(self, scene: Scene) -> None:
        if self.current_scene:
            self.current_scene.on_exit()
        self.current_scene = scene
        self.current_scene.on_enter()

    def on_update(self, delta_time: float) -> None:
        if self.current_scene:
            self.current_scene.update(delta_time)

    def on_draw(self) -> None:
        self.clear()
        if self.current_scene:
            self.current_scene.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.current_scene:
            self.current_scene.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if self.current_scene:
            self.current_scene.on_key_release(symbol, modifiers)

    def run(self) -> None:
        arcade.run()
