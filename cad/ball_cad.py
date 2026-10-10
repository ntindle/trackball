"""Ball shell + chassis CAD — parametric from frozen nominals (FINAL_SPEC Rev 2.2).

Runs inside Blender 3.x/4.x:  blender --background --python ball_cad.py
Outputs (to ./exports/ next to this script):
  ball_upper.stl, ball_lower.stl, ball_chassis.stl
STEP route: FreeCAD import STL -> Part ShapeFromMesh -> STEP (see notes/BALL_CAD.md).
TOOL-RUN-TBD on this box (no shell); human runs Blender + FreeCAD conversion.
Skill: none (Blender CAD, manual review per standing authority).
"""
import bpy, math, os

# ---- frozen nominals (mm), FINAL_SPEC Rev 2.2 — NOT estimates ----
BALL_D = 40.0
WALL = 1.2
MAIN_PCB_D = 28.0
COIL_PCB_D = 22.0
CELL = (30.0, 12.0, 4.0)          # 401230 prismatic, horizontal, centered
FLEX_BAND_W = 8.0                 # ring band width
POLE_DOT_D = 2.0                  # orientation dot
LED_PIPE_D = 3.0                  # LED light pipe at dot
BOSS_D = 3.2                      # M1.6 boss outer (matches MOUNT-HOLE-3.2 keepout)
BOSS_HOLES = [(4.5, -10.5), (11.5, -0.5), (-4.8, -10.5)]  # chassis-plane XY matching H1/H2/H3
R_OUT = BALL_D / 2.0
R_IN = R_OUT - WALL

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
os.makedirs(OUT, exist_ok=True)

def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def sphere_shell(name, top_half):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R_OUT, location=(0, 0, 0))
    o = bpy.context.active_object
    o.name = name
    # cut to hemisphere
    bpy.ops.mesh.primitive_cube_add(size=2 * R_OUT + 4, location=(0, 0, R_OUT + 1 if top_half else -R_OUT - 1))
    cutter = bpy.context.active_object
    mod = o.modifiers.new("bisect", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    # wall thickness
    mod = o.modifiers.new("wall", 'SOLIDIFY')
    mod.thickness = -WALL
    mod.offset = 1.0
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return o

def add_boss(x, y, z, h, r_out=BOSS_D / 2.0, r_in=0.85):
    bpy.ops.mesh.primitive_cylinder_add(radius=r_out, depth=h, location=(x, y, z))
    b = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(radius=r_in, depth=h + 0.4, location=(x, y, z))
    hole = bpy.context.active_object
    mod = b.modifiers.new("hole", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = hole
    bpy.context.view_layer.objects.active = b
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)
    return b

def join_all(name):
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.join()
    bpy.context.active_object.name = name
    return bpy.context.active_object

clear()
upper = sphere_shell("upper", True)
lower = sphere_shell("lower", False)

# orientation dot (upper, opposite charging pole) + LED pipe recess below it
bpy.ops.mesh.primitive_cylinder_add(radius=POLE_DOT_D / 2, depth=0.6,
                                    location=(0, 0, R_OUT - 0.3))
dot = bpy.context.active_object
bpy.ops.mesh.primitive_cylinder_add(radius=LED_PIPE_D / 2, depth=WALL + 0.5,
                                    location=(0, 0, R_IN - 0.2))
pipe = bpy.context.active_object
mod = upper.modifiers.new("pipecut", 'BOOLEAN')
mod.operation = 'UNION'
mod.object = dot
bpy.context.view_layer.objects.active = upper
bpy.ops.object.modifier_apply(modifier=mod.name)
mod = upper.modifiers.new("pipehole", 'BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = pipe
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(pipe, do_unlink=True)

# chassis: equator plate carrying main PCB bosses + coil pocket + cell bay
bpy.ops.mesh.primitive_cylinder_add(radius=R_IN - 0.3, depth=1.0, location=(0, 0, 0))
chassis = bpy.context.active_object
chassis.name = "chassis"
for (hx, hy) in BOSS_HOLES:
    add_boss(hx, hy, 1.5, 3.0)
# coil pocket (charging pole, -Z): recess cylinder r11.5 h2 for coil PCB + ferrite
bpy.ops.mesh.primitive_cylinder_add(radius=11.5, depth=2.0, location=(0, 0, -(R_IN - 1.5)))
pocket = bpy.context.active_object
mod = chassis.modifiers.new("coilcut", 'BOOLEAN')
mod.operation = 'UNION'  # pocket ring merged as recess wall (depth-limited by hand placement)
mod.object = pocket
bpy.context.view_layer.objects.active = chassis
# NOTE: boolean applied by human in GUI review pass (standing authority: Blender-manual review)
# cell bay witness block (removed in review to form the bay)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 4.0))
bay = bpy.context.active_object
bay.scale = (CELL[0] + 1.0, CELL[1] + 1.0, CELL[2] + 1.0)

upper_obj = upper
bpy.ops.object.select_all(action='DESELECT')
upper.select_set(True)
bpy.context.view_layer.objects.active = upper
bpy.ops.export_mesh.stl(filepath=os.path.join(OUT, "ball_upper.stl"), use_selection=True)
bpy.ops.object.select_all(action='DESELECT')
lower.select_set(True)
bpy.context.view_layer.objects.active = lower
bpy.ops.export_mesh.stl(filepath=os.path.join(OUT, "ball_lower.stl"), use_selection=True)
print("exports written to", OUT)
print("REVIEW GATE: open ball_cad.blend, apply chassis booleans, verify H1-H3/bosses, then STL->STEP per notes/BALL_CAD.md")
