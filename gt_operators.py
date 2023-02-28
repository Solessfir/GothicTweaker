import bpy
import bmesh

class GT_OT_CleanCollision(bpy.types.Operator):
    bl_idname = "operator.clean_collision"
    bl_label = "Clean Collision"
    bl_description = "This will remove all collision and sun blocker faces and their materials"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        self.clean_collision(context)
        return {"FINISHED"}
    
    def clean_collision(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode = "EDIT")

        bpy.ops.mesh.select_all(action = "DESELECT")

        # Variables
        object = context.edit_object
        mesh = object.data
        removed_materials_amount = 0
        bm = bmesh.from_edit_mesh(mesh)
        drauf_material_fix_index = None
        do_drauf_material_fix = True

        # Collision materials names to search through
        names = ["p:", "alpha", "ghostoccluder", "sun_blocker"]

        for name in names:
            for material_slot in object.material_slots:
                # Xardas Tower wrong material index fix
                if do_drauf_material_fix:
                    if drauf_material_fix_index is None and "nw_misc_insidecave_wall_01" in material_slot.name.casefold():
                        drauf_material_fix_index = material_slot.slot_index
                        continue

                    if drauf_material_fix_index is not None and "nixdrauf" in material_slot.name.casefold():
                        do_drauf_material_fix = False
                        # Create a list with all faces
                        face_list = [face for face in bm.faces if face.material_index == material_slot.slot_index]
                        # Select all found faces
                        for face in face_list:
                            face.material_index = drauf_material_fix_index
                        continue

                if name.casefold() in material_slot.name.casefold():
                    # Create a list with all faces
                    face_list = [face for face in bm.faces if face.material_index == material_slot.slot_index]
                    # Select all found faces
                    for face in face_list:
                        face.select = True
                    # Delete faces
                    bpy.ops.mesh.delete(type = "FACE")
                    removed_materials_amount += 1

        bm.free()
        bpy.ops.object.mode_set(mode = "OBJECT")

        # Remove Materials
        bpy.ops.object.material_slot_remove_unused()
        self.report({"INFO"}, "Total cleaned: " + str(removed_materials_amount))


class GT_OT_FixAlpha(bpy.types.Operator):
    bl_idname = "operator.fix_alpha"
    bl_label = "Fix Alpha"
    bl_description = "This will fix Alpha on the Trees, Flags, etc."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        self.fix_alpha(context)
        return {"FINISHED"}
    
    def fix_alpha(self, context):
        if context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode = "OBJECT")

        # Variables
        object = context.active_object
        materials_with_aplha = ["tree", "branch", "bush", "leave", "needle", "grass", "ivy", "root", "plant", "palm", "liana", "duckweed", "seerose", "flag", "leathersleeve", "ropes", "chain", "reed", "woodengate", "ratpoison", "hitsurface", "gitterzaun"]
        water_with_blend = ["water", "puddle", "lake", "wfall"]

        for material_slot in object.material_slots:
            material = material_slot.material
            material.use_nodes = True
            nodes = material.node_tree.nodes
            principledBSDF = nodes.get("Principled BSDF")
            links = material.node_tree.links
            node_texture = None

            # Look for existing Image Texture node
            for node in material.node_tree.nodes:
                if node.name == "Image Texture":
                    node_texture = node
                    break

            # No Image Texure - skip it       
            if node_texture is None:
                continue

            # Set Specular Value
            principledBSDF.inputs[7].default_value = 0.0
            # Set Roughness Value
            principledBSDF.inputs[9].default_value = 1.0
            # Alpha input
            alpha = principledBSDF.inputs[21]

            # Connect Alpha from texture
            for material_with_aplha in materials_with_aplha:
                if material_with_aplha in material_slot.name.casefold():
                    material.blend_method = "CLIP"
                    links.new(node_texture.outputs[1], alpha)

            # Set Alpha to fixed value
            for water in water_with_blend:
                if water in material_slot.name.casefold():
                    material.blend_method = "BLEND"
                    alpha.default_value = 0.75

        self.report({"INFO"}, "Alpha fixed")


class GT_OT_RenameMaterialSlots(bpy.types.Operator):
    bl_idname = "operator.rename_material_slots"
    bl_label = "Rename Material Slots"
    bl_description = "This will rename all material slots by their texture name"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        self.rename_material_slots(context)
        return {"FINISHED"}
    
    def rename_material_slots(self, context):
        if context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode = "OBJECT")

        object = context.active_object

        for material_slot in object.material_slots:
            material = material_slot.material
            material.use_nodes = True
            node_texture = None

            # Look for existing Image Texture node
            for node in material.node_tree.nodes:
                if node.name == "Image Texture":
                    node_texture = node
                    break

            # No Image Texure - skip it       
            if node_texture is None:
                continue

            if node_texture.image:
                fixed_material_slot_name = node_texture.image.name
                fixed_material_slot_name = fixed_material_slot_name[:-len(".TGA")]
                material.name = fixed_material_slot_name


class GT_OT_RenameAllMeshsByMaterialName(bpy.types.Operator):
    bl_idname = "operator.rename_all_meshs_by_material_name"
    bl_label = "Rename All Meshes"
    bl_description = "This will rename all meshes by their material name. Assuming that you have split mesh by material."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        self.rename_mesh_by_material_name(context)
        return {"FINISHED"}
    
    def rename_mesh_by_material_name(self, context):
        if context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode = "OBJECT")

        for object in bpy.context.scene.objects:
            if object.type == "MESH" and object.material_slots:
                material = object.material_slots[0].material
                material.use_nodes = True
                node_texture = None

                # Look for existing Image Texture node
                for node in material.node_tree.nodes:
                    if node.name == "Image Texture":
                        node_texture = node
                        break

                # If None found create new Node
                if node_texture is None or node_texture.image is None:
                    continue

                desired_name = node_texture.image.name
                desired_name = desired_name[:-len(".TGA")]
               
                object.name = desired_name