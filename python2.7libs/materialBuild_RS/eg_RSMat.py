#####################################
#             LICENSE               #
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


class RSMat():
    """Creates an RS-Material in the given context"""
    def __init__(self, context=hou.node("/mat"), name="RedshiftMaterial", files=None):

        # Variables used by Class
        self.img = ""

        # RS Material
        self.material_builder = None
        self.rs_mat = None
        self.redshift_material = None

        self.files = files
        self.context = context
        self.name = name

    def get_material_builder(self):
        """Returns the MaterialBuilder"""
        return self.material_builder

    def get_path(self):
        """Returns the Path to the MaterialBuilder"""
        return self.material_builder.path()

    def get_displace(self):
        if self.files["displace"]:
            return True
        else:
            return False

    def get_files(self):
        return self.files

    def create_material(self):
        """Creates an RS-Material in the given context"""

        # RS Material Builder
        self.material_builder = self.context.createNode("redshift_vopnet")
        self.material_builder.setName(self.name, True)
        self.material_builder.moveToGoodPosition()

        # RS Material
        self.redshift_material = self.material_builder.children()[0]
        self.rs_mat = self.material_builder.createNode('redshift::Material')
        self.redshift_material.setInput(0, self.rs_mat, 0)

        if self.files:
            self.create_layers()

        self.material_builder.layoutChildren()

    def create_layers(self):

        if self.files["basecolor"]:
            self.create_texture(self.material_builder, self.rs_mat, self.files["basecolor"], "Base_Color")
            if self.files["ao"]:
                self.create_texture(self.material_builder, self.rs_mat, self.files["ao"], "Ambient_Occlusion")
        if self.files["roughness"]:
            self.create_texture(self.material_builder, self.rs_mat, self.files["roughness"], "Roughness")
        if self.files["metallic"]:
            self.create_texture(self.material_builder, self.rs_mat, self.files["metallic"], "Metallic")
        if self.files["reflect"]:
            self.create_texture(self.material_builder, self.rs_mat, self.files["reflect"], "Reflectivity")
        if self.files["normal"]:
            self.create_normal(self.material_builder, self.rs_mat, self.files["normal"], "Normal")
        if self.files["bump"]:
            self.create_bump(self.material_builder, self.rs_mat, self.files["bump"], "Bump")
        if self.files["displace"]:
            self.create_displace(self.material_builder, self.redshift_material, self.files["displace"], "Displacement")
            self.displaceFlag = 1

    def create_texture(self, parent, connector, channel, channelName):

        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)

        if channelName == "Base_Color":
            connector.setNamedInput("diffuse_color", tex, 0)
        elif channelName == "Roughness":
            connector.setNamedInput("refl_roughness", tex, 0)
        elif channelName == "Metallic":
            connector.setNamedInput("refl_metalness", tex, 0)
            # Enable Metalness Model
            connector.parm("refl_fresnel_mode").set('2')
        elif channelName == "Reflectivity":
            connector.setNamedInput("refl_weight", tex, 0)
        elif channelName == "Ambient_Occlusion":
            mult = parent.createNode("redshift::RSMathMulVector")
            connector.setNamedInput("diffuse_color", mult, 0)
            bc = parent.glob("Base_Color")[0]
            mult.setInput(0, bc, 0)
            mult.setInput(1, tex, 0)
        return

    def create_normal(self, parent, connector, channel, channelName):

        # Create Bump Node
        bump = parent.createNode("redshift::BumpMap")
        # Object Space Normal - seems to be a bug in RS for now (Object Space enables Tangent Space Normals)
        bump.parm("inputType").set('2')
        # Create Tex
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)
        tex.parm("tex0_gammaoverride").set('1')

        # Connect Things
        bump.setInput(0, tex, 0)
        connector.setNamedInput("bump_input", bump, 0)

    def create_displace(self, parent, connector, channel, channelName):

        # Create Displace Node
        displace = parent.createNode("redshift::Displacement")

        # Create Tex
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)
        tex.parm("tex0_gammaoverride").set('1')

        # Connect Things
        displace.setInput(0, tex, 0)
        connector.setNamedInput("Displacement", displace, 0)

    def create_bump(self, parent, connector, channel, channelName):

        # Create Bump Node
        bump = parent.createNode("redshift::BumpMap")

        # Create Tex
        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)

        # Connect Things
        bump.setInput(0, tex, 0)
        connector.setNamedInput("bump_input", bump, 0)
