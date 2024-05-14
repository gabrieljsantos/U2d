from functions import*


body_generator()

# Loop principal
executando = True
while executando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False



    # Atualiza a tela
    tela.fill((0, 0, 0))
    mechanics_force_acceleration()
    mechanics_collision_screen()
    fields_draw()
    #body_draw()
    menu_draw()
    pygame.display.flip()

    # Controla o FPS
    #clock.tick(30)  # Defina a taxa de quadros desejada, por exemplo, 30 FPS



# Encerra o Pygame
pygame.quit()
