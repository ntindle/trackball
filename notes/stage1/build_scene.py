# Stage-1 Blender-manual review scene for trackball-base (drc127) — v2.
# Usage: blender --background --python /tmp/stage1_scene.py   (cwd = work root)
# Env PREVIEW=1 -> fast 800px/32sp top+sensor+back diagnostic renders.
# Builds fallback bodies for parts missing from the KiCad GLB export
# (custom .wrl unloadable in KiCad 10 export; J201/L501/F101/D502 stock
# models absent from install), lights a neutral stage, renders 4 views.
import bpy, math, os

PREVIEW = os.environ.get('PREVIEW', '') == '1'
OUT = 'notes/stage1'
GLB = os.path.join(OUT, 'trackball-base-review.glb')

# ---- clear ----
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
    for b in list(datablocks):
        datablocks.remove(b)

# ---- import ----
bpy.ops.import_scene.gltf(filepath=GLB)
print('imported:', len(bpy.context.selected_objects), 'objects')

# ---- calibrate pcb-mm -> world mapping from known nodes ----
CAL = {'U501': (55.0, 16.0), 'U202': (55.0, 124.0),
       'SW201': (74.5, 4.5), 'SW202': (85.5, 5.0)}
pts = []
for ref, (px, py) in CAL.items():
    o = bpy.data.objects.get(ref)
    if o is None:
        print('CAL MISSING:', ref); continue
    w = o.matrix_world.translation
    pts.append((px, py, w.x, w.y, w.z))
assert len(pts) >= 3, 'calibration failed'
def fit(pairs):
    n = len(pairs); sx = sum(p[0] for p in pairs); sy = sum(p[1] for p in pairs)
    sxx = sum(p[0]*p[0] for p in pairs); sxy = sum(p[0]*p[1] for p in pairs)
    s = (n*sxy - sx*sy)/(n*sxx - sx*sx); t = (sy - s*sx)/n
    return s, t
sx, tx = fit([(px, X) for px, py, X, Y, Z in pts])
sy, ty = fit([(py, Y) for px, py, X, Y, Z in pts])
def G(px, py):
    return (sx*px + tx, sy*py + ty)
print('map: X = %.6f*px + %.6f ; Y = %.6f*py + %.6f' % (sx, tx, sy, ty))
z0 = [Z for px, py, X, Y, Z in pts if abs(px-55.0) < 0.01 and abs(py-16.0) < 0.01][0]
print('board-top z0 =', round(z0, 6))

# ---- materials ----
def mat(name, base, rough=0.6, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*base, 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metallic
    return m
M_CHAR = mat('FB_charcoal', (0.07, 0.07, 0.08), 0.8)
M_DARK = mat('FB_darkgrey', (0.14, 0.14, 0.16), 0.7)
M_MID  = mat('FB_midgrey', (0.13, 0.13, 0.14), 0.65)
M_MET  = mat('FB_metal', (0.5, 0.51, 0.53), 0.35, 1.0)
M_MOD  = mat('FB_module', (0.55, 0.55, 0.58), 0.5)

def box(name, px, py, lx, ly, lz, sxmm, symm, szmm, rot, material):
    dx, dy = (lx, ly) if abs(((rot % 360)+180) % 360 - 180) < 1 else (-lx, -ly)
    X, Y = G(px+dx, py+dy)
    s = abs(sx)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(X, Y, z0 + lz*s))
    o = bpy.context.active_object
    o.name = name
    o.dimensions = (sxmm*s, symm*s, szmm*s)
    o.data.materials.append(material)
    return o

def cyl(name, px, py, lx, ly, lz, rmm, hmm, rot, material):
    dx, dy = (lx, ly) if abs(((rot % 360)+180) % 360 - 180) < 1 else (-lx, -ly)
    X, Y = G(px+dx, py+dy)
    s = abs(sx)
    bpy.ops.mesh.primitive_cylinder_add(radius=rmm*s, depth=hmm*s,
                                        location=(X, Y, z0 + lz*s), vertices=48)
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(material)
    return o

# Fallbacks from project .wrl massing dims (numbers-as-mm; KiCad 10 export
# cannot load the .wrl files, see LAYOUT_REVIEW §9).
for ref, (px, py) in {'U301': (41.66, 71.59), 'U302': (68.34, 71.59)}.items():
    box(ref+'_body', px, py, -0.57, 0, 1.2, 16.2, 10.1, 2.4, 0, M_CHAR)
    cyl(ref+'_lens', px, py, 0, 0, 5.75, 5.0, 6.7, 0, M_DARK)
    box(ref+'_plate', px, py, -0.295, 0, 8.9, 21.15, 18.85, 1.0, 0, M_MID)
for ref, (px, py) in {'SW401': (35.0, 100.0), 'SW402': (75.0, 100.0), 'SW403': (55.0, 93.0)}.items():
    box(ref+'_body', px, py, 0, 0, 3.0, 12.8, 5.8, 6.0, 0, M_CHAR)
    cyl(ref+'_plunger', px, py, -5.2, 0, 6.5, 0.6, 1.5, 0, M_MET)
box('U201_body', 22.0, 10.0, 0, 0, 1.1, 13, 18, 2.2, 180, M_MOD)
box('U201_shield', 22.0, 10.0, 0, 7.5, 2.6, 10, 3, 0.8, 180, M_CHAR)
# J201/L501: courtyard-extruded placeholders, NOMINAL heights (no vendor
# model in repo/install; verify against vendor drawings before MECH sign-off).
box('J201_FALLBACK', 55.0, 133.44, 0, 0, 1.75, 10.68, 9.47, 3.5, 0, M_MET)
box('L501_FALLBACK', 55.0, 10.0, 0, 0, 3.0, 7.04, 6.06, 6.0, 0, M_CHAR)
fb = [o for o in bpy.data.objects if o.name.startswith(('U30', 'SW40', 'U201', 'J201', 'L501'))]
print('fallbacks:', len(fb))

# Recolor the anonymous near-white partial-board sheet (mat_17) to mask
# green so it cannot wash out the top face; it is used by exactly one mesh.
m17 = bpy.data.materials.get('mat_17')
if m17 is not None:
    m17.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.08, 0.2, 0.14, 1.0)
    print('mat_17 -> mask green')

# ---- world / lights / ground ----
world = bpy.data.worlds['World']
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.05, 0.055, 0.065, 1.0)
bg.inputs['Strength'].default_value = 0.25

def area(name, loc, energy, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    o = bpy.context.active_object; o.name = name
    o.data.energy = energy; o.data.size = size
    # aim at board center
    bpy.ops.object.empty_add(location=(cx, cy, z0))
    e = bpy.context.active_object
    tr = o.constraints.new(type='TRACK_TO')
    tr.target = e; tr.track_axis = 'TRACK_NEGATIVE_Z'; tr.up_axis = 'UP_Y'
    return o
cx, cy = G(55.0, 70.0)
area('Key', (cx-0.15, cy-0.12, z0+0.35), 4, 0.25)
area('Fill', (cx+0.18, cy+0.05, z0+0.22), 1.2, 0.3)
area('Rim', (cx+0.02, cy+0.20, z0+0.18), 2, 0.2)
area('Under_key', (cx-0.10, cy+0.08, z0-0.25), 3, 0.3)
area('Under_fill', (cx+0.12, cy-0.10, z0-0.25), 1.2, 0.3)
bpy.ops.mesh.primitive_plane_add(size=2.0, location=(cx, cy, z0-0.035))
ground = bpy.context.active_object
ground.name = 'Ground'
ground.is_shadow_catcher = True

# ---- cameras ----
def cam(name, loc, target):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.active_object; c.name = name
    c.data.lens = 50
    c.data.clip_start = 0.005
    c.data.clip_end = 5.0
    bpy.ops.object.empty_add(location=target)
    e = bpy.context.active_object; e.name = name + '_tgt'
    tr = c.constraints.new(type='TRACK_TO')
    tr.target = e; tr.track_axis = 'TRACK_NEGATIVE_Z'; tr.up_axis = 'UP_Y'
    return c
cam('Cam_hero', (cx+0.16, cy-0.19, z0+0.17), (cx, cy, z0))
cam('Cam_top', (cx+0.005, cy-0.055, z0+0.27), (cx, cy, z0))
sgx, sgy = G(55.0, 71.59)
cam('Cam_sensor', (sgx+0.085, sgy-0.10, z0+0.105), (sgx, sgy, z0+0.004))
cam('Cam_back', (cx-0.13, cy+0.15, z0-0.20), (cx, cy, z0))

# ---- render ----
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 32 if PREVIEW else 64
scene.cycles.use_denoising = True
try:
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception:
    pass
scene.render.film_transparent = False
if PREVIEW:
    jobs = [('Cam_top', 'prev-top.png', 800, 800, False),
            ('Cam_sensor', 'prev-sensor.png', 800, 800, False),
            ('Cam_back', 'prev-back.png', 800, 800, True)]
else:
    jobs = [('Cam_hero', 'blend-hero.png', 1920, 1080, False),
            ('Cam_top', 'blend-top.png', 1600, 1600, False),
            ('Cam_sensor', 'blend-sensor.png', 1600, 1600, False),
            ('Cam_back', 'blend-back.png', 1600, 1600, True)]
for camname, fn, w, h, hide_ground in jobs:
    scene.camera = bpy.data.objects[camname]
    ground.hide_render = hide_ground
    scene.render.resolution_x = w; scene.render.resolution_y = h
    scene.render.filepath = os.path.join(OUT, fn)
    bpy.ops.render.render(write_still=True)
    print('wrote', fn)
