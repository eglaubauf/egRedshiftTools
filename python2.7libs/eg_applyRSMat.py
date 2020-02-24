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
import eg_createRSMat
import eg_setupOGL
from collections import Iterable

reload(eg_createRSMat)
reload(eg_setupOGL)


class ApplyRSMat():
    """Applies an RS MAT to a Selection"""
    def __init__(self, n=None):
        self.context = hou.node("/mat")

        # Check if Called Via RightClickMenu
        if not n:
            self.nodes = self.get_nodes()
        else:
            self.nodes = n

        self.count = 0
        self.create_materials()
        self.display_message()

    def get_nodes(self):
        """Calls the Selected Nodes"""
        return hou.selectedNodes()

    def create_materials(self):
        """Iterates over all selected Nodes and applies a Material"""
        # With No Selection just create a Material Node
        if not self.nodes:
            m = eg_createRSMat.RSMat(self.context)
            # Setup OpenGL Shaders
            eg_setupOGL.rsOGL(m.get_materialbuilder())
            self.count += 1
        # Check if Called Via RightClickMenu
        if isinstance(self.nodes, Iterable):
            for n in self.nodes:
                # Check against OBJ-Level Nodes and Subnets
                if n.type().category() != hou.objNodeTypeCategory():
                    break
                if not n.isSubNetwork():
                    m = eg_createRSMat.RSMat(self.context, n.name())
                    n.parm("shop_materialpath").set(m.get_path())
                    # Setup OpenGL Shaders
                    eg_setupOGL.rsOGL(m.get_materialbuilder())
                    self.count += 1
        else:
            # For Calling Via Right Click Menu
            if self.nodes.type().category() != hou.objNodeTypeCategory():
                return
            if not self.nodes.isSubNetwork():
                m = eg_createRSMat.RSMat(self.context, self.nodes.name())
                self.nodes.parm("shop_materialpath").set(m.get_path())
                # Setup OpenGL Shaders
                eg_setupOGL.rsOGL(m.get_materialbuilder())
                self.count += 1

    def display_message(self):
        """Displays the Count of Created Materials to the User"""
        if self.count > 0:
            hou.ui.displayMessage(str(self.count) + ' Materialnodes have been created')
        else:
            hou.ui.displayMessage('Please select OBJ-Nodes to create Materials')
