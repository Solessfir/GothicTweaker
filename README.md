# Gothic Tweaker
Blender Addon for fixing Gothic World after importing it using [KrxImpExp](https://gitlab.com/Patrix9999/krximpexp)

### Installation:
1. Rename the downloaded folder to GothicTweaker
2. Copy to *...Blender \*version*\\*version\*\scripts\addons*<br><br>
Alternatively, use *Install an Addon* from Blender *Preferences*

### Usage:
Press *N* and find *Gothic Tweaker* tab

### What it does:
* **Clean Collision:** This will remove all collision and sun blocker faces and their materials
* **Fix Alpha:** This will fix Alpha on the Trees, Flags, etc.
* **Rename Material Slots:** This will rename all material slots by their texture name
* **Rename All Meshes:** This will rename all meshes in *.blend* file by their material name. Assuming that you have split mesh by material otherwise, it will use the first material index as name

### Notes:
* I have extensively used *Material Utilities* addon that comes with *Blender* to clean and merge materials
* This Addon was used to clean exported *.zen* world with all *VOBs*. Guide can be found [here](https://telegra.ph/How-to-export-all-VOBs-from-ZEN-02-26)