from panda3d.core import NodePath
from physics import Physics
from bcolors import bcolors

class Entity(NodePath):
    def __init__(self, base, position = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1), texture = None, model = "models/cube", collider = None, color = (1, 1, 1, 1), double_sided = False):
        
        if not model == None:
            self.entity = base.loader.loadModel(model)

        if not texture == None:
            texture = base.loader.loadTexture(texture)
            self.entity.setTexture(texture)
        
        if collider == 'box':
            self.collider = Physics.applyBoxCollider(base, self.entity,shape=tuple(x / 2 for x in scale))
        if collider == 'dynamic':
            self.collider = Physics.applyDynamicBoxCollider(base, self.entity)

        self.entity.setPos(position)
        self.entity.setHpr(rotation)
        self.entity.setScale(scale)
        self.entity.setColor(color)

        self.entity.reparentTo(base.render)