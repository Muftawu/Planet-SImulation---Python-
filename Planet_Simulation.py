import pygame 
import math 

pygame.init()
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

yellow = (255, 255, 0)
white = (255, 255, 255)
red = (188, 39, 50)
blue = (100, 149, 237)
dark_grey = (80, 78, 81)

clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24

    def __init__(self,x,y,radius,color,mass):
        self.x = x 
        self.y = y 
        self.radius = radius 
        self.color = color 
        self.mass = mass 

        self.x_vel = 0
        self.y_vel = 0
        self.distance_to_sun = 0
        self.orbit = []
        self.sun = False 
    
    def drawPlanet(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x,y = point 
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x,y))
            
            pygame.draw.lines(win,self.color,False,updated_points,2)

        pygame.draw.circle(win,self.color,(x,y),self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km",1, white)
            win.blit(distance_text, (x - distance_text.get_width()/2,y-distance_text.get_height()/2))
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y 
        x_distance = other_x - self.x 
        y_distance = other_y - self.y 
        distance = math.sqrt(x_distance**2 + y_distance**2)

        if other.sun:
            self.distance_to_sun = distance 
        
        theta = math.atan2(y_distance, x_distance)
        force = self.G * self.mass * other.mass / distance**2
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y

    def updatePosition(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if planet == self:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx 
            total_fy += fy 
        
        self.x_vel += total_fx * self.TIMESTEP / self.mass 
        self.y_vel += total_fy * self.TIMESTEP / self.mass 

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))

def main():
    run = True

    sun = Planet(0,0,30,yellow,1.98892*10**30)
    sun.sun = True

    mercury = Planet(0.387*Planet.AU,0,8,dark_grey,3.30*10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723*Planet.AU,0,14, white, 4.8685*10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1*Planet.AU,0,16,blue,5.9742*10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524*Planet.AU,0,12,red,6.39*10**23)
    mars.y_vel = 24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]

    while run:
        screen.fill((0,0,0))
        clock.tick(FPS)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False 

        for planet in planets:
            planet.drawPlanet(screen)
            planet.updatePosition(planets)

        pygame.display.update()

if __name__ == "__main__":
    main()