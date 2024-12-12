from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3, ClockObject
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.filter.CommonFilters import CommonFilters
from camera import CameraController
from entity import Entity
from lighting import Lighting
from movything import MovyThing
from physics import Physics
import random

class scene():
    def __init__(self,base) -> None:
        self.base = base

        self.base.task_mgr.add(self.update_Scene, "update_scene")
        self.clock = ClockObject().getGlobalClock()

        Lighting(base)

        self.bullet_world = BulletWorld()
        self.bullet_world.setGravity(Vec3(0, 0, -9.81))

        cube = self.base.loader.loadModel("models/cube.egg")
        cube.setColorScale((1.0, 0.1, 0.1, 1.0))
        cube.reparentTo(self.base.render)
        cube_col = Physics.applyDynamicBoxCollider(self.base, cube)
        cube_col.setPos(Vec3(5.0, 0.0, 3.0))
        cube_col.node().setLinearVelocity(self.base.render.getRelativeVector(self.base.camera, Vec3.forward()) * 10.0)
        print('red cube: ',cube_col.node().getLinearVelocity())


        self.cube_array = []

        base.disableMouse()
        CameraController(base)

        cf = CommonFilters(base.win, base.cam)
        cf.setBloom(intensity = 1)
        ShowBase.setBackgroundColor(base, 0.0, 0.0, 0.0, 1.0)

        Entity(self.base, scale=(1000,1000,1), color=(0,0.7,0,1), collider='box')
        
        for x in range(100):
            Entity(self.base, position=(random.randint(-500,500), random.randint(-500,500), 1), scale=(10,10,random.randint(50,175)), color=(0.7,0.7,0.7,1))
        
        
        for x in range(100):
            g = MovyThing(base, position=(random.randint(-10,10), random.randint(-10,10), 1))
            self.cube_array.append(g)
        
        #self.base.accept("l",self.killEverything)
        
    
    def killEverything(self):
        n = 0
        for x in self.cube_array:
            print(x)
            cube_col = self.cube_array[n]
            self.bullet_world.removeRigidBody(cube_col.node())
            cube_col.removeNode()
            n += 1
            del x
    
    def update_Scene(self, task):
        dt = self.clock.dt

        return task.cont