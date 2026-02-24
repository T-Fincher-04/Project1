from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.SetupScene()
    
        
        
    def SetupScene(self):
            self.Universe = self.loader.loadModel("./Assets/Universe/Universe.glb")
            self.Universe.reparentTo(self.render)
            self.Universe.setScale(15000)
            self.Planet1 = self.loader.loadModel("./Assets/Planets/Planet1.glb")
            self.Planet1.reparentTo(self.render)
            self.Planet1.setPos(150, 5000, 67)
            self.Planet1.setScale(100)
            self.Planet2 = self.loader.loadModel("./Assets/Planets/Planet2.glb")
            self.Planet2.reparentTo(self.render)
            self.Planet2.setPos(500, 5000, 67)
            self.Planet2.setScale(100)
            self.Planet3 = self.loader.loadModel("./Assets/Planets/Planet3.glb")
            self.Planet3.reparentTo(self.render)
            self.Planet3.setPos(1000, 5000, 67)
            self.Planet3.setScale(100)
            self.Planet4 = self.loader.loadModel("./Assets/Planets/Planet4.glb")
            self.Planet4.reparentTo(self.render)
            self.Planet4.setPos(1500, 5000, 67)
            self.Planet4.setScale(100)
            self.Planet5 = self.loader.loadModel("./Assets/Planets/Planet5.glb")
            self.Planet5.reparentTo(self.render)
            self.Planet5.setPos(2000, 5000, 67)
            self.Planet5.setScale(100)
            self.Planet6 = self.loader.loadModel("./Assets/Planets/Planet6.glb")
            self.Planet6.reparentTo(self.render)
            self.Planet6.setPos(2500, 5000, 67)
            self.Planet6.setScale(100)
            self.Spaceship = self.loader.loadModel("./Assets/Spaceships/phaser.egg")
            self.Spaceship.reparentTo(self.render)
            self.Spaceship.setPos(-1000, 4000, 67)
            self.Spaceship.setScale(50)
            self.Space_Station = self.loader.loadModel("./Assets/Space Station/spaceStation.egg")
            self.Space_Station.reparentTo(self.render)
            self.Space_Station.setPos(2000, 3000, 67)
            self.Space_Station.setScale(100)
            




app = MyApp()
app.run()

