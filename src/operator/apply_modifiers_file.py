import bpy
from typing import Set
from bpy.types import Operator
from ..lib import pkginfo
from ..lib import apply_modifiers

if "_LOADED" in locals():
    import importlib

    for mod in (pkginfo, apply_modifiers):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = pkginfo.package_name()


def generate_enum_items(self, context) -> list[tuple[str, str, str]]:
    result = []
    for sign in "+-":
        for axis in "XYZ":
            result.append((f"{sign}{axis}", f"Align {sign}{axis}", f"Align something on the {sign}{axis} axis"))
    return result


class ApplyModifiersEntireFile(Operator):
    """Apply all Modifiers in the open Scene"""
    bl_idname = "blender_apply_all_modifiers.apply_modifiers_file"
    bl_label = "Apply Modifiers in Entire File"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context) -> bool:
        return True

    def execute(self, context) -> Set[str]:
        count = 0
        for obj in bpy.data.objects:
            affected = apply_modifiers.apply_modifiers(obj)
            count += len(affected)

        self.report({'INFO'}, f"Applied modifiers on {count} of {len(bpy.data.objects)} objects")
        return {'FINISHED'}


REGISTER_CLASSES = [ApplyModifiersEntireFile]
