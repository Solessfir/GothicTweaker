import bpy
import bmesh
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper

class Operator_CleanCollision(bpy.types.Operator):
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
        selected_object = context.active_object

        if selected_object and selected_object.type == "MESH":
            bpy.ops.object.mode_set(mode = "OBJECT")
            collision_substrings = ["p:", "alpha", "ghostoccluder", "sun_blocker"]
            bm = bmesh.new()
            bm.from_mesh(selected_object.data)
            faces_to_remove = []
            invalid_xardas_tower_faces = []
            xardas_valid_material_index = -1

            # Check each face's material index
            for face in bm.faces:
                material_name = selected_object.data.materials[face.material_index].name.casefold()

                if any(substring in material_name for substring in collision_substrings):
                    faces_to_remove.append(face)
                    continue

                if xardas_valid_material_index < 0 and "nw_misc_insidecave_wall_01" in material_name:
                    xardas_valid_material_index = face.material_index
                    continue

                if "nixdrauf" in material_name:
                    invalid_xardas_tower_faces.append(face)
            
            if xardas_valid_material_index > -1:
                for invalid_face in invalid_xardas_tower_faces:
                    invalid_face.material_index = xardas_valid_material_index

            # Delete the faces with matching materials
            bmesh.ops.delete(bm, geom = faces_to_remove, context = "FACES")
            bm.to_mesh(selected_object.data)
            bm.free()

            # Remove unused Materials after cleanup
            bpy.ops.object.material_slot_remove_unused()
            self.report({"INFO"}, f"Total Faces removed: {len(faces_to_remove)}")
        else:
            self.report({"INFO"}, "No valid mesh object selected")


class Operator_ApplyAlpha(bpy.types.Operator):
    bl_idname = "operator.apply_alpha"
    bl_label = "Apply Alpha"
    bl_description = "This will fix Alpha on the Trees, Water, Flags, etc.\nThis should be used if KrxImpExp didn't fix it on the import or you want to apply opacity to Gothic 2 water bodies"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        self.apply_alpha(context)
        return {"FINISHED"}
    
    def apply_alpha(self, context):
        bpy.ops.object.mode_set(mode="EDIT")

        object = context.active_object
        properties = context.scene.PropertyGroup_GothicTweaker
        gothic2_water_opacity = properties.water_opacity

        # Water material names
        water_with_blend = ["water", "puddle", "lake", "wfall"]

        for material_slot in object.material_slots:
            material = material_slot.material
            material_wrapper = PrincipledBSDFWrapper(material, is_readonly = False)
            material_wrapper.specular = 0.0  # Gothic doesn't use PBR textures - disable Specular
            material.use_backface_culling = True
            nodes = material.node_tree.nodes
            links = material.node_tree.links

            # Find Image Texture and Principled BSDF nodes
            image_texture_node = next((node for node in nodes if isinstance(node, bpy.types.ShaderNodeTexImage)), None)
            principled_bsdf_node = next((node for node in nodes if isinstance(node, bpy.types.ShaderNodeBsdfPrincipled)), None)

            if image_texture_node and self.image_has_alpha(image_texture_node.image) and principled_bsdf_node:
                links.new(image_texture_node.outputs["Alpha"], next((input for input in principled_bsdf_node.inputs if input.identifier == "Alpha"), None))
                material.show_transparent_back = False
                material.blend_method = "CLIP"
                material["biplanar"] = True  

            if gothic2_water_opacity >= 0.0 and any(water in material_slot.name.casefold() for water in water_with_blend):
                material.show_transparent_back = False
                material.blend_method = "BLEND"
                material_wrapper.alpha = gothic2_water_opacity
                material["biplanar"] = True

        self.report({"INFO"}, "Completed")

    def image_has_alpha(self, image):
        if not image:
            return False
        b = 32 if image.is_float else 8
        # Grayscale + Alpha or RGB + Alpha
        return image.depth == 2 * b or image.depth == 4 * b


class Operator_RenameMaterialSlots(bpy.types.Operator):
    bl_idname = "operator.rename_material_slots"
    bl_label = "Rename Material Slots"
    bl_description = "Renames all Material Slots to the name of their Texture file and cleans all duplicates"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        self.rename_material_slots(context)
        return {"FINISHED"}
    
    def rename_material_slots(self, context):
        bpy.ops.object.mode_set(mode = "OBJECT")

        object = context.active_object
        material_slots = object.material_slots

        for material_slot in material_slots:
            material = material_slot.material
            material.use_nodes = True
            node_texture = next((node for node in material.node_tree.nodes if isinstance(node, bpy.types.ShaderNodeTexImage)), None)

            if not node_texture or not node_texture.image:
                continue

            fixed_material_slot_name = node_texture.image.name.rsplit(".", 1)[0]
            old_name = material.name
            material.name = fixed_material_slot_name

            # Remove copies, like .001, .002, etc
            material_slot.material = bpy.data.materials.get(fixed_material_slot_name)

            self.report({"INFO"}, f"Material Slot: {old_name} renamed to: {material.name}")

        # Remove unused Materials after cleanup
        bpy.ops.object.material_slot_remove_unused()
        self.report({"INFO"}, "Completed")


class Operator_RenameAllMeshsByMaterialName(bpy.types.Operator):
    bl_idname = "operator.rename_all_meshs_by_material_name"
    bl_label = "Rename All Meshes"
    bl_description = "This will rename all meshes by their material name.\nAssuming that you have split mesh by material"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        self.rename_mesh_by_material_name(context)
        return {"FINISHED"}
    
    def rename_mesh_by_material_name(self, context):
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

                object.name = node_texture.image.name.rsplit(".", 1)[0]

        self.report({"INFO"}, "Completed")
