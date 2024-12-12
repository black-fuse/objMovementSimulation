from panda3d.core import DirectionalLight, AmbientLight, Vec3

class Lighting:
    def __init__(self, base, shadows = True, shadow_direction = (0.5, 0.75, -1.0), shadow_resolution = 2048, shadow_size = 50, sun_color = (1.0, 0.9, 0.8, 1.0), ambient_color = (0.3, 0.4, 0.5, 1.0)):
        super().__init__()
        self.base = base
        self.shadow_size = shadow_size

        # turns on the sun
        self.dlight = DirectionalLight("sun")
        self.dlight.setColor(sun_color)

        if (shadows):
            self.dlight.setShadowCaster(True, shadow_resolution, shadow_resolution, -2000) # turns on shadows and changes shadow quality
            self.dlight.setCameraMask(0b0001)
            lens = self.dlight.getLens()
            lens.setNearFar(-100, 100) # shadow max/min distance
            lens.setFilmSize((shadow_size, shadow_size))

        self.dlnp = base.render.attachNewNode(self.dlight)
        self.dlnp.lookAt(shadow_direction)
        base.render.setLight(self.dlnp)
        
        # ambient lighting
        self.alight = AmbientLight("alight")
        self.alight.setColor(ambient_color)
        self.alnp = self.base.render.attachNewNode(self.alight)
        self.base.render.setLight(self.alnp)

        base.render.setShaderAuto()
        #base.render.setDepthOffset(-2)

        # Render shadows
        self.dlnp.setBin("fixed", 0)
        self.base.graphicsEngine.renderFrame()

        base.taskMgr.add(self.update, "update lighting", sort=0)

    def update(self, task):
        cam_forward = self.base.render.getRelativeVector(self.base.cam, Vec3.forward())
        self.dlnp.setPos(self.base.cam.getPos(self.base.render) + cam_forward * self.shadow_size * 0.5)

        return task.cont

        