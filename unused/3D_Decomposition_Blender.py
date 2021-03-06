#              DECOMPOSITION OF A 3D MODEL VIA GENETIC ALGORITHM
#
#   This algorithm of Decomposition of a 3D Model via Genetic Algorithm
# approaches the problem with 3 steps. First, volume of the model is measured
# and determine the number of pieces it would make based on the size of given
# printing bed. Second, it initializes a population of chromosomes with
# cutting instructions (cutting angle and coordinate of the cutting plane)
# -- of which the length differs based on number of cuts. Lastly, all the cut
# pieces are laid on the printing bed with their largest faces on the bottom.

import random
import math
import bpy
import bmesh
from mathutils import Vector

X_MIN = 0						# minimum angle (0)
X_MAX = math.pi*2				# maximum angle (2π)
A_OVERHANG = math.pi/4			# overhang angle (π/4)
N_POPULATION = 10 				# desired population size
P_MUTATION = 0.1 				# probability of mutation
P_CROSSOVER = 0.1 				# probability of crossover
CHROMOSOME_SIZE = 8 			# define the length of binary string
TIME_LIMIT = 100 				# define when to stop the loop
FILE_PATH = "./t.stl" 			# import file path

# import an STL file
def import_mesh():
	bpy.ops.import_mesh.stl(filepath=FILE_PATH)

# bmesh_copy_from_object
# *from https://github.com/jaredly/blender-addons/blob/master/
# 		object_print3d_utils/mesh_helpers.py
def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    """
    Returns a transformed, triangulated copy of the mesh
    """

    assert(obj.type == 'MESH')

    if apply_modifiers and obj.modifiers:
        import bpy
        me = obj.to_mesh(bpy.context.scene, True, 'PREVIEW', calc_tessface=False)
        bm = bmesh.new()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
        del bpy
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # TODO. remove all customdata layers.
    # would save ram

    if transform:
        bm.transform(obj.matrix_world)

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces, use_beauty=True)

    return bm

# rotate by modifying Euler angles [x, y, z] using binary string chromosome
def rotate_mesh(chromosome):
	# initialize every Euler angles to 0
	bpy.context.object.rotation_euler[0] = 0
	bpy.context.object.rotation_euler[1] = 0
	bpy.context.object.rotation_euler[2] = 0
	angle = inContext(X_MIN, X_MAX, toDecimal(chromosome))
	bpy.context.object.rotation_euler[1] = angle

# cut a mesh using bisect
def cut_mesh(X, Y, Z):
	# change to edit mode
	bpy.ops.object.mode_set(mode='EDIT')

	#							SEPARATING INTO PARTS
	#
	# 								**IMPORTANT**
	#
	#	First perform bisect, hide the loop (H), hover over the half you want
	#	to select, select a link (L), then finally unhide everything (option
	#	+ H). You can then use Separate tool (P) via Selection to separate the
	#	two parts.

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

# fitness function that returns the amount of support material
# This is where most of Blender works are done
def f(chromosome):
    # import mesh
    import_mesh()
	# set overhang angle
    bpy.context.scene.print_3d.angle_overhang = A_OVERHANG
    # rotate the mesh
    rotate_mesh(chromosome)
    # check faces don't overhang past a certain angle
    obj = bpy.context.active_object
    print_3d = bpy.context.scene.print_3d
    angle_overhang = (math.pi / 2.0) - print_3d.angle_overhang
    bm = bmesh_copy_from_object(obj, transform=True, triangulate=False)
    bm.normal_update()
    z_down_angle = Vector((0, 0, -1.0)).angle
    faces_overhang = [ele.index for ele in bm.faces
                        if z_down_angle(ele.normal) < angle_overhang]
    bm.free()
    bpy.ops.object.delete()
    return len(faces_overhang)

# 					**** GENETIC ALGORITHM FROM HERE ****

# loop stops when the condition is not met
def loop_condition_is_met(bestGene, timeCounter):
    idealSolution = 0
    precision = 0.001
    return abs(idealSolution - f(bestGene)) > precision and\
            timeCounter < TIME_LIMIT

# generate initial population
def initial_population(n_population):
    population = []
    for p_index in range(n_population):
        chromosome = ""
        for c_index in range(CHROMOSOME_SIZE):
            chromosome += random.choice(["0", "1"])
        population.append(chromosome)
    return population

# convert the binary into decimal
def toDecimal(binaryString):
    decimalNumber = 0
    length = len(binaryString)
    for index, digit in enumerate(binaryString):
        if digit == "1":
            decimalNumber += 2**(length - index - 1)
    return decimalNumber

# convert the decimal number into real value in context
def inContext(x_min, x_max, decimal):
    r_min = 0.0
    r_max = 2**CHROMOSOME_SIZE-1
    precision = (x_max - x_min) / (r_max - r_min)
    return x_min + decimal * precision

# mutate each index of a chromosome with a chance of P_MUTATION
def mutated(chromosome):
    mutatedChromosome = ""
    for index in range(CHROMOSOME_SIZE):
        if random.uniform(0.0, 1.0) < P_MUTATION:
            if chromosome[index] == "0":
                mutatedChromosome += "1"
            elif chromosome[index] == "1":
                mutatedChromosome += "0"
        else:
            mutatedChromosome += chromosome[index]
    return mutatedChromosome

# randomly select two parents from a population
def random_selection(population):
    adam = random.choice(population)
    population.remove(adam)
    eve = random.choice(population)
    population.remove(eve)
    return adam, eve

# uniform crossover that return two children
def uniform_crossover(adam, eve):
    child_1 = "" # first child - adam side
    child_2 = "" # second child - eve side
    for index in range(CHROMOSOME_SIZE):
        chance = random.uniform(0.0, 1.0)
        # if there is a crossover, add exchanged bit to each child
        if chance < P_CROSSOVER:
            child_1 += eve[index]
            child_2 += adam[index]
        # otherwise, add the promised bit to each child
        else:
            child_1 += adam[index]
            child_2 += eve[index]
    return child_1, child_2

# Genetic Algorithm main function
def genetic_algorithm():
	# delete the default cube
    bpy.ops.object.delete()
    population = initial_population(N_POPULATION)
    bestGene = "XXXXXXXX" # initially best is nobody
    timeCounter = 0
    while loop_condition_is_met(bestGene, timeCounter):
        for chromosome in population:
            if bestGene == "XXXXXXXX" or f(chromosome) < f(bestGene):
                bestGene = chromosome
        children = []
        for index in range(int(N_POPULATION/2)):
            adam, eve = random_selection(population)
            child_1, child_2 = uniform_crossover(adam, eve)
            children.append(child_1)
            children.append(child_2)
        population = children
        timeCounter += 1
    # print result
    print("GA Optimum: " + str((bestGene, f(bestGene))))
    bestGene_inContext = inContext(X_MIN, X_MAX, toDecimal(bestGene))
    print("Best Rotation Angle: " + str(bestGene_inContext))

# execute
genetic_algorithm()
