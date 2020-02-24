#####################################
#              LICENSE              #
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
"""
This script will create a Redshift Node Network based on a file selection

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou
import Node

reload(Node)


class rsOGL():

    def __init__(self, material=None):

        self.loadTex = True
        self.mat = None

        # If exectude in Mat-Context
        if not material:
            self.nodes = hou.selectedNodes()

            for self.n in self.nodes:
                if self.n.type().name() == "redshift_vopnet":
                    self.setup_parms()
                else:
                    hou.ui.displayMessage("Please Execute with RS-Material-Builder Selection.")
        else:
            self.n = material
            self.setup_parms()

    def setup_parms(self):

        # Load UI Template
        Node.rs_OGL_UI(self.n)

        # Get Material within new Network
        for c in self.n.children():
            if c.type().name() == "redshift_material":
                for i in c.inputs():
                    if i.type().name() == "redshift::Material":
                        self.mat = i

        # Link Parms to RS_material
        if self.mat:
            # Diffuse
            self.link_vparm("ogl_diff", "diffuse_color")
            self.link_parm("ogl_diff_intensity", "diffuse_weight")

            # Specular
            self.link_vparm("ogl_spec", "refl_color")
            self.link_parm("ogl_rough", "refl_roughness")
            self.link_parm("ogl_metallic", "refl_metalness")
            self.link_parm("ogl_ior", "refl_ior")
            self.link_parm("ogl_spec_intensity", "refl_weight")
            self.link_parm("ogl_reflect", "refl_weight")
            # Emit
            self.link_vparm("ogl_emit", "emission_color")
            self.link_parm("ogl_emit_intensity", "emission_weight")

            if self.loadTex:
                self.link_textures()

    def link_textures(self):
        # Link Textures
        inputs = self.mat.inputConnectors()
        for i in inputs:
            if i:
                if i[0].outputNode():
                    if i[0].inputNode().type().name() == "redshift::TextureSampler":
                        # Diffuse Texture
                        if(i[0].inputIndex() == 0):
                            self.n.parm("ogl_tex1").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)
                        # Roughness Texture
                        if(i[0].inputIndex() == 7):
                            self.n.parm("ogl_roughmap").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)
                            self.n.parm("ogl_rough").set(1)
                        # Metal Texture
                        if(i[0].inputIndex() == 14):
                            self.n.parm("ogl_metallicmap").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)
                        # Emit Texture
                        if(i[0].inputIndex() == 48):
                            self.n.parm("ogl_emissionmap").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)

                    if i[0].inputNode().type().name() == "redshift::NormalMap":
                        # Normal Texture
                        if(i[0].inputIndex() == 49):
                            self.n.parm("ogl_normalmap").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)

    def link_vparm(self, target, source):
        self.n.parm(target + "r").set(self.mat.parm(source + "r"), follow_parm_reference=False)
        self.n.parm(target + "g").set(self.mat.parm(source + "g"), follow_parm_reference=False)
        self.n.parm(target + "b").set(self.mat.parm(source + "b"), follow_parm_reference=False)

    def link_parm(self, target, source):
        self.n.parm(target).set(self.mat.parm(source), follow_parm_reference=False)
