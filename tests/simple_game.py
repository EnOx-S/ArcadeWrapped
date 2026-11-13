import arcade
from arcadewrapped import Engine, Entity, Scene


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, color=arcade.color.AMBER)
        self.speed = 250.0

    def move_left(self):
        self.vx = -self.speed

    def move_right(self):
        self.vx = self.speed

    def stop_x(self):
        self.vx = 0


class GameplayScene(Scene):
    def on_enter(self) -> None:
        self.player = self.add(Player(400, 300))

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.move_left()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.move_right()

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.stop_x()


if __name__ == "__main__":
    game = Engine(width=800, height=600, title="Demo ArcadeWrapper")
    game.switch_scene(GameplayScene())
    game.run()
