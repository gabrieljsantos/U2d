# Importing necessary libraries
import pygame  # For graphical interface
import random  # For generating random numbers
import math    # For mathematical operations
import time    # For time-related functions

# Pygame initialization
pygame.init()

# Main screen settings
screen_width = 200 # put 800 here
screen_height = 200 # put 600 here
menu_width = 0  # Currently unused
screen = pygame.display.set_mode((screen_width + menu_width, screen_height))
pygame.display.set_caption("U2d")
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)

fields = []

# Body settings
body = []
num_bodies = 3
num_seated_bodies = 200

# Constants
K = 40000  # Coulomb constant
G = 1000   # Gravitational constant
g = 0      # Gravity acceleration
delta_t = 0.005  # Time step for simulation # put 0.005 here


def body_generator():
    """
    Generates bodies with random properties.

    Generates num_bodies bodies with random colors, positions, velocities,
    mass, and charge within the defined constraints.
    """
    global body, num_bodies

    for i in range(num_bodies):
        # Random color
        color = (
            random.randint(20, 255),
            random.randint(20, 255),
            random.randint(20, 255)
        )

        # Initial position within screen bounds
        raio = 10
        x = random.randint(raio, screen_width - raio)
        y = random.randint(raio, screen_height - raio)

        # Initial velocity
        if x >= screen_width / 2:
            vy = 100
        else:
            vy = -50
        
        if y >= screen_height / 2:
            vx = 100
        else:
            vx = -50
        
        # Initial acceleration (set to zero for now)
        vx = 0
        vy = 0

        # Mass and charge
        mass = 100
        Q = 10

        # Append body properties to the body list
        body.append((color, (x, y), raio, (vx, vy), mass, Q))


def mechanics_force_acceleration():
    """
    Computes the force and acceleration acting on each body.

    Calculates the gravitational and electrical forces between each pair
    of bodies and updates their acceleration, velocity, and position
    accordingly.
    """
    global body, num_bodies, delta_t, K, G, g

    for i in range(num_bodies):
        # Extract body properties
        mass1 = body[i][4]  # Mass of body i
        x = body[i][1][0]
        y = body[i][1][1]
        force_x = 0
        force_y = 0

        Q1 = body[i][5]  # Charge of body i

        # Iterate through other bodies to compute forces
        for j in range(num_bodies):
            if i != j:
                # Extract properties of other body
                mass2 = body[j][4]  # Mass of body j
                Q2 = body[j][5]  # Charge of body j
                x2 = body[j][1][0]
                y2 = body[j][1][1]

                # Compute distance between bodies
                dpx = x2 - x
                dpy = y2 - y
                r = math.sqrt((dpx**2) + (dpy**2))

                # Compute electrical and gravitational forces
                forceE = K * Q1 * Q2 / (r**2)
                forceG = G * mass1 * mass2 / (r**2)

                # Update total forces
                force_x += (forceG - forceE) * dpx / r
                force_y += (forceG - forceE) * dpy / r

        # Compute acceleration
        ax = force_x / mass1
        ay = g + (force_y / mass1)

        # Update velocity
        velocity_list = list(body[i][3])
        velocity_list[0] += ax * delta_t
        velocity_list[1] += ay * delta_t
        
        # Update position
        position_list = list(body[i][1])
        position_list[0] += velocity_list[0] * delta_t
        position_list[1] += velocity_list[1] * delta_t

        # Update body properties
        body[i] = (*body[i][:3], tuple(velocity_list), *body[i][4:])
        body[i] = (body[i][0], tuple(position_list), *body[i][2:])


def mechanics_collision_screen():
    """
    Handles collision of bodies with the screen boundaries.

    Checks if a body has collided with the screen boundaries and adjusts
    its velocity accordingly to prevent it from moving out of the screen.
    """
    global body, num_bodies, screen_height, screen_height, delta_t

    for i in range(num_bodies):
        # Extract body properties
        raio = body[i][2]  # Radius of the specific body
        x, y = body[i][1]  # Coordinates of the specific body
        vx, vy = body[i][3]  # Velocity components of the specific body

        # Check for collision with left screen boundary
        if (x - raio) <= 0:
            if vx < 0:
                vx = abs(vx)

        # Check for collision with right screen boundary
        if (x + raio) >= screen_height:
            if vx > 0:
                vx = -vx

        # Check for collision with top screen boundary
        if (y - raio) <= 0:
            if vy <= 0:
                vy = abs(vy)

        # Check for collision with bottom screen boundary
        if (y + raio) >= screen_height:
            if vy >= 0:
                vy = -vy

        # Update position based on velocity and time interval
        x += vx * delta_t
        y += vy * delta_t

        # Update velocity components in the body list
        body[i] = (body[i][0], (x, y), body[i][2], (vx, vy), body[i][4], body[i][5])

def body_draw():
    """
    Draws bodies on the screen.

    Iterates through the body list and draws circles representing each body
    onto the screen using Pygame's draw.circle function.
    """
    global body, num_bodies, screen

    for i in range(num_bodies):
        color, position, radius, _, _, _ = body[i]
        pygame.draw.circle(screen, color, position, radius)


def fields_draw():
    """
    Draws gravitational fields on the screen.

    Iterates through each pixel on the screen and calculates the gravitational
    field strength caused by the bodies at that point. Then, assigns colors
    based on the field strength and sets the corresponding pixel color on the screen.
    """
    global body, num_bodies, delta_t, K, G, g, screen_height

    for pixelx in range(screen_height):
        new_var = screen_height
        for pixely in range(new_var):
            gf = 0  # Gravitational field strength at the pixel

            # Iterate through each body to calculate the gravitational field
            for j in range(num_bodies):
                mass = body[j][4]  # Mass of the body j
                x = body[j][1][0]  # X-coordinate of the body j
                y = body[j][1][1]  # Y-coordinate of the body j

                # Calculate distance between pixel and body j
                dpx = pixelx - x
                dpy = pixely - y
                r = math.sqrt((dpx**2) + (dpy**2))

                # Calculate gravitational field strength contribution of body j
                gf += G * mass / (r**2)

            # Convert gravitational field strength to color values
            red = min(gf, 255)
            green = min(gf / 500, 255)
            blue = min(gf / 1000, 255)

            # Set the pixel color on the screen based on the gravitational field
            screen.set_at((pixelx, pixely), (int(red), int(green), int(blue)))
def center_of_body_exception(with_the_exception_of_body_i):
    """
    Calculates the center of mass excluding a specific body.

    Args:
        with_the_exception_of_body_i (int): Index of the body to be excluded.

    Returns:
        Tuple[float, float]: Coordinates of the center of mass (CMx, CMy) excluding the specified body.
    """
    global body

    # Mass of the body to be ignored
    wteob_mass = body[with_the_exception_of_body_i][4]

    # List of masses of all bodies excluding the specified body
    massas = [m[4] for m in body]

    # Extract x and y values, excluding the specified body
    valores_x = [x[1][0] for x in body if x != body[with_the_exception_of_body_i]]
    valores_y = [y[1][1] for y in body if y != body[with_the_exception_of_body_i]]

    # Calculate the center of mass in x and y directions (CMx, CMy)
    CMx = sum(xi * wi for xi, wi in zip(valores_x, massas)) / (sum(massas) - wteob_mass)
    CMy = sum(yi * wi for yi, wi in zip(valores_y, massas)) / (sum(massas) - wteob_mass)

    return CMx, CMy


def center_of_body():
    """
    Calculates the center of mass of all bodies.

    Returns:
        Tuple[float, float]: Coordinates of the center of mass (CMx, CMy).
    """
    global body  

    # Extract x and y values
    values_x = [x[1][0] for x in body]
    values_y = [y[1][1] for y in body]

    # Extract mass values as weights
    massas = [m[4] for m in body]

    # Calculate the sum of products of x and y by weights
    sum_p_x = sum(xi * wi for xi, wi in zip(values_x, massas))
    sum_p_y = sum(yi * wi for yi, wi in zip(values_y, massas))

    # Calculate the center of mass in x and y directions (CMx, CMy)
    CMx = sum_p_x / (sum(massas))
    CMy = sum_p_y / (sum(massas))

    return CMx, CMy
def menu_draw():
    """
    Draws the menu square and renders the text "F".

    Returns:
        str: 'null' if the mouse position is not within the menu square, otherwise None.
    """
    global screen_width

    # Get mouse position
    posision = pygame.mouse.get_pos()
    selecion_x = posision[0]
    selecion_y = posision[1]

    # Check if mouse position is within the menu square
    if selecion_x > 2:
        return 'null'

    # Define coordinates and dimensions of the square
    x = screen_height + 0
    y = 0
    l_square = 50

    # Draw the square on the main screen
    pygame.draw.rect(screen, white, (x, y, l_square, l_square))

    # Render the text "F"
    fonte = pygame.font.Font(None, 36)  # Choose font and text size
    texto = fonte.render("F", True, (0, 0, 0))  # Render the text
    screen.blit(texto, (x + 10, y + 10))  # Draw the text at the desired position
    # if pygame.mouse.get_focused() == True:
