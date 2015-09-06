#!/usr/bin/env python
#
# Joey Navarro
#
# This is a test of a Lindenmayer grammar that generates
# rather realistic-looking plant shrubbery. You can go to
# http://en.wikipedia.org/wiki/L-system for more information.
# This script requires the python-pygame dependency.
#
# I don't know jack about licensing so this is public domain.

import pygame, sys, math, os, random
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] ="1" ## Makes the window centered on-screen

class Main: ## Wrapper for the main method
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()

        self.screen = pygame.display.set_mode((800,600), SWSURFACE)
        self.screen.fill((179,229,254)) ## Fill with a sort of sky-bluish color
        pygame.display.set_caption("L-System Test")

        self.clock = pygame.time.Clock()

        self.positions = []        ## Stack of origin points from which to draw a branch
        self.angles = []           ## Stack of angles at which to draw each branch
        self.widths = []           ## Stack of widths of each branch
        self.color_scales = []     ## Stack of color values for each branch
        self.string = "X"          ## Initial "seed" for the iterative process
        self.angle = 180           ## Initial angle at which to draw the tree
        self.cur_pos = [1000,1000] ## Offset the origin point offscreen
        self.length = 4            ## Length of each segment
        self.width = 8             ## Starting width to draw each branch
        self.color_scale = 1.0     ## Color value is initialized to 100%

        self.skip = False          ## This permits the user to skip drawing

    def _quit(self): ## Safe exiting method
        pygame.quit()
        sys.exit()

    def iterate(self):            ## Handles one iteration of L-system recursion
        temp_string = ""          ## Create a new string
        for ch in self.string:    ## Read through the current string
            if ch == "X":         ## Grammar rule: (X -> F-[[X]+X]+F[+FX]-X)
                temp_string += "F-[[X]+X]+F[+FX]-X"
            elif ch == "F":       ## Grammar rule: (F -> FF)
                temp_string += "FF"
            else:                 ## Write in any constants
                temp_string += ch
        self.string = temp_string ## Update our string

    def read(self):               ## Interprets and renders the recursed string
        length = len(self.string) ## Length and count measure how much progress we've made in parsing this string
        count = 0
        for ch in self.string:
            if ch == "F":         ## Draw a line straight forward in the current angle, from the current origin
                new_pos_x = self.cur_pos[0] + math.cos(self.angle) * self.length
                new_pos_y = self.cur_pos[1] + math.sin(self.angle) * self.length
                pygame.draw.line(self.screen, (int(78*self.color_scale),
                                               int(117*self.color_scale),
                                               int(28*self.color_scale)),
                                               self.cur_pos, [int(new_pos_x),int(new_pos_y)], self.width)
                self.cur_pos = [int(new_pos_x),int(new_pos_y)]
                self.angle += 0.02 * random.randint(-1,1)
            elif ch == "+" or ch == "-": ## Randomly choose between rotating the angle 170 degrees left or right
                self.angle += 170 * random.choice((-1,1))
            elif ch == "[": ## Push our current state onto the stack and enter a sub-branch
                self.positions.append(self.cur_pos)
                self.angles.append(self.angle)
                self.widths.append(self.width)
                self.color_scales.append(self.color_scale)
                self.width = max(1, self.width-1)                  ## Branches get smaller further up
                self.color_scale = max(0.01, self.color_scale-0.1) ## Branches get darker further up
            elif ch == "]": ## Pop the previous state off the stack and exit a sub-branch
                self.cur_pos = self.positions.pop(-1)
                self.angle = self.angles.pop(-1)
                self.width = self.widths.pop(-1)
                self.color_scale = self.color_scales.pop(-1)

            count += 1
            pygame.draw.rect(self.screen, (0,0,0), (10,550,780,20)) ## This displays how much progress we've made
            pygame.draw.rect(self.screen, (255,255,255), (10,550,int(780*count/float(length)),20))

            if not self.skip: ## If we're not skipping, update the tree picture each frame
                pygame.display.flip()

                for e in pygame.event.get():           ## Makes it so the program doesn't hang while drawing
                    if e.type == pygame.QUIT:
                        self._quit()
                    elif e.type == pygame.KEYDOWN:     ## You can exit, too
                        if e.key == pygame.K_ESCAPE:
                            self._quit()
                        elif e.key == pygame.K_RETURN: ## Press ENTER to fast-forward
                            self.skip = True

    def run(self):
        for n in range(7): ## Seven levels of recursion, we could do more but it'll take a lot longer
            self.iterate()
            
        self.read()        ## Parse what we've generated
        
        while True:
            self.clock.tick(30) ## 30 FPS
            pygame.display.flip()
            
            for e in pygame.event.get(): ## Allow the user to bask in the glory of their randomly generated tree
                if e.type == pygame.QUIT:
                    self._quit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self._quit()

if __name__ == "__main__":
    main = Main()
    main.run()
