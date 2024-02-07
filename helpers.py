import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
SCREEN_CENTER = SCREEN_WIDTH // 2

IMAGES_DIR = "assets/images"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TukTuk Craze")

clock = pygame.time.Clock()
FPS = 60

run = True
intro_shown = False
moving_up = False
moving_down = False
moving_left = False
moving_right = False

BG = (66, 173, 55)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

curses = [
    "Koheda Malli Yanney!",
    "Apoo Tuk Tuk kaarayo",
    "Assen daanna epa",
    "Lan unata simbinna epa",
    "Ehata gannawako poddak",
    "Onna onna balagena!!",
]

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
    pygame.draw.rect(screen, bgColor, (text[1].left - 10, text[1].top - 10, text[1].width + 20, text[1].height + 20), 0, 10)
    screen.blit(text[0], text[1])


def get_scaled_image(image, scale, width=0, height=0):
    return pygame.transform.scale(
        image,
        (
            int(image.get_width() * scale) + width,
            int(image.get_height() * scale) + height,
        ),
    )

enemy_group = pygame.sprite.Group()
enemy_cooldown = 0
enemy_cooldown_reducing_val = 1
enemy_speed = 2

def set_initial_values():
    global enemy_cooldown, enemy_cooldown_reducing_val, enemy_speed
    enemy_cooldown = 0
    enemy_cooldown_reducing_val = 1
    enemy_speed = 2