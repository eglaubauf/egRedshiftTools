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
This script will create a Redshift Node Network based on a file selection

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou


class convertOCIO():
    """Converts the given Textures to OCIO and returns a dictionary with the filestrings"""
    def __init__(self, files):

        self.files = files

    def convert(self):
        if self.ocio_check():
            for key in self.files:
                self.files[key] = self.convert_file(self.files[key])
        else:
            return False

    def ocio_check(self):
        # Check against OCIO
        if not hou.getenv("OCIO"):
            hou.ui.displayMessage("Please enable OCIO to convert Textures")
            return False
        return True

    def convert_file(self, channel):

        linear = self.check_linear(channel)

        # Get Reference to COPs Context
        cop = hou.node("/img")
        img = cop.createNode("img", "tmp")

        # Create ReadNode
        read = img.createNode("file")

        # Set ColorSpace
        if linear:
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

    # TODO: Implement Linear check
    def check_linear(self, channel):
        return True

    def get_files(self):
        return self.files

    def print_files(self):
        for key in self.files:
            print(self.files[key])
