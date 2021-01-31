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
"""
This script will convert Mantra to Redshift Nodes

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou
import materialBuild_RS.eg_RSMat as rs_mat
import materialBuild_RS.eg_setupOGL as ogl
import eg_applyRSMat

# reload(ogl)
# reload(rs_mat)
# reload(eg_applyRSMat)

def run():
    """Run Script from Shelf"""

    c = convertMantraToRS()
    if c.getNodes():
        c.createMaterialFromMantra()


class convertMantraToRS():
    """Converts the given Materials from Mantra to Redshift"""

    def __init__(self, files=None):
        self.context = hou.node("/mat")
        self.nodes = None
        self.mantra_mats = []  # Nodes
        self.convert_and_replace = True


    def debug(self):
        for m in self.mantra_mats:
            print m

    def getNodes(self):

        """ Gets Nodes from User"""
        self.nodes = hou.selectedNodes()

        if self.nodes:
            for node in self.nodes:
                if node.type().name() == "principledshader::2.0":
                    self.mantra_mats.append(node)
        else:
            self.shutdown()
            return False

        if not self.mantra_mats:
            self.shutdown()
            return False

        return True
        # for m in mantra_mats:
        #     print


        #print(candidates)

        # for n in self.nodes:
        #     if n.type().name() == "geo":
        #         if n.parm("shop_materialpath").evalAsString != "":

        #             tupe = (n, n.parm("shop_materialpath").evalAsNode())
        #             self.mantra_mats.append(tupe)


    def shutdown(self):
        hou.ui.displayMessage("No Nodes selected")


    def createMaterialFromMantra(self):

        for material in self.mantra_mats:


            name = material.name()

            context = material.node("..")

            materialHandler = rs_mat.RSMat(context, name)
            materialHandler.create_material()

            mb = materialHandler.get_material_builder()

            self.transferAttributes(material, materialHandler)

            if self.convert_and_replace:
                material.destroy()
                mb.setName(name)

            #material.parm("shop_materialpath").set(materialHandler.get_path())

            # Link OpenGl
            o = ogl.rsOGL()
            o.link(mb)


    def transferAttributes(self, old_mat, m_handler):


        new_mat = m_handler.get_rsMat()

        #Set Diffuse

        new_mat.parm("diffuse_colorr").set(old_mat.parm("basecolorr").eval())
        new_mat.parm("diffuse_colorg").set(old_mat.parm("basecolorg").eval())
        new_mat.parm("diffuse_colorb").set(old_mat.parm("basecolorb").eval())
        new_mat.parm("diffuse_weight").set(old_mat.parm("albedomult").eval())

        #Set Reflect
        new_mat.parm("refl_weight").set(old_mat.parm("reflect").eval())
        new_mat.parm("refl_roughness").set(old_mat.parm("rough").eval())
        new_mat.parm("refl_metalness").set(old_mat.parm("metallic").eval())
        new_mat.parm("refl_ior").set(old_mat.parm("ior").eval())
        new_mat.parm("refl_aniso").set(old_mat.parm("aniso").eval())
        new_mat.parm("refl_aniso_rotation").set(old_mat.parm("anisodir").eval())

        #Coat
        new_mat.parm("coat_weight").set(old_mat.parm("coat").eval())
        new_mat.parm("coat_roughness").set(old_mat.parm("coatrough").eval())

        #Opacity
        new_mat.parm("opacity_colorr").set(old_mat.parm("opac").eval())
        new_mat.parm("opacity_colorg").set(old_mat.parm("opac").eval())
        new_mat.parm("opacity_colorb").set(old_mat.parm("opac").eval())

        #SSS
        new_mat.parm("ms_amount").set(old_mat.parm("sss").eval())

        #Emit
        new_mat.parm("emission_colorr").set(old_mat.parm("emitcolorr").eval())
        new_mat.parm("emission_colorg").set(old_mat.parm("emitcolorg").eval())
        new_mat.parm("emission_colorb").set(old_mat.parm("emitcolorb").eval())
        new_mat.parm("emission_colorb").set(old_mat.parm("emitint").eval())

        if old_mat.parm("basecolor_useTexture").eval():
            diffuse_tex = old_mat.parm("basecolor_texture").evalAsString()
            m_handler.create_texture(m_handler.get_material_builder(), new_mat, diffuse_tex, "Base_Color")


        m_handler.get_material_builder().layoutChildren()

        return
