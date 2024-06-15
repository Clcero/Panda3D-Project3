from direct.showbase.ShowBase import ShowBase
from direct.task import Task 
from panda3d.core import *

class Planet(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName) 
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName) 
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

    # How many drones have been spawned.
    droneCount = 0

class Universe(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName) 
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class SpaceStation(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName) 
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Spaceship(ShowBase): # Player
    def __init__(self, base: ShowBase, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName) 
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.base = base # Must access ShowBase for taskMgr function

    # All key bindings for ship's movement.
    def SetKeyBindings(self):
        '''Space moves forwards, WASD are turning controls, Q&E move left and right.'''
        self.accept('space', self.fwdThrust, [1])
        self.accept('space-up', self.fwdThrust, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])
        self.accept('d', self.RightTurn, [1])
        self.accept('d-up', self.RightTurn, [0])
        self.accept('w', self.UpTurn, [1])
        self.accept('w-up', self.UpTurn, [0])
        self.accept('s', self.DownTurn, [1])
        self.accept('s-up', self.DownTurn, [0])
        self.accept('q', self.leftThrust, [1])
        self.accept('q-up', self.leftThrust, [0])
        self.accept('e', self.rightThrust, [1])
        self.accept('e-up', self.rightThrust, [0])


    # Movement
    def fwdThrust(self, keyDown):
        if keyDown:
            self.base.taskMgr.add(self.ApplyFwdThrust, 'forward-thrust')
        else:
            self.base.taskMgr.remove('forward-thrust')
    
    def ApplyFwdThrust(self, task):
        rate = 20
        trajectory = self.base.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()

        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

        return Task.cont
    
    def leftThrust(self, keyDown):
        if keyDown:
            self.base.taskMgr.add(self.ApplyLeftThrust, 'left-thrust')
        else:
            self.base.taskMgr.remove('left-thrust')
    
    def ApplyLeftThrust(self, task):
        rate = 10
        trajectory = self.base.render.getRelativeVector(self.modelNode, Vec3.left())
        trajectory.normalize()

        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

        return Task.cont

    def rightThrust(self, keyDown):
        if keyDown:
            self.base.taskMgr.add(self.ApplyRightThrust, 'right-thrust')
        else:
            self.base.taskMgr.remove('right-thrust')
    
    def ApplyRightThrust(self, task):
        rate = 10
        trajectory = self.base.render.getRelativeVector(self.modelNode, Vec3.right())
        trajectory.normalize()

        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

        return Task.cont
    

    # Keeps player from going upside down
    def constrainPitch(self):
        '''Constrains pitch to straight up or straight down, does not allow
            the player to go upside down.'''
        pitch = self.modelNode.getP()
        if pitch > 89.0:
            self.modelNode.setP(89.0)
        elif pitch < -89.0:
            self.modelNode.setP(-89.0)

    def updateCameraRotation(self, headingChange, pitchChange):
        '''Updates the camera rotation, calls constrainPitch().'''
        self.modelNode.setH(self.modelNode.getH() + headingChange)
        self.modelNode.setP(self.modelNode.getP() + pitchChange)
        self.constrainPitch()

    # Left and Right Turns - Gimbal locks at high pitch values
    def LeftTurn(self, keyDown):
        if keyDown:
            self.base.taskMgr.add(self.ApplyLeftTurn, 'left-turn')      
        else:
            self.base.taskMgr.remove('left-turn')

    def ApplyLeftTurn(self, task):
        rate = 1.25
        self.updateCameraRotation(rate, 0)
        return Task.cont

    def RightTurn(self, keyDown):
        if keyDown:
            self.base.taskMgr.add(self.ApplyRightTurn, 'right-turn')     
        else:
            self.base.taskMgr.remove('right-turn')

    def ApplyRightTurn(self, task):
        rate = 1.25
        self.updateCameraRotation(-rate, 0)
        return Task.cont

    # Up and Down Turns - Stops at +-89
    def UpTurn(self, keyDown):
        if keyDown:
            self.base.taskMgr.add(self.ApplyUpTurn, 'up-turn')      
        else:
            self.base.taskMgr.remove('up-turn')

    def ApplyUpTurn(self, task):
        rate = 1.25
        self.updateCameraRotation(0, rate)
        return Task.cont

    def DownTurn(self, keyDown):
        if keyDown:
            self.base.taskMgr.add(self.ApplyDownTurn, 'down-turn')     
        else:
            self.base.taskMgr.remove('down-turn')

    def ApplyDownTurn(self, task):
        rate = 1.25
        self.updateCameraRotation(0, -rate)
        return Task.cont

