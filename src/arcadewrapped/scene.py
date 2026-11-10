"""Gestionnaire de scène / niveau."""

from .entity import Entity


class Scene:
    def __init__(self) -> None:
        self.entities: list[Entity] = []

    def add(self, entity: Entity) -> Entity:
        self.entities.append(entity)
        return entity

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

    def draw(self) -> None:
        for entity in self.entities:
            entity.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        pass

    def on_key_release(self, key: int, modifiers: int) -> None:
        pass
