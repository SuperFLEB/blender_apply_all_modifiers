import bpy
from typing import Set
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator
from ..lib import pkginfo
from ..lib import apply_modifiers

if "_LOADED" in locals():
    import importlib

    for mod in (pkginfo, apply_modifiers):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = pkginfo.package_name()


class ApplyModifiersEntireFile(Operator):
    """Apply all Modifiers in the open Scene"""
    bl_idname = "blender_apply_all_modifiers.apply_modifiers_file"
    bl_label = "Apply Modifiers in Entire File"
    bl_options = {'REGISTER', 'UNDO'}

    view_render_resolve: EnumProperty(name="", items=[
        ("view", "View", 'Use a "View" value if both View and Render are options'),
        ("render", "Render", 'Use a "Render" value if both View and Render are options'),
        ("lower", "Lower Value",
         'Use the lower of a View or Render value if both are options, or the View value if the options are not quantifiable'),
        ("higher", "Higher Value",
         'Use the higher of a View or Render value if both are options, or the Render value if the options are not quantifiable'),
    ], default="view")
    enable_hidden: BoolProperty(name="Enable hidden modifiers", default=False)

    @classmethod
    def poll(cls, context) -> bool:
        if bpy.context.mode == 'OBJECT':
            return True
        cls.poll_message_set("Only available in Object mode")
        return False

    def draw(self, context) -> None:
        self.layout.label(text="Use View or Render values?")
        self.layout.prop(self, "view_render_resolve")
        self.layout.prop(self, "enable_hidden")

    def execute(self, context) -> Set[str]:
        count = 0
        for obj in bpy.data.objects:
            affected = apply_modifiers.apply_modifiers(obj, self.view_render_resolve, self.enable_hidden)
            count += len(affected)

        self.report({'INFO'}, f"Applied modifiers on {count} of {len(bpy.data.objects)} objects")
        return {'FINISHED'}


REGISTER_CLASSES = [ApplyModifiersEntireFile]
