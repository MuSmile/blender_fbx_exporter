import bpy, bmesh
import os
import mathutils
from mathutils import Vector

from . import objects_organise

class op(bpy.types.Operator):
	bl_idname = "fbxbundle.select_all"
	bl_label = "Select All Mesh"
	bl_description = "Select all Mesh in scene"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		for obj in bpy.context.scene.objects:
			if obj.type == 'MESH':
				obj.select_set(state = True)
		return {'FINISHED'}

