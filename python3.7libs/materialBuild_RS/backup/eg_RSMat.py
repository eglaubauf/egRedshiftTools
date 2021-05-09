#####################################
#  LICENSE                            #
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

# TODO: Make OOP Texture Convert and File Read
# TODO: Make Linear/sRBG Switch, based on File name

class RSMat():
    """Creates an RS-Material in the given context"""
    def __init__(self, context=hou.node("/mat"), name="RedshiftMaterial", tex=False, convert=False):

        self.convert = convert

        if self.convert:
            # Check against OCIO
            if not hou.getenv("OCIO"):
                hou.ui.displayMessage("Please enable OCIO to convert Textures")
                return

        self.context = context
        self.name = name
        self.tex = tex
        self.init_variables()

        self.create_material()

    def init_variables(self):
        # Variables used by Class
        self.img = ""

        # RS Material
        self.material_builder = None
        self.rs_mat = None
        self.redshift_material = None

        # MaterialComponents
        self.base_color = ""
        self.roughness = ""
        self.normal = ""
        self.metallic = ""
        self.reflect = ""
        self.displace = ""
        self.bump = ""
        self.ao = ""

    def create_material(self):
        """Creates an RS-Material in the given context"""

        # Get Files if requested by User
        if self.tex:
            if not self.get_files():
                return

        # RS Material Builder
        self.material_builder = self.context.createNode("redshift_vopnet")
        self.material_builder.setName(self.name, True)
        self.material_builder.moveToGoodPosition()

        # RS Material
        self.redshift_material = self.material_builder.children()[0]
        self.rs_mat = self.material_builder.createNode('redshift::Material')
        self.redshift_material.setInput(0, self.rs_mat, 0)

        # Create Layers if requested by User
        if self.tex:
            self.create_layers()

        self.material_builder.layoutChildren()

    def create_layers(self):
        #################
        #     Layers    #
        #################
        if self.base_color != "":
            if self.convert:
                self.base_color = self.convert_files(self.base_color, 0)
            self.create_texture(self.material_builder, self.rs_mat, self.base_color, "Base_Color")
            if self.ao != "":
                if self.convert:
                    self.ao = self.convert_files(self.ao, 0)
                self.create_texture(self.material_builder, self.rs_mat, self.ao, "Ambient_Occlusion")
        if self.roughness != "":
            if self.convert:
                self.roughness = self.convert_files(self.roughness, 0)
            self.create_texture(self.material_builder, self.rs_mat, self.roughness, "Roughness")
        if self.metallic != "":
            if self.convert:
                self.metallic = self.convert_files(self.metallic, 0)
            self.create_texture(self.material_builder, self.rs_mat, self.metallic, "Metallic")
        if self.reflect != "":
            if self.convert:
                self.reflect = self.convert_files(self.reflect, 0)
            self.create_texture(self.material_builder, self.rs_mat, self.reflect, "Reflectivity")
        if self.normal != "":
            if self.convert:
                self.normal = self.convert_files(self.normal, 0)
            self.create_normal(self.material_builder, self.rs_mat, self.normal, "Normal")
        if self.bump != "":
            if self.convert:
                self.bump = self.convert_files(self.bump, 0)
            self.create_bump(self.material_builder, self.rs_mat, self.bump, "Bump")
        if self.displace != "":
            if self.convert:
                self.displace = self.convert_files(self.displace, 0)
            self.create_displace(self.material_builder, self.redshift_material, self.displace, "Displacement")
            self.displaceFlag = 1

    def create_texture(self, parent, connector, channel, channelName):

        tex = parent.createNode("redshift::TextureSampler")
        tex.setName(channelName, True)
        tex.parm("tex0").set(channel)

        #################
        #    Layers     #
        #################
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

    def get_files(self):

        # Read Files from User
        files = hou.ui.selectFile(title="Please choose Files to create a Material from", collapse_sequences=False, multiple_select=True, file_type=hou.fileType.Image)
        if files == "":
            return False
        strings = files.split(";")

        # Get all Entries
        for i, s in enumerate(strings):
            # Remove Spaces
            s = s.rstrip(' ')
            s = s.lstrip(' ')

            # Get Name of File
            name = s.split(".")
            k = name[0].rfind("/")
            name = name[0][k + 1:]

            # Check which types have been selected. Config as you need
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
        return True

    def convert_files(self, channel, linear):

        # Get Reference to COPs Context
        cop = hou.node("/img")
        img = cop.createNode("img", "tmp")

        # Create ReadNode
        read = img.createNode("file")

        # Set ColorSpace
        if linear == 1:
            read.parm("colorspace").set("linear")
        else:
            read.parm("colorspace").set("srgb")

        # Create OCIO Node
        ocio = img.createNode("eg_ocio_convert")
        ocio.setInput(0, read, 0)

        # Create RopNode
        rop = img.createNode("rop_comp")
        rop.setInput(0, ocio, 0)
        rop.parm("trange").set(0)

        # Convert Stuff
        read.parm("filename1").set(channel)

        # Change Filename
        namePos = channel.rfind(".")
        ext = channel[namePos:]
        print(ext)
        name = channel[:namePos]
        name = name + "_OCIO" + ext

        # Render
        rop.parm("copoutput").set(name)
        rop.parm("execute").pressButton()

        # Cleanup
        img.destroy()

        # Return new Filename to Caller
        return name

    def get_material_builder(self):
        """Returns the MaterialBuilder"""
        return self.material_builder

    def get_path(self):
        """Returns the Path to the MaterialBuilder"""
        return self.material_builder.path()

    def get_displace(self):
        if self.displace != "":
            return True
        else:
            return False
