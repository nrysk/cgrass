import math
import os
import random
from enum import StrEnum

import bpy
import mathutils

from fetch import ContributionData, ContributionLevel

GRID_SIZE = 1


class ObjectName(StrEnum):
    GROUND0 = "Ground0"
    GROUND1 = "Ground1"
    GROUND2 = "Ground2"
    GROUND3 = "Ground3"
    GROUND4 = "Ground4"
    GRASS = "Grass"
    DIRT_BLOCK = "DirtBlock"
    GRASS_BLOCK = "GrassBlock"
    GRASS_FLOOR = "GrassFloor"
    FOG = "Fog"


class MaterialName(StrEnum):
    GROUND_NONE = "GroundNone"
    GROUND_FIRST_QUARTILE = "GroundFirst"
    GROUND_SECOND_QUARTILE = "GroundSecond"
    GROUND_THIRD_QUARTILE = "GroundThird"
    GROUND_FOURTH_QUARTILE = "GroundFourth"


def delete_all():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def load_objects(blend_file: str, object_filenames: list[str]):
    for f in object_filenames:
        bpy.ops.wm.append(
            filename=f,
            filepath=os.path.join(blend_file, "Object", f),
            directory=os.path.join(blend_file, "Object"),
        )


def delete_objects(object_names: list[str]):
    for obj in bpy.data.objects:
        if obj.name in object_names:
            bpy.data.objects.remove(obj)


def place_fog(
    object_name: str,
):
    pass


def place_ground(level_matrix: list[list[ContributionLevel]]):
    ground_objects = [
        bpy.data.objects[ObjectName.GROUND1],
        bpy.data.objects[ObjectName.GROUND2],
        bpy.data.objects[ObjectName.GROUND3],
        bpy.data.objects[ObjectName.GROUND4],
    ]
    level_to_material = {
        ContributionLevel.NONE: MaterialName.GROUND_NONE,
        ContributionLevel.FIRST_QUARTILE: MaterialName.GROUND_FIRST_QUARTILE,
        ContributionLevel.SECOND_QUARTILE: MaterialName.GROUND_SECOND_QUARTILE,
        ContributionLevel.THIRD_QUARTILE: MaterialName.GROUND_THIRD_QUARTILE,
        ContributionLevel.FOURTH_QUARTILE: MaterialName.GROUND_FOURTH_QUARTILE,
    }

    for i_col, week in enumerate(level_matrix):
        for i_row, level in enumerate(week):
            obj = random.choice(ground_objects)
            obj = obj.copy()
            obj.data = obj.data.copy()

            obj.dimensions = (
                GRID_SIZE,
                GRID_SIZE,
                0.5 * GRID_SIZE,
            )
            obj.location = (
                (i_col + 0.5) * GRID_SIZE,
                -(i_row + 0.5) * GRID_SIZE,
                0,
            )

            obj.data.materials.clear()
            mat = bpy.data.materials[level_to_material[level]]
            obj.data.materials.append(mat)

            bpy.context.collection.objects.link(obj)


def place_grass(data: ContributionData):
    object_name_dict = {
        ContributionLevel.NONE: ObjectName.GRASS,
        ContributionLevel.FIRST_QUARTILE: ObjectName.GRASS,
        ContributionLevel.SECOND_QUARTILE: ObjectName.GRASS,
        ContributionLevel.THIRD_QUARTILE: ObjectName.GRASS,
        ContributionLevel.FOURTH_QUARTILE: ObjectName.GRASS,
    }

    for i, week in enumerate(data.level_matrix):
        for j, level in enumerate(week):
            obj = bpy.data.objects[object_name_dict[level]]
            obj = obj.copy()
            obj.data = obj.data.copy()

            obj.dimensions = (
                GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            )
            obj.location = (
                (i + 0.5) * GRID_SIZE,
                -(j + 0.5) * GRID_SIZE,
                0,
            )
            bpy.context.collection.objects.link(obj)


def place_camera(
    location: tuple[float, float, float],
    look_at: tuple[float, float, float],
):
    direction = mathutils.Vector(location) - mathutils.Vector(look_at)
    quaternion = direction.to_track_quat("Z", "Y")
    bpy.ops.object.camera_add(location=location)
    bpy.context.object.rotation_euler = quaternion.to_euler()

    bpy.context.object.data.ortho_scale = 20
    bpy.context.scene.camera = bpy.context.object


def place_sun(rotation: tuple[float, float, float]):
    bpy.ops.object.light_add(type="SUN", rotation=rotation)
    bpy.context.object.data.energy = 6


def render_image(
    output_dir: str,
    resolution: tuple[int, int] = (1920, 256),
    samples: int = 32,
):
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = os.path.join(output_dir, "output.png")
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]
    bpy.context.scene.cycles.samples = samples
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.device = "CPU"
    bpy.ops.render.render(write_still=True)


def generate(
    blend_file: str,
    data: ContributionData,
):
    delete_all()
    load_objects(blend_file, [o.value for o in ObjectName])
    place_ground(data.level_matrix)
    # place_grass(data)

    delete_objects([o.value for o in ObjectName])
    place_camera(
        location=(53 / 2 * GRID_SIZE, -65 * GRID_SIZE, 45 * GRID_SIZE),
        look_at=(53 / 2 * GRID_SIZE, -7 / 4 * GRID_SIZE, 0),
    )
    place_sun((math.pi / 4, 0, -math.pi / 4))
    render_image("./dist")
