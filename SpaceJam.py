from math import dist
from direct.showbase.ShowBase import ShowBase
import DefensePaths as DefensePaths
import SpaceJamClasses
import Player as Player
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionHandlerEvent
from direct.particles.ParticleEffect import ParticleEffect
from direct.interval.LerpInterval import LerpFunc
from panda3d.core import Vec3
from direct.showbase import ShowBaseGlobal
from direct.gui.OnscreenText import OnscreenText
class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.SetupScene()
        self.InitializeDefenses() 
        self.SetCamera()
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Spaceship.collisionNode, self.Spaceship.modelNode)
        self.cTrav.addCollider(self.Spaceship.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)
        self.eventHandler = CollisionHandlerEvent()
        ShowBaseGlobal.base.eventHandler = self.eventHandler
        self.eventHandler.addInPattern('%fn-into-%in')
        self.accept('%fn-into-%in', self.HandleInto)
        self.taskMgr.add(self.updateCollisions, "updateCollisions")
        self.cTrav.showCollisions(self.render)
        self.SetParticles()
        self.cntExplode = 0
        self.explodeIntervals = {}
        self.planets = [self.Planet1, self.Planet2, self.Planet3, self.Planet4, self.Planet5, self.Planet6]
        self.velocity = Vec3(0, 0, 0)
        self.canLand = False
        self.currentPlanet = None
        self.isLanded = False
        self.taskMgr.add(self.ApplyGravity, "ApplyGravity")
        self.accept("l", self.Land)
        self.accept("k", self.TakeOff)
        self.lockOn = False
        self.currentTarget = None
        self.lockText = OnscreenText(text='Lock On: None', pos=(-1.3, 0.9), scale=0.07, fg=(1, 1, 1, 1), align=0)
        self.accept("t", self.ToggleLock)
        self.taskMgr.add(self.UpdateLockUI, "UpdateLockOn")
        self.taskMgr.add(self.UpdateMissiles, "UpdateMissiles")

    
    def UpdateMissiles(self, task):

        dt = ShowBaseGlobal.globalClock.getDt()

        for missileName in SpaceJamClasses.Missile.fireModels:

            missileNode = SpaceJamClasses.Missile.fireModels[missileName]

            if missileNode.isEmpty():
                continue

            missile = missileNode  

        
            if hasattr(missile, "velocity"):
                missile.setFluidPos(missile.getPos() + missile.velocity * dt)

        return task.cont
         


    
    def ToggleLock(self):
         self.lockOn = not self.lockOn

         if not self.lockOn:
              self.currentTarget = None
              self.lockText.setText("")
              print("Lock OFF")
         else:
              print("Lock ON")

    
    def UpdateLockUI(self, task):
         if not self.lockOn:
              return task.cont
         
         shipPos = self.Spaceship.modelNode.getPos()

         closest = None
         closestDist = float('inf')

         objects = []

         for obj in self.render.findAllMatches("**/Drone_*"):
              objects.append(obj)
         for obj in self.render.findAllMatches("**/Planet_*"):
              objects.append(obj)

         for obj in objects:
              dist = (obj.getPos() - shipPos).length()
              if dist < closestDist:
                    closestDist = dist
                    closest = obj
         if closest:
              self.currentTarget = closest
              self.lockText.setText(f"Locked: {closest.getName()}")

    def ApplyGravity(self, task):
        planetRadius = 100
        ship = self.Spaceship.modelNode
        shipPos = ship.getPos()
        self.canLand = False  
        
        for planet in self.planets:
            planetPos = planet.modelNode.getPos()

            direction = planetPos - shipPos
            distance = direction.length()
            
            if distance < 1500:  
                direction.normalize()
                strength = 1000 / (distance * distance)
                pull = direction * strength

                self.velocity += pull
                ship.setFluidPos(ship.getPos() + self.velocity)
            
            if distance < planetRadius + 150:
                    self.canLand = True
                    self.currentPlanet = planet
        

        for missileName in SpaceJamClasses.Missile.fireModels:

            missileNode = SpaceJamClasses.Missile.fireModels[missileName]

            if missileNode.isEmpty():
                continue

            missilePos = missileNode.getPos()

            for planet in self.planets:
                planetPos = planet.modelNode.getPos()

            direction = planetPos - missilePos
            distance = direction.length()

            if distance < 2000:
                direction.normalize()

                strength = 100000 / (distance * distance)
                pull = direction * strength

            if hasattr(missileNode, "velocity"):
                missileNode.velocity += pull
            

        return task.cont
        
        
        


    
    def Land(self):

        if not self.canLand or self.isLanded:
            print("Cannot land")
            return

        print("Landing...")

        ship = self.Spaceship.modelNode
        planet = self.currentPlanet.modelNode

        planetPos = planet.getPos()

        normal = ship.getPos() - planetPos
        normal.normalize()

        planetRadius = 100

        ship.setPos(planetPos + normal * (planetRadius + 10))
        ship.lookAt(planetPos)
        ship.setP(ship.getP() + 90)
        self.velocity = Vec3(0, 0, 0)
        self.isLanded = True

    def TakeOff(self):
        if not self.isLanded:
            return

        print("Taking off...")

        self.Spaceship.modelNode.setZ(self.Spaceship.modelNode.getZ() + 200)

        self.isLanded = False
    
    def updateCollisions(self, task):
         self.cTrav.traverse(self.render)
         return task.cont
    
        
    def SetupScene(self):
            self.Universe = SpaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, "Universe", "./Assets/Universe/Universe.png", (0, 0, 0), 15000)
            self.Planet1 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/Planet1.x", self.render, "Planet_1", "./Assets/Planets/Planet1.png", (150, 5000, 67), 100)
            self.Planet2 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/Planet2.x", self.render, "Planet_2", "./Assets/Planets/Planet2.png", (500, 5000, 67), 100)
            self.Planet3 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/Planet3.x", self.render, "Planet_3", "./Assets/Planets/Planet3.png", (1000, 5000, 67), 100)
            self.Planet4 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/Planet4.x", self.render, "Planet_4", "./Assets/Planets/Planet4.png", (1500, 5000, 67), 100)
            self.Planet5 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/Planet5.x", self.render, "Planet_5", "./Assets/Planets/Planet5.png", (2000, 5000, 67), 100)
            self.Planet6 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/Planet6.x", self.render, "Planet_6", "./Assets/Planets/Planet6.png", (2500, 5000, 67), 100)
            self.Spaceship = Player.Spaceship(self.loader, self.taskMgr, self.accept, "./Assets/Spaceships/Dumbledore.egg", self.render, "Spaceship", "./Assets/Spaceships/spacejet_C.png", (-1000, 4000, 67), 50)
            self.Space_Station = SpaceJamClasses.Space_Station(self.loader, "./Assets/Space Station/spaceStation.egg", self.render, "Space_Station", "./Assets/Space Station/SpaceStation1_Dif2.png", (2000, 3000, 67), 100)
            self.Sentinal1 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/DroneDefender/octotoad1_auv.png", self.Planet2, 900, "MLB", self.Spaceship)
            self.Sentinal2 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/DroneDefender/octotoad1_auv.png", self.Planet5, 500, "Cloud", self.Spaceship)
            self.Sentinal3 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/DroneDefender/octotoad1_auv.png", self.Planet1, 600, "MLB", self.Spaceship)
            self.Sentinal4 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/DroneDefender/octotoad1_auv.png", self.Planet5, 300, "Cloud", self.Spaceship)

            

            
    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
            unitVec = DefensePaths.BaseballSeams(step, numSeams, B = 0.4)
            unitVec.normalize()
            position = unitVec * radius * 250 + centralObject.modelNode.getPos()
            SpaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)


    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = DefensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 10)

   
    def InitializeDefenses(self):
        fullcycle = 60
        for j in range(fullcycle):
            SpaceJamClasses.Drone.droneCount += 1
            nickname = "Drone_" + str(SpaceJamClasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet1, nickname)
            self.DrawBaseballSeams(self.Space_Station, nickname, j, fullcycle, 2)


    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Spaceship.modelNode)
        self.camera.setPos(0, 1, 0)
   
    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        intoNode = entry.getIntoNodePath().getName()

        print(f"{fromNode} hit {intoNode}")
        if "Missile" not in fromNode:
            return

        missileNode = entry.getFromNodePath().getParent()
        hitNode = entry.getIntoNodePath().getParent()

        if "Planet" in intoNode:
            print("Missile hit a planet")
            if not missileNode.isEmpty():
                missileNode.removeNode()
                return

        if "Drone" in intoNode:
            print("Missile hit a drone")
            hitPos = entry.getSurfacePoint(self.render)
            self.explodeNode.setPos(hitPos)
            self.Explode()
            if not hitNode.isEmpty():
                hitNode.removeNode()
                if not missileNode.isEmpty():
                    missileNode.removeNode()
                    return
        
        if "Space_Station" in intoNode:
            print("Missile hit space station")

        if not missileNode.isEmpty():
            missileNode.removeNode()
            return

       
    def DestroyObject(self, hitID, hitPosition):
              nodeID = self.render.find("**/" + hitID)
              nodeID.detachNode()

              self.explodeNode.setPos(hitPosition)
              self.Explode()

       
    def Explode(self):
              self.cntExplode += 1
              tag = 'particles-' + str(self.cntExplode)

              self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
              self.explodeIntervals[tag].start()


    def ExplodeLight(self, t):
              if t == 1.0 and self.explodeEffect:
                     self.explodeEffect.disable()

              elif t == 0:
                     self.explodeEffect.start(self.explodeNode)

       
    def SetParticles(self):
              self.enableParticles()
              self.explodeEffect = ParticleEffect()
              self.explodeEffect.loadConfig("./Assets/Part-Fx/Part-Efx/basic_xpld_efx.ptf")
              self.explodeEffect.setScale(20)
              self.explodeNode = self.render.attachNewNode('ExplosionEffects')
            




app = MyApp()
app.run()

