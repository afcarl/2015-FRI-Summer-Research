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


# create a box object
box = doc.addObject("Part::Box", "box")
# create a placement object
pl = FreeCAD.Placement()
# rotate 45 degrees along z axis
pl.Rotation = App.Rotation(45,0,0) # (z, y, x)?
# assign the placement to
myObj.Placement = pl
