from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3, ClockObject
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.filter.CommonFilters import CommonFilters
from camera import CameraController
from entity import Entity
from lighting import Lighting
import random

class scene():
    def __init__(self,base) -> None:
        self.base = base
        self.clock = ClockObject().getGlobalClock()

        Lighting(base)
        #CameraController(base)

        base.disableMouse()


        cf = CommonFilters(base.win, base.cam)
        cf.setBloom(intensity = 10)
        ShowBase.setBackgroundColor(base, 0.0, 0.0, 0.0, 1.0)


        
        #Lighting(self, False)
    
    def update_Scene(self, task):
        dt = self.clock.dt

        self.base.bullet_world.doPhysics(dt)

        return task