# Blender import
import math
import os
import random
import sys

import bmesh
import bpy
import mathutils

sys.path.append(os.path.dirname(__file__))
from fetch import fetch_github_contributions

GRID_SIZE = 0.5
GRASS_FILE = "./grass.blend"


# 環境変数の読み込み
github_username = os.getenv("GITHUB_USERNAME")
github_token = os.getenv("GITHUB_TOKEN")

# すべてのオブジェクト削除
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# grass object の読み込み
filenames = ["grass_none", "grass_first", "grass_second", "grass_third", "grass_fourth"]
for filename in filenames:
    bpy.ops.wm.append(
        filename=filename,
        directory=GRASS_FILE + "/Object",
    )

# GitHub contributions を取得
data = fetch_github_contributions(github_username, github_token).get("data")
calender = data.get("user").get("contributionsCollection").get("contributionCalendar")

# 位置
for i, week in enumerate(calender.get("weeks")):
    for j, day in enumerate(week.get("contributionDays")):
        level = day.get("contributionLevel")
        if level == "NONE":
            obj = bpy.data.objects[filenames[0]]
        elif level == "FIRST_QUARTILE":
            obj = bpy.data.objects[filenames[1]]
        elif level == "SECOND_QUARTILE":
            obj = bpy.data.objects[filenames[2]]
        elif level == "THIRD_QUARTILE":
            obj = bpy.data.objects[filenames[3]]
        elif level == "FOURTH_QUARTILE":
            obj = bpy.data.objects[filenames[4]]
        else:
            continue

        obj = obj.copy()
        obj.data = obj.data.copy()
        obj.dimensions = (
            GRID_SIZE,
            GRID_SIZE,
            obj.dimensions.z,
        )
        obj.location = (
            (i + 1 / 2) * GRID_SIZE,
            -(j + 1 / 2) * GRID_SIZE,
            obj.dimensions.z / 2,
        )
        bpy.context.collection.objects.link(obj)

# Original grass object の削除
for obj in bpy.data.objects:
    if obj.name in filenames:
        bpy.data.objects.remove(obj)

# カメラ
look_at = (53 * GRID_SIZE / 2, -7 * GRID_SIZE / 2, 0)
camera_location = (53 * GRID_SIZE / 2, -40 * GRID_SIZE / 2, 40)
direction = mathutils.Vector(camera_location) - mathutils.Vector(look_at)
quaternion = direction.to_track_quat("Z", "Y")
bpy.ops.object.camera_add(location=camera_location)
bpy.context.object.rotation_euler = quaternion.to_euler()

bpy.context.object.data.ortho_scale = 20
bpy.context.scene.camera = bpy.context.object

# ライト
bpy.ops.object.light_add(type="SUN", location=(10, 10, 10))
bpy.context.object.data.energy = 2

# レンダリング
bpy.context.scene.render.image_settings.file_format = "PNG"
bpy.context.scene.render.filepath = "./output.png"
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 256
bpy.context.scene.cycles.samples = 256
bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "CPU"
bpy.ops.render.render(write_still=True)
