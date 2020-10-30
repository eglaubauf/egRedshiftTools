# egRedshiftTools

A collection of scripts for Redshift in SideFx Houdini

## Features:

- MaterialBuilder with a set of Options which include:
  - Apply to Selection
  - Create Material in Current Context
  - Setup OpenGL Shaders for the Materials
  - Load Textures (via User Selection)
  - Convert Textures to OCIO (If Houdini is loaded with OCIO enabled)
  - Add a ColorCorrection Node on the Diffuse/BaseColor Texture
  - Apply Diffuse as a Linear Texture
  - Enable/Disable Displacement
  - Set a Name for the Material

- Apply Material (with OGL-Shaders) to Multiple Objects - no Texture Loading
- Set the Active Viewport Camera to the first ROP found - or create a ROP if none found
- Create Takes from selected Cameras and the active Redshift-ROP
- Setup OpenGL Shaders - also via Right-Click Menu in Mat Context and Textures in VOPNet (e.g.: use as Diffuse, Spec, Rough-Map,...)
- Convert Textures to OCIO (sequentiall conversion via COP-Net - slow but applicable also to Full Houdini License)
- clear OpenGL Shaders from Selection
- A TOP-Net HDA for converting Textures to OCIO - Houdini Indie Only
- sets default icons for Redshift Lights to Yellow Lamp-Icons

### additional Infos

- easy Usage via Right-Click Menus and provided shelf
- easy Install via Packages Workflow - see more below
- Tested on Houdini 18.5.376 & Redshift 3.0.31
- Tested on Windows 10
- You need Redshift installed to have this working/prevent Houdini from Crashing on Startup.

### Installation:

Copy the Provided egRedshiftTools.json to your houdini user Directory within the packages folder:

```/home/<user>/houdini18.0/packages```

Change the below line according to where you downloaded the git-Repository:

```"EGRS": "/home/elmar/git/egRedshiftTools"```


### Notes:

All of the scripts are free of charge for free use, commercial or non commercial whatsoever.  Individual Licenses are added to each file as some of these are based on work done by other devs and shall be included in branches, adaptions of this scripts. Anyone is allowed to modify, develop, change the files for his/her purpose.


### Contact/Issues/Features/Questions

If you find any bugs, have suggestions or anything else please open Issues or contact me via twitter or mail. Please check out my other Repos as well, they might be handy to you.

<br>
Twitter: @eglaubauf <br>
Web: www.elmar-glaubauf.at
