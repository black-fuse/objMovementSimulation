from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode, BulletPlaneShape

class Physics():
    def applyBoxCollider(self, node_path, shape=(0.5, 0.5, 0.5)):
        col_shape = BulletBoxShape(shape)

        col_node = BulletRigidBodyNode('box_collider')
        col_node.addShape(col_shape)

        col_np = self.render.attachNewNode(col_node)
        col_np.reparentTo(node_path)
                
        self.bullet_world.attachRigidBody(col_node)

        return col_np  
    
    def applyPlaneCollider(base, node_path, normal = (0.0, 0.0, 1.0), dist = 0.0):
        col_shape = BulletPlaneShape(normal, dist)

        col_node = BulletRigidBodyNode("plane_collider")
        col_node.addShape(col_shape)

        col_np = base.render.attachNewNode(col_node)
        col_np.reparentTo(node_path)
                
        base.bullet_world.attachRigidBody(col_node)

        return col_np
    
    def applyDynamicBoxCollider(base, node_path, mass = 1.0, friction = 10.0):
            col_shape = BulletBoxShape((0.5, 0.5, 0.5))

            col_node = BulletRigidBodyNode("dyn_box_collider")
            col_node.setMass(mass)
            col_node.setFriction(friction)
            col_node.addShape(col_shape)

            col_np = base.render.attachNewNode(col_node)
            node_path.reparentTo(col_np)
                    
            base.bullet_world.attachRigidBody(col_node)

            return col_np