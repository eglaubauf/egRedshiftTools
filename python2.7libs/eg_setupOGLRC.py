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


class rsOGLRC():

    def __init__(self, node, channel=None):

        self.tex = node
        self.n = self.tex.parent()
        self.channel = channel

        # uild UI
        Node.rs_OGL_UI(self.n)

        self.link_textures()

    def link_textures(self):
        # Link Textures

        if self.channel == 1:
            self.n.parm("ogl_tex1").set(self.tex.parm("tex0"), follow_parm_reference=False)
        elif self.channel == 2:
            self.n.parm("ogl_roughmap").set(self.tex.parm("tex0"), follow_parm_reference=False)
            self.n.parm("ogl_rough").set(1)
        elif self.channel == 3:
            self.n.parm("ogl_metallicmap").set(self.tex.parm("tex0"), follow_parm_reference=False)
        elif self.channel == 4:
            self.n.parm("ogl_emissionmap").set(self.tex.parm("tex0"), follow_parm_reference=False)
        elif self.channel == 5:
            self.n.parm("ogl_normalmap").set(self.tex.parm("tex0"), follow_parm_reference=False)

        hou.ui.displayMessage("Texture linked")
