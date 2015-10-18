# import bpy module
import bpy
# import bmesh module
import bmesh


# cut a mesh using bisect
def cut_mesh(X, Y, Z):
	# change to edit mode
	bpy.ops.object.mode_set(mode='EDIT')

	#						SEPARATING INTO PARTS
	#
	# 							**IMPORTANT**
	#
	#	First perform bisect, hide the loop (H), hover over the half you want to  
	#	select, select a link (L), then finally unhide everything (option + H).
	#	You can then use Separate tool (P) via Selection to separate the two 
	#	parts. 

	# bisect the model
	bpy.ops.mesh.bisect(plane_co=(-2.38322, 5.2225, 14.4246), 
						plane_no=(0.931226, 0.363737, 0.022675), 
						xstart=225, 
						xend=238, 
						ystart=393, 
						yend=60)

	# hide the loop
	bpy.ops.mesh.hide(unselected=False)

	# select parts via select_linked_pick
	# this part of the object will be labeled "OBJECT.001"
	# always pick index=0 since every object is guaranteed to have it
	bpy.ops.mesh.select_linked_pick(deselect=False, index=0)

	# reveal the loop (at this point, only "OBJECT.001" is selected)
	bpy.ops.mesh.reveal()

	# Separate via Selection
	bpy.ops.mesh.separate(type='SELECTED')

	# change to object mode
	bpy.ops.object.mode_set(mode='OBJECT')

	# deselect all objects
	bpy.ops.object.select_all(action='DESELECT')

	#				**USEFUL!**
	# Below commented script changes an object's name
	# bpy.context.space_data.context = 'DATA'
	# bpy.context.object.data.name = "Cube!"

	# select one of the parts
	bpy.ops.object.select_pattern(pattern="OBJECT")

	# move the selected part
	bpy.ops.transform.translate(value=(-2.55165, -1.43464, -0.494163), 
								constraint_axis=(False, False, False), 
								constraint_orientation='GLOBAL', 
								mirror=False, 
								proportional='DISABLED', 
								proportional_edit_falloff='SMOOTH', 
								proportional_size=1)
# end of [def cut_mesh(X, Y, Z):]


# rotate the selected model (two suggested methods)
def rotate_object(X, Y, Z):
	# 						**IMPORTANT**
	#
	# This funtion finds the largest face and rotates each part of the
	# model so that the largest surface of each part faces downward.
	# However, in an STL file, a face means a triangle. When selecting a 
	# 'face', a triangle formed with three vertices is selected. A possible
	# problem is that the largest triangle on an STL file is not necessarily 
	# the largest 'face' of the object. Therefore, each time a face is selected,
	# its "Co-Planar" triangles have to be selected as well.

	# change to edit mode
	bpy.ops.object.mode_set(mode='EDIT')

	# change select mode to "Select Face"
 	bpy.ops.mesh.select_mode(type="FACE")

 	# define MESH as the object in context
 	OBJECT = bpy.context.object
 	MESH = bmesh.from_edit_mesh(OBJECT.data)

 	# define largestSurface
 	largestArea = 0.0

 	# selection loop (brute force method)
 	for face in MESH.faces:
 		# temporary face area that will be compared to largest area
 		tempFaceArea = 0.0
 		# select a face
 		face.select = True
 		# select its co-planar triangles
 		bpy.ops.mesh.select_similar(type='COPLANAR')
 		# gather selected face's info(area, angle)
 		

	# method #1: rotate by modifying Euler angles [x, y, z]
	bpy.context.object.rotation_euler[0] = 0
	bpy.context.object.rotation_euler[1] = 0
	bpy.context.object.rotation_euler[2] = 0

	# method #2: rotate <value> along (X,Y,Z) axes
	bpy.ops.transform.rotate(value=X, 
				   			 constraint_axis=(True, False, False))
	bpy.ops.transform.rotate(value=Y, 
				   			 constraint_axis=(False, True, False))
	bpy.ops.transform.rotate(value=Z, 
				   			 constraint_axis=(False, False, True))
# end of [def rotate_object(X, Y, Z):]


# export the the parts as one STL file
def export_result(version):
	# define export file path 
	EXPORT_FILE_PATH = "/Users/jinyeom/Desktop/AI Research/" + 
						"Decomposition_via_NEAT/test_programs/" +
						"Blender/result/Decomp_" + str(version) + ".stl"
	# select everything
	bpy.ops.object.select_all(action='SELECT')
	# export the STL file
	bpy.ops.export_mesh.stl(filepath=EXPORT_FILE_PATH)
# end of [def export_result(version):]


# main function
def main():	
	# delete the default model ("Cube")
	bpy.ops.object.delete()

	# STL files importing locations
	FILE_PATH = "/Users/jinyeom/Desktop/AI Research/" + 
				"Decomposition_via_NEAT/sample_models/" +
				"The_Colonel/colonel.stl"

	# initially define object name so that any model can be named "OBJECT"
	bpy.context.space_data.context = 'DATA'
	bpy.context.object.data.name = 'OBJECT'

	# 						**VERSION CONTROL**
	#
	# 	Add VER to EXPORT_FILE_PATH when multiple versions of the result files 
	# 	are needed; use this same variable for each log file for each exported
	# 	file as well.

	for VER in range(0, 10):
		# import an STL file
		bpy.ops.import_mesh.stl(filepath=FILE_PATH)

		# 				**GENETIC ALGORITHM HERE**
		# define the cutting angle x, y, z for bisect function
		X = 0
		Y = 0
		Z = 0



		# cut the model
		cut_mesh(X,Y,Z)

		# sliced face down
		rotate_object()

		# export different versions of the sliced models
		export_result(VER)

		# select everything and delete
		bpy.ops.object.select_all(action='SELECT')
		bpy.ops.object.delete()
	# end of [for VER in range(0,10):]
# end of [def main():]


# execute [main()]
main()






