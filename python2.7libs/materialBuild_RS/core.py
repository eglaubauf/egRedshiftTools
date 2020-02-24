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
import eg_setupOGL
import re

reload(eg_RSMat)
reload(eg_setupOGL)


class Core():

    def __init__(self):
        self.nodes = hou.selectedNodes()
        self.name = self.init_name()
        self.context = hou.node("/mat")
        self.ogl = False
        self.apply = False
        self.convert = False
        self.material = None
        self.useTex = False

    def set_apply_mat(self, enabled):
        if enabled:
            self.apply = True
        else:
            self.apply = False

    def set_context(self, enabled):
        if enabled:
            # get Context from caller
            if self.nodes:
                self.context = self.nodes[0].parent()
            else:
                self.context = hou.node("/mat")
        else:
            self.context = hou.node("/mat")

    def set_convert(self, enabled):
        self.convert = enabled

    def set_ogl(self, enabled):
        self.ogl = enabled

    def set_use_tex(self, enabled):
        self.useTex = enabled

    def init_name(self):
        if self.nodes:
            return self.nodes[0].name()
        else:
            return "RedshiftMaterial"

    def set_name(self, text):
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

    def get_context_name(self):
        return self.context.name()

    def create_material(self):
        # Create RS Material
        if self.get_context_name() != "mat":
            # create mat contxt here
            # print("Current Context:     " + self.get_context_name())
            self.context = self.context.createNode("matnet")

        # Create Material
        self.material = eg_RSMat.RSMat(self.context, self.name, self.useTex, self.convert)

        # Apply Material to Selection
        if self.apply:
            self.apply_mat()

        # Create OGL Attributes
        if self.ogl:
            self.create_ogl_attribs()

        # TODO: Convert Textures to OCIO - OOP
        # if self.convert:
        #     self.convert_textures()

    def create_ogl_attribs(self):
        eg_setupOGL.rsOGL(self.material.get_material_builder())

    def apply_mat(self):
        displace = self.material.get_displace()
        if self.nodes:
            for n in self.nodes:
                n.parm("shop_materialpath").set(self.material.get_path())
                if displace:
                    n.parm("RS_objprop_rstess_enable").set(1)
                    n.parm("RS_objprop_displace_enable").set(1)
