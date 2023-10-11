import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, CollectionProperty

for a in bpy.data.screens:
    #if a.name == 'Layout':
    for b in a.areas:
        if b.type == 'VIEW_3D':
            for c in b.spaces:
                if c.type == 'VIEW_3D':
                    c.clip_end = 10000
                    c.shading.type = 'WIREFRAME'
                    c.shading.wireframe_color_type = 'RANDOM'
                    c.shading.background_type = 'VIEWPORT'
                    c.shading.background_color = (1, 1, 1)
                    c.overlay.show_floor = False
                    c.overlay.show_axis_x = False
                    c.overlay.show_axis_y = False

class OT_File_Select(bpy.types.Operator, ImportHelper):
    bl_label = 'Select Qualisys'
    bl_idname = 'wm.fileselect_operator'
    
    files: CollectionProperty(
        type = bpy.types.OperatorFileListElement)
        
    directory: StringProperty(subtype='DIR_PATH')
    
    def execute(self, context):
        for t in self.files:
            with open(self.directory+t.name, 'r') as file:
                verts = []
                edges = []
                faces = []
                file_ql = list(file)
                for l in file_ql:
                    l = l.split(',')
                    verts.append([float(l[0]),float(l[1]),float(l[2])])
                edges = [[i, i+1] for i in range(len(file_ql)-1)]
                
                mesh = bpy.data.meshes.new(t.name)
                obj = bpy.data.objects.new(mesh.name, mesh)
                col = bpy.data.collections.get("Collection")
                col.objects.link(obj)
                mesh.from_pydata(verts, edges, faces)

        return {'FINISHED'}
        
    
if __name__ == '__main__':
    bpy.utils.register_class(OT_File_Select)
    bpy.ops.wm.fileselect_operator('INVOKE_DEFAULT')
    


