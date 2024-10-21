# Blender import
import math
import random
import sys

import bmesh
import bpy

GRASS_FILE = "./grass.blend"

# すべてのオブジェクト削除
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# 0: 無し, 1: grass_low, 2: grass_mid, 3: grass_high
field = [[random.randint(0, 3) for i in range(10)] for j in range(7)]

# grass object の読み込み
bpy.ops.wm.append(
    filename="grass_low",
    directory=GRASS_FILE + "/Object",
)
bpy.ops.wm.append(
    filename="grass_mid",
    directory=GRASS_FILE + "/Object",
)
bpy.ops.wm.append(
    filename="grass_high",
    directory=GRASS_FILE + "/Object",
)

# 位置
for i in range(7):
    for j in range(10):
        if field[i][j] == 1:
            obj = bpy.data.objects["grass_low"]
        elif field[i][j] == 2:
            obj = bpy.data.objects["grass_mid"]
        elif field[i][j] == 3:
            obj = bpy.data.objects["grass_high"]
        else:
            continue

        obj = obj.copy()
        obj.data = obj.data.copy()

        obj.location = (j * 2, i * 2, 0)
        bpy.context.collection.objects.link(obj)

# カメラ
bpy.ops.object.camera_add(location=(10, -20, 30), rotation=(math.pi / 4, 0, 0))
bpy.context.object.data.ortho_scale = 20
bpy.context.scene.camera = bpy.context.object

# ライト
bpy.ops.object.light_add(type="SUN", location=(10, 10, 10))
bpy.context.object.data.energy = 2

# レンダリング
bpy.context.scene.render.image_settings.file_format = "PNG"
bpy.context.scene.render.filepath = "./render.png"
bpy.context.scene.render.resolution_x = 256 * 4
bpy.context.scene.render.resolution_y = 128 * 4
bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "CPU"
bpy.ops.render.render(write_still=True)
