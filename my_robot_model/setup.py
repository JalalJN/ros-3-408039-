from setuptools import setup
from glob import glob

package_name = 'my_robot_model'
setup(name=package_name, version='1.0.0', packages=[package_name],
      data_files=[
          ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
          ('share/' + package_name, ['package.xml']),
          *[('share/' + package_name + '/' + folder, glob(folder + '/*'))
            for folder in ('launch', 'urdf', 'config', 'meshes')]],
      install_requires=['setuptools'], zip_safe=True,
      maintainer='Student', maintainer_email='student@example.com',
      description='Mobile robot with a two-link arm', license='Apache-2.0')
