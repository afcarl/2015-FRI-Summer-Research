class Print3DCheckOverhang(Operator):
    """Check faces don't overhang past a certain angle"""
    bl_idname = "mesh.print3d_check_overhang"
    bl_label = "Print3D Check Overhang"

    @staticmethod
    def main_check(obj, info):
        import math
        from mathutils import Vector

        scene = bpy.context.scene
        print_3d = scene.print_3d
        angle_overhang = (math.pi / 2.0) - print_3d.angle_overhang

        if angle_overhang == math.pi:
            info.append(("Skipping Overhang", ()))
            return

        bm = mesh_helpers.bmesh_copy_from_object(obj, transform=True, triangulate=False)
        bm.normal_update()

        z_down = Vector((0, 0, -1.0))
        z_down_angle = z_down.angle

        faces_overhang = [ele.index for ele in bm.faces
                          if z_down_angle(ele.normal) < angle_overhang]

        info.append(("Overhang Face: %d" % len(faces_overhang),
                    (bmesh.types.BMFace, faces_overhang)))
        bm.free()

    def execute(self, context):
        return execute_check(self, context)
