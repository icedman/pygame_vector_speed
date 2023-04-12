class SceneType:
    menu = 0
    game = 1
    demo = 2


class Scene:
    type = SceneType.menu

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def onUpdate(self, dt):
        pass

    def onRender(self, gfx):
        pass


class SceneService:
    defs = {}
    current = None

    def enterScene(self, scn):
        _ = self
        if _.current != None:
            if _.current.type == scn:
                return
            _.current.onExit()
        _.current = self.defs[scn]
        _.current.type = scn
        _.current.onEnter()


sceneService = SceneService()
