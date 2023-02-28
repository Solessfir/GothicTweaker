import bpy.types
from bpy.props import BoolProperty

class GT_PG_Properties(bpy.types.PropertyGroup):
    bl_idname = "gt.properties"
    bl_label = "Gothic Tweaker Properties"
    bl_options = {"REGISTER", "UNDO"}

    b_collapse_optional_settings: BoolProperty(name = "Collapse Optional Settings", default = False)


class GT_PT_Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Gothic Tweaker"
    bl_category = "Gothic Tweaker"
    #bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        # Pointer to the Property Group
        properties = context.scene.GT_PG_Properties

        layout = self.layout
        row = layout.row()
        column = row.column()
        column.operator("operator.clean_collision")

        row = layout.row()
        column = row.column()
        column.operator("operator.fix_alpha")

        row = layout.row()
        column = row.column()
        column.operator("operator.rename_material_slots")

        # Optional Dropdown
        row = self.layout.row()
        row.prop(properties, "b_collapse_optional_settings", icon = "DOWNARROW_HLT" if properties.b_collapse_optional_settings else "RIGHTARROW", icon_only = True, emboss = False)
        row.label(text = "Optional")
        
        if properties.b_collapse_optional_settings:
            row = layout.row()
            column = row.column()
            column.operator("operator.rename_all_meshs_by_material_name")