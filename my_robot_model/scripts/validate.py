#!/usr/bin/env python3
"""Offline checks. Requires xacro, urdf-parser-py and PyYAML."""
from pathlib import Path
import ast
import math
import struct
import xml.etree.ElementTree as ET
import xacro
import yaml
from urdf_parser_py.urdf import URDF

p = Path(__file__).resolve().parents[1]
for f in p.rglob('*.py'):
    ast.parse(f.read_text())
for f in [p/'package.xml', *list((p/'urdf').iterdir())]:
    ET.parse(f)
print('PASS: Python syntax and XML parsing')
expanded = xacro.process_file(str(p/'urdf/diff_robot_model.urdf.xacro')).toxml()
robot = URDF.from_xml_string(expanded)
assert robot.get_root() == 'base_footprint'
assert len(robot.links) == 12 and len(robot.joints) == 11
assert len({l.name for l in robot.links}) == len(robot.links)
children = [j.child for j in robot.joints]
assert len(set(children)) == len(children)
for link in robot.links:
    robot.get_chain('base_footprint', link.name)
assert sum(j.type == 'continuous' for j in robot.joints) == 2
assert sum(j.type == 'revolute' for j in robot.joints) == 2
print('PASS: Xacro expansion, connected tree: 12 links, 11 joints, 4 moving joints')
# Compare normalized XML structures; ignore insignificant numeric formatting.
def normalize(node):
    def value(v):
        try: return tuple(round(float(x), 10) for x in v.split())
        except ValueError: return v
    return (node.tag, sorted((k,value(v)) for k,v in node.attrib.items()), [normalize(c) for c in node])
assert normalize(ET.fromstring(expanded)) == normalize(ET.parse(p/'urdf/diff_robot_model.urdf').getroot())
URDF.from_xml_file(str(p/'urdf/my_first_model.urdf'))
print('PASS: expanded model matches plain URDF; introductory URDF parses')
for name in ('wheel_left_joint', 'wheel_right_joint'):
    j=robot.joint_map[name]
    assert j.axis == [0,1,0]
    assert abs((.16+j.origin.xyz[2])-.1)<1e-9
for name, bound in [('shoulder_joint', .6), ('elbow_joint', .8)]:
    j=robot.joint_map[name]
    assert j.limit.lower == -bound and j.limit.upper == bound
    assert j.limit.effort > 0 and j.limit.velocity > 0
# In frame 1, first collision box ends at z=.24; second box's
# minimum z is .28+.04*cos(q2)-.025*abs(sin(q2)).
clearances = [.28+.04*math.cos(q)-.025*abs(math.sin(q))-.24
              for q in [-.8+i*1.6/1600 for i in range(1601)]]
assert min(clearances) > .049
# Analytic minimum also occurs at |q2|=.8, derivative negative for q2>=0.
minimum=.04+.04*math.cos(.8)-.025*math.sin(.8)
assert minimum > .049
print(f'PASS: arm box separation, analytic bound {minimum:.6f} m; 1601 sampled elbow angles')
for q1 in [-.6+i*1.2/120 for i in range(121)]:
    for q2 in [-.8+i*1.6/160 for i in range(161)]:
        z1=.28+.04*math.cos(q1)-.025*abs(math.sin(q1))
        z2=.28+.28*math.cos(q1)+.04*math.cos(q1+q2)-.025*abs(math.sin(q1+q2))
        assert min(z1,z2) > .22
print('PASS: arm bodies above platform in 19481 joint configurations')
mesh=p/'meshes/sensor.stl'; b=mesh.read_bytes()
assert len(b)==84+50*struct.unpack_from('<I',b,80)[0]
cfg=yaml.safe_load((p/'config/rviz.rviz').read_text())
assert cfg['Visualization Manager']['Global Options']['Fixed Frame']=='base_link'
print('PASS: binary STL and RViz YAML')
print('NOT RUN: colcon build, ROS 2 nodes, RViz GUI, native check_urdf (ROS 2 unavailable here).')
