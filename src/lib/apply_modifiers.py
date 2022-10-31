import bpy


def apply_modifiers(subject) -> list[bpy.types.Object]:
    """Apply this object's modifiers to all objects sharing the same mesh data, and clear modifiers on those.
    Returns a list of all affected Objects, with the source object being the first item."""

    if subject.type != 'MESH' or len(subject.modifiers) == 0:
        return []

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
