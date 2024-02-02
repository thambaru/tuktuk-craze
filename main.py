import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
SCREEN_CENTER = SCREEN_WIDTH // 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")

clock = pygame.time.Clock()
FPS = 60

moving_up = False
moving_down = False
moving_left = False
moving_right = False

enemy_group = pygame.sprite.Group()

BG = (66, 173, 55)


def draw_bg():
    screen.fill(BG)
    Road().draw()


def get_scaled_image(image, scale, width=0, height=0):
    return pygame.transform.scale(
        image,
        (
            int(image.get_width() * scale) + width,
            int(image.get_height() * scale) + height,
        ),
    )


class Road:
    def __init__(self, scale=2):
        self.image = pygame.image.load("assets/images/road.png").convert_alpha()
        self.image = get_scaled_image(self.image, scale)
        self.scale = scale

    def draw(self):
        img_x = (SCREEN_CENTER) - (self.image.get_width() * self.scale // 2)
        img_y = 0
        for i in range(SCREEN_HEIGHT // self.image.get_height() + 1):
            img_y = i * self.image.get_height()
            screen.blit(get_scaled_image(self.image, self.scale), (img_x, img_y))


class Car(pygame.sprite.Sprite):
    def __init__(self, char_type, x=0, y=0, scale=0.8, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed

        self.image = pygame.image.load(
            f"assets/images/{self.char_type}.png"
        ).convert_alpha()
        self.image = get_scaled_image(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        dx = 0
        dy = 0

        if self.char_type == "player":
            if moving_up and self.rect.y > 0:
                dy = self.speed * -1
            if moving_down and self.rect.y < SCREEN_HEIGHT - self.image.get_height():
                dy = self.speed * 1
            if (
                moving_left
                and self.rect.x > (SCREEN_CENTER - self.image.get_width()) - 125
            ):
                dx = self.speed * -1
            if (
                moving_right
                and self.rect.x < (SCREEN_CENTER + self.image.get_width()) + 75
            ):
                dx = self.speed * 1
            
            if self.rect.y > SCREEN_HEIGHT:
                self.rect.y = 0
                self.rect.x = random.randint(SCREEN_CENTER - 100, SCREEN_CENTER + 100)
        else:
            dy = self.speed * 1

        self.rect.x += dx
        self.rect.y += dy

        


enemy_cooldown = 0
def create_enemies():
    global enemy_cooldown
    if enemy_cooldown == 0:
        enemy_group.add(
            Car(
                "enemy-0",
                random.randint(SCREEN_CENTER - 150, SCREEN_CENTER + 150),
                -80,
                0.6,
                2,
            )
        )
        enemy_cooldown = 80
    else:
        enemy_cooldown -= 1


player = Car("player", SCREEN_CENTER, SCREEN_HEIGHT - 70, 0.8, 5)

run = True
while run:
    clock.tick(FPS)

    draw_bg()

    player.update()
    player.draw()

    create_enemies()
    enemy_group.update()
    enemy_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False

    pygame.display.update()

pygame.quit()
