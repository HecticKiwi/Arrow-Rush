import math, random
import pygame
from pygame.locals import *

FPS = 60
WIDTH = 480
HEIGHT = 360
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GAME_OVER = USEREVENT + 1

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Rush")
background = pygame.image.load("data\\" + "background.jpg")

score = 0

class Text(pygame.sprite.Sprite):
    def __init__(self, text="null", size=50, center=(0,0), wobble=False, visible=True):
        super().__init__()

        self.font = pygame.font.SysFont("comicsansms", size)
        self.theta = 0
        self.center = center
        self.wobble = wobble
        self.visible = visible
        self.set_text(text)

    def update(self):
        if self.visible:
            if self.wobble:
                self.theta += 0.05
                self.image = pygame.transform.rotate(self.original, math.sin(self.theta) * 5)
                self.rect = self.image.get_rect(center=self.center)

            screen.blit(self.image, self.rect)

    def set_text(self, text):
        self.original = self.font.render(text, True, BLACK)
        self.image, self.rect = self.original.copy(), self.original.get_rect(center=self.center)

class Button(pygame.sprite.Sprite):
    def __init__(self, file, center=(0,0), visible=True):
        super().__init__()

        self.center = center
        self.image = pygame.image.load("data\\" + file)
        self.rect = self.image.get_rect(center=self.center)
        self.width, self.height = self.rect.width, self.rect.height
        self.mask = pygame.mask.from_surface(self.image)
        self.brightness, self.brightness_cap = 0, 25
        self.size, self.size_cap = 1, 1.05
        self.visible = visible

    def is_selected(self) -> bool:
        x, y = pygame.mouse.get_pos()
        pos_in_mask = x - self.rect.x, y - self.rect.y
        return self.rect.collidepoint((x, y)) and self.mask.get_at(pos_in_mask)

    def update(self):
        if self.visible:
            if self.is_selected():
                self.brightness += 3 if self.brightness < self.brightness_cap else 0
                self.size += (self.size_cap - self.size) / 5
            else:
                self.brightness -= 3 if self.brightness > 0 else 0
                self.size += (1 - self.size) / 5

            self.new_image = self.image.copy()
            self.new_image = pygame.transform.smoothscale(
                self.new_image, (round(self.width*self.size), round(self.height*self.size)))
            self.new_image.fill(
                tuple(num + self.brightness for num in BLACK), special_flags=BLEND_RGB_ADD)
            self.new_rect = self.new_image.get_rect(
                center=self.center)

            screen.blit(self.new_image, self.new_rect)


class Arrows(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.directions = [
            K_UP,
            K_DOWN,
            K_LEFT,
            K_RIGHT
        ]
        self.rotations = {
            K_UP: 90,
            K_DOWN: -90,
            K_LEFT: 180,
            K_RIGHT: 0
        }
        self.visible = False
    
    def refresh_arrow(self):
        self.color = "red" if random.randrange(0, 3) == 1 else "black"

        if self.color == "black":
            self.image = pygame.image.load("data\\" + "arrow.png")
        else:
            self.image = pygame.image.load("data\\" + "red_arrow.png")

        self.direction = self.directions[random.randrange(0, 4)]
        self.image = pygame.transform.rotate(
            self.image, self.rotations[self.direction] if self.color == "black" else self.rotations[self.direction] + 180)
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT*2/5))

    def update(self):
        if self.visible:
            screen.blit(self.image, self.rect)

    def handle_input(self, key):
        if self.direction == key:
            arrow_push.play()
            global score
            score += 1
            print(score)
            self.refresh_arrow()
            score_text.set_text(f"Score: {score}")
            time_meter.meter = 1
        else:
            time_meter.meter -= 0.3 if time_meter.meter > 0.3 else time_meter.meter


class TimeMeter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.meter = 1
        self.visible = False

        self.rect = pygame.Rect([0, 0, 0, 0])
        self.rect.width = 400
        self.rect.height = 50
        self.rect.center = (WIDTH / 2, HEIGHT * 4 / 5)

        self.inner_rect = self.rect.copy()
        self.inner_rect = self.inner_rect.inflate(-10, -10)
        self.inner_rect_left = self.inner_rect.left

    def update(self):
        if self.visible:
            self.inner_rect.width = 390 * self.meter
            self.meter -= 0.001 + score*0.001 if self.meter > 0 else 0

            if self.meter <= 0:
                pygame.time.set_timer(GAME_OVER, 1, True)

            pygame.draw.rect(screen, BLACK, self.rect, border_radius=5)
            pygame.draw.rect(screen, RED, self.inner_rect, border_radius=5)


clock = pygame.time.Clock()

button_push = pygame.mixer.Sound("data\\" + "button_push.mp3")
arrow_push = pygame.mixer.Sound("data\\" + "arrow_push.mp3")
crowd_aww = pygame.mixer.Sound("data\\" + "crowd_aww.wav")
bgm = pygame.mixer.Sound("data\\" + "bgm.mp3")
bgm.play(-1)


title_text = Text("Arrow Rush", size=50, center=(WIDTH/2, HEIGHT/4), wobble=True, visible=True)
score_text = Text(f"Score: {score}", size=35, center=(WIDTH/2, HEIGHT/2), wobble=False, visible=False)
game_over_text = Text("Game Over...", size=50, center=(WIDTH/2, HEIGHT/4), wobble=True, visible=False)
text_sprites = pygame.sprite.Group(title_text, score_text, game_over_text)

play_button = Button("play_button.png", center=(WIDTH/2, HEIGHT*3/4), visible=True)
retry_button = Button("retry_button.png", center=(WIDTH/2, HEIGHT*3/4), visible=False)
button_sprites = pygame.sprite.Group(play_button, retry_button)

arrows = Arrows()
arrows.refresh_arrow()
time_meter = TimeMeter()

game_active = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if play_button.is_selected() and play_button.visible:
                button_push.play()
                play_button.visible = False
                title_text.visible = False

                arrows.visible = True
                time_meter.visible = True
                game_active = True
            elif retry_button.is_selected() and retry_button.visible:
                button_push.play()
                retry_button.visible = False
                game_over_text.visible = False
                score_text.visible = False

                score = 0
                time_meter.meter = 1
                time_meter.visible = True
                arrows.visible = True
                game_active = True
        if event.type == KEYDOWN and game_active:
            arrows.handle_input(event.key)
        if event.type == GAME_OVER:
            crowd_aww.play()
            arrows.visible = False
            time_meter.visible = False
            game_active = False

            score_text.visible = True
            game_over_text.visible = True
            retry_button.visible = True

    screen.blit(background, (0, 0))

    text_sprites.update()
    button_sprites.update()
    arrows.update()
    time_meter.update()

    pygame.display.update()
    clock.tick(FPS)
