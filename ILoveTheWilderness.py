# Example file showing a basic pygame "game loop"
import pygame
import math
import random

########### PROPERTIES ###########

# pygame setup
pygame.init()
pygame.font.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) #fullscreen

# Sprites
man = pygame.image.load('sprite.png').convert_alpha()
man = pygame.transform.scale_by(man, 0.45)

# Fonts
ComicSans = pygame.font.SysFont('Comic Sans MS', 30)

# Object properties
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /2) # Initial Position
velocity = pygame.math.Vector2(0, 0)
lookflag = False
speed = 1
previous_x = 0

# Background Properties
spawn_interval = 60 * 4
num_objects = 3
fade_speed = 0.75

########### PROPERTIES ###########

# Background items
background = pygame.image.load("backgroundtest.jpg")
bgBubble = pygame.image.load("bubble.png")

########### CLASSES ###########

class FadeOneObject:
    def __init__(self):
        self.position = (random.randint(0, infoObject.current_w), random.randint(0, infoObject.current_h))
        self.alpha = 0
        self.fading_in = True
        self.done = False
        
        # Set randum radius
        self.radius = random.randint(50, 300)
        
        # Scale image
        self.original_image = pygame.transform.smoothscale(bgBubble, (self.radius * 2, self.radius * 2))
        
    def update(self):
        if self.fading_in:
            self.alpha += fade_speed
            if self.alpha > 255:
                self.alpha = 255
                self.fading_in = False
        else:
            self.alpha -= fade_speed
            if self.alpha < 0:
                self.alpha = 0
                self.done = True
        
    def draw(self, screen):
        image = self.original_image.copy()
        image.set_alpha(self.alpha)
        rect = image.get_rect(center=self.position)
        screen.blit(image,rect)        

########### CLASSES ###########

# Main game loop
clock = pygame.time.Clock()
running = True
frame_count = 0
circles = []

while running:
    # Get input
    keys = pygame.key.get_pressed()
    
    # Create background
    screen.blit(background, (0,0))
    
    if frame_count % spawn_interval == 0 and len(circles) < num_objects:
        circles.append(FadeOneObject())
        
    for circle in circles[:]:
        circle.update()
        circle.draw(screen)
        if circle.done:
            circles.remove(circle)
            
    frame_count += 1
    
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_ESCAPE]:
        running = False

    # Friction function
    if (velocity.x > 0):
        velocity.x -= velocity.x/10
    if (velocity.y > 0):
        velocity.y -= velocity.y/10
    if (velocity.x < 0):
        velocity.x += velocity.x/10
    if (velocity.y < 0):
        velocity.y += velocity.y/10
    
    # Velocity function
    if keys[pygame.K_LEFT]:
        velocity.x += -speed
    if keys[pygame.K_RIGHT]:
        velocity.x += speed
    if keys[pygame.K_UP]:
        velocity.y += -speed
    if keys[pygame.K_DOWN]:
        velocity.y += speed
        
    # Bounding Box functions
    
    playerCenterHoriz = man.get_width()/2
    playerCenterVert = man.get_height()/2
    
    if (player_pos.x < 0):
        player_pos.x = playerCenterVert
        velocity.x *= -1
    if (player_pos.y < 0):
        player_pos.y = playerCenterVert
        velocity.y *= -1
    if (player_pos.x + playerCenterHoriz > infoObject.current_w):
        player_pos.x = infoObject.current_w - playerCenterHoriz
        velocity.x *= -1
    if (player_pos.y + playerCenterVert > infoObject.current_h):
        player_pos.y = infoObject.current_h - playerCenterVert
        velocity.y *= -1
        
    # Add velocity    
    player_pos += velocity
        
    angle = math.degrees(math.atan2(-velocity.y, velocity.x))
    rotated_sprite = pygame.transform.rotate(man, angle)
        
    rotated_rect = rotated_sprite.get_rect(center =(int(player_pos.x), int(player_pos.y)))
    
    screen.blit(rotated_sprite, rotated_rect.topleft)
         
    previous_x = player_pos.x
    
    ########### DEBUG TOOLS ###########
    fps = clock.get_fps()
    text_surface = ComicSans.render(
        f"Position: ({int(player_pos.x)}, {int(player_pos.y)}), FPS: {int(fps)}",
        False, "Black")
    screen.blit(text_surface, (0,0))
    
    ########### DEBUG TOOLS ###########
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()