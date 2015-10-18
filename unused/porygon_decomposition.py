# import bpy module
import bpy

# delete the default model ('Cube')
bpy.ops.object.delete()

# STL file importing location
FILE_PATH = "/Users/jinyeom/Desktop/AI Research/Decomposition_via_NEAT/test_programs/Blender/porygon.stl"


def cut_porygon(X, Y, Z):
	# change to edit mode
	bpy.ops.object.mode_set(mode = 'EDIT')

	#						SEPARATING INTO PARTS
	#
	# 							**IMPORTANT**
	# 	If making different parts via bisect function, the work has to be done
	#	recursively. The model has to be duplicated; the two same model, then,
	# 	has to be bisected with the same cutting plane, each of them deleting
	# 	either top or bottom. This process shall be repeated until the pieces
	# 	are small enough.
	#
	#							(ALTERNATIVE)
	#	Another way to do it -- and this way is probably more efficient -- is to 
	#	first perform bisect, hide the loop (H), hover over the half you want to  
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
	# this part of the object will be labeled with .001
	bpy.ops.mesh.select_linked_pick(deselect=False, index=31)
	bpy.ops.mesh.select_linked_pick(deselect=False, index=14)
	bpy.ops.mesh.select_linked_pick(deselect=False, index=88)
	bpy.ops.mesh.select_linked_pick(deselect=False, index=68)

	# reveal the loop (at this point, only previously picked part is selected)
	bpy.ops.mesh.reveal()

	# Separate via Selection
	bpy.ops.mesh.separate(type='SELECTED')

	# change to object mode
	bpy.ops.object.mode_set(mode = 'OBJECT')

	# deselect all objects
	bpy.ops.object.select_all(action='DESELECT')

	#				**MIGHT BE USEFUL!**
	# Below commented script changes an object's name
	# bpy.context.space_data.context = 'DATA'
	# bpy.context.object.data.name = "Cube!"

	# select one of the parts
	bpy.ops.object.select_pattern(pattern="Porygon")

	# move the selected part
	bpy.ops.transform.translate(value=(-2.55165, -1.43464, -0.494163), 
								constraint_axis=(False, False, False), 
								constraint_orientation='GLOBAL', 
								mirror=False, 
								proportional='DISABLED', 
								proportional_edit_falloff='SMOOTH', 
								proportional_size=1)


def rotate_model():
	# 						**IMPORTANT**
	# This funtion finds out each sliced surface and rotates each part of the
	# model so that the sliced surface of each part faces downward.

	# rotate by modifying Euler angles [x, y, z]
	bpy.context.object.rotation_euler[0] = 0
	bpy.context.object.rotation_euler[1] = 0
	bpy.context.object.rotation_euler[2] = 0


def export_result(version):
	# define export file path 
	EXPORT_FILE_PATH = "/Users/jinyeom/Desktop/AI Research/Decomposition_via_NEAT/test_programs/Blender/result/porygon_cut_" + str(version) + ".stl"
	# select everything
	bpy.ops.object.select_all(action='SELECT')
	# export the STL file
	bpy.ops.export_mesh.stl(filepath=EXPORT_FILE_PATH)


def main():	
	# 						**VERSION CONTROL**
	#
	# 	Add VER to EXPORT_FILE_PATH when multiple versions of the result files 
	# 	are needed; use this same variable for each log file for each exported
	# 	file as well. 
	for VER in range(0,10):
		# import an STL file
		bpy.ops.import_mesh.stl(filepath=FILE_PATH)

		# 				**GENETIC ALGORITHM HERE**
		# define the cutting angle x, y, z for bisect function
		X = 0
		Y = 0
		Z = 0



		# cut the model
		cut_porygon(X,Y,Z)

		# sliced face down
		rotate_model()

		# export different versions of the sliced models
		export_result(VER)

		# select everything and delete
		bpy.ops.object.select_all(action='SELECT')
		bpy.ops.object.delete()



# execute
main()







