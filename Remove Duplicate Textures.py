bl_info = {
    "name": "Remove Duplicate Textures",
    "author": "Chat GPT ft Andy Tanguay",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "File > Clean Up",
    "description": "Finds duplicate texture maps and remaps users to the first file, then deletes duplicates",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy
from collections import defaultdict

class RemoveDuplicateTexturesOperator(bpy.types.Operator):
    bl_idname = "image.remove_duplicate_textures"
    bl_label = "Remove Duplicate Textures"
    bl_description = "Finds duplicate texture maps and remaps users to the first file, then deletes duplicates"

    def execute(self, context):
        find_and_remove_duplicates()
        self.report({'INFO'}, "Duplicate textures removed")
        return {'FINISHED'}

def find_and_remove_duplicates():
    image_groups = defaultdict(list)
    for image in bpy.data.images:
        if image.source == 'FILE':
            abs_path = bpy.path.abspath(image.filepath)
            image_groups[abs_path].append(image)

    for images in image_groups.values():
        if len(images) > 1:
            target_image = images[0]
            for duplicate_image in images[1:]:
                for material in bpy.data.materials:
                    if material.use_nodes:
                        for node in material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image == duplicate_image:
                                node.image = target_image
                bpy.data.images.remove(duplicate_image)

def menu_func(self, context):
    self.layout.separator() # Adds a menu divider
    self.layout.operator(RemoveDuplicateTexturesOperator.bl_idname)

def register():
    bpy.utils.register_class(RemoveDuplicateTexturesOperator)
    bpy.types.TOPBAR_MT_file_cleanup.append(menu_func)

def unregister():
    bpy.utils.unregister_class(RemoveDuplicateTexturesOperator)
    bpy.types.TOPBAR_MT_file_cleanup.remove(menu_func)

if __name__ == "__main__":
    register()
