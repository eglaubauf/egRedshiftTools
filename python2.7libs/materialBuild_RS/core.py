#####################################
#           LICENSE                 #
#####################################
#
# Copyright (C) 2020  Elmar Glaubauf
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

import hou
import eg_RSMat
import re

reload(eg_RSMat)


class Core():

    def __init__(self):
        self.nodes = hou.selectedNodes()
        self.name = self.initName()
        self.context = hou.node("/mat")
        self.ogl = False
        self.apply = False
        self.convert = False
        self.material = None
        self.useTex = False

    def setApplyMat(self, enabled):
        if enabled:
            self.apply = True
        else:
            self.apply = False

    def setContext(self, enabled):
        if enabled:
            # get Context from caller
            if self.nodes:
                self.context = self.nodes[0].parent()
            else:
                self.context = hou.node("/mat")
        else:
            self.context = hou.node("/mat")

    def setConvert(self, enabled):
        self.convert = enabled

    def setOGL(self, enabled):
        self.ogl = enabled

    def setUseTex(self, enabled):
        self.useTex = enabled

    def initName(self):
        if self.nodes:
            return self.nodes[0].name()
        else:
            return "RedshiftMaterial"

    def setName(self, text):
        if text == "":
            if self.nodes:
                self.name = self.nodes[0].name()
                return
            else:
                self.name = "RedshiftMaterial"
                return
        # Check against unavailable Syntax in Houdini
        # Remove Special Chars and replace them with "_"
        for k in text.split("\n"):
            text = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
        self.name = text.replace(" ", "_")

    def getContextName(self):
        return self.context.name()

    def createMaterial(self):
        # Create RS Material
        if self.getContextName() != "mat":
            # create mat contxt here
            print("Current Context:     " + self.getContextName())
            self.context = self.context.createNode("matnet")

        # Create Material
        self.material = eg_RSMat.RSMat(self.context, self.name, self.useTex)

        # Apply Material to Selection
        if self.apply:
            self.applyMat()

        # Create OGL Attributes
        if self.ogl:
            self.createOGLAttribs()

        # Convert Textures to .rs Files
        if self.convert:
            self.convertTextures()

    def applyMat(self):
        displace = self.material.get_displace()
        for n in self.nodes:
            n.parm("shop_materialpath").set(self.material.get_path())
            if displace:
                n.parm("RS_objprop_rstess_enable").set(1)
                n.parm("RS_objprop_displace_enable").set(1)
