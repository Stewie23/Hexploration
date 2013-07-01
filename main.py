# Embedding example of the Renderer in an own pygame mainloop with
# partial screen assignment.
import sys, random
import pygame, pygame.locals
from ocempgui.draw import Draw
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
#test commit
class Application:
    def __init__(self):       
        self.move = True
        
    def Switch(self):
        if self.move == True:
            self.move = False
        else:
            self.move = True
    
    def init(self):
        # Initialize the drawing window.
        pygame.init ()
        self.screen = pygame.display.set_mode ((400, 400))
        self.screen.fill ((250, 250, 250))
        pygame.display.set_caption ('Hexploration')
        
        # Draw a rectangle, which can moev around on the screen.
        self.rect = Draw.draw_rect (55, 40, (255, 0, 0))
        self.screen.blit (self.rect, (20, 20))
        self.x,self.y = 20, 20
    
        # Partial screen assignment for the Renderer.
        self.renderer = Renderer ()
        surface = pygame.Surface ((200, 400))
        self.renderer.screen = surface
        self.renderer.color = 100, 100, 100
    
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

    def main(self):
    
        while True:
            events = pygame.event.get ()
            for event in events:
                if event.type == pygame.locals.QUIT:
                    sys.exit ()
            # Pass all events to the Renderer.
            self.renderer.distribute_events (*events)

            # Blit the rect at a new position
            if self.move == True:
                
                # Clean the old red rect area.
                self.screen.fill ((250, 250, 250), (self.x, self.y, 55, 40))
                
                self.x += random.randint (-1, 1)
                self.y += random.randint (-1, 1)
                # Do not let it leave the bounds.
                if self.x < 0: self.x = 0
                if self.y < 0: self.y = 0
                if self.x > 200: self.x = 200
                if self.y > 365: self.y = 365
                self.screen.blit (self.rect, (self.x, self.y))
        
                #test to set entry caption
                caption = str(self.x) + ","+ str(self.y)
                self.entry.set_text(caption)
    
            # Blit the renderer, too
            self.screen.blit (self.renderer.screen, self.renderer.topleft)
            pygame.display.flip ()
            pygame.time.delay (30)
        
mApp = Application()
mApp.init()
mApp.main()
