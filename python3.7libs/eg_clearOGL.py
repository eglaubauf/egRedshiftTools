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
This script will remove an OpenGL-Setup from a Material

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import hou


def run():
    clr = ClearOGL(hou.selectedNodes())
    clr.clear_ogl()

class ClearOGL():
    """Clears OGL Connections from a RS-MaterialBuilder"""
    def __init__(self, n=None):

        self.context = hou.node("/mat")
        self.nodes = n
        self.count = 0


    def clear_ogl(self):
        """Iterates over all selected Nodes and applies a Material"""
        # With No Selection just create a Material Node
        if not self.nodes:
            self.display_message()
            return

        for mb in self.nodes:
            if mb.type().name() == "redshift_vopnet":
                parms = mb.parms()
                for p in reversed(parms):
                    if p is not None:
                        p.deleteAllKeyframes()
                    pt = p.tuple()
                    if pt:
                        pt.revertToAndRestorePermanentDefaults()




    def display_message(self):
        """Displays the Count of Created Materials to the User"""
        if self.count > 0:
            hou.ui.displayMessage(str(self.count) + ' Materialnodes have been cleared')
        else:
            hou.ui.displayMessage('No Materials Found!')
