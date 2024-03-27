import bpy.types
from bpy.props import BoolProperty
from bpy.props import FloatProperty

class PropertyGroup_GothicTweaker(bpy.types.PropertyGroup):
    bl_idname = "gt.properties"
    bl_label = "Gothic Tweaker Properties"
    bl_options = {"REGISTER", "UNDO"}

    b_collapse_optional_settings: BoolProperty(name = "Collapse Optional Settings", default = False)
    water_opacity: FloatProperty(name = "", default = -1.0, min = -1.0, max = 1.0, description = "-1 = Disabled\nOpacity that will be added to Gothic 2 Water.\nDon't use it for Gothic 1 it will probably not work or will work partially only")


class VIEW3D_PT_Gothic_Tweaker_Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Gothic Tweaker"
    bl_category = "Gothic Tweaker"
    #bl_options = {"HIDE_HEADER"}

    def draw_header(self, context):
        layout = self.layout
        layout.label(text = "", icon = "SETTINGS")

    def draw(self, context):
        # Pointer to the Property Group
        properties = context.scene.PropertyGroup_GothicTweaker

        layout = self.layout
        row = layout.row()
        column = row.column()
        column.operator("operator.clean_collision")

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

            row = layout.row()
            column = row.column()
            row.prop(properties, "water_opacity")
            column.operator("operator.apply_alpha")