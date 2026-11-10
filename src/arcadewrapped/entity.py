"""Abstraction des objets du jeu (Entity / Actor)."""

import arcade


class Entity:
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        color: tuple[int, int, int] = arcade.color.WHITE,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.width = 30
        self.height = 30
        self.vx = 0.0
        self.vy = 0.0

    def update(self, dt: float) -> None:
        """Met à jour la position selon la vélocité."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self) -> None:
        """Rendu par défaut : un rectangle coloré."""
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height, self.color
        )
