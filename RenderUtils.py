import bpy

# Metadata about the addon
bl_info = {
    "name": "Resolution Presets",
    "author": "Nwadilioramma Azuka-Onwuka",
    "version": (1, 0),
    "blender": (4, 5, 0),
    "location": "Properties > Ouput > Resolution Presets",
    "description": "Set various screen ratios for different platforms",
    "category": "Render",
}

def get_resolution_presets():
    """
    Returns a dictionary of resolution presets.
    Each key is a preset name, and the value is a tuple of (width, height, aspect_ratio).
    """
    presets = {
        "Instagram Post": (1080, 1440, 3/4),
        "Instagram Story (Portrait)": (1080, 1920, 9/16),
        "YouTube Thumbnail (Landscape)": (1280, 720, 16/9),
        "YouTube Video (HD 720p)": (1280, 720, 16/9),
        "YouTube Video (Full HD 1080p)": (1920, 1080, 16/9),
        "YouTube Video (4K UHD)": (3840, 2160, 16/9),
        "TikTok / Mobile Portrait": (1080, 1920, 9/16),
        "DCI 2K": (2048, 1080, 1.896),
        "DCI 4K": (4096, 2160, 1.896),
        "4K Widescreen": (4096, 1716, 2.39),
        "Quad HD": (2560, 1440, 16/9),
        "Custom 1 (Widescreen)": (2560, 1080, 21/9), 
        "Custom 2 (Square - 2560)": (2560, 2560, 1.0)
    }
    return presets

class ResolutionSelectorOperator(bpy.types.Operator):
    """Operator to select a resolution preset."""
    bl_idname = "render.resolution_selector"
    bl_label = "Apply Resolution" # Modified label

    def execute(self, context):
        scene = context.scene
        presets = get_resolution_presets()
        width, height, aspect_ratio = presets[scene.resolution_preset]

        # Set the scene's resolution
        scene.render.resolution_x = int(width)
        scene.render.resolution_y = int(height)

        self.report({'INFO'}, f"Resolution set to {width}x{height} ({scene.resolution_preset})")
        return {'FINISHED'}

class VIEW3D_PT_resolution_presets(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport"""
    bl_label = "Resolution Presets"
    bl_idname = "VIEW3D_PT_resolution_presets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Render Utils" # Optional: Adds a category to the panel

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "resolution_preset", text="Preset")  # Display the dropdown
        layout.operator("render.resolution_selector", text="Apply Resolution")


def register():
    bpy.utils.register_class(ResolutionSelectorOperator)
    bpy.utils.register_class(VIEW3D_PT_resolution_presets)

    #Register a scene property for our ENUM
    bpy.types.Scene.resolution_preset = bpy.props.EnumProperty(
        name="Resolution Preset",
        description="Choose a resolution preset",
        items=[(preset_name, preset_name, preset_name) for preset_name in get_resolution_presets()]
    )


def unregister():
    bpy.utils.unregister_class(ResolutionSelectorOperator)
    bpy.utils.unregister_class(VIEW3D_PT_resolution_presets)
    del bpy.types.Scene.resolution_preset # Remove the scene property

if __name__ == "__main__":
    register()