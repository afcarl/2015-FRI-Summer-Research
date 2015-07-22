# import bpy module
import bpy

# delete the default model
bpy.ops.object.delete()

# 							VERSION CONTROL
#
# 	Add VER to EXPORT_FILE_PATH when multiple versions of the result files 
# 	are needed; use this same variable for each log file for each exported
# 	file as well. 

# initialize VER as 0.0
VER = 0.0

# STL file location
FILE_PATH = "/Users/jinyeom/Desktop/AI Research/Decomposition_via_NEAT/test_programs/Blender/porygon.stl"
EXPORT_FILE_PATH = "/Users/jinyeom/Desktop/AI Research/Decomposition_via_NEAT/test_programs/Blender/result/porygon_cut_" + str(VER) + ".stl"

# model rotation angles
X = 0.0
Y = 0.0
Z = 0.0



# import an STL file
bpy.ops.import_mesh.stl(filepath=FILE_PATH)

# rotate by modifying Euler angles [x, y, z]
bpy.context.object.rotation_euler[0] = X
bpy.context.object.rotation_euler[1] = Y
bpy.context.object.rotation_euler[2] = Z

# rotate freehand
bpy.ops.transform.rotate(value=-7.52441, 
						axis=(1.0, 0.0, 0.0), 
						constraint_axis=(False, False, False), 
						constraint_orientation='GLOBAL', 
						mirror=False, 
						proportional='DISABLED', 
						proportional_edit_falloff='SMOOTH', 
						proportional_size=1)

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

# rotate so that the cut-surface is facing down


# select everything
bpy.ops.object.select_all(action='SELECT')

# export the STL file
bpy.ops.export_mesh.stl(filepath=EXPORT_FILE_PATH)




