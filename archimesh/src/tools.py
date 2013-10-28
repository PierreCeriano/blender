# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

#----------------------------------------------------------
# File: tools.py
# support routines and general functions
# Author: Antonio Vazquez (antonioya)
#
#----------------------------------------------------------
import bpy

#--------------------------------------------------------------------
# Set normals
# True= faces to inside
# False= faces to outside
#--------------------------------------------------------------------
def set_normals(myObject,direction=False):
    bpy.context.scene.objects.active = myObject
# go edit mode
    bpy.ops.object.mode_set(mode='EDIT')
# select all faces
    bpy.ops.mesh.select_all(action='SELECT')
# recalculate outside normals 
    bpy.ops.mesh.normals_make_consistent(inside = direction)
# go object mode again
    bpy.ops.object.editmode_toggle()
#--------------------------------------------------------------------
# Remove doubles
#--------------------------------------------------------------------
def remove_doubles(myObject):
    bpy.context.scene.objects.active = myObject
# go edit mode
    bpy.ops.object.mode_set(mode='EDIT')
# select all faces
    bpy.ops.mesh.select_all(action='SELECT')
# remove
    bpy.ops.mesh.remove_doubles()
# go object mode again
    bpy.ops.object.editmode_toggle()
    
#--------------------------------------------------------------------
# Set shade smooth
#--------------------------------------------------------------------
def set_smooth(myObject):
    # deactivate others
    for o in bpy.data.objects:
        if (o.select == True):
            o.select = False
    
    myObject.select = True
    bpy.context.scene.objects.active = myObject
    if (bpy.context.scene.objects.active.name == myObject.name):
        bpy.ops.object.shade_smooth()
    
#--------------------------------------------------------------------
# Add modifier (subdivision)
#--------------------------------------------------------------------
def set_modifier_subsurf(myObject):
    bpy.context.scene.objects.active = myObject
    if (bpy.context.scene.objects.active.name == myObject.name):
        bpy.ops.object.modifier_add(type='SUBSURF')
        for mod in myObject.modifiers:
            if (mod.type == 'SUBSURF'):
                mod.levels = 2
#--------------------------------------------------------------------
# Add modifier (mirror)
#--------------------------------------------------------------------
def set_modifier_mirror(myObject,axis="Y"):
    bpy.ops.object.select_all(False)
    myObject.select = True
    bpy.context.scene.objects.active = myObject
    if (bpy.context.scene.objects.active.name == myObject.name):
        bpy.ops.object.modifier_add(type='MIRROR')
        for mod in myObject.modifiers:
            if (mod.type == 'MIRROR'):
                if (axis == "X"): 
                    mod.use_x = True
                else:
                    mod.use_x = False

                if (axis == "Y"): 
                    mod.use_y = True
                else:
                    mod.use_y = False
                    
                if (axis == "Z"): 
                    mod.use_z = True
                else:
                    mod.use_z = False
                    
                mod.use_clip = True
#--------------------------------------------------------------------
# Add modifier (array)
#--------------------------------------------------------------------
def set_modifier_array(myObject,axis,move,repeat, fix=False, fixmove = 0):
    bpy.ops.object.select_all(False)
    myObject.select = True
    bpy.context.scene.objects.active = myObject
    if (bpy.context.scene.objects.active.name == myObject.name):
        bpy.ops.object.modifier_add(type='ARRAY')
        for mod in myObject.modifiers:
            if (mod.type == 'ARRAY'):
                if (mod.name == "Array"):
                    mod.name = "Array_" + axis
                    mod.count = repeat
                    mod.use_constant_offset = fix
                    if (axis == "X"):
                        mod.relative_offset_displace[0] = move
                        mod.constant_offset_displace[0] = fixmove
                        mod.relative_offset_displace[1] = 0.0
                        
                    if (axis == "Y"):
                        mod.relative_offset_displace[0] = 0.0
                        mod.relative_offset_displace[1] = move
                        mod.constant_offset_displace[1] = fixmove
                    
                    
#--------------------------------------------------------------------
# Add modifier (curve)
#--------------------------------------------------------------------
def set_modifier_curve(myObject,myCurve):
    bpy.context.scene.objects.active = myObject
    if (bpy.context.scene.objects.active.name == myObject.name):
        bpy.ops.object.modifier_add(type='CURVE')
        for mod in myObject.modifiers:
            if (mod.type == 'CURVE'):
                mod.deform_axis = 'POS_X'
                mod.object = myCurve
#--------------------------------------------------------------------
# Add modifier (solidify)
#--------------------------------------------------------------------
def set_modifier_solidify(myObject,width):
    bpy.context.scene.objects.active = myObject
    if (bpy.context.scene.objects.active.name == myObject.name):
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        for mod in myObject.modifiers:
            if (mod.type == 'SOLIDIFY'):
                mod.thickness = width
                mod.use_even_offset = True
                mod.use_quality_normals = True
#--------------------------------------------------------------------
# Set material to object
#--------------------------------------------------------------------            
def set_material(myObject,myMaterial):
    bpy.context.scene.objects.active = myObject
    if (bpy.context.scene.objects.active.name == myObject.name):
        myObject.data.materials.append(myMaterial)
#--------------------------------------------------------------------
# Set material to selected faces
#--------------------------------------------------------------------
def set_material_faces(myObject,idx):
    bpy.context.scene.objects.active = myObject
    myObject.select = True
    bpy.context.object.active_material_index = idx
    if (bpy.context.scene.objects.active.name == myObject.name):
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.material_slot_assign()
            # Deselect 
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
#--------------------------------------------------------------------
# Select faces
#--------------------------------------------------------------------            
def select_faces(myObject,selFace,clear):
    myObject.select = True
    bpy.context.scene.objects.active = myObject
    if (bpy.context.scene.objects.active.name == myObject.name):
        # deselect everything
        if (clear):
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'DESELECT')
        
        # reselect the originally selected face
        bpy.ops.object.mode_set(mode = 'OBJECT')
        myObject.data.polygons[selFace].select = True
#        bpy.ops.object.mode_set(mode = 'EDIT')
        
#--------------------------------------------------------------------
# Create cycles diffuse material
#--------------------------------------------------------------------
def create_diffuse_material(matName, replace, r, g, b ,rv=0.8, gv=0.8, bv=0.8,mix = 0.1,twosides=False):
    
    # Avoid duplicate materials
    if (replace == False):
        matlist = bpy.data.materials
        for m in matlist:
            if (m.name == matName):
                return m
    # Create material
    scn = bpy.context.scene
    # Set cycles render engine if not selected
    if not scn.render.engine == 'CYCLES':
        scn.render.engine = 'CYCLES'
 
    mat = bpy.data.materials.new(matName)
    mat.diffuse_color = (rv,gv,bv) # viewport color
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
 
    node = nodes['Diffuse BSDF']
    node.inputs[0].default_value = [r, g, b, 1]
    node.location = 200, 320
    
    node = nodes.new('ShaderNodeBsdfGlossy')
    node.name = 'Glossy_0'
    node.location = 200, 0

    node = nodes.new('ShaderNodeMixShader')
    node.name = 'Mix_0'
    node.inputs[0].default_value = mix
    node.location = 500, 160
    
    node = nodes['Material Output']
    node.location = 1100, 160

    # Connect nodes
    outN = nodes['Diffuse BSDF'].outputs[0]
    inN = nodes['Mix_0'].inputs[1]
    mat.node_tree.links.new(outN, inN)   
    
    outN = nodes['Glossy_0'].outputs[0]
    inN = nodes['Mix_0'].inputs[2]
    mat.node_tree.links.new(outN, inN)   

    if (twosides == False):
        outN = nodes['Mix_0'].outputs[0]
        inN = nodes['Material Output'].inputs[0]
        mat.node_tree.links.new(outN, inN)

    
    if (twosides == True):
        node = nodes.new('ShaderNodeNewGeometry')
        node.name = 'Input_1'
        node.location = -80, -70

        node = nodes.new('ShaderNodeBsdfDiffuse')
        node.name = 'Diffuse_1'
        node.inputs[0].default_value = [0.30,0.30,0.30, 1]
        node.location = 200, -280
        
        node = nodes.new('ShaderNodeMixShader')
        node.name = 'Mix_1'
        node.inputs[0].default_value = mix
        node.location = 800, -70
        
        outN = nodes['Input_1'].outputs[6]
        inN = nodes['Mix_1'].inputs[0]
        mat.node_tree.links.new(outN, inN)   

        outN = nodes['Diffuse_1'].outputs[0]
        inN = nodes['Mix_1'].inputs[2]
        mat.node_tree.links.new(outN, inN)   

        outN = nodes['Mix_0'].outputs[0]
        inN = nodes['Mix_1'].inputs[1]
        mat.node_tree.links.new(outN, inN)
        
        outN = nodes['Mix_1'].outputs[0]
        inN = nodes['Material Output'].inputs[0]
        mat.node_tree.links.new(outN, inN)
    
       
    return mat

#--------------------------------------------------------------------
# Create cycles glossy material
#--------------------------------------------------------------------
def create_glossy_material(matName, replace, r, g, b,rv = 0.578, gv = 0.555, bv = 0.736):
    
    # Avoid duplicate materials
    if (replace == False):
        matlist = bpy.data.materials
        for m in matlist:
            if (m.name == matName):
                return m
    # Create material
    scn = bpy.context.scene
    # Set cycles render engine if not selected
    if not scn.render.engine == 'CYCLES':
        scn.render.engine = 'CYCLES'
 
    mat = bpy.data.materials.new(matName)
    mat.use_nodes = True
    mat.diffuse_color = (rv,gv,bv)
    nodes = mat.node_tree.nodes
 
    node = nodes['Diffuse BSDF']
    mat.node_tree.nodes.remove(node) # remove not used
    
    node = nodes.new('ShaderNodeBsdfGlossy')
    node.name = 'Glossy_0'
    node.inputs[0].default_value = [r, g, b, 1]
    node.location = 200, 160

    node = nodes['Material Output']
    node.location = 700, 160
    
    # Connect nodes
    outN = nodes['Glossy_0'].outputs[0]
    inN = nodes['Material Output'].inputs[0]
    mat.node_tree.links.new(outN, inN)
       
    return mat

#--------------------------------------------------------------------
# Create cycles glass material
#--------------------------------------------------------------------
def create_glass_material(matName, replace,rv=0.352716, gv=0.760852, bv=0.9):
    
    # Avoid duplicate materials
    if (replace == False):
        matlist = bpy.data.materials
        for m in matlist:
            if (m.name == matName):
                return m
    # Create material
    scn = bpy.context.scene
    # Set cycles render engine if not selected
    if not scn.render.engine == 'CYCLES':
        scn.render.engine = 'CYCLES'
 
    mat = bpy.data.materials.new(matName)
    mat.use_nodes = True
    mat.diffuse_color = (rv, gv, bv)
    nodes = mat.node_tree.nodes
 
    node = nodes['Diffuse BSDF']
    mat.node_tree.nodes.remove(node) # remove not used

    node = nodes.new('ShaderNodeLightPath')
    node.name = 'Light_0'
    node.location = 10, 160

    node = nodes.new('ShaderNodeBsdfGlass')
    node.name = 'Glass_0'
    node.location = 250, 300

    node = nodes.new('ShaderNodeBsdfTransparent')
    node.name = 'Transparent_0'
    node.location = 250, 0

    node = nodes.new('ShaderNodeMixShader')
    node.name = 'Mix_0'
    node.inputs[0].default_value = 0.1
    node.location = 500, 160
    
    node = nodes.new('ShaderNodeMixShader')
    node.name = 'Mix_1'
    node.inputs[0].default_value = 0.1
    node.location = 690, 290

    node = nodes['Material Output']
    node.location = 920, 290
    
    # Connect nodes
    outN = nodes['Light_0'].outputs[1]
    inN = nodes['Mix_0'].inputs[0]
    mat.node_tree.links.new(outN, inN)   
    
    outN = nodes['Light_0'].outputs[2]
    inN = nodes['Mix_1'].inputs[0]
    mat.node_tree.links.new(outN, inN)   
    
    outN = nodes['Glass_0'].outputs[0]
    inN = nodes['Mix_0'].inputs[1]
    mat.node_tree.links.new(outN, inN)   

    outN = nodes['Transparent_0'].outputs[0]
    inN = nodes['Mix_0'].inputs[2]
    mat.node_tree.links.new(outN, inN)   

    outN = nodes['Mix_0'].outputs[0]
    inN = nodes['Mix_1'].inputs[1]
    mat.node_tree.links.new(outN, inN)
    
    outN = nodes['Mix_1'].outputs[0]
    inN = nodes['Material Output'].inputs[0]
    mat.node_tree.links.new(outN, inN)
       
    return mat

#--------------------------------------------------------------------
# Create cycles brick texture material
#--------------------------------------------------------------------
def create_brick_material(matName, replace, r, g, b, rv = 0.8, gv = 0.636, bv = 0.315):
    
    # Avoid duplicate materials
    if (replace == False):
        matlist = bpy.data.materials
        for m in matlist:
            if (m.name == matName):
                return m
    # Create material
    scn = bpy.context.scene
    # Set cycles render engine if not selected
    if not scn.render.engine == 'CYCLES':
        scn.render.engine = 'CYCLES'
 
    mat = bpy.data.materials.new(matName)
    mat.use_nodes = True
    mat.diffuse_color = (rv, gv, bv)
    nodes = mat.node_tree.nodes
 
    node = nodes['Diffuse BSDF']
    node.inputs[0].default_value = [r, g, b, 1]
    node.location = 500, 160
    
    node = nodes['Material Output']
    node.location = 700, 160
    
    node = nodes.new('ShaderNodeTexBrick')
    node.name = 'Brick_0'
    node.inputs[3].default_value = [0.407, 0.411, 0.394, 1] # mortar color
    node.inputs[4].default_value = 3 # scale
    node.inputs[5].default_value = 0.001 # mortar
    node.inputs[7].default_value = 0.60 # size_w
    node.inputs[8].default_value = 0.30 # size_h
    node.location = 300, 160
       
    node = nodes.new('ShaderNodeRGB')
    node.name = 'RGB_0'
    node.outputs[0].default_value = [r, g, b, 1]
    node.location = 70, 160   
    
    # Connect nodes
    outN = nodes['RGB_0'].outputs['Color']
    inN = nodes['Brick_0'].inputs['Color1']
    mat.node_tree.links.new(outN, inN)   
      
    inN = nodes['Brick_0'].inputs['Color2']
    mat.node_tree.links.new(outN, inN)     
    
    outN = nodes['Brick_0'].outputs['Color']
    inN = nodes['Diffuse BSDF'].inputs['Color']
    mat.node_tree.links.new(outN, inN)     
    
    return mat             