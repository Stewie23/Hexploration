# Embedding example of the Renderer in an own pygame mainloop with
# partial screen assignment.
import sys, random

import pygame, pygame.locals
import pygame.gfxdraw #we want to be able to use filled polys...

from ocempgui.draw import Draw
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from customGuiElements import mTextListItem
import HexMath,HexMap



class Application:
    def __init__(self):
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
        #list
        mScrolledList = ScrolledList (200, 200)
        mScrolledList.selectionmode = SELECTION_SINGLE
        mScrolledList.connect_signal (SIG_SELECTCHANGED, self.listselected,mScrolledList)
        
        item = mTextListItem ("Entry")
        mScrolledList.items.append (item)
        
         
        self.renderer.add_widget(mScrolledList)
        
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
                elif event.type == MOUSEMOTION:
                    #set caption with mouse cords
                    pass
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #mouse picking                       
                        self.HexGridMousePick(event.pos[0],event.pos[1])
            # Pass all events to the Renderer.
            self.renderer.distribute_events (*events)
   
            # Blit the renderer, too
            self.screen.blit (self.renderer.screen, self.renderer.topleft)
            pygame.display.flip ()
            pygame.time.delay (30)

    def HexGridMousePick(self,x,y):
        #addjust for offset of the hex grid
        x -= self.mMap.offsetX
        y -= self.mMap.offsetY     
        #convert mouse to hex cords   
        ArrayCord =  HexMath.ScreenToHex(x, y,self.mMap.radius)
        #check if in grid
        if HexMath.checkInGrid(ArrayCord[0],ArrayCord[1],self.mMap.x,self.mMap.y):
            print ArrayCord
        else:
            pass
       
    def listselected(self,list):
        print list.get_selected()[0].get_text()
      
        
mApp = Application()
mApp.init()
mApp.main()
