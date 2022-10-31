import bpy
from ..operator import apply_modifiers_file

if "_LOADED" in locals():
    import importlib

    for mod in (apply_modifiers_file,):  # list all imports here
        importlib.reload(mod)
_LOADED = True


class ApplyAllModifiersSubmenu(bpy.types.Menu):
    bl_idname = 'blender_apply_all_modifiers.edit_apply_all_modifiers'
    bl_label = 'Apply All Modifiers'

    def draw(self, context) -> None:
        self.layout.operator(apply_modifiers_file.ApplyModifiersEntireFile.bl_idname)


REGISTER_CLASSES = [ApplyAllModifiersSubmenu]
