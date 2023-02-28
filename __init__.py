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
    "version" : (1, 0, 1),
    "location" : "3D Viewport Sidebar",
    "warning" : "",
    "category" : "3D View"
}

import bpy.utils, bpy.types, bpy.props
from .gt_panel import GT_PG_Properties, GT_PT_Panel
from .gt_operators import GT_OT_CleanCollision, GT_OT_FixAlpha, GT_OT_RenameMaterialSlots, GT_OT_RenameAllMeshsByMaterialName

classes = (
    GT_PG_Properties,
    GT_PT_Panel,
    GT_OT_CleanCollision,
    GT_OT_FixAlpha,
    GT_OT_RenameMaterialSlots,
    GT_OT_RenameAllMeshsByMaterialName
)

def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)

    # Assign property group
    bpy.types.Scene.GT_PG_Properties = bpy.props.PointerProperty(type = GT_PG_Properties)
    

def unregister():
    # Delete property group
    del bpy.types.Scene.GT_PG_Properties

    for class_to_unregister in reversed(classes):
        bpy.utils.unregister_class(class_to_unregister)

if __name__ == "__main__":
    register()