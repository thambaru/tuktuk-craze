import pygame
import helpers
import game
import intro

while helpers.run:
    helpers.clock.tick(helpers.FPS)

    if helpers.intro_shown:
        game.execute_game()
    else:
        if helpers.intro_sound.get_num_channels() == 0:
            helpers.intro_sound.play()
        intro.show_intro()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    helpers.run = False
                    continue
                if event.key == pygame.K_RETURN:
                    helpers.intro_sound.fadeout(1000)
                    ignition_playing = helpers.get_audio("tuktuk_start").play()
                    while ignition_playing.get_busy():
                        pass
                    helpers.intro_shown = True
            if event.type == pygame.QUIT:
                helpers.run = False

pygame.quit()
