import pygame
import os
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join ("imgs","pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join ("imgs","base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join ("imgs","bg.png")))
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join ("imgs","bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join ("imgs","bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join ("imgs","bird3.png")))
              ]

pygame.font.init()
POINTS_FONT= pygame.font.SysFont("segoe ui",30)

class Bird:
    IMGS = BIRD_IMAGES
    #rotation animation
    MAX_ROTATION = 25
    VEL_ROTATION = 20
    ANIMATION_TIME = 5

    #x,y - bird coordinates
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.height = self.y
        self.time = 0
        self.image_counting = 0
        self.image = self.IMGS[0]

    #function - y axis increase when you go down (+), to jump (-)
    def jump(self):
        self.velocity = - 10.5
        self.time = 0
        self.height = self.y

    def move(self):
        self.time += 1
        displacement = 1.5 * (self.time ** 2) + self.velocity * self.time

        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
            else:
                if self.angle > -90:
                    self.angle -= self.VEL_ROTATION
    def display_image(self,screen):
        #choose the bird image
        self.image_counting += 1

        if self.image_counting < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_counting < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.image_counting < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.image_counting < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.image_counting < self.ANIMATION_TIME*4 +1:
            self.image = self.IMGS[0]
            self.image_counting = 0

        # if bird is falling down, it won't move its wings
        if self.angle <=-80:
            self.image = self.IMGS[1]
            self.image_counting = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate (self.image, self.angle)
        center_image = self.image.get_rect(topleft =(self.x,self.y)).center
        rectangle = rotated_image.get_rect(center=center_image)
        screen.blit(rotated_image,rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Pipe:
    DISTANCE = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_position = 0
        self.bottom_position = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.BOT_PIPE = PIPE_IMAGE
        self.pass_pipe = False
        self.height_def()

    def height_def(self):
        self.height = random.randrange(50,450)
        self.top_position = self.height - self.TOP_PIPE.get_height()
        self.bottom_position = self.height + self.DISTANCE

    def move(self):
        self.x -= self.VELOCITY

    def display_image(self,screen):
        screen.blit(self.TOP_PIPE, (self.x,self.top_position))
        screen.blit(self.BOT_PIPE, (self.x,self.bottom_position))

    def colision(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        base_mask = pygame.mask.from_surface(self.BOT_PIPE)

        top_distance = (self.x - bird.x, self.top_position - round(bird.y))
        bottom_distance = (self.x - bird.x, self.bottom_position - round(bird.y))

        base_ponto = bird_mask.overlap(base_mask, bottom_distance)
        top_ponto = bird_mask.overlap(top_mask, top_distance)

        if base_ponto or top_ponto:
            return True
        else:
            return False

class Base:
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self. WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def display_image(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))

def screen_image(screen, birds, pipes, base, score):
    screen.blit(BACKGROUND_IMAGE, (0,0))
    for bird in birds:
        bird.display_image(screen)
    for pipe in pipes:
        pipe.display_image(screen)

    text = POINTS_FONT.render(f"Pontuação: {score}",1, (255,255,255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    base.display_image(screen)
    pygame.display.update()

def main():
    birds = [Bird(230,350)]
    base = Base(630)
    pipes = [Pipe(600)]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    score = 0
    clock = pygame.time.Clock()

    working = True
    while working:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        for bird in birds:
            bird.move()
        base.move()

        add_pipe = False
        remove_pipes =[]
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colision(bird):
                    birds.pop(i)
                if not pipe.pass_pipe and bird.x > pipe.x:
                    pipe.pass_pipe = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                remove_pipes.append(pipe)

        if add_pipe:
            score +=1
            pipes.append(Pipe(600))
        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i,bird in enumerate(birds):
            if(bird.y + bird.image.get_height()) > base.y or bird.y < 0:
                birds.pop(i)
        

        screen_image(screen, birds, pipes, base, score)

if __name__ == '__main__':
    main()


