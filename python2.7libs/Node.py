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


class rs_OGL_UI:

    def __init__(self, n):

        hou_parm_template_group = hou.ParmTemplateGroup()
        # Code for parameter template
        hou_parm_template = hou.FolderParmTemplate("Redshift_SHOP_parmSwitcher3", "Settings", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template2 = hou.IntParmTemplate("RS_matprop_ID", "Material ID", 1, default_value=([0]), min=0, max=100, min_is_strict=True, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        hou_parm_template_group.append(hou_parm_template)
        # Code for parameter template
        hou_parm_template = hou.FolderParmTemplate("Redshift_SHOP_parmSwitcher3_1", "OpenGL", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template2 = hou.ToggleParmTemplate("ogl_light", "OGL Use Lighting", default_value=True)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        # Code for parameter template
        hou_parm_template2 = hou.FloatParmTemplate("ogl_alpha", "OGL Alpha", 1, default_value=([1]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        # Code for parameter template
        hou_parm_template2 = hou.FolderParmTemplate("folder0", "Diffuse", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_diff_intensity", "Diffuse Intensity", 1, default_value=([1]), min=0, max=2, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("The diffuse intensity multiplies the Diffuse color, allowing it to be easily adjusted without affecting the its hue or saturation.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_diff", "OGL Diffuse", 3, default_value=([1, 1, 1]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.ColorSquare, naming_scheme=hou.parmNamingScheme.RGBA)
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FolderParmTemplate("ogl_numtex", "Diffuse Texture Layers", folder_type=hou.folderType.MultiparmBlock, default_value=0, ends_tab_group=False)
        hou_parm_template3.setTags({"spare_category": "OpenGL"})
        # Code for parameter template
        hou_parm_template4 = hou.ToggleParmTemplate("ogl_use_tex#", "Use Diffuse Map #", default_value=True)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        # Code for parameter template
        hou_parm_template4 = hou.StringParmTemplate("ogl_tex#", "Texture #", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        # Code for parameter template
        hou_parm_template4 = hou.StringParmTemplate("ogl_texuvset#", "UV Set", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["uv","uv2","uv3","uv4","uv5","uv6","uv7","uv8"]), menu_labels=(["uv","uv2","uv3","uv4","uv5","uv6","uv7","uv8"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        # Code for parameter template
        hou_parm_template2 = hou.FolderParmTemplate("folder0_1", "Specular", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_spec", "Enable Specular", default_value=True)
        hou_parm_template3.setHelp("Toggles contribution of the specular color. When off, no specular highlights will appear.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_spec_intensity", "Specular Intensity", 1, default_value=([1]), min=0, max=2, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("The specular intensity multiplies the Specular color, allowing it to be easily adjusted without affecting the its hue or saturation.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_spec", "OGL Specular", 3, default_value=([0.2, 0.2, 0.2]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.ColorSquare, naming_scheme=hou.parmNamingScheme.RGBA)
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_rough", "OGL Roughness", 1, default_value=([0.05]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_reflect", "Reflect", 1, default_value=([0]), min=0, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("The reflectiveness of the material, from 0 (not at all reflective) to 1 (completely reflective).")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_ior", "Index of Refraction", 1, default_value=([1.33]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("Index of refraction of the material, used for fresnel calculations and reflection.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_metallic", "Metallic", 1, default_value=([0]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("Metallic factor, from 0-1. The more metallic a surface is (approaching 1), the less diffuse and more reflection the material will have. A metallic factor closer to zero behaves more like a dielectric material. ")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_metallicmap", "Use Metallic Map", default_value=True)
        hou_parm_template3.setHelp("When enabled, use the map specified in ogl_metallicmap for the metallic map. If this property is not present, it is assumed to be enabled.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_metallicmap", "Metallic Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("Texture map for Metallic. The GL Metallic parameter is multiplied by the texture map value.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.IntParmTemplate("ogl_metallicmap_comp", "Metallic Channel", 1, default_value=([0]), min=0, max=4, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1","2","3","4"]), menu_labels=(["Luminance","Red","Green","Blue","Alpha"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_metallicmap == \\\"\\\\\\\"\\\\\\\"\\\" }")
        hou_parm_template3.setHelp("Channel of the metallic texture map to sample (luminance, red, green, blue, alpha).")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_roughmap", "Use Roughness Map", default_value=True)
        hou_parm_template3.setHelp("When enabled, use the map specified in ogl_roughmap for the roughness map. If this property is not present, it is assumed to be enabled.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_roughmap", "Roughness Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("Texture map for Roughness. Rougher surfaces have larger but dimmer specular highlights. This overrides the constant ogl_rough.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_invertroughmap", "Invert Roughness Map (Glossiness)", default_value=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_roughmap == \\\"\\\\\\\"\\\\\\\"\\\" }")
        hou_parm_template3.setHelp("Invert the roughness map so that it is interpreted as a gloss map - zero is no gloss (dull), one is very glossy (shiny).")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.IntParmTemplate("ogl_roughmap_comp", "Roughness Channel", 1, default_value=([0]), min=0, max=4, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1","2","3","4"]), menu_labels=(["Luminance","Red","Green","Blue","Alpha"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_roughmap == \\\"\\\\\\\"\\\\\\\"\\\" }")
        hou_parm_template3.setHelp("Texture component used for Roughness within the Roughness texture map, which can be the luminance of RGB, red, green, blue or alpha. This allows roughness to be sourced from packed texture maps which contain parameters in the other texture channels.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        # Code for parameter template
        hou_parm_template2 = hou.FolderParmTemplate("folder0_2", "Normal", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_normalmap", "Use Normal Map", default_value=True)
        hou_parm_template3.setHelp("When enabled, use the map specified in ogl_normalmap for the normal map. If this property is not present, it is assumed to be enabled.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_normalmap", "Normal Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("Use a normal map to specify normals instead of interpolating normals across a polygon. The RGB values are used for the normal's XYZ vector.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_normalmap_type", "Normal Map Type", 1, default_value=(["uvtangent"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["uvtangent","world","object"]), menu_labels=(["Tangent Space","World Space","Object Space"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
        hou_parm_template3.setHelp("Specifies the space that the normal map operates in: UV Tangent, World, or Object space.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.IntParmTemplate("ogl_normalbias", "Normal Map Range", 1, default_value=([0]), min=0, max=10, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1"]), menu_labels=(["0 to 1","-1 to 1"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\\\\\"\\\\\\\"\\\" }")
        hou_parm_template3.setHelp("The range of the normal map is either 0-1 (8b map) or -1 to 1 (floating point map). This bias must match the type of normal map used.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_normalmap_scale", "Normal Scale", 1, default_value=([1]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\\\\\"\\\\\\\"\\\" }")
        hou_parm_template3.setHelp("Scales the X and Y components of a tangent normal map to increase or decrease the effect the normal map has on the normals.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_normalflipx", "Flip Normal Map X", default_value=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\\\\\"\\\\\\\"\\\" }")
        hou_parm_template3.setHelp("Flip the normal's X direction when applying the normal map. This may be needed for normal maps generated by other applications. ")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_normalflipy", "Flip Normal Map Y", default_value=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\\\\\"\\\\\\\"\\\" }")
        hou_parm_template3.setHelp("Flip the normal's Y direction when applying the normal map. This may be needed for normal maps generated by other applications. ")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        # Code for parameter template
        hou_parm_template2 = hou.FolderParmTemplate("folder0_3", "Emission", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_emit_intensity", "Emission Intensity", 1, default_value=([1]), min=0, max=2, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("The emission intensity multiplies the Emission color, allowing it to be easily adjusted without affecting the its hue or saturation.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_emissionmap", "Emission Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("An image file used for emission texturing. Unlike a diffuse map, the emission map is not affected by lighting and appears constant. The RGB values of the emission map are multiplied by the ogl_emit color which defaults to (0,0,0), so this should be set to (1,1,1) if an emission map is used. The alpha of an emission map is ignored.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_emit", "OGL Emission", 3, default_value=([0, 0, 0]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.ColorSquare, naming_scheme=hou.parmNamingScheme.RGBA)
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        hou_parm_template.addParmTemplate(hou_parm_template2)

        hou_parm_template_group.append(hou_parm_template)
        n.setParmTemplateGroup(hou_parm_template_group)
        # Set Default States
        n.parm("ogl_numtex").set(1)
