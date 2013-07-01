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
        self.selectedTerrain = None
        self.file = None
                 
    def init(self):       
        self.initScreen()
        self.initHexMap()
        self.initWidgets()
                
    def initScreen(self):
        # Initialize the drawing window.
        pygame.init ()
        self.screen = pygame.display.set_mode ((1000, 680))
        self.screen.fill ((250, 250, 250))
        pygame.display.set_caption ('Hexploration')
           
        # Partial screen assignment for the Renderer.
        self.renderer = Renderer ()
        surface = pygame.Surface ((800, 680))
        self.renderer.screen = surface
        self.renderer.color = 100, 100, 100
    
    def initWidgets(self):
        # Some widgets.
        #list
   
        mScrolledList = ScrolledList(200, 200)
        mScrolledList.selectionmode = SELECTION_SINGLE
        mScrolledList.connect_signal (SIG_SELECTCHANGED, self.terrainselected,mScrolledList)
        
        mScrolledList.topleft = 0,26
        
        for terrain in self.mMap.TerrainList:
            if terrain.name != "Dummy":
                item = mTextListItem (terrain.name)
                mScrolledList.items.append (item)
                
        buttons = [Button ("Load"), Button ("#Save")]
        buttons[0].minsize = 80, buttons[0].minsize[1]
        buttons[0].topleft = 0,300
        buttons[0].connect_signal (SIG_CLICKED,self.LoadHexMap,self.renderer)
        buttons[1].minsize = 80, buttons[1].minsize[1]
        buttons[1].topleft = 90,300
        
                                
        self.renderer.add_widget(mScrolledList,self.create_file_view(self.renderer),buttons[0],buttons[1])
        
        # Blit the Renderer's contents at the desired position.
        self.renderer.topleft = 400,0
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
        if HexMath.checkInGrid(ArrayCord[0],ArrayCord[1],self.mMap.x,self.mMap.y) and self.selectedTerrain != None:
            tile = self.mMap.getTile(ArrayCord)
            terrain = self.mMap.getTerrain(self.selectedTerrain)
            tile.changeTerrain(self.mMap.getTerrain(self.selectedTerrain))           
        else:
            pass
       
    def terrainselected(self,list):
        self.selectedTerrain = list.get_selected()[0].get_text()

#widget handling
#file handling
    def create_file_view (self,renderer):
        table = Table (1, 2)
        
        
        
        hframe2 = HFrame (Label ("Save/Load Hexmap"))
        label = Label ("Selection:")
        entry = Entry ()
        entry.minsize = 200, entry.minsize[1]
        button = Button ("#Browse")
        button.connect_signal (SIG_CLICKED, self.open_filedialog, renderer, entry)
        hframe2.add_child (label, entry, button)
        table.add_child (0, 1, hframe2)
        
        table.set_row_align (0, ALIGN_TOP)
        table.topleft = 0,240
        return table        
    
    def open_filedialog (self,renderer, entry):
        buttons = [Button ("#OK"), Button ("#Cancel")]
        buttons[0].minsize = 80, buttons[0].minsize[1]
        buttons[1].minsize = 80, buttons[1].minsize[1]
        results = [DLGRESULT_OK, DLGRESULT_CANCEL]
    
        dialog = FileDialog ("Select your file(s)", buttons, results)
        dialog.depth = 1 # Make it the top window.
        dialog.topleft = 100, 20
        dialog.filelist.selectionmode = SELECTION_MULTIPLE
        dialog.connect_signal (SIG_DIALOGRESPONSE, self.set_files, dialog, entry)
        renderer.add_widget (dialog)
    
    def set_files (self,result, dialog, entry):
        string = ""
        if result == DLGRESULT_OK:
            string = "".join(["\"%s\"" % f for f in dialog.get_filenames ()])
            self.file = string
        else:
            string = "Nothing selected"
            self.file = None
        dialog.destroy ()
        entry.text = string

    def LoadHexMap(self,renderer):
        #make sure file ends with .map
        ending = 'map"'
        if self.file != None:
            check = self.file.split('\\')
            check = check[len(check)-1].split('.')
            if len(check) > 1:
                if check[1] == ending: 
                    #we should have a legit .map file, so 
                    self.file = self.file.strip('"')
                    self.mMap.LoadMap(self.file)
                    self.mMap.drawMap(self.screen)
                    self.createSimpleDialog("Erfolgreich geladen")
                else:
                    self.createSimpleDialog("Bitte .map Datein auswaehlen")
            else:
                self.createSimpleDialog("Bitte .map Datein auswaehlen")         
    
    #creating simple dialogs (with just one option for the user)
    def createSimpleDialog(self,caption):
        buttons = [Button ("OK")]
        buttons[0].minsize = 180,buttons[0].minsize[1]
        results = [DLGRESULT_OK]
        dialog = GenericDialog(caption, buttons, results)
        dialog.depth = 1 # Make it the top window.
        dialog.topleft = 100, 20
        self.renderer.add_widget (dialog)
        dialog.connect_signal(SIG_DIALOGRESPONSE,self.simpleDialog,dialog) 
    #simple fucntion for destroying dialogs with just one option, after clicking          
    def simpleDialog(self,result,dialog):
        dialog.destroy()
                
            
    
        
mApp = Application()
mApp.init()
mApp.main()
