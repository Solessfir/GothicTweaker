# MIT License

# Copyright (c) 2024 Solessfir

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

bl_info = {
    "name" : "Gothic Tweaker",
    "author" : "Solessfir",
    "description" : "",
    "blender" : (2, 80, 0),
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