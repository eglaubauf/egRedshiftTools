#####################################
#LICENSE                            #
#####################################
#
# Copyright (C) 2019  Elmar Glaubauf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
This script will create a Redshift Node Network based on a file selection

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at

TODO: Enable optional Texture conversion to /rs
"""

import re
import hou
import os
import shutil

#Context
obj = hou.node("/obj")
mat = hou.node("/mat")

def run():

    c = MaterialBuildRS()
 
    
class MaterialBuildRS():
    
    def __init__(self):
        #Init Variables 
        self.initVariables()
        #Fill Variables (by User)
        self.getFiles()
        #Fill Username (by User)
        self.username = self.getName()
        #Create Material
        self.createMaterial()
        
        if self.displaceFlag == 1:
            self.notifyUser()


    def initVariables(self):
        # Variables used by Class
        self.img = ""
        
        #MaterialComponents
        self.base_color = ""
        self.roughness = ""
        self.normal = ""
        self.metallic = ""
        self.reflect = ""
        self.displace = ""
        self.bump = ""
        self.ao = ""
        self.displaceFlag = 0

    def createMaterial(self):

        #RS Material Builder
        mb = mat.createNode("redshift_vopnet")
        mb.setName(self.username, True)
        mb.moveToGoodPosition()
        
        #RS Material
        rs_mat = mb.children()[0]
        pc = mb.createNode('redshift::Material')
        rs_mat.setInput(0,pc,0)

        #################
        ######Layers#####
        #################
        if self.base_color is not "":
            #base_color = self.convertFiles(base_color, 0)
            self.createTexture(mb, pc, self.base_color, "Base_Color")
            if self.ao is not "":
        #       self.ao = convertFiles(mb, pc, self.ao, 1)
                self.createTexture(mb, pc, self.ao, "Ambient_Occlusion")
        if self.roughness is not "":
        #   roughness = convertFiles(roughness, 1)
            self.createTexture(mb, pc, self.roughness, "Roughness")
        if self.metallic is not "":
        #    metallic = convertFiles(metallic, 1)
            self.createTexture(mb, pc, self.metallic, "Metallic")
        if self.reflect is not "":
        #   reflect = convertFiles(reflect, 1)
            self.createTexture(mb, pc, self.reflect, "Reflectivity")
        if self.normal is not "":
        #   normal = convertFiles(normal, 1)
            self.createNormal( mb, pc, self.normal, "Normal")  
        if self.bump is not "":
        #     bump = convertFiles(bump, 1)
            self.createBump(mb, pc, self.bump, "Bump")     
        if self.displace is not "":
        #     bump = convertFiles(bump, 1)
            self.createDisplace(mb, rs_mat, self.displace, "Displacement")     
            self.displaceFlag = 1


        mb.layoutChildren()
        
        return

    def createTexture(self, parent, connector, channel, channelName):
        
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)

        #################
        ######Layers#####
        #################
        if channelName is "Base_Color":
            connector.setNamedInput("diffuse_color", tex, 0)
        elif channelName is "Roughness":
            connector.setNamedInput("refl_roughness",tex, 0)
        elif channelName is "Metallic":
            connector.setNamedInput("refl_metalness",tex, 0)
            #Enable Metalness Model
            connector.parm("refl_fresnel_mode").set('2')
        elif channelName is "Reflectivity":
            connector.setNamedInput("refl_weight",tex, 0)
        elif channelName is "Ambient_Occlusion":
            mult = parent.createNode("redshift::RSMathMulVector")
            connector.setNamedInput("diffuse_color", mult, 0) 
            bc = parent.glob("Base_Color")[0]
            mult.setInput(0, bc, 0)
            mult.setInput(1, tex,0)
        return

    def createNormal(self, parent, connector, channel, channelName):
        
        #Create Bump Node
        bump = parent.createNode("redshift::BumpMap")
        #Object Space Normal - seems to be a bug in RS for now (Object Space enables Tangent Space Normals)
        bump.parm("inputType").set('2')
        #Create Tex
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)
        tex.parm("tex0_gammaoverride").set('1')

        #Connect Things
        bump.setInput(0,tex,0)
        connector.setNamedInput("bump_input",bump, 0)

    def createDisplace(self, parent, connector, channel, channelName):
        
        #Create Displace Node
        displace = parent.createNode("redshift::Displacement")
        
        #Create Tex
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)
        tex.parm("tex0_gammaoverride").set('1')

        #Connect Things
        displace.setInput(0,tex,0)
        connector.setNamedInput("Displacement",displace, 0)
        
    def createBump(self, parent, connector, channel, channelName):
        
        #Create Bump Node
        bump = parent.createNode("redshift::BumpMap")
        
        #Create Tex
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)

        #Connect Things
        bump.setInput(0,tex,0)
        connector.setNamedInput("bump_input",bump, 0)
        

    def getName(self):

        #Make InputField
        username = hou.ui.readInput("Call me Names", title="Name")[1]
        if username is "":
            exit()
        #Remove Special Chars and replace them with "_"
        for k in username.split("\n"):
            username = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
        return username.replace(" ", "_")
        
        
    def getFiles(self):
        
        #Read Files from User
        files = hou.ui.selectFile(title="Please choose Files to create a Material from", collapse_sequences = False, multiple_select = True, file_type = hou.fileType.Image)
        if files is "":
            exit()
        strings = files.split(";")
    
        #Get all Entries
        for i, s in enumerate(strings):
            #Remove Spaces
            s = s.rstrip(' ')
            s = s.lstrip(' ')
            
            #Get Name of File
            name = s.split(".")
            k = name[0].rfind("/")
            name = name[0][k+1:]
        
            #Check which types have been selected. Config as you need
            if "base_color" in name.lower() or "basecolor" in name.lower():
                self.base_color = s
            elif "roughness" in name.lower():
                self.roughness = s
            elif "normal" in name.lower():
                self.normal = s
            elif "metallic" in name.lower():
                self.metallic = s
            elif "reflect" in name.lower():
                self.reflect = s
            elif "height" in name.lower():
                self.displace = s
            elif "displace" in name.lower():
                self.displace = s
            elif "bump" in name.lower():
                self.bump = s
            elif "ao" in name.lower() or "ambient_occlusion" in name:
                self.ao = s
        
        return

    def notifyUser(self):

        hou.ui.displayMessage('A Displacement Node has been created - Please enable Displacement on Mesh')

