import pygame
import random
import math
import time
# Inicialização do Pygame
pygame.init()

# Configurações da tela principal
largura_tela = 800
altura_tela = 600
largura_menu_tela = 00
tela = pygame.display.set_mode((largura_tela+largura_menu_tela, altura_tela))
pygame.display.set_caption("U2d")
clock = pygame.time.Clock()


# Cores
branco = (255, 255, 255)

fields = []

body = []
N_body = 100
N_body_seated = 200

K = 40000
G = 1000
g = 000
Delta_t = 0.005


def body_generator():
    global body, N_body
    for i in range(N_body):
        color = (
            random.randint(20, 255),random.randint(20, 255),random.randint(20, 255))
        raio = 10
        x = random.randint(raio, largura_tela - raio)
        y = random.randint(raio, altura_tela - raio)
        if (x >= largura_tela/2) :
            vy = 100
        else:
            vy = -50
        
        if (y >= altura_tela/2) :
            vx = 100
        else:
            vx = -50
        
        vx = 0 #random.randint(0, 5)
        vy = 0 #random.randint(0, 5)
        #vx = 100*x / (math.sqrt((x*x) + (y*y)))
        #vy = 100*y / (math.sqrt((x*x) + (y*y)))
        mass = 100
        Q = 10
        body.append((color, (x, y), raio, (vx,vy), mass, Q))
    
def mechanics_force_acceleration():
    global body, N_body, Delta_t, K, G , g, altura_tela
    for i in range(N_body):
        mass1 = body[i][4]  # Massa da partícula i
        x = body[i][1][0]
        y = body[i][1][1]
        x2 = 0
        y2 = 0
        force_x = 0
        force_y = 0


        Q1 = body[i][5]  # Carga da partícula i
        for j in range(N_body):
            if (i != j):
                mass2 = body[j][4]  # Massa da partícula j
                Q2 = body[j][5]  # Carga da partícula j
                x2 = body[j][1][0]
                y2 = body[j][1][1]
                dpx = x2 - x
                dpy = y2 - y
                r = math.sqrt((dpx**2) + (dpy**2))
                forceE = K * Q1 * Q2 / (r**2)
                forceG = G * mass1 * mass2 / (r**2)

                if (r > (body[i][2]+body[j][2]*0.1)):
                    # Atualização das forças
                    force_x += (forceG-forceE) * dpx / r
                    force_y += (forceG-forceE) * dpy / r

        ax = force_x / mass1
        ay = g + (force_y / mass1)

        # Atualização da velocidade
        velocity_list = list(body[i][3])
        velocity_list[0] += ax * Delta_t
        velocity_list[1] += ay * Delta_t
        
        # Atualização da posição
        position_list = list(body[i][1])
        position_list[0] += velocity_list[0] * Delta_t
        position_list[1] += velocity_list[1] * Delta_t

        # Atualização da partícula
        body[i] = (*body[i][:3], tuple(velocity_list), *body[i][4:])
        body[i] = (body[i][0], tuple(position_list), *body[i][2:])
            
def mechanics_collision_screen():
    global body, N_body, altura_tela
    for i in range(N_body):
        raio = body[i][2]  # Acesse o raio da partícula específica
        x, y = body[i][1]  # Acesse as coordenadas x e y da posição da partícula específica
        vx, vy = body[i][3]  # Acesse as componentes x e y da velocidade da partícula específica

        if (x - raio) <= 0:  # Verifica se a partícula atingiu a borda esquerda da tela
            if vx < 0:  # Verifica se a partícula está se movendo para a esquerda
                vx = abs(vx)  # Inverte a componente x da velocidade para evitar que saia da tela

        if (x + raio) >= largura_tela:  # Verifica se a partícula atingiu a borda direita da tela
            if vx > 0:  # Verifica se a partícula está se movendo para a direita
                vx = -vx  # Inverte a componente x da velocidade para evitar que saia da tela

        if (y - raio) <= 0:  # Verifica se a partícula atingiu a borda superior da tela
            if vy <= 0:  # Verifica se a partícula está se movendo para cima
                vy = abs(vy)  # Inverte a componente y da velocidade para evitar que saia da tela

        if (y + raio) >= altura_tela:  # Verifica se a partícula atingiu a borda inferior da tela
            if vy >= 0:  # Verifica se a partícula está se movendo para baixo
                vy = -vy  # Inverte a componente y da velocidade para evitar que saia da tela

        # Atualiza a posição com base na velocidade e no intervalo de tempo
        x += vx * Delta_t
        y += vy * Delta_t

        # Atualiza as componentes x e y da velocidade na lista body[i]
        body[i] = (body[i][0], (x, y), body[i][2], (vx, vy), body[i][4], body[i][5])

def body_draw():
    global body, N_body
    for i in range(N_body):
        A, B, C, _, _, _ = body[i]
        pygame.draw.circle(tela, A, B, C)

def fields_draw():
    global body, N_body, Delta_t, K, G , g, altura_tela , altura_tela_tela
    for pixelx in range(largura_tela): 
        for pixely in range(altura_tela): 
            gf = 0
            for j in range(N_body):
                mass = body[j][4]  # Massa da partícula i
                x = body[j][1][0]
                y = body[j][1][1]
                dpx = pixelx - x
                dpy = pixely - y
                r = math.sqrt((dpx**2) + (dpy**2))
                gf += G * mass / (r**2)
                red = min(gf, 255)
                gleen = min(gf / 500, 255)
                blue = min(gf / 1000, 255)
                tela.set_at((pixelx, pixely), (int(red), int(gleen), int(blue)))



def center_of_body_exception(with_the_exception_of_body_i):
    global body
    wteob_mass = body[with_the_exception_of_body_i][4]  # Massa da partícula a ser ignorada
    massas = [m[4] for m in body]  # Lista de massas de todas as partículas
    valores_x = [x[1][0] for x in body if x != body[with_the_exception_of_body_i]] # Extrai os valores de x, excluindo a partícula específica
    valores_y = [y[1][1] for y in body if y != body[with_the_exception_of_body_i]] # Extrai os valores de y, excluindo a partícula específica
    CMx = sum(xi * wi for xi, wi in zip(valores_x, massas)) / (sum(massas) - wteob_mass) # Calcula o centro de massa em x (CMx)
    CMy = sum(yi * wi for yi, wi in zip(valores_y, massas)) / (sum(massas) - wteob_mass) # Calcula o centro de massa em y (CMy)
    return CMx, CMy

def center_of_body():
    global body  
    valores_x = [x[1][0] for x in body] # Extrai os valores de x
    valores_y = [y[1][1] for y in body] # Extrai os valores de y
    massas = [m[4] for m in body] # Extrai os valores de massa como pesos
    sum_p_x = sum(xi * wi for xi, wi in zip(valores_x, massas)) # Calcula a soma dos produtos de x pelos pesos 
    sum_p_y = sum(yi * wi for yi, wi in zip(valores_y, massas)) # Calcula a soma dos produtos de y pelos pesos
    CMx = sum_p_x / (sum(massas)) # Calcula o centro de massa em x (CMx)
    CMy = sum_p_y / (sum(massas)) # Calcula o centro de massa em y (CMy)
    return CMx, CMy

def menu_draw():
    ## Marcar a seleção e retorna o bloco selecionado
    global largura_tela
    posision = pygame.mouse.get_pos()
    selecion_x=posision[0]
    selecion_y=posision[1]
    if selecion_x > 2:
        return 'null'    # Define as coordenadas e dimensões do quadrado
    x = largura_tela+00
    y = 0
    l_quadrado = 50

    # Desenha o quadrado na tela principal
    pygame.draw.rect(tela, branco, (x, y, l_quadrado, l_quadrado))

    # Renderiza o texto "F"
    fonte = pygame.font.Font(None, 36)  # Escolha a fonte e o tamanho do texto
    texto = fonte.render("F", True, (0, 0, 0))  # Renderiza o texto
    tela.blit(texto, (x + 10, y + 10))  # Desenha o texto na posição desejada
    #if (pygame.mouse.get_focused() == True) :
        