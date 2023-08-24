import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *
import sys, os
import argparse

# Command Line Arguments 
# To use, add "--" after the python script name in the command line, then add arguments
parser = argparse.ArgumentParser(description='Python Blender script for time series scene')
parser.add_argument('-c', '--current-frame', type=int, default='0', help='current animation frame')
parser.add_argument('-s', '--script-path', type=str, default='E:/Argonne/23/Blender/', help='full path to top directory')
parser.add_argument('-o', '--output-path', type=str, default='image', help='image output name and full path')
parser.add_argument('-d', '--render-device', type=str, default='CPU', help='use CPU or GPU')

args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])

current_frame = args.current_frame
script_path = args.script_path
output_full = args.output_path
render_device = args.render_device

#Each of the dta sources
bad_rbc_data_name = "bad_rbc_%s" % current_frame
rbc_data_name = "rbc_%s" % current_frame
cont_data_name = "continuum_%s" % current_frame
cont_volume_data_name = "continuum__%05d" % current_frame

# Remove everything
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

## SCIENTIFIC DATA ## 

#Import PLY - bad_rbc
full_file_path = "%s/data/%s.ply" % (script_path, bad_rbc_data_name)
bpy.ops.import_mesh.ply(filepath=full_file_path)
object = bpy.data.objects[bad_rbc_data_name]

object.modifiers.new("sub", "SUBSURF")
object.modifiers["sub"].render_levels = 2

# MATERIAL SET UP
MAT_NAME = "badMat"

badMat = bpy.data.materials.new(MAT_NAME)
badMat.use_nodes = True

# Main material node
badMat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.2
badMat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1,1,1,1)

# Access vertex colors
colAttr = badMat.node_tree.nodes.new('ShaderNodeAttribute')
colAttr.attribute_name = "Col"

# Create material output node
matOutput = badMat.node_tree.nodes.new('ShaderNodeOutputMaterial')

#Link nodes
badMat.node_tree.links.new(
    colAttr.outputs['Color'],
    badMat.node_tree.nodes['Principled BSDF'].inputs['Base Color']
)

badMat.node_tree.links.new(
    badMat.node_tree.nodes['Principled BSDF'].outputs['BSDF'],
    matOutput.inputs['Surface']
)
# Apply material to data object 
bpy.context.view_layer.objects.active = object
bpy.context.active_object.data.materials.append(badMat)

#Import PLY - rbc
full_file_path = "%s/data/%s.ply" % (script_path, rbc_data_name)
bpy.ops.import_mesh.ply(filepath=full_file_path)
object = bpy.data.objects[rbc_data_name]

object.modifiers.new("sub", "SUBSURF")
object.modifiers["sub"].render_levels = 2

# MATERIAL SET UP
MAT_NAME = "rbcMat"

rbcMat = bpy.data.materials.new(MAT_NAME)
rbcMat.use_nodes = True

# Main material node
rbcMat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.2
rbcMat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1,0,0,1)


# Create material output node
matOutput = rbcMat.node_tree.nodes.new('ShaderNodeOutputMaterial')

#Link nodes
rbcMat.node_tree.links.new(
    rbcMat.node_tree.nodes['Principled BSDF'].outputs['BSDF'],
    matOutput.inputs['Surface']
)
# Apply material to data object 
bpy.context.view_layer.objects.active = object
bpy.context.active_object.data.materials.append(rbcMat)

#Import PLY - continuum
full_file_path = "%s/data/%s.ply" % (script_path, cont_data_name)
bpy.ops.import_mesh.ply(filepath=full_file_path)
object = bpy.data.objects[cont_data_name]

MAT_NAME = "Cont_mat"

contMat = bpy.data.materials.new(MAT_NAME)
contMat.use_nodes = True

# Main material node
contMat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.2
contMat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1,1,1,1)

# Access vertex colors
colAttr = contMat.node_tree.nodes.new('ShaderNodeAttribute')
colAttr.attribute_name = "Col"

# Set up Color Ramp
colRamp = contMat.node_tree.nodes.new('ShaderNodeValToRGB')

colRamp.color_ramp.color_mode = 'RGB'
colRamp.color_ramp.interpolation = 'B_SPLINE'

# set the left most color 
colRamp.color_ramp.elements[0].color=(0.973444, 0.98225, 0.514918, 1)
colRamp.color_ramp.elements.new(position = 0.25)
colRamp.color_ramp.elements.new(position = 0.5)
colRamp.color_ramp.elements.new(position = 0.75)

# set the left middle
colRamp.color_ramp.elements[1].color=(0.973445, 0.250158, 0.122139, 1)
# set the middle color 
colRamp.color_ramp.elements[2].color=(0.473532, 0.0382042, 0.191202, 1)
# set the right middle
colRamp.color_ramp.elements[3].color=(0.0822826, 0.00604874, 0.201556, 1)
# set the right color to blue
colRamp.color_ramp.elements[4].color=(0, 0, 0.00121411, 1)

# Create material output node
matOutput = bpy.data.materials["Cont_mat"].node_tree.nodes.new('ShaderNodeOutputMaterial')

#Link nodes
bpy.data.materials["Cont_mat"].node_tree.links.new(
    colAttr.outputs['Color'],
    colRamp.inputs['Fac']
)

bpy.data.materials["Cont_mat"].node_tree.links.new(
    colRamp.outputs['Color'],
    bpy.data.materials["Cont_mat"].node_tree.nodes['Principled BSDF'].inputs['Base Color']
)

bpy.data.materials["Cont_mat"].node_tree.links.new(
    bpy.data.materials["Cont_mat"].node_tree.nodes['Principled BSDF'].outputs['BSDF'],
    matOutput.inputs['Surface']
)

# Apply material to data object 
bpy.context.view_layer.objects.active = object
bpy.context.active_object.data.materials.append(contMat)

#Import VDB - continuum
'''
full_file_path = "%s/data/%s.vdb" % (script_path, cont_volume_data_name)
bpy.ops.object.volume_import(filepath=full_file_path)
object = bpy.data.objects[cont_volume_data_name]

#Material set up
MAT_NAME = "prinVolMat"

prinVolMat = bpy.data.materials.new(MAT_NAME)
prinVolMat.use_nodes = True

prinVol = prinVolMat.node_tree.nodes.new('ShaderNodeVolumePrincipled')
prinVolMat.node_tree.nodes['Principled Volume'].inputs['Color Attribute'].default_value = "color"
prinVolMat.node_tree.nodes['Principled Volume'].inputs['Density Attribute'].default_value = "alpha"

bpy.context.view_layer.objects.active = object
bpy.context.active_object.data.materials.append(prinVolMat)
'''

#SCENE OBJECTS

#Background Plane
bpy.ops.mesh.primitive_plane_add(
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=Vector((-23.87725067138672, 25.3665771484375, -16.26943588256836)),
        rotation=Euler((-0.06135699152946472, 0.9851000905036926, -0.5607742667198181), 'XYZ'),
        scale=Vector((38.806793212890625, 58.36347961425781, 25.71484375))
)
object = bpy.data.objects['Plane']
object.location = Vector((-12.482641220092773, 44.34839630126953, -16.14191436767578))
object.scale = Vector((204.99540328979492, 170.237186431884766, 11.1422924995422363))
object.rotation_euler = Euler((1.1034115552902222, -0.0, 0.5590581893920898), 'XYZ')

# Set up materials

MAT_NAME = "Plane_mat"
# Main material node
planeMat = bpy.data.materials.new(MAT_NAME)
planeMat.use_nodes = True
planeMat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.613528, 1, 0.908286, 1)

# Create material output
matOutput = planeMat.node_tree.nodes.new('ShaderNodeOutputMaterial')

planeMat.node_tree.links.new(
    planeMat.node_tree.nodes['Principled BSDF'].outputs['BSDF'],
    matOutput.inputs['Surface']
)

# Apply material
bpy.context.view_layer.objects.active = object
bpy.context.active_object.data.materials.append(planeMat)


# Create camera
bpy.ops.object.add(type='CAMERA', location=Vector((97.48680114746094, -43.38798141479492, 30.169830322265625)))
camera = bpy.context.object
camera.rotation_euler = Euler((1.220420002937317, 0.013844029977917671, 1.0379341840744019), 'XYZ')
camera.data.lens = 50


# Make this the current camera
bpy.context.scene.camera = camera

# Create Empty 
bpy.ops.object.add(type='EMPTY', location=Vector((0, 0, 0)))

# Make Camera a child of Empty 
empty = bpy.data.objects['Empty']
camera.parent = empty

# Set keyframe 1 on Empty z-axis rotation
# Set the keyframe with that location, and which frame.
empty.keyframe_insert(data_path="rotation_euler", frame=1)

# Rotate Empty Z axis
empty.rotation_euler = Euler((0.0, 0.0, 0.19914574921131134), 'XYZ')

# Set keyframe 5
empty.keyframe_insert(data_path="rotation_euler", frame=5)

# Set key frame 10
empty.rotation_euler = Euler((0.0, 0.0, 0.0), 'XYZ')
empty.keyframe_insert(data_path="rotation_euler", frame=10)

# Lights
pos = Vector((4.076245307922363, 1.0054539442062378, 5.903861999511719))
bpy.ops.object.add(type='LIGHT', location=pos)
obj = bpy.context.object
obj.data.type = 'SUN'
obj.data.energy = 10

# Render image
scene = bpy.context.scene
scene.view_settings.look = "Medium High Contrast"
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 256
scene.frame_set(current_frame+1)

scene.render.filepath = "%s_%d.png" % (output_full, current_frame)
bpy.ops.render.render(write_still=True)
