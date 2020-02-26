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
from collections import Iterable

reload(Node)


# Run from Shelf Tool
def run():
    c = rsOGL()
    c.link_mat(True)


# Run from RightClick Menu
def run_rc(mb, channel=None):
    """Run Single Script from Shelf Menu"""
    c = rsOGL()
    c.link_mat(True, mb)


def run_rc_channel(tex, channel=None):
    """Run Single Script from RC Menu"""
    c = rsOGL(tex.parent())
    c.set_ogl_texture(tex, channel)


class rsOGL():
    """Class for Holding OGL Attributes"""
    def __init__(self, material_builder=None, load_tex=True):

        self.mb = material_builder
        self.rs_mat = None
        self.load_tex = load_tex

    def set_material(self, material):
        self.mat = material

    def link_mat(self, load_tex=False, nodes=None):
        """Link multiple from Material Context"""
        # Get Selected if started without them
        if not nodes:
            nodes = hou.selectedNodes()
        count = 0
        if isinstance(nodes, Iterable):

            for mb in nodes:
                if mb.type().name() == "geo":
                    mb = mb.parm("shop_materialpath").evalAsNode()
                if mb.type().name() == "redshift_vopnet":
                    ogl = rsOGL(load_tex)
                    ogl.link(mb)
                    count += 1
        else:
            if nodes.type().name() == "geo":
                nodes = nodes.parm("shop_materialpath").evalAsNode()
            if nodes.type().name() == "redshift_vopnet":
                ogl = rsOGL(load_tex)
                ogl.link(nodes)
                count += 1
        hou.ui.displayMessage("OGL Attributes for " + str(count) + " Nodes created (RSMB Nodes only)")

    def link(self, material_builder):
        self.mb = material_builder
        # Load UI Template
        Node.rs_OGL_UI(self.mb)
        self.setup_parms()

    def setup_parms(self):
        """Setup Parameters"""
        # Get Material within new Network
        for c in self.mb.children():
            if c.type().name() == "redshift_material":
                for i in c.inputs():
                    if i.type().name() == "redshift::Material":
                        self.rs_mat = i

        # Link Parms to RS_material
        if self.rs_mat:
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

            if self.load_tex:
                self.link_textures()

    def link_textures(self):
        """Link Textures from RS-Mat to RSMB(Vopnet)"""
        # Link Textures
        inputs = self.rs_mat.inputConnectors()
        for i in inputs:
            if i:
                if i[0].outputNode():
                    if i[0].inputNode().type().name() == "redshift::TextureSampler":
                        # Diffuse Texture
                        if(i[0].inputIndex() == 0):
                            self.mb.parm("ogl_tex1").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)
                        # Roughness Texture
                        if(i[0].inputIndex() == 7):
                            self.mb.parm("ogl_roughmap").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)
                            self.mb.parm("ogl_rough").set(1)
                        # Metal Texture
                        if(i[0].inputIndex() == 14):
                            self.mb.parm("ogl_metallicmap").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)
                        # Emit Texture
                        if(i[0].inputIndex() == 48):
                            self.mb.parm("ogl_emissionmap").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)

                    if i[0].inputNode().type().name() == "redshift::NormalMap":
                        # Normal Texture
                        if(i[0].inputIndex() == 49):
                            self.mb.parm("ogl_normalmap").set(i[0].inputNode().parm("tex0"), follow_parm_reference=False)

    def link_vparm(self, target, source):
        """Link a single Vector Parm"""
        self.mb.parm(target + "r").set(self.rs_mat.parm(source + "r"), follow_parm_reference=False)
        self.mb.parm(target + "g").set(self.rs_mat.parm(source + "g"), follow_parm_reference=False)
        self.mb.parm(target + "b").set(self.rs_mat.parm(source + "b"), follow_parm_reference=False)

    def link_parm(self, target, source):
        """Link a single Scalar Parm"""
        self.mb.parm(target).set(self.rs_mat.parm(source), follow_parm_reference=False)

    def set_ogl_texture(self, tex, channel):
        """Link the OGL Textures - Run from RC-Menu"""
        if channel == 1:
            self.mb.parm("ogl_tex1").set(tex.parm("tex0"), follow_parm_reference=False)
        elif channel == 2:
            self.mb.parm("ogl_roughmap").set(tex.parm("tex0"), follow_parm_reference=False)
            self.mb.parm("ogl_rough").set(1)
        elif channel == 3:
            self.mb.parm("ogl_metallicmap").set(tex.parm("tex0"), follow_parm_reference=False)
        elif channel == 4:
            self.mb.parm("ogl_emissionmap").set(tex.parm("tex0"), follow_parm_reference=False)
        elif channel == 5:
            self.mb.parm("ogl_normalmap").set(tex.parm("tex0"), follow_parm_reference=False)

        hou.ui.displayMessage("Texture linked")
