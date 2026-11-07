"""Original Learjet 60 construction blockout; all component stations estimated.
Run: blender -b --factory-startup --python scripts/model/build-lod3.py
No downloaded model geometry or textures are imported.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
bpy.ops.wm.read_factory_settings(use_empty=True)
def material(name,color,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.32
 return m
white=material('white-paint',(.9,.9,.9));dark=material('rubber-and-glazing',(.025,.035,.045));metal=material('hardware',(.45,.48,.5),.8)
def mesh(name,verts,faces,mat=white,parent=None):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update();o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o.parent=parent
 for p in d.polygons:p.use_smooth=True
 return o
def pivot(name,point,parent=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=point;o.parent=parent;return o
def panel(name,corners,thickness=.04,parent=None):
 v=[(x,y,z+dz) for dz in [-thickness/2,thickness/2] for x,y,z in corners];return mesh(name,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],parent=parent)
# Blender frame X right, Y aft, Z up. glTF export converts to Y-up, +Z nose.
# Overall length sourced; section radii and stations are provisional design inputs.
stations=[(-8.945,.03,.04,.0),(-8.5,.32,.30,.08),(-7.5,.65,.65,.22),(-6,.90,.93,.35),(-4,.94,.98,.36),(0,.94,.98,.36),(3,.85,.88,.42),(5,.62,.65,.56),(7,.35,.39,.66),(8.945,.03,.06,.72)]
verts=[];N=20
for y,rx,rz,cz in stations:
 for i in range(N):
  a=i*2*math.pi/N;verts.append((rx*math.cos(a),y,cz+rz*math.sin(a)))
faces=[tuple(reversed(range(N))),tuple(range((len(stations)-1)*N,len(stations)*N))]
for j in range(len(stations)-1):
 for i in range(N):a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
mesh('fuselage-blockout',verts,faces)
for s,label in [(-1,'left'),(1,'right')]:
 panel(label+'-wing',[(s*.8,-.9,-.25),(s*6.675,2.0,.0),(s*6.675,2.65,.0),(s*.8,1.6,-.25)],.13)
 panel(label+'-winglet',[(s*6.675,2,.0),(s*6.675,2.65,.0),(s*6.55,2.8,.85),(s*6.55,2.35,.85)])
 for component,x0,x1,y in [('aileron',3.8,6.2,2.5),('flap',1.0,3.7,1.7),('spoiler',1.4,3.5,.8)]:
  p=pivot(label+'-'+component+'-hinge',(s*x0,y,-.12));panel(label+'-'+component,[(0,0,0),(s*(x1-x0),.3,0),(s*(x1-x0),.65,0),(0,.6,0)],parent=p)
 panel(label+'-stabilizer',[(0,6.2,2.8),(s*2.2,7.4,2.8),(s*2.2,8,2.8),(0,7.7,2.8)])
 p=pivot(label+'-elevator-hinge',(0,7.7,2.8));panel(label+'-elevator',[(0,0,0),(s*2.2,.3,0),(s*2.2,.6,0),(0,.6,0)],parent=p)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=(s*1.4,3.5,.8));o=bpy.context.object;o.name=label+'-nacelle-blockout';o.scale=(.45,1.6,.45);o.data.materials.append(white)
 for axle in [0]:
  p=pivot(label+'-main-gear-retract',(s*1.65,1.2,-.35))
  bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=.065,depth=.9,location=(0,0,-.45));o=bpy.context.object;o.name=label+'-gear-strut';o.parent=p;o.data.materials.append(metal)
  for offset in [-.12,.12]:
   bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.22225,depth=.13,location=(offset,0,-.95),rotation=(0,math.pi/2,0));o=bpy.context.object;o.name=label+'-wheel';o.parent=p;o.data.materials.append(dark)
panel('vertical-fin',[(0,5.2,.7),(0,6.25,2.8),(0,7.7,2.8),(0,8.1,.8)],.12)
p=pivot('rudder-hinge',(0,7.65,.8));panel('rudder',[(0,0,0),(0,.5,0),(0,.25,2),(0,-.05,2)],.06,parent=p)
p=pivot('nose-gear-retract',(0,-6.1,-.4))
bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=.055,depth=.8,location=(0,0,-.4));o=bpy.context.object;o.name='nose-strut';o.parent=p;o.data.materials.append(metal)
bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.2286,depth=.112,location=(0,0,-.9),rotation=(0,math.pi/2,0));o=bpy.context.object;o.name='nose-wheel';o.parent=p;o.data.materials.append(dark)
for o in bpy.context.scene.objects:o['construction_status']='estimated blockout; not realism validated'
out=ROOT/'build/lod3';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Learjet_60_LOD3.blend'))
bpy.ops.export_scene.gltf(filepath=str(out/'Learjet_60_LOD3.glb'),export_format='GLB')
triangles=0
for o in bpy.context.scene.objects:
 if o.type=='MESH':o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
(out/'report.json').write_text(json.dumps({'status':'initial estimated blockout','triangles':triangles,'materials':len(bpy.data.materials),'animationBindings':'not implemented','referenceGeometryImported':False},indent=2))
print('LOD3_BLOCKOUT',triangles)
