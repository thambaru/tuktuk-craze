import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
SCREEN_CENTER = SCREEN_WIDTH // 2

IMAGES_DIR = "assets/images"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TukTuk Craze")

clock = pygame.time.Clock()
FPS = 60

moving_up = False
moving_down = False
moving_left = False
moving_right = False

BG = (66, 173, 55)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

curses = [
    "Koheda Malli Yanney!",
    "Apoo Tuk Tuk kaarayo",
    "Assen daanna epa",
    "Lan unata simbinna epa",
    "Ehata gannawako poddak",
    "Onna onna balagena!!",
]


def draw_bg():
    screen.fill(BG)
    Road().draw()
    drawTextWithBg(f"SCORE: {player.score}", 20, 20)


font = pygame.font.SysFont("Comic Sans MS", 30)


def drawText(text, color=WHITE, x=0, y=0, font=font, draw=True):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    if draw:
        screen.blit(textobj, textrect)
    return (textobj, textrect)


def drawTextWithBg(text, x=0, y=0, textColor=BLACK, bgColor=WHITE):
    text = drawText(text, textColor, x, y, font, False)
    pygame.draw.rect(screen, bgColor, (x - 10, x - 10, text[1].w + 20, y + 20), 0, 15)
    screen.blit(text[0], text[1])


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
        self.image = pygame.image.load(f"{IMAGES_DIR}/road.png").convert_alpha()
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
        self.scale = scale
        self.lives = 2
        self.alive = True
        self.score = 0
        self.death_animation_list = []
        self.death_animation_frame_index = 1
        self.death_animation_repitition = 0
        self.update_time = pygame.time.get_ticks()
        self.isGoodDriver = random.choice([True, False])

        self.image = self.get_alive_image()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        num_of_frames = len(os.listdir(f"{IMAGES_DIR}/death"))
        for i in range(1, num_of_frames):
            img = pygame.image.load(f"{IMAGES_DIR}/death/exp{i}.png").convert_alpha()
            self.death_animation_list.append(img)

    def get_alive_image(self):
        img = pygame.image.load(f"{IMAGES_DIR}/{self.char_type}.png").convert_alpha()
        return get_scaled_image(img, self.scale)

    def draw(self):
        screen.blit(self.image, self.rect)

    def explode(self):
        if self.death_animation_repitition >= len(self.death_animation_list) * 3:
            self.kill()
            drawText(
                "Game over!",
                WHITE,
                (SCREEN_CENTER),
                (SCREEN_HEIGHT / 2),
            )
            drawText(
                "Press any key to restart",
                WHITE,
                SCREEN_CENTER,
                (SCREEN_HEIGHT + 50) / 2,
            )
            return
        
        ANIMATION_COOLDOWN = 100

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.death_animation_frame_index += 1

        if self.death_animation_frame_index >= len(self.death_animation_list):
            self.death_animation_frame_index = 0

        self.image = self.death_animation_list[self.death_animation_frame_index]

        if (
            self.death_animation_frame_index
            == len(self.death_animation_list) - 1
        ):
            self.death_animation_repitition += 1

    def update(self):
        dx = 0
        dy = 0

        if self.char_type == "player":

            if not self.alive:
                self.explode()
                return

            # Player controls
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

            # Check collision with enemies
            self.check_collision()

        else:
            dy = self.speed * 1

            self.curse()

            if self.rect.y > SCREEN_HEIGHT:
                self.kill()
                player.addScore()

        self.rect.x += dx
        self.rect.y += dy

    def addScore(self, score=5):
        if not self.alive:
            return

        self.score += score

    def reset(self):
        self.image = self.get_alive_image()
        self.rect.y = SCREEN_HEIGHT - self.image.get_height()
        self.rect.x = SCREEN_CENTER
        self.alive = True
        self.death_animation_repitition = 0
        enemy_group.empty()
        player.lives = 2
        player.score = 0
        set_initial_values()

    def check_collision(self):
        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.alive = False
            self.lives -= 1

            if self.lives == 0:
                drawText(
                    "Game over!",
                    WHITE,
                    (SCREEN_CENTER),
                    (SCREEN_HEIGHT / 2),
                )
                drawText(
                    "Press any key to restart.",
                    WHITE,
                    SCREEN_CENTER,
                    (SCREEN_HEIGHT + 50) / 2,
                )

    def curse(self):
        if self.isGoodDriver:
            return

        if not hasattr(self, "curseChoice"):
            self.curseChoice = random.choices(curses)[0]

        self.vision = pygame.Rect(0, 0, 150, self.rect.h)
        self.vision.center = (self.rect.x + 10, self.rect.y + 100)

        # draw vision to see the collision
        # pygame.draw.rect(screen, (255, 0, 0), self.vision)

        if self.vision.colliderect(player.rect):
            drawText(self.curseChoice, WHITE, self.rect.x, self.rect.y - 20)


enemy_group = pygame.sprite.Group()
enemy_cooldown = 0
enemy_cooldown_reducing_val = 1
enemy_speed = 2

def set_initial_values():
    global enemy_cooldown, enemy_cooldown_reducing_val, enemy_speed
    enemy_cooldown = 0
    enemy_cooldown_reducing_val = 1
    enemy_speed = 2

def create_enemies():
    global enemy_cooldown, enemy_cooldown_reducing_val, enemy_speed

    if player.score != 0 and player.score % 100 == 0:
        enemy_speed += 0.01
        enemy_cooldown_reducing_val += 0.01
        for enemy in enemy_group:
            enemy.speed += 0.01

    if enemy_cooldown <= 0:
        enemy_group.add(
            Car(
                "enemy-%s" % random.randint(0, 4),
                random.randint(SCREEN_CENTER - 150, SCREEN_CENTER + 150),
                -80,
                0.6,
                enemy_speed,
            )
        )
        enemy_cooldown = 80
    else:
        enemy_cooldown -= enemy_cooldown_reducing_val


player = Car("player", SCREEN_CENTER, SCREEN_HEIGHT - 70, 0.8, 5)

run = True
while run:
    clock.tick(FPS)

    draw_bg()

    player.update()
    player.draw()

    if player.alive:
        create_enemies()
        enemy_group.update()
        enemy_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if not player.alive:
            moving_up = moving_down = moving_left = moving_right = False

            if event.type == pygame.KEYDOWN:
                player.reset()

            continue

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
