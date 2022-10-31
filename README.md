# Apply All Modifiers

https://github.com/SuperFLEB/blender_apply_all_modifiers

Apply all modifiers in the current file, preserving linked duplicates.

## Caveats

This is a very quick-and-dirty solution to my immediate needs, so it's a bit less
than thoroughly featured and tested. A few things to watch out for:

* It works on the entire file. If you need to be more particular, move the objects to a different file.
* It only works on Mesh objects, not Curves, Metaballs, etc.
* It will clone the modifier stack from the first-encountered instance of a set of linked duplicates. If there are different modifiers on different instances, they will not be retained.
* Modifiers that use textures or randomness will all share the texture or random values of the first-encountered instance.
* Modifiers that are not displayed in the viewport will be discarded
* Did I mention "quick" and "dirty"? This might do what you want. It might completely blow up your file. It might have subtle bugs you don't find until later. Keep a pre-apply backup.

Also, this comes with some of the same gotchas as a manual Apply Modifier:
* Boolean modifiers will be applied, but boolean "brushes" will not be deleted. (This is how applying the modifier would work, but it's still something to keep in mind.)
* Modifiers such as Subdivision Surface, that have different View and Render values, will apply the View value.

## To install

Either install the ZIP file from the release, clone this repository and use the
build_release.py script to build a ZIP file that you can install into Blender.

## To use

Use the "Apply All Modifiers" menu item in the Edit menu in the 3D Viewport mode.

## Testing

***Tests do not currently exist, but I'm leaving the unit test code in just in case I develop this further.***

To run unit tests, run (from the Blender install directory):

```shell
blender --factory-startup --background --python path/to/module/run_tests.py
```
