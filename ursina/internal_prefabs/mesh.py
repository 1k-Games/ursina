from panda3d.core import MeshDrawer, NodePath
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomNode
from panda3d.core import GeomTriangles, GeomTristrips, GeomTrifans
from panda3d.core import GeomLines, GeomLinestrips, GeomPoints

class Mesh(NodePath):

    def __init__(self, verts, tris=None, colors=None, uvs=None, normals=None, static=True, mode='ngon', thickness=1):
        super().__init__('mesh')
        if not verts:
            return

        static_mode = Geom.UHStatic if static else Geom.UHDynamic

        formats = {
            (0,0,0) : GeomVertexFormat.getV3(),
            (1,0,0) : GeomVertexFormat.getV3c4(),
            (0,1,0) : GeomVertexFormat.getV3t2(),
            (1,0,1) : GeomVertexFormat.getV3n3c4(),
            (1,1,0) : GeomVertexFormat.getV3c4t2(),
            (0,1,1) : GeomVertexFormat.getV3n3t2(),
            (1,1,1) : GeomVertexFormat.getV3n3c4t2()
            }

        vertex_format = formats[(colors != None, uvs != None, normals != None)]
        vdata = GeomVertexData('name', vertex_format, static_mode)
        vdata.setNumRows(len(verts)) # for speed

        # normal = GeomVertexWriter(vdata, 'normal')
        # texcoord = GeomVertexWriter(vdata, 'texcoord')

        vertexwriter = GeomVertexWriter(vdata, 'vertex')
        for v in verts:
            vertexwriter.addData3f((v[0], v[2], v[1])) # swap y and z

        if colors:
            colorwriter = GeomVertexWriter(vdata, 'color')
            for c in colors:
                colorwriter.addData4f(c)

        if uvs:
            uvwriter = GeomVertexWriter(vdata, 'texcoord')
            for uv in uvs:
                uvwriter.addData2f(uv)
        # normal.addData3f(0, 0, 1)
        # texcoord.addData2f(1, 0)
        modes = {
            'triangle' : GeomTriangles(static_mode),
            'tristrip' : GeomTristrips(static_mode),
            'ngon' : GeomTrifans(static_mode),
            'line' : GeomLines(static_mode),
            'lines' : GeomLinestrips(static_mode),
            'point' : GeomPoints(static_mode),
            }
        if mode == 'line' and len(verts) % 2 > 0:
            if len(verts) == 1:
                mode = point
            print('warning: number of verts must be even for line mode, ignoring last vert')
            verts = verts[ : len(verts)-1]

        prim = modes[mode]

        if tris:
            for t in triss:
                prim.addVertex(t)
        else:
            prim.addConsecutiveVertices(0, len(verts))

        prim.close_primitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        geomNode = GeomNode('mesh')
        geomNode.addGeom(geom)
        self.attachNewNode(geomNode)
        # print('finished')
        self.thickness = thickness


    @property
    def thickness(self):
        return self.getRenderModeThickness()

    @thickness.setter
    def thickness(self, value):
        self.setRenderModeThickness(value)


if __name__  == '__main__':
    from ursina import *
    app = Ursina()
    verts = ((-2,0,0), (2,0,0), (1,4,0), (-1,4,0), (-2,0,0))
    uvs = ((-2,0), (2,0), (1,4), (-1,4), (-2,0))
    colors = (color.red, color.blue, color.lime, color.black)
    m = Mesh(verts, uvs=uvs, mode='ngon', thickness=20)
    # m.thickness = 50
    # nodePath = render.attachNewNode(m)
    e = Entity()
    e.model = m
    # e.color = color.red

    app.run()