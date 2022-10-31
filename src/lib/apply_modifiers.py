import bpy

_view_render_props_cache = {}


def _view_render_resolve(mod: bpy.types.Modifier, view_render_resolve: str):
    """Apply any properties necessary to get the view_... to match the associated render_... property, if necessary."""

    type_name = type(mod).__name__

    # Types don't change, so cache them as we see them
    if type_name in _view_render_props_cache:
        view_render_props = _view_render_props_cache[type_name]
    else:
        view_render_props = [p for p in dir(mod) if hasattr(mod, f"render_{p}")]
        _view_render_props_cache[type_name] = view_render_props

    for p in view_render_props:
        if view_render_resolve == 'render':
            setattr(mod, p, getattr(mod, f"render_{p}"))
            continue

        view_value = getattr(mod, p)
        render_value = getattr(mod, f"render_{p}")
        if view_render_resolve == 'lower':
            # Default to view value if they can't be compared, because view value is usually lower
            result_value = view_value
            try:
                result_value = render_value if render_value < view_value else view_value
            except:
                # The values couldn't be compared for some reason
                pass
            setattr(mod, p, result_value)
            continue
        if view_render_resolve == 'higher':
            # Default to render value if they can't be compared, because view value is usually lower
            result_value = render_value
            try:
                result_value = render_value if render_value > view_value else view_value
            except:
                # The values couldn't be compared for some reason
                pass
            setattr(mod, p, result_value)
            continue


def _show_all(obj: bpy.types.Object):
    """Show all modifiers in an object. This does not check for object type, so that should be done prior"""
    for mod in [m for m in obj.modifiers if m.show_viewport == False]:
        mod.show_viewport = True


def apply_modifiers(subject: bpy.types.Object, view_render_resolve: str = "view", show_all: bool = False) -> list[
    bpy.types.Object]:
    """Apply this object's modifiers to all objects sharing the same mesh data, and clear modifiers on those.
    Returns a list of all affected Objects, with the source object being the first item."""

    if subject.type != 'MESH' or len(subject.modifiers) == 0:
        return []

    if show_all:
        _show_all(subject)


    # "view" is also a valid option, but it doesn't require doing anything, since applying uses view by default
    if view_render_resolve in ['render', 'lower', 'higher']:
        for mod in subject.modifiers:
            _view_render_resolve(mod, view_render_resolve)

    linked = [subject] + [ob for ob in bpy.context.scene.objects if ob != subject and ob.data == subject.data]

    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = subject.evaluated_get(depsgraph)

    applied_mesh = bpy.data.meshes.new_from_object(object_eval, preserve_all_data_layers=True, depsgraph=depsgraph)
    original_mesh = subject.data

    for obj in linked:
        obj.data = applied_mesh
        obj.modifiers.clear()

    bpy.data.meshes.remove(original_mesh)

    return linked
