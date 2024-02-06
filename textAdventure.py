

# importer sys og pygame
import pygame
import sys

# initialiser pygame
pygame.init()


# declarer noen konstanter
WIDTH, HEIGHT = 1000, 750
TEXT_HEIGHT = HEIGHT / 2
BOX_WIDTH = WIDTH / 2
BOX_HEIGHT = HEIGHT / 2
MAX_LENGTH = 85

# window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# lager de 3 områdene jeg har på skjermen
text_area = pygame.Rect(0, 0, WIDTH, TEXT_HEIGHT)
image_box = pygame.Rect(0, TEXT_HEIGHT, BOX_WIDTH, BOX_HEIGHT)
input_box = pygame.Rect(BOX_WIDTH, TEXT_HEIGHT, BOX_WIDTH, BOX_HEIGHT)


# putter et bilde i botom right corner
image = pygame.image.load('placeholder.png')
image = pygame.transform.scale(image, (BOX_WIDTH, BOX_HEIGHT))

# font size
font = pygame.font.Font(None, 32)

# noen variabler og boleans
user_input = ''
game_text = 'Press enter to start!'
area = 'start'
parts = []
is_finished = False
options_text = ''
options_text_bolean = False
lost = False
TYPING_EVENT = pygame.USEREVENT + 1
delay = 0.05
instant_complete = False


# function for å åpne en fil
def load_text(filename):
    with open(filename, 'r') as f:
        return f.read()

# function for å skape typing effekten
def start_typing(text, delay=0.05):
    global game_text
    game_text = '' 
    pygame.time.set_timer(TYPING_EVENT, int(delay*1000), True)
    return iter(text)

text_iterator = start_typing(game_text)

# function for å gjøre sp teksten ikke går ut av vinduet.
# den bruker konstanten max lenght også sjekker den om ordet passer inn i den lengden 
# og går til ny linje før hvis den må så den ikke bytter midt i et ord
def split_text(text, max_length):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        if len(current_line + word) <= max_length:
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)
    return lines

# splitter teksten til ny linje
def split_dialogue(text):
    return text.split('\n\n')

# her kommer functions til forksjellige areas i spillet mitt.
# hadde jeg hatt litt mer tid så hadde jeg nok puttet dette inn i en class også brukt noen __init__ functions. 
# jeg bruker også ikke alle av disse functionsene men det er padding på hvor lang koden min ser ut /S
# disse funskjsjonene er for det meste det samme, bare forskjellige verdier

def start():
    #declarer global variables
    global game_text, text_iterator, area, is_finished
    
    # reseter to variabler
    is_finished = False
    game_text = ''

    #gir nye verdier til variabler
    text = load_text('start.txt')
    text_iterator = start_typing(text)
    area = 'intro'

def intro():
    global game_text, text_iterator, area, is_finished
    is_finished = False
    game_text = ''
    text = load_text('dialouge.txt')
    text_iterator = start_typing(text)
    area = 'oransj'

def choice():
    global game_text, text_iterator, area, is_finished
    is_finished = False
    game_text = ''
    text = "Please choose between Jens, Daniil, or Hightower."
    text_iterator = start_typing(text)
    area = 'choice'

def jens():
    global game_text, text_iterator, area, is_finished
    is_finished = False
    game_text = ''
    text = load_text('choices.txt')
    text_iterator = start_typing(text)
    area = 'jens'


# game loop 
while True:
    # event handler
    for event in pygame.event.get():
        # viktig å ha med så man kan quitte
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # sjekker hvis det er noe input fra tastaturet
        elif event.type == pygame.KEYDOWN:
            # sjekker hvis det var enter som ble presset
            if event.key == pygame.K_RETURN:
                # if else løkke som sjekker for vairablen area
                if area == 'start':
                    game_text = load_text('start.txt')
                    parts = split_dialogue(game_text)
                    text_iterator = start_typing(parts.pop(0))
                    area = 'intro'
                elif area == 'intro':
                    if user_input.lower() == 'talk':
                        game_text = load_text('dialouge.txt')
                        parts = split_dialogue(game_text)
                        text_iterator = start_typing(parts.pop(0))
                        options_text_bolean = True
                        area = 'intro2'
                    elif user_input.lower() == 'walk':
                        game_text = 'you choose to walk away. you was never seen again'
                        parts = split_dialogue(game_text)
                        text_iterator = start_typing(parts.pop(0))
                        lost = True
                elif area == 'intro2':
                    game_text = load_text('choices.txt')
                    parts = split_dialogue(game_text)
                    text_iterator = start_typing(parts.pop(0))
                    if user_input.lower() in ['jens', 'daniil', 'hightower']:
                        if user_input.lower() == 'jens' and is_finished:  # HVORFOR BLIR DENNE FUCKING TINGEN RUNNA TO GANGER
                            area = 'jens'
                        else:
                            user_input = ''
                elif area == 'jens':
                    game_text = load_text('valg.JENS.txt')
                    parts = split_dialogue(game_text)
                    text_iterator = start_typing(parts.pop(0))
                elif area == 'oransj':
                    pass
                
                user_input = ''
            # sjekker for hvis inputen var space
            # fordi da auto completer den setningen
            elif event.key == pygame.K_SPACE:
                instant_complete = True

            # for alle andre inputs som er unicdoe så adder den det til user input som blir blitta på skjermen.
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.unicode:
                user_input += event.unicode

            # This block handles the typing effect for the game text
        elif event.type == TYPING_EVENT:
            options_text = ''  # Reset the options text
            try:
                if instant_complete:  # If the user pressed space, complete the typing effect instantly
                    game_text += ''.join(text_iterator)
                    instant_complete = False
                else:  # Otherwise, type the next character
                    next_char = next(text_iterator)
                    game_text += next_char
                pygame.time.set_timer(TYPING_EVENT, int(delay*1000), True)  # Set the timer for the next character
            except StopIteration:  # If there are no more characters to type
                if parts:  # If there are more parts of the dialogue to type
                    if parts[0].startswith('Officer:'):  # If the next part is from the officer
                        image = pygame.image.load('placeholder.png')  # Load the officer's image
                    else:
                        image = pygame.image.load('test.png')  # Otherwise, load the other image
                    text_iterator = start_typing(parts.pop(0))  # Start typing the next part
                else:  # If there are no more parts of the dialogue to type
                    is_finished = True  # Indicate that the typing effect is finished
                    # Set the options text based on the current area
                    if area == 'start':
                        options_text = 'Press enter to continue'
                    elif area == 'intro':
                        options_text = 'Choose to "talk" or "walk" away'
                    elif options_text_bolean == True:
                        options_text = 'Choose who to talk to. "jens", "daniil" or "hightower" '

        # This block handles the rendering of the game window
        window.fill((255, 255, 255))  # Fill the window with white

        # Draw the text area, image box, and input box
        pygame.draw.rect(window, (200, 200, 200), text_area)
        pygame.draw.rect(window, (0, 200, 200), image_box)
        pygame.draw.rect(window, (200, 200, 0), input_box)

        # Render the game text
        lines = split_text(game_text, MAX_LENGTH)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (0, 0, 0))
            window.blit(text_surface, (10, 10 + i*font.get_height()))

        # Render the options text
        option_lines = split_text(options_text,MAX_LENGTH / 2 )
        for i, line in enumerate(option_lines):
            text_surface = font.render(line, True, (0, 0, 0))
            window.blit(text_surface, (WIDTH / 2, TEXT_HEIGHT + (i + 1)*font.get_height()))

        # Render the image
        image = pygame.transform.scale(image, (BOX_WIDTH, BOX_HEIGHT))
        window.blit(image, (0, TEXT_HEIGHT))

        # Render the user input
        input_surface = font.render(user_input, True, (0, 0, 0))
        window.blit(input_surface, (WIDTH / 2, TEXT_HEIGHT ))

        # Update the display
        pygame.display.update()
