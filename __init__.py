# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Gothic Tweaker",
    "author" : "Solessfir",
    "description" : "",
    "blender" : (3, 4, 1),
    "version" : (1, 0, 0),
    "location" : "3D Viewport Sidebar",
    "warning" : "",
    "category" : "3D View"
}

import bpy.utils, bpy.types, bpy.props
from .GothicTweakerPanel import PropertyGroup_GothicTweaker, Panel_GothicTweaker
from .GothicTweakerOperators import Operator_CleanCollision, Operator_ApplyAlpha, Operator_RenameMaterialSlots, Operator_RenameAllMeshsByMaterialName

classes = (
    PropertyGroup_GothicTweaker,
    Panel_GothicTweaker,
    Operator_CleanCollision,
    Operator_ApplyAlpha,
    Operator_RenameMaterialSlots,
    Operator_RenameAllMeshsByMaterialName
)

def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)

    # Assign property group
    bpy.types.Scene.PropertyGroup_GothicTweaker = bpy.props.PointerProperty(type = PropertyGroup_GothicTweaker)
    

def unregister():
    # Delete property group
    del bpy.types.Scene.PropertyGroup_GothicTweaker

    for class_to_unregister in reversed(classes):
        bpy.utils.unregister_class(class_to_unregister)

if __name__ == "__main__":
    register()