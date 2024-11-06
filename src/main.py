import argparse
import math
import os
import random
import sys

import bpy
import mathutils

sys.path.append(os.path.dirname(__file__))
from fetch import fetch_github_contributions

GRID_SIZE = 0.5


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--blend-file", type=str, default="./assets/objects.blend"
    )

    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


if __name__ == "__main__":
    # 引数の読み込み
    args = parse_args()
    blend_file = args.blend_file

    # 環境変数の読み込み
    github_username = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")

    # すべてのオブジェクト削除
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # grass object の読み込み
    object_filenames = ["Grass", "DirtBlock", "GrassBlock", "GrassFloor", "Fog"]
    for f in object_filenames:
        bpy.ops.wm.append(
            filename=f,
            filepath=os.path.join(blend_file, "Object", f),
            directory=os.path.join(blend_file, "Object"),
        )

    # GitHub contributions を取得
    data = fetch_github_contributions(github_username, github_token)

    # Fog の生成
    obj = bpy.data.objects["Fog"]
    obj = obj.copy()
    obj.data = obj.data.copy()
    obj.dimensions = (
        GRID_SIZE * data.total_weeks * 4,
        GRID_SIZE * 7 * 4,
        40 * 2,
    )
    obj.location = (
        (data.total_weeks) * GRID_SIZE,
        -14 * GRID_SIZE,
        0,
    )
    bpy.context.collection.objects.link(obj)

    # 位置
    for i, week in enumerate(data.level_matrix):
        for j, level in enumerate(week):

            # Dirt の生成
            obj = bpy.data.objects["DirtBlock"]
            obj = obj.copy()
            obj.data = obj.data.copy()
            obj.dimensions = (
                GRID_SIZE,
                GRID_SIZE,
                obj.dimensions.z,
            )
            obj.scale.z = GRID_SIZE / obj.dimensions.x
            obj.location = (
                (i + 1 / 2) * GRID_SIZE,
                -(j + 1 / 2) * GRID_SIZE,
                0,
            )
            bpy.context.collection.objects.link(obj)

            # Grass の生成
            if level == "NONE":
                obj = bpy.data.objects["Grass"]
                z_scale = 0
                density = 0
            elif level == "FIRST_QUARTILE":
                obj = bpy.data.objects["Grass"]
                z_scale = 0.1
                density = 1
            elif level == "SECOND_QUARTILE":
                obj = bpy.data.objects["Grass"]
                z_scale = 0.3
                density = 2
            elif level == "THIRD_QUARTILE":
                obj = bpy.data.objects["Grass"]
                z_scale = 0.5
                density = 3
            elif level == "FOURTH_QUARTILE":
                obj = bpy.data.objects["Grass"]
                z_scale = 1.0
                density = 4
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
            obj.scale.z = z_scale

            obj.modifiers["GeometryNodes"]["Socket_4"] = density

            bpy.context.collection.objects.link(obj)

    # Original grass object の削除
    for obj in bpy.data.objects:
        if obj.name in object_filenames:
            bpy.data.objects.remove(obj)

    # カメラ
    look_at = (53 * GRID_SIZE / 2, -7 * GRID_SIZE / 4, 0)
    camera_location = (53 * GRID_SIZE / 2, -65 * GRID_SIZE, 45 * GRID_SIZE)
    direction = mathutils.Vector(camera_location) - mathutils.Vector(look_at)
    quaternion = direction.to_track_quat("Z", "Y")
    bpy.ops.object.camera_add(location=camera_location)
    bpy.context.object.rotation_euler = quaternion.to_euler()

    bpy.context.object.data.ortho_scale = 20
    bpy.context.scene.camera = bpy.context.object

    # ライト
    bpy.ops.object.light_add(type="SUN", rotation=(math.pi / 4, 0, -math.pi / 4))
    bpy.context.object.data.energy = 2

    # レンダリング
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = "./dist/output.png"
    # 背景を透過
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.resolution_x = int(1280 * 2)
    bpy.context.scene.render.resolution_y = int(128 * 2.5)
    bpy.context.scene.cycles.samples = 32
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.device = "CPU"
    bpy.ops.render.render(write_still=True)
