import bpy, bmesh
import os
import mathutils
from mathutils import Vector

from . import objects_organise

class op(bpy.types.Operator):
	bl_idname = "fbxbundle.pivot_center"
	bl_label = "Center pivot"
	bl_description = "Aligns the pivot to the center of the bundle bounds"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if len(bpy.context.selected_objects) == 0:
			return False

		if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
			return False

		if len( objects_organise.get_bundles() ) == 0:
			return False

		return True

	def execute(self, context):
		ground_center(self)
		return {'FINISHED'}


def ground_center(self):
	bundles = objects_organise.get_bundles()
	
	# Store previous settings
	previous_selection = bpy.context.selected_objects.copy()
	previous_active = bpy.context.view_layer.objects.active
	previous_pivot = bpy.context.tool_settings.transform_pivot_point
	previous_cursor = bpy.context.scene.cursor.location.copy()

	for name,objects in bundles.items():

		bounds = objects_organise.get_bounds_combined(objects)
		for obj in objects:
			print("assign {}".format(obj.name))

			# Select object as active
			bpy.ops.object.select_all(action="DESELECT")
			obj.select_set(state = True)
			bpy.context.view_layer.objects.active = obj

			# bpy.context.scene.cursor.location = Vector((obj.location.x,obj.location.y,bounds.max.z))
			x = (bounds.min.x + bounds.max.x) / 2
			y = (bounds.min.y + bounds.max.y) / 2
			z = (bounds.min.z + bounds.max.z) / 2
			bpy.context.scene.cursor.location = Vector((x, y, z))
			bpy.ops.object.origin_set(type='ORIGIN_CURSOR')


	# Restore previous settings
	bpy.context.tool_settings.transform_pivot_point = previous_pivot
	bpy.context.scene.cursor.location = previous_cursor
	bpy.context.view_layer.objects.active = previous_active
	bpy.ops.object.select_all(action='DESELECT')
	for obj in previous_selection:
		obj.select_set(state = True)