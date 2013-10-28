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
# File: column_maker.py
# Automatic generation of columns
# Author: Antonio Vazquez (antonioya)
#
#----------------------------------------------------------
import bpy
import mathutils
import math
from tools import *

#------------------------------------------------------------------------------
# Generate mesh data
# All custom values are passed using self container (self.myvariable)
#------------------------------------------------------------------------------
def create_mesh(self,context):

    # deactivate others
    for o in bpy.data.objects:
        if (o.select == True):
            o.select = False
            
    bpy.ops.object.select_all(False)
    
    radio_top = self.rad_top
    if (self.keep_size == True):
        radio_mid = radio_top
        radio_bottom = radio_top
    else:
        radio_mid = self.rad_mid
        radio_bottom = self.rad_bottom    

    # Calculate height
    base_column = 0.0 
    height = self.col_height
    if (self.box_base):
        height = height - self.box_base_z
        base_column = self.box_base_z
    if (self.box_top):
        height = height - self.box_top_z
    #------------------------
    # Create circular column
    #------------------------
    if (self.model == "1"):
        bpy.ops.object.select_all(False)
        myColumn = create_circular_column(self,context,"Column",radio_top,radio_mid,radio_bottom,height)
        myColumn.select = True
        bpy.context.scene.objects.active = myColumn
        # Subsurf    
        set_smooth(myColumn)
        set_modifier_subsurf(myColumn)
    #------------------------
    # Create rectangular column
    #------------------------
    if (self.model == "2"):
        myColumn = create_rectangular_base(self,context,"Column",self.col_sx,self.col_sy,height)
        bpy.ops.object.select_all(False)
        myColumn.select = True
        bpy.context.scene.objects.active = myColumn
    #------------------------
    # Circular base
    #------------------------
    if (self.cir_base == True):
        cir_bottom = create_torus(self,context,"Column_cir_bottom",radio_bottom,self.cir_base_r,self.cir_base_z)
        bpy.ops.object.select_all(False)
        cir_bottom.select = True
        bpy.context.scene.objects.active = cir_bottom
        set_modifier_subsurf(cir_bottom)
        set_smooth(cir_bottom)
        cir_bottom.location.x = 0.0
        cir_bottom.location.y = 0.0
        cir_bottom.location.z = self.cir_base_z / 2
        cir_bottom.parent = myColumn
        
    #------------------------
    # Rectangular base
    #------------------------
    if (self.box_base == True):
        box_bottom = create_rectangular_base(self,context,"Column_box_bottom", self.box_base_x, self.box_base_y, self.box_base_z)
        bpy.ops.object.select_all(False)
        box_bottom.select = True
        bpy.context.scene.objects.active = box_bottom
        box_bottom.parent = myColumn
        box_bottom.location.x = 0.0
        box_bottom.location.y = 0.0
        box_bottom.location.z = - self.box_base_z
        # move column
        myColumn.location.z += self.box_base_z
        
    #------------------------
    # Circular top
    #------------------------
    if (self.cir_top == True):
        cir_top = create_torus(self,context,"Column_cir_top",radio_top,self.cir_top_r,self.cir_top_z)
        bpy.ops.object.select_all(False)
        cir_top.select = True
        bpy.context.scene.objects.active = cir_top
        set_modifier_subsurf(cir_top)
        set_smooth(cir_top)
        cir_top.parent = myColumn
        cir_top.location.x = 0.0 
        cir_top.location.y = 0.0 
        cir_top.location.z = height - self.cir_top_z / 2 
    
    #------------------------
    # Rectangular top
    #------------------------
    if (self.box_top == True):
        box_top = create_rectangular_base(self,context,"Column_box_bottom", self.box_top_x, self.box_top_y, self.box_top_z)
        bpy.ops.object.select_all(False)
        box_top.select = True
        bpy.context.scene.objects.active = box_top
        box_top.parent = myColumn
        box_top.location.x = 0.0
        box_top.location.y = 0.0
        box_top.location.z = height

    #------------------------
    # Create arc        
    #------------------------
    if (self.arc_top):
        myArc = create_arc(self,context,"Column_arch",self.arc_radio,self.arc_gap,self.arc_width,self.array_space_factor)
        myArc.parent = myColumn
        bpy.ops.object.select_all(False)
        myArc.select = True
        bpy.context.scene.objects.active = myArc
        set_normals(myArc)
        set_modifier_mirror(myArc,"X")
        myArc.location.x = self.arc_radio + self.arc_gap
        myArc.location.y = 0.0
        if (self.box_top == True):
            myArc.location.z = height + self.box_top_z
        else:
            myArc.location.z = height
    #------------------------
    # Create Array X       
    #------------------------
    if (self.array_num_x > 0):    
        if (self.arc_top):
            distance = ((self.arc_radio + self.arc_gap) * 2)
        else:
            distance = self.array_space_x    
            
        if (self.crt_array):
            set_modifier_array(myColumn,"X",0,self.array_num_x, True, distance) 
    
            if (self.box_base == True):
                set_modifier_array(box_bottom,"X",0,self.array_num_x,True,distance) 
            if (self.box_top == True):
                set_modifier_array(box_top,"X",0,self.array_num_x,True,distance)
    
            if (self.cir_base == True):
                set_modifier_array(cir_bottom,"X",0,self.array_num_x, True, distance) 
            if (self.cir_top == True):
                set_modifier_array(cir_top,"X",0,self.array_num_x, True, distance) 
            
            if (self.arc_top):
                if (self.array_num_x > 1):
                    set_modifier_array(myArc,"X",1,self.array_num_x - 1) # one arc minus 
    #------------------------
    # Create Array Y       
    #------------------------
    if (self.array_num_y > 0):    
        if (self.arc_top):
            distance = self.arc_width
        else:
            distance = self.array_space_y    
            
        if (self.crt_array):
            set_modifier_array(myColumn,"Y",0,self.array_num_y, True, distance) 
    
            if (self.box_base == True):
                set_modifier_array(box_bottom,"Y",0,self.array_num_y,True,distance) 
            if (self.box_top == True):
                set_modifier_array(box_top,"Y",0,self.array_num_y,True,distance)
    
            if (self.cir_base == True):
                set_modifier_array(cir_bottom,"Y",0,self.array_num_y, True, distance) 
            if (self.cir_top == True):
                set_modifier_array(cir_top,"Y",0,self.array_num_y, True, distance) 
            
            if (self.arc_top):
                if (self.array_num_y > 1):
                    set_modifier_array(myArc,"Y",1,self.array_num_y - 1) # one less
                    
    #------------------------
    # Create materials        
    #------------------------
    if (self.crt_mat):
        # Column material
        mat = create_diffuse_material("Column_material",False,0.748, 0.734, 0.392,0.573,0.581,0.318)
        set_material(myColumn,mat)
        
        if (self.box_base == True or self.box_top == True):
            mat = create_diffuse_material("Column_rect",False,0.56,0.56,0.56,0.56,0.56,0.56)
        if (self.box_base == True): set_material(box_bottom,mat)
        if (self.box_top == True): set_material(box_top,mat)
        
        if (self.cir_base == True or self.cir_top == True):
            mat = create_diffuse_material("Column_cir",False,0.65,0.65,0.65,0.65,0.65,0.65)
        if (self.cir_base == True): set_material(cir_bottom,mat)
        if (self.cir_top == True): set_material(cir_top,mat)
        
        if (self.arc_top):
            mat = create_diffuse_material("Column_arch",False,0.8,0.8,0.8)
            set_material(myArc,mat)
            
            
    bpy.ops.object.select_all(False)    
    myColumn.select = True
    bpy.context.scene.objects.active = myColumn

    return
#------------------------------------------------------------------------------
# Create Column
#------------------------------------------------------------------------------
def create_circular_column(self,context,objName,radio_top,radio_mid,radio_bottom,height):
         
    myVertex = []
    myFaces = []
    pies = [0,30,60,90,120,150,180,210,240,270,300,330] # circle
    
    # Add bottom circle
    for pie in pies:
        x = math.cos(math.radians(pie)) * radio_bottom
        y = math.sin(math.radians(pie)) * radio_bottom
        myPoint = [(x,y,0.0)]
        myVertex.extend(myPoint)
    # Add middle circle
    for pie in pies:
        x = math.cos(math.radians(pie)) * radio_mid
        y = math.sin(math.radians(pie)) * radio_mid
        myPoint = [(x,y,height / 2)]
        myVertex.extend(myPoint)
    # Add top circle
    for pie in pies:
        x = math.cos(math.radians(pie)) * radio_top
        y = math.sin(math.radians(pie)) * radio_top
        myPoint = [(x,y,height)]
        myVertex.extend(myPoint)
    #------------------------------------- 
    # Faces
    #------------------------------------- 
    t = 1       
    for n in range(0,len(pies) * 2):        
        t = t + 1
        if (t > len(pies)): 
            t = 1
            myFace = [(n,n - len(pies) + 1,n + 1,n + len(pies))]
            myFaces.extend(myFace)
        else:
            myFace = [(n,n+1,n + len(pies) + 1,n + len(pies))]
            myFaces.extend(myFace)

    
    mesh = bpy.data.meshes.new(objName)
    myobject = bpy.data.objects.new(objName, mesh)
    
    myobject.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(myobject)
    
    mesh.from_pydata(myVertex, [], myFaces)
    mesh.update(calc_edges=True)
   
    return myobject
#------------------------------------------------------------------------------
# Create Torus
#------------------------------------------------------------------------------
def create_torus(self,context,objName,radio_inside, radio_outside, height):
        
    myVertex = []
    myFaces = []
    pies = [0,30,60,90,120,150,180,210,240,270,300,330] # circle
    segments = [80,60,30,0,330,300,280] # section
    
    radio_mid = radio_outside + radio_inside - (height / 2)
    # Add internal circles Top
    for pie in pies:
        x = math.cos(math.radians(pie)) * radio_inside
        y = math.sin(math.radians(pie)) * radio_inside
        myPoint = [(x,y,height / 2)]
        myVertex.extend(myPoint)
    # Add external circles Top
    for pie in pies:
        x = math.cos(math.radians(pie)) * radio_mid
        y = math.sin(math.radians(pie)) * radio_mid
        myPoint = [(x,y,height / 2)]
        myVertex.extend(myPoint)
    # Add Intermediate lines
    for segment in segments:
        for pie in pies:
            radio_externo = radio_mid + (height * math.cos(math.radians(segment)))
            x = math.cos(math.radians(pie)) * radio_externo
            y = math.sin(math.radians(pie)) * radio_externo
            z = math.sin(math.radians(segment)) * (height / 2)
            
            myPoint = [(x,y,z)]
            myVertex.extend(myPoint)
            
    # Add internal circles Bottom
    for pie in pies:
        x = math.cos(math.radians(pie)) * radio_inside
        y = math.sin(math.radians(pie)) * radio_inside
        myPoint = [(x,y,height / 2 * -1)]
        myVertex.extend(myPoint)
    # Add external circles bottom
    for pie in pies:
        x = math.cos(math.radians(pie)) * radio_mid
        y = math.sin(math.radians(pie)) * radio_mid
        myPoint = [(x,y,height  / 2 * -1)]
        myVertex.extend(myPoint)
    
    #------------------------------------- 
    # Faces
    #------------------------------------- 
    t = 1       
    for n in range(0,len(pies) * len(segments) + (len(pies) * 2)):        
        t = t + 1
        if (t > len(pies)): 
            t = 1
            myFace = [(n,n - len(pies) + 1,n + 1,n + len(pies))]
            myFaces.extend(myFace)
        else:
            myFace = [(n,n+1,n + len(pies) + 1,n + len(pies))]
            myFaces.extend(myFace)

    
    mesh = bpy.data.meshes.new(objName)
    myobject = bpy.data.objects.new(objName, mesh)
    
    myobject.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(myobject)
    
    mesh.from_pydata(myVertex, [], myFaces)
    mesh.update(calc_edges=True)

    return myobject

#------------------------------------------------------------------------------
# Create rectangular base
#------------------------------------------------------------------------------
def create_rectangular_base(self,context,objName,x,y,z):
         
    myVertex = [(-x/2, -y/2, 0.0), (- x/2, y/2, 0.0), (x/2, y/2, 0.0), (x/2, -y/2, 0.0)
                ,(-x/2, -y/2, z), (- x/2, y/2, z), (x/2, y/2, z), (x/2, -y/2, z)]
    myFaces = [(0,1,2,3),(0,1,5,4),(1,2,6,5),(2,6,7,3),(5,6,7,4),(0,4,7,3)]
    
    mesh = bpy.data.meshes.new(objName)
    myobject = bpy.data.objects.new(objName, mesh)
    
    myobject.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(myobject)
    
    mesh.from_pydata(myVertex, [], myFaces)
    mesh.update(calc_edges=True)
   
    return myobject

#------------------------------------------------------------------------------
# Create arc
#------------------------------------------------------------------------------
def create_arc(self,context,objName,radio,gap,thickness,center):
        
    myVertex = []
    
    half = (thickness / 2)
    move = half * center
    
    list = [half + move,-half + move]
    for pos_y in list:
        #--------------------------------
        # First vertices
        #--------------------------------
        myVertex.extend([(-radio - gap,pos_y,radio + radio / 10)])
        # Flat cuts
        angle = 13 * (180 / 16)
        for i in range(1,4):
            z = math.sin(math.radians(angle)) * radio
            myPoint = [(-radio - gap,pos_y,z)]
            myVertex.extend(myPoint)        
            angle = angle + 180 / 16
    
        myVertex.extend([(-radio - gap,pos_y,0.0)])
        #--------------------------------
        # Arc points
        #--------------------------------
        angle = 180
        for i in range(0,9):
            x = math.cos(math.radians(angle)) * radio
            z = math.sin(math.radians(angle)) * radio
            myPoint = [(x,pos_y,z)]
            myVertex.extend(myPoint)        
            
            angle = angle - 180 / 16
#        #--------------------------------
        # vertical cut points
        #--------------------------------
        angle = 8 * (180 / 16)
        for i in range(1,5):
            x = math.cos(math.radians(angle)) * radio
            myPoint = [(x,pos_y,radio + radio / 10)]
            myVertex.extend(myPoint)        
            
            angle = angle + 180 / 16
        

    myFaces = [(23, 24, 21, 22),(24, 25, 20, 21),(25, 26, 19, 20),(27, 18, 19, 26),(18, 27, 28, 35)
    ,(28, 29, 34, 35),(29, 30, 33, 34),(30, 31, 32, 33),(12, 13, 31, 30),(29, 11, 12, 30)
    ,(11, 29, 28, 10),(10, 28, 27, 9),(9, 27, 26, 8),(25, 7, 8, 26),(24, 6, 7, 25)
    ,(23, 5, 6, 24),(22, 4, 5, 23),(5, 4, 3, 6),(6, 3, 2, 7),(7, 2, 1, 8)
    ,(8, 1, 0, 9),(9, 0, 17, 10),(10, 17, 16, 11),(11, 16, 15, 12),(14, 13, 12, 15)
    ,(21, 3, 4, 22),(20, 2, 3, 21),(19, 1, 2, 20),(1, 19, 18, 0),(0, 18, 35, 17)
    ,(17, 35, 34, 16),(33, 15, 16, 34),(32, 14, 15, 33)]
            
    mesh = bpy.data.meshes.new(objName)
    myObject = bpy.data.objects.new(objName, mesh)
    
    myObject.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(myObject)
    
    mesh.from_pydata(myVertex, [], myFaces)
    mesh.update(calc_edges=True)

    return myObject
#----------------------------------------------
# Code to run alone the script
#----------------------------------------------
if __name__ == "__main__":
    create_mesh(0)
    print("Executed")
