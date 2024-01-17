import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1000, 750
TEXT_HEIGHT = HEIGHT / 2
IMAGE_BOX_HEIGHT = HEIGHT / 4
INPUT_BOX_HEIGHT = HEIGHT / 4

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Create the areas
# Create the areas
text_area = pygame.Rect(0, 0, WIDTH, TEXT_HEIGHT)
image_box = pygame.Rect(0, TEXT_HEIGHT, WIDTH, IMAGE_BOX_HEIGHT)
input_box = pygame.Rect(0, TEXT_HEIGHT + IMAGE_BOX_HEIGHT, WIDTH, INPUT_BOX_HEIGHT)

"""
text_area = pygame.Rect(0, 0, WIDTH, TEXT_HEIGHT)
image_box = pygame.Rect(0, TEXT_HEIGHT, IMAGE_BOX_HEIGHT, IMAGE_BOX_HEIGHT)
input_box = pygame.Rect(IMAGE_BOX_HEIGHT, TEXT_HEIGHT, INPUT_BOX_HEIGHT, INPUT_BOX_HEIGHT)
"""

# Load an image
image = pygame.image.load('placeholder.png')
image = pygame.transform.scale(image, (IMAGE_BOX_HEIGHT, IMAGE_BOX_HEIGHT))  # Resize the image

# Create a font object
font = pygame.font.Font(None, 32)

# Create a variable to store the user's input
user_input = ''

# Create a variable to store the game's text
game_text = 'You wake up in a house, what do you do? Scream or whisper?'

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_input.lower() == 'scream':
                    game_text = 'You scream. The house seems to shake.'
                    image = pygame.image.load('test.png')
                    image = pygame.transform.scale(image, (IMAGE_BOX_HEIGHT, IMAGE_BOX_HEIGHT))  # Resize the image
                elif user_input.lower() == 'whisper':
                    game_text = 'You whisper. The house is silent.'
                    image = pygame.image.load('placeholder.png')
                    image = pygame.transform.scale(image, (IMAGE_BOX_HEIGHT, IMAGE_BOX_HEIGHT))  # Resize the image
                user_input = ''
            else:
                user_input += event.unicode

    # Fill everything with white
    window.fill((255, 255, 255))

    # Draw the areas
    pygame.draw.rect(window, (200, 200, 200), text_area)  # Grey
    pygame.draw.rect(window, (0, 200, 200), image_box)  # Grey
    pygame.draw.rect(window, (200, 200, 0), input_box)  # Grey

    # Render the game's text
    text_surface = font.render(game_text, True, (0, 0, 0))
    window.blit(text_surface, (10, 10))

    # Render the image
    window.blit(image, (0, TEXT_HEIGHT))

    # Render the user's input
    input_surface = font.render(user_input, True, (0, 0, 0))
    window.blit(input_surface, (WIDTH / 2, TEXT_HEIGHT ))

    # Update the display
    pygame.display.update()
