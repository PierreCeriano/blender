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
# File: room_maker.py
# Automatic generation of rooms
# Author: Antonio Vazquez (antonioya)
#
#----------------------------------------------------------
import bpy
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
    # Create room
    myRoom = create_room(self,context,"Room",self.room_height)
    myRoom.select = True
    bpy.context.scene.objects.active = myRoom
    
    remove_doubles(myRoom)
    set_normals(myRoom,not self.inverse) # inside/outside

    if (self.wall_width > 0.0):
        set_modifier_solidify(myRoom,self.wall_width)
        
    # Create baseboard
    if (self.baseboard):
        myBase = create_room(self,context,"Baseboard",self.base_height,True)
        set_normals(myBase,self.inverse) # inside/outside room
        if (self.base_width > 0.0):
            set_modifier_solidify(myBase,self.base_width)
        myBase.parent = myRoom    
        
    # Create floor
    if (self.floor):
        myFloor = create_floor(self,context,"Floor",myRoom)
        myFloor.parent = myRoom    

    # Create ceiling
    if (self.ceiling):
        myCeiling = create_floor(self,context,"Ceiling",myRoom)
        myCeiling.parent = myRoom    

    # Create materials        
    if (self.crt_mat):
        # Wall material (two faces)
        mat = create_diffuse_material("Wall_material",False,0.765, 0.650, 0.588,0.8,0.621,0.570,0.1,True)
        set_material(myRoom,mat)
        # Baseboard material
        if (self.baseboard):
            mat = create_diffuse_material("Baseboard_material",False,0.8, 0.8, 0.8)
            set_material(myBase,mat)
        
        # Ceiling material
        if (self.ceiling):
            mat = create_diffuse_material("Ceiling_material",False,0.95, 0.95, 0.95)
            set_material(myCeiling,mat)
            
        # Floor material    
        if (self.floor):
            mat = create_brick_material("Floor_material",False,0.711, 0.668, 0.668,0.8,0.636,0.315)
            set_material(myFloor,mat)
          
    bpy.ops.object.select_all(False)    
    myRoom.select = True
    bpy.context.scene.objects.active = myRoom
            
    return
#------------------------------------------------------------------------------
# Create Room/baseboard
# Some custom values are passed using self container (self.myvariable)
#------------------------------------------------------------------------------
def create_room(self,context,objName,height,baseboard = False):

    myVertex = []
    myFaces = []
    lastFace = 0
    #---------------------------------
    # Horizontal (First)
    #---------------------------------
    if (self.wall_num >= 1):
        if (self.a01 == False or baseboard == True):
            myVertex.extend([(0.0,0.0,0.0),(0.0,0.0,height),(self.w01,0.0,height),(self.w01,0.0,0.0)])
            myFaces.extend([(0,1,2,3)])
            lastFace = 2
            lastX = self.w01
            lastY = 0.0
        else:
            mid = self.w01 / 2 + ((self.w01 / 2) * self.f01)
            # first
            myVertex.extend([(0.0,0.0,0.0)
                             ,(0.0,0.0,height)
                             ,(mid,0.0,height + self.m01)
                             ,(mid,0.0,0.0)])
            if (math.fabs(self.f01) != 1):
                myFaces.extend([(0,1,2,3)])  
            # second
            myVertex.extend([(self.w01,0.0,0.0),(self.w01,0.0,height)])
            if (math.fabs(self.f01) != 1): 
                myFaces.extend([(2,3,4,5)])
            else:    
                myFaces.extend([(0,1,5,4),(1,2,5)])
            
            lastFace = 4
                
            lastX = self.w01
            lastY = 0.0
            
        
    #---------------------------------
    # Vertical
    #---------------------------------
    if (self.wall_num >= 2):
        myDat = vertical_wall(self.a01,
                              self.a02,self.w02,self.m02,self.f02
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]
        
    # Horizontal
    if (self.wall_num >= 3):
        myDat = horizontal_wall(self.a02,
                              self.a03,self.w03,self.m03,self.f03
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]
        
    # Vertical
    if (self.wall_num >= 4):
        myDat = vertical_wall(self.a03,
                              self.a04,self.w04,self.m04,self.f04
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]
        
    # Horizontal
    if (self.wall_num >= 5):
        myDat = horizontal_wall(self.a04,
                              self.a05,self.w05,self.m05,self.f05
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]
        
    # Vertical
    if (self.wall_num >= 6):
        myDat = vertical_wall(self.a05,
                              self.a06,self.w06,self.m06,self.f06
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]

    # Horizontal
    if (self.wall_num >= 7):
        myDat = horizontal_wall(self.a06,
                              self.a07,self.w07,self.m07,self.f07
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]
        
    # Vertical
    if (self.wall_num >= 8):
        myDat = vertical_wall(self.a07,
                              self.a08,self.w08,self.m08,self.f08
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]

    # Horizontal
    if (self.wall_num >= 9):
        myDat = horizontal_wall(self.a08,
                              self.a09,self.w09,self.m09,self.f09
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]
        
    # Vertical
    if (self.wall_num >= 10):
        myDat = vertical_wall(self.a09,
                              self.a10,self.w10,self.m10,self.f10
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]

    # Horizontal
    if (self.wall_num >= 11):
        myDat = horizontal_wall(self.a10,
                              self.a11,self.w11,self.m11,self.f11
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]
        
    # Vertical
    if (self.wall_num >= 12):
        myDat = vertical_wall(self.a11,
                              self.a12,self.w12,self.m12,self.f12
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]

    # Horizontal
    if (self.wall_num >= 13):
        myDat = horizontal_wall(self.a12,
                              self.a13,self.w13,self.m13,self.f13
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]
        
    # Vertical
    if (self.wall_num >= 14):
        myDat = vertical_wall(self.a13,
                              self.a14,self.w14,self.m14,self.f14
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]

    # Horizontal
    if (self.wall_num >= 15):
        myDat = horizontal_wall(self.a14,
                              self.a15,self.w15,self.m15,self.f15
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]
        
    # Vertical
    if (self.wall_num >= 16):
        myDat = vertical_wall(self.a15,
                              self.a16,self.w16,self.m16,self.f16
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]

    # Horizontal
    if (self.wall_num >= 17):
        myDat = horizontal_wall(self.a16,
                              self.a17,self.w17,self.m17,self.f17
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]
        
    # Vertical
    if (self.wall_num >= 18):
        myDat = vertical_wall(self.a17,
                              self.a18,self.w18,self.m18,self.f18
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]

    # Horizontal
    if (self.wall_num >= 19):
        myDat = horizontal_wall(self.a18,
                              self.a19,self.w19,self.m19,self.f19
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastX = myDat[0]
        lastFace = myDat[1]

    # Vertical
    if (self.wall_num >= 20):
        myDat = vertical_wall(self.a19,
                              self.a20,self.w20,self.m20,self.f20
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces)
        lastY = myDat[0]
        lastFace = myDat[1]
        
    # Close room
    if (self.merge == True):
        if (baseboard == False):     
            if ((self.wall_num == 1 and self.a01 == True)
            or (self.wall_num == 2 and self.a02 == True)
            or (self.wall_num == 3 and self.a03 == True)
            or (self.wall_num == 4 and self.a04 == True)
            or (self.wall_num == 5 and self.a05 == True)
            or (self.wall_num == 6 and self.a06 == True)
            or (self.wall_num == 7 and self.a07 == True)
            or (self.wall_num == 8 and self.a08 == True)
            or (self.wall_num == 9 and self.a09 == True)
            or (self.wall_num == 10 and self.a10 == True)
            or (self.wall_num == 11 and self.a11 == True)
            or (self.wall_num == 12 and self.a12 == True)
            or (self.wall_num == 13 and self.a13 == True)
            or (self.wall_num == 14 and self.a14 == True)
            or (self.wall_num == 15 and self.a15 == True)
            or (self.wall_num == 16 and self.a16 == True)
            or (self.wall_num == 17 and self.a17 == True)
            or (self.wall_num == 18 and self.a18 == True)
            or (self.wall_num == 19 and self.a19 == True)
            or (self.wall_num == 20 and self.a20 == True)):
                myFaces.extend([(0,1,lastFace + 1, lastFace)])
            else:   
                myFaces.extend([(0,1,lastFace, lastFace + 1)])
        else:
            myFaces.extend([(0,1,self.wall_num * 2, self.wall_num * 2 + 1)])   
        
        
    mymesh = bpy.data.meshes.new(objName)
    myobject = bpy.data.objects.new(objName, mymesh)
    
    myobject.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(myobject)
    
    mymesh.from_pydata(myVertex, [], myFaces)
    mymesh.update(calc_edges=True)
    
    return myobject
#------------------------------------------------------------------------------
# Vertical Wall
#------------------------------------------------------------------------------
def vertical_wall(prv,advance,size,over,factor,baseboard,lastFace,lastX,lastY,height,myVertex,myFaces):
    if (advance == False or baseboard == True):
        myVertex.extend([(lastX,size + lastY,height),(lastX,size + lastY,0.0)])
        if (prv == False or baseboard == True):
            myFaces.extend([(lastFace,lastFace + 2,lastFace + 3,lastFace + 1)]) # no advance
        else:
            myFaces.extend([(lastFace,lastFace + 1,lastFace + 2,lastFace + 3)]) # advance
            
        lastFace = lastFace + 2
    else:
        mid = size / 2 + ((size / 2) * factor)
        # first
        myVertex.extend([(lastX,mid + lastY,height + over)
                         ,(lastX,mid + lastY,0.0)])
        if (math.fabs(factor) != 1):
            if (prv == False):
                myFaces.extend([(lastFace,lastFace + 2,lastFace + 3,lastFace + 1)]) # no advance
            else:
                myFaces.extend([(lastFace,lastFace + 1,lastFace + 2,lastFace + 3)]) # advance
        # second
        myVertex.extend([(lastX,lastY + size,0.0),(lastX,lastY + size,height)])
        if (math.fabs(factor) != 1): 
            myFaces.extend([(lastFace + 2,lastFace + 3,lastFace + 4,lastFace+ 5)])
        else:   
            if (prv == False):
                myFaces.extend([(lastFace, lastFace + 5, lastFace + 4, lastFace + 1)
                               ,(lastFace, lastFace + 2, lastFace + 5)])
            else:
                myFaces.extend([(lastFace, lastFace + 4, lastFace + 5, lastFace + 1)
                               ,(lastFace + 1, lastFace + 2, lastFace + 5)])
            
        lastFace = lastFace + 4
        
    lastY = size + lastY
        
    return (lastY,lastFace)

#------------------------------------------------------------------------------
# Horizontal Wall
#------------------------------------------------------------------------------
def horizontal_wall(prv,advance,size,over,factor,baseboard,lastFace,lastX,lastY,height,myVertex,myFaces):
    if (advance == False or baseboard == True):
        myVertex.extend([(lastX + size,lastY,height),(lastX + size,lastY,0.0)])
        if (prv == False or baseboard == True):
            myFaces.extend([(lastFace,lastFace + 2,lastFace + 3,lastFace + 1)]) # no advance
        else:
            myFaces.extend([(lastFace,lastFace + 1,lastFace + 2,lastFace + 3)]) # advance
            
        lastFace = lastFace + 2
    else:
        mid = size / 2 + ((size / 2) * factor)
        # first
        myVertex.extend([(mid + lastX,lastY,height + over)
                         ,(mid + lastX,lastY,0.0)])
        if (math.fabs(factor) != 1):
            if (prv == False):
                myFaces.extend([(lastFace,lastFace + 2,lastFace + 3,lastFace + 1)]) # no advance
            else:
                myFaces.extend([(lastFace,lastFace + 1,lastFace + 2,lastFace + 3)]) # advance
        # second
        myVertex.extend([(lastX + size,lastY,0.0),(lastX + size,lastY,height)])
        if (math.fabs(factor) != 1): 
            myFaces.extend([(lastFace + 2,lastFace + 3,lastFace + 4,lastFace+ 5)])
        else:   
            if (prv == False):
                myFaces.extend([(lastFace, lastFace + 5, lastFace + 4, lastFace + 1)
                               ,(lastFace, lastFace + 2, lastFace + 5)])
            else:
                myFaces.extend([(lastFace, lastFace + 4, lastFace + 5, lastFace + 1)
                               ,(lastFace + 1, lastFace + 2, lastFace + 5)])
            
        lastFace = lastFace + 4
        
    lastX = size + lastX
        
    return (lastX,lastFace)

#------------------------------------------------------------------------------
# Create Floor or Ceiling
#------------------------------------------------------------------------------
def create_floor(self,context,typ,myRoom):
    bpy.context.scene.objects.active = myRoom

    myVertex = []
    myFaces = []
    verts = []
    
    obverts = bpy.context.active_object.data.vertices
    for vertex in obverts:
        verts.append(tuple(vertex.co))
    # Loop only selected
    i = 0 
    for e in verts:
        if (typ == "Floor"):
            if(e[2] == 0.0):
                myVertex.extend([(e[0],e[1],e[2])])
                i = i + 1    
        else: # ceiling
            if(e[2] == self.room_height):
                myVertex.extend([(e[0],e[1],e[2])])    
                i = i + 1
    # Create faces
    fa = []
    for f in range(0,i):
        fa.extend([f])
                        
    myFaces.extend([fa])
        
        
    mymesh = bpy.data.meshes.new(typ)
    myobject = bpy.data.objects.new(typ, mymesh)
    
    myobject.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(myobject)
    
    mymesh.from_pydata(myVertex, [], myFaces)
    mymesh.update(calc_edges=True)
    
    return myobject

#----------------------------------------------
# Code to run alone the script
#----------------------------------------------
if __name__ == "__main__":
    create_mesh(0)
    print("Executed")
