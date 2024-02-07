import pygame
import helpers
import game
import intro

while helpers.run:
    helpers.clock.tick(helpers.FPS)

    if helpers.intro_shown:
        game.execute_game()
    else:
        intro.show_intro()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    helpers.run = False
                    continue
                if event.key == pygame.K_RETURN:
                    helpers.intro_shown = True
            if event.type == pygame.QUIT:
                helpers.run = False

pygame.quit()