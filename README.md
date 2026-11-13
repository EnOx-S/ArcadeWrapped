# ArcadeWrapped
Python motor powered by PythonArcade

## Tiled maps

`Scene.load_tilemap()` loads a Tiled TMX map, applies an optional scale, and draws
its layers before the scene's entities:

```python
scene = Scene()
tile_map = scene.load_tilemap("maps/level.tmx", scaling=0.5)
```

Set an entity's `render_layer` to a Tiled layer name to draw it after that
layer. The default `"entities"` layer draws entities above the map. Tiled
layers whose names start with `c_` (case-insensitive), or are exactly
`collision`, `collisions`, or `collided`, are automatically treated as
collision layers. Collision layers are still rendered in their Tiled order
unless the layer is hidden in Tiled:

```python
scene.load_tilemap("maps/level.tmx")
scene.move(player, dx=player.vx * dt, dy=player.vy * dt)
```

Alternatively, explicitly select any Tiled tile layer as solid in code:

```python
scene.load_tilemap("maps/level.tmx", collision_layers=("Walls", "Platforms"))
```

The sample map has a `c_ground` collision layer. Add or edit dedicated `c_`
tile layers in Tiled to define solid areas; this keeps collision data separate
from decorative art. The demo's player uses the `entities` render layer from
the map.

Run the player movement example with the sample map:

```powershell
python tests/map_demo.py
```

Use the arrow keys or WASD to move. The camera follows the player. Run the
focused map-loading test with:

```powershell
python -m pytest tests/test_scene_tilemap.py
```
