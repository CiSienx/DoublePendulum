import numpy as np 
import pygame as pg
import pygame.gfxdraw as gfx
import keyboard as key

class physics:
    def __init__(self,mass1,mass2,lenght):
        self.U1 = 0
        self.U2 = 0
        self.time = 0.1
        self.gravity = 10
        self.lenght = lenght
        self.m1 = mass1
        self.m2 = mass2

    def action1(self,angle,fangle):
        c1 = - self.gravity * (2 * self.m1 + self.m2) *  np.sin(angle)
        c2 = - self.m2 * self.gravity * np.sin(angle - 2 * fangle)
        c3 = - 2 * np.sin(angle - fangle) * self.m2 * (np.square(self.U2) * self.lenght + np.square(self.U1) * self.lenght * np.cos(angle - fangle))
        d1 = self.lenght * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * angle - 2 * fangle))
        alpha = (c1 + c2 + c3)/d1
        dPhi = self.U1 * self.time + 0.5 * alpha * np.square(self.time)
        self.U1 += alpha * self.time
        return angle + dPhi

    def action2(self,angle,fangle):
        c0 = 2 * np.sin(angle - fangle)
        c1 = np.square(self.U1) * self.lenght * (self.m1 + self.m2)
        c2 = self.gravity * (self.m1 + self.m2) * np.cos(angle)
        c3 = np.square(self.U2) * self.lenght * self.m2 * np.cos(angle - fangle)
        d1 = self.lenght * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * angle - 2 * fangle))
        alpha = c0 * (c1 + c2 + c3)/d1
        dPhi = self.U2 * self.time + 0.5 * alpha * np.square(self.time)
        self.U2 += alpha * self.time
        return fangle + dPhi

class simulate:
    def __init__(self):
        self.size = (1200,700)
        self.screen = pg.display.set_mode(self.size)

    class Trail:
        def __init__(self,surface,color):
            self.trail = []
            self.color = color
            self.surface = surface

        def draw(self,pos,l):
            self.trail.append(pos)
            if len(self.trail) > l:
                self.trail.pop(0)
            for i in range(len(self.trail)-2):
                pg.draw.line(self.surface,self.color,self.trail[i],self.trail[i+1])

    def control(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break

    def pendulum(self,origin,angle,length,color):
        pos = (origin[0] +length*np.sin(angle), origin[1] +length*np.cos(angle))
        pg.draw.circle(self.screen,color,pos,8)
        pg.draw.line(self.screen,(0,0,0),origin,pos,width=1)
        return pos

    def main(self):
        pen1 = physics(1,1,150)
        pen2 = physics(1,1,150)
        thi = np.pi/3 + 0.01
        thi2 = np.pi/4
        phi = np.pi/3 - 0.01
        phi2 = np.pi/4
        origin = (self.size[0]/2 - 300,self.size[1]/2 - 100)
        originS = (self.size[0]/2 + 300,self.size[1]/2 - 100)
        trail1 = self.Trail(self.screen,(0,200,0))
        trail2 = self.Trail(self.screen,(200,0,200))
        trail11 = self.Trail(self.screen,(100,100,0))
        trail12 = self.Trail(self.screen,(0,100,200))
        colori = 0
        while True:
            #screen clearing
            if key.is_pressed('q'):
                if colori < 255:
                    colori += 1
            elif key.is_pressed('w'):
                if colori > 1:
                    colori -= 1
            self.screen.fill((255-colori,255-colori,255-colori))
            pg.draw.circle(self.screen,(0,0,0),origin,4)
            pg.draw.circle(self.screen,(0,0,0),originS,4)
            self.control()

            #drawing
                #pendulum
            origin1 = self.pendulum(origin,phi,150,(250,0,0))
            origin2 = self.pendulum(origin1,phi2,150,(0,0,200))
            originS1 = self.pendulum(originS,thi,150,(200,0,200))
            originS2 = self.pendulum(originS1,thi2,150,(100,50,250))
                #trail
            trail1.draw(origin1,100)
            trail2.draw(origin2,1000)
            trail11.draw(originS1,100)
            trail12.draw(originS2,1000)

            #calculation
            phi2 = pen1.action2(phi,phi2)
            phi = pen1.action1(phi,phi2)
            thi2 = pen2.action2(thi,thi2)
            thi = pen2.action1(thi,thi2)

            #finally
            pg.display.flip()

if __name__ == "__main__":
    play = simulate()
    play.main()