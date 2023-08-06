import bpy
from collections import defaultdict

def find_and_remove_duplicates():
    # Group images by absolute file path
    image_groups = defaultdict(list)
    for image in bpy.data.images:
        if image.source == 'FILE':
            abs_path = bpy.path.abspath(image.filepath)
            image_groups[abs_path].append(image)

    # Iterate over groups of images with the same file path
    for images in image_groups.values():
        if len(images) > 1:
            # The first image in the group
            target_image = images[0]

            # Iterate over all other images in the group
            for duplicate_image in images[1:]:
                # Replace references to duplicate image with references to target image
                for material in bpy.data.materials:
                    if material.use_nodes:
                        for node in material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image == duplicate_image:
                                node.image = target_image

                # Remove the duplicate image
                bpy.data.images.remove(duplicate_image)

find_and_remove_duplicates()
