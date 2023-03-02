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

        # Remove unused Materials after cleanup
        bpy.ops.object.material_slot_remove_unused()
        self.report({"INFO"}, "Total cleaned: " + str(removed_materials_amount))


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
        if context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode = "OBJECT")

        object = context.active_object
        properties = context.scene.PropertyGroup_GothicTweaker
        gothic2_water_opacity = properties.water_opacity

        for material_slot in object.material_slots:
            material = material_slot.material
            material_wrapper = PrincipledBSDFWrapper(material, is_readonly = False)
            material_wrapper.specular = 0.0 # Gothic doesn't use PBR textures - disable Specular
            material.use_backface_culling = True
            nodes = material.node_tree.nodes
            links = material.node_tree.links
            image_texture = nodes.get("Image Texture")

            if image_texture and self.image_has_alpha(image_texture.image):
                links.new(image_texture.outputs["Alpha"], nodes["Principled BSDF"].inputs["Alpha"])
                material.show_transparent_back = False
                material.blend_method = "CLIP"
                material["biplanar"] = True  

            if gothic2_water_opacity >= 0.0:
                # Set Alpha to a fixed value for water bodies
                water_with_blend = ["water", "puddle", "lake", "wfall"]
                for water in water_with_blend:
                    if water in material_slot.name.casefold():
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

    material_error = [] # Collect materials for warning messages

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        self.material_error = [] # Reset Material errors, otherwise we risk reporting errors erroneously

        self.rename_material_slots(context)

        if self.material_error:
            materials = ", ".join(self.material_error)

            if len(self.material_error) == 1:
                waswere = " was"
                suff_s = ""
            else:
                waswere = " were"
                suff_s = "s"

            self.report({"WARNING"}, materials + waswere + " not removed or set as Base" + suff_s)

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
                old_name = material.name
                material.name = fixed_material_slot_name
                self.report({"INFO"}, "Material Slot: " + old_name + " renamed to: " + material.name)

        # Remove duplicated
        for slot in object.material_slots:
            self.fixup_slot(slot)
             
        self.report({"INFO"}, "Completed")

    # Fix material slots that was assigned to materials now removed
    def fixup_slot(self, slot):
        if not slot.material:
            return
        
        base, suffix = self.split_name(slot.material)
        if suffix is None:
            return

        try:
            base_mat = bpy.data.materials[base]
        except KeyError:
            self.report({"ERROR"}, "Base material %r not found" % base)
            return

        slot.material = base_mat

    # Split the material name into a base and a suffix
    def split_name(self, material):
        name = material.name

        # No need to do this if it's already "clean"/there is no suffix
        if "." not in name:
            return name, None

        base, suffix = name.rsplit(".", 1)

        try:
            # trigger the exception
            num = int(suffix, 10)
        except ValueError:
            # Not a numeric suffix
            # Don't report on materials not actually included in the merge!
            if (base == self.material_base_name and name not in self.material_error):
                self.material_error.append(name)
            return name, None

        return base, suffix


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

        self.report({"INFO"}, "Completed")