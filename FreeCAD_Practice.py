# This is a practice code for FreeCAD

# import stuff
import Mesh

# constants
FILE_PATH = "/"

# create a new document ("<document name for parameter>")
doc = FreeCAD.newDocument()
# import a new mesh (obj file)
mesh = Mesh.Mash(FILE_PATH)

# create a new object with a mesh
meshobj = doc.addObject("Mesh::feature","new obj")

# add mesh to meshobj
meshobj.Mesh = mesh

# manually update the document
doc.recompute()




# rotate the model 
