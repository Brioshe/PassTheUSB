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

# Fonts
fontText = pygame.font.SysFont('Segoe UI', 30)
menuFont = pygame.font.Font('Fonts/Peignot.ttf', 30)

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
background = pygame.image.load("Images/background.jpg")
background = pygame.transform.scale_by(background, 1.50)
bgBubble = pygame.image.load("Images/bubble.png")

########### CLASSES ###########

class FadeOneObject:
    def __init__(self):
        self.position = (random.randint(0, infoObject.current_w), random.randint(0, infoObject.current_h))
        self.alpha = 0
        self.fading_in = True
        self.done = False
        
        # Set randum radius
        self.radius = random.randint(100, 400)
        
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

def fade_in(screen, duration):
    bgFade = 0.5
    fade_surface = pygame.Surface((infoObject.current_w, infoObject.current_h))
    fade_surface.fill(color=(0, 0, 0))
    alpha = 255
    
    pygame.mixer.music.load("Audio/PS2Start.mp3")
    pygame.mixer.music.play(0, 0, 0)
    pygame.mixer.music.set_volume(0.1)

    # Fade loop
    start_time = pygame.time.get_ticks()

    while alpha > 0:
        alpha -= bgFade
        fade_surface.set_alpha(alpha)

        screen.blit(background, (0,0))
        screen.blit(man, (player_pos.x - man.get_width()/2, player_pos.y-man.get_height()/2))
        screen.blit(fade_surface, (0, 0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                alpha = 0
        pygame.display.update()
        clock.tick(60)

########### CLASSES ###########

########### FLAGS ###########

debugFlag = True
menuFlag = False
gameMusicPaused = False
menuMusicPaused = True

########### FLAGS ###########


# Main game loop
clock = pygame.time.Clock()
frame_count = 0
circles = []

# Sprites
man = pygame.image.load('Images/sprite.png').convert_alpha()
man = pygame.transform.scale_by(man, 0.45)

# Fade into game
fade_in(screen,duration = 10)
pygame.mixer.music.fadeout(3)

# Music
pygame.mixer.init()

defaultBGMusic = pygame.mixer.Sound("Audio/bgaudio.mp3")
menuMusic = pygame.mixer.Sound("Audio/menuMusic.mp3")

channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel1.play(defaultBGMusic)

channel1.set_volume(0.2)

running = True
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
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menuFlag = not menuFlag

    while menuFlag == True:
        screen.fill("Black")
        if menuMusicPaused:
            channel1.pause()
            gameMusicPaused = True
            channel2.play(menuMusic)
            menuMusicPaused = False 
            channel2.set_volume(0.2)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menuFlag = not menuFlag
        
        pygame.display.flip()
        clock.tick(60)

    # Set settings
    if menuFlag == False:
        if gameMusicPaused == True:
            menuMusicPaused = True
            channel2.pause()
            gameMusicPaused = False
            channel1.unpause()

    # Friction function
    if (velocity.x > 0):
        velocity.x -= 0.5
    if (velocity.y > 0):
        velocity.y -= 0.5
    if (velocity.x < 0):
        velocity.x += 0.5
    if (velocity.y < 0):
        velocity.y += 0.5
    
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
    
    if debugFlag == True:
        #Background
        rect_color = (0, 0, 0, 128)
        rect_width = 250
        rect_height = 200
        rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        rect_surface.fill(rect_color)
        screen.blit(rect_surface,(0,0))

        # Text
        fps = clock.get_fps()
        text_line1 = fontText.render(f"Position: ({int(player_pos.x)}, {int(player_pos.y)})", False, "White") # Coordinates
        text_line2 = fontText.render(f"FPS: {int(fps)}", False, "White") # FPS
        text_line3 = fontText.render(f"Man Width: {int(man.get_width())}", False, "White") # Man Width
        screen.blit(text_line1, (0,0))
        screen.blit(text_line2, (0,(text_line1.get_height())))
        screen.blit(text_line3, (0,(text_line1.get_height() * 2)))
    
    ########### DEBUG TOOLS ###########
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()