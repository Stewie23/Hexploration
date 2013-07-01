# Embedding example of the Renderer in an own pygame mainloop with
# partial screen assignment.
import sys, random
import pygame, pygame.locals
from ocempgui.draw import Draw
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
import HexMath,HexMap
import pygame.gfxdraw #we want to be able to use filled polys...


class Application:
    def __init__(self):       
        self.move = True
        
    def Switch(self):
       pass
    
    def init(self):       
        self.initScreen()
        self.initWidgets()
        self.initHexMap()
        
    def initScreen(self):
        # Initialize the drawing window.
        pygame.init ()
        self.screen = pygame.display.set_mode ((400, 400))
        self.screen.fill ((250, 250, 250))
        pygame.display.set_caption ('Hexploration')
           
        # Partial screen assignment for the Renderer.
        self.renderer = Renderer ()
        surface = pygame.Surface ((200, 400))
        self.renderer.screen = surface
        self.renderer.color = 100, 100, 100
    
    def initWidgets(self):
        # Some widgets.
        button = Button ("Stop/Go")
        button.topleft = 10, 10
        button.connect_signal (SIG_CLICKED,self.Switch)
        self.entry = Entry ("Awesome...")
        self.entry.topleft = 30, 50
        self.renderer.add_widget (button, self.entry)
    
        # Blit the Renderer's contents at the desired position.
        self.renderer.topleft = 200,0
        self.screen.blit (self.renderer.screen, self.renderer.topleft)
        
        # Set up the tick event for timer based widgets.
        pygame.time.set_timer (Constants.SIG_TICK, 10)
        
    def initHexMap(self):
        #init hex map
        TileFont = pygame.font.Font(None,15)
        color = pygame.Color(250,250, 250, 250)
        self.mMap = HexMap.Map()
        self.mMap.setFont(TileFont,color)
        self.mMap.LoadMap()
        self.mMap.drawMap(self.screen)
       
    def main(self):
    
        while True:
            events = pygame.event.get ()
            for event in events:
                if event.type == pygame.locals.QUIT:
                    sys.exit ()
            # Pass all events to the Renderer.
            self.renderer.distribute_events (*events)
   
            # Blit the renderer, too
            self.screen.blit (self.renderer.screen, self.renderer.topleft)
            pygame.display.flip ()
            pygame.time.delay (30)
        
mApp = Application()
mApp.init()
mApp.main()
