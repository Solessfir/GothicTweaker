# Gothic Tweaker
Blender Addon for fixing Gothic World after importing it using [KrxImpExp](https://gitlab.com/Patrix9999/krximpexp)  
**Tested for Gothic 2 only! You may encounter some problems if you use it with Gothic 1**

![image](https://user-images.githubusercontent.com/34831419/222477330-d5cf2d72-bac5-438e-af0a-818558535d69.png)

### Installation:
1. [Download](https://github.com/Solessfir/GothicTweaker/releases/tag/3.4) GothicTweaker.zip
2. Extract to *...Blender [version]\\[version]\scripts\addons*
* Alternatively, use *Install an Addon* from Blender *Preferences*

### Usage:
Press N and find *Gothic Tweaker* tab

### What it does:
* **Clean Collision:** This will remove all collision and sun blocker faces and their materials
* **Rename Material Slots:** Renames all Material Slots to the name of their Texture file and cleans all duplicates
* **Rename All Meshes:** This will rename all meshes in *.blend* file by their material name. Assuming that you have split mesh by material otherwise, it will use the first material index as the name
* **Apply Alpha:** This will fix Alpha on the Trees, Water, Flags, etc. This should be used if KrxImpExp didn't fix it on the import or you want to apply opacity to Gothic 2 water bodies
* **Float parameter:** -1 = Disabled. Opacity that will be added to Gothic 2 Water. Don't use it for Gothic 1 it will probably not work or will work partially only

### Notes:
* I have extensively used *Material Utilities* addon that comes with *Blender* to clean and merge materials
* This Addon was used to clean exported *.zen* world with all *VOBs*. Guide can be found [here](https://telegra.ph/How-to-export-all-VOBs-from-ZEN-02-26)
* There is an old alternative that can be found [here](https://forum.worldofplayers.de/forum/threads/1492323-Blender-Script-Gothic-MaT-Blender)
