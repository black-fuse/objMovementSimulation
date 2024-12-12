from entity import Entity
from physics import Physics
from panda3d.core import ClockObject, Vec3, NodePath
import random


class MovyThing(NodePath):
    def __init__(self, base, position=(0,0,0), scale=(0,0,0)):
        super().__init__("thing")

        self.base = base
        self.position = position
        self.scale = scale

        self.body = self.base.loader.loadModel("models/cube.egg")
        #tex = base.loader.loadTexture('textures/skybox.cubemap.png')
        #self.body.setTexture(tex)
        self.body.setColorScale((1.0, 1.0, 1.0, 1.0))
        #self.body.setPos(position)
        self.setScale(scale)
        self.body.reparentTo(self.base.render)
        self.collider = Physics.applyDynamicBoxCollider(self.base, self.body, mass=1, friction=1)

        self.speed = 2
        self.moving = False
        
        self.tagList = ["living"]

        self.forward = Vec3(0.0, -1.0, 0.0)
        self.velocity = Vec3(0.0, -1.0, 0.0)

        self.globalClock = ClockObject().getGlobalClock()
        base.taskMgr.add(self.update, "update_thing")


        self.base.accept("+", self.increaseSpeed)
        self.base.accept("-", self.decreaseSpeed)
        self.base.accept("m", self.moveToggle)
        self.base.accept("l", self.die)

        self.reparentTo(base.render)


    def moveToggle(self):
        self.moving = not self.moving
    

    def die(self):
        self.bullet_world.removeRigidBody(self.collider.node())
        self.collider.removeNode()
        self.removeNode()

    
    def increaseSpeed(self):
        self.speed += 1
        print("increasing speed")
    

    def decreaseSpeed(self):
        self.speed -= 1
    
    def decide_turn(self):
        n = random.randint(0,20)

        if n == 0:
            return 10
        elif n == 1:
            return -10
        else:
            return 0
        
    
    def decide_if_moving(self):
        n = random.randint(0,100)
        if n == 1:
            self.moving = not self.moving
    

    def update(self, task):
        dt = self.globalClock.dt

        #self.setPos(self.getPos() + self.velocity)
        self.forward = self.base.render.getRelativeVector(self.body, Vec3(0,-1,0))

        self.velocity = (self.forward * self.speed * dt)
        #print(self.velocity)
        #self.speed = self.speed - 0.1

        self.decide_if_moving()

        #print(self.collider.getP())
        self.collider.setP(self.collider.getP() + self.decide_turn())

        if self.moving:
            self.collider.node().setLinearVelocity(self.velocity * 1000)
            self.moving = False
            #print(self.collider.node().getLinearVelocity())

        return task.cont
