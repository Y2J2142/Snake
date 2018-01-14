import sys
import random
import pygame


screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Turbo Snek 3000')
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsansms', 50)
segments = []
sprites_list = pygame.sprite.Group()
apple_sprite = pygame.sprite.Group()
size = 30
jump = 30

offset_x = 0
offset_y = 0

class Segment(pygame.sprite.Sprite):
    def __init__(self, position, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

class Applel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('apple.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 20) * 30
        self.rect.y = random.randint(0, 20) * 30
    def update(self, hit_list):
        if self in hit_list:
           self.rect = self.image.get_rect()
           self.rect.x = random.randint(0, 19) * 30 
           self.rect.y = random.randint(0, 19) * 30

for i in range(4):
    x = 300 - size * i
    y = 300 
    _segment = Segment((x, y), 'segment.jpg')
    segments.append(_segment)
    sprites_list.add(_segment)
apple = Applel()
apple_sprite.add(apple)
play = True
direction = 0
while play:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] and direction != 2:
                offset_x = -size
                offset_y = 0
                direction = 1
            if pressed[pygame.K_RIGHT] and direction != 1:
                offset_x = size
                offset_y = 0
                direction = 2
            if pressed[pygame.K_UP] and direction != 4:
                offset_x = 0
                offset_y = -size
                direction = 3  
            if pressed[pygame.K_DOWN] and direction != 3:  
                offset_x = 0
                offset_y = size
                direction = 4
        if direction == 0:
            offset_x = 0
            offset_y = -size
            direction = 3  
    score = font.render(str(len(segments)), False, (255,255,255))
    
    screen.fill((0,0,0))
    screen.blit(score, (560, 10))
    sprites_list.draw(screen)
    apple_sprite.draw(screen)
    x = (segments[0].position[0] + offset_x) % 600
    y = (segments[0].position[1] + offset_y) % 600
    new_segment = Segment((x, y), 'segment.jpg')
    collisions = pygame.sprite.spritecollide(new_segment, apple_sprite, False)
    snake_collisions =pygame.sprite.spritecollide(new_segment, segments, False)
    if snake_collisions:
        print(len(segments))
        play = False
    if collisions:
        apple_sprite.update(collisions)
    if not collisions:
        old_seg = segments.pop()
        sprites_list.remove(old_seg)
    segments.insert(0, new_segment)
    sprites_list.add(new_segment)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()