import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 750
TEXT_HEIGHT = HEIGHT / 2
BOX_WIDTH = WIDTH / 2
BOX_HEIGHT = HEIGHT / 2
MAX_LENGTH = 85

window = pygame.display.set_mode((WIDTH, HEIGHT))

text_area = pygame.Rect(0, 0, WIDTH, TEXT_HEIGHT)
image_box = pygame.Rect(0, TEXT_HEIGHT, BOX_WIDTH, BOX_HEIGHT)
input_box = pygame.Rect(BOX_WIDTH, TEXT_HEIGHT, BOX_WIDTH, BOX_HEIGHT)

image = pygame.image.load('placeholder.png')
image = pygame.transform.scale(image, (BOX_WIDTH, BOX_HEIGHT))

font = pygame.font.Font(None, 32)

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

def load_text(filename):
    with open(filename, 'r') as f:
        return f.read()

def start_typing(text, delay=0.05):
    global game_text
    game_text = '' 
    pygame.time.set_timer(TYPING_EVENT, int(delay*1000), True)
    return iter(text)

text_iterator = start_typing(game_text)

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

def split_dialogue(text):
    return text.split('\n\n')

def start():
    global game_text, text_iterator, area, is_finished
    is_finished = False
    game_text = ''
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
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
            elif event.key == pygame.K_SPACE:
                instant_complete = True
            elif event.unicode:
                user_input += event.unicode

        elif event.type == TYPING_EVENT:
            options_text = '' 
            try:
                if instant_complete:
                    game_text += ''.join(text_iterator)
                    instant_complete = False
                else:
                    next_char = next(text_iterator)
                    game_text += next_char
                pygame.time.set_timer(TYPING_EVENT, int(delay*1000), True)
            except StopIteration:
                if parts:
                    if parts[0].startswith('Officer:'):
                        image = pygame.image.load('placeholder.png')
                    else:
                        image = pygame.image.load('test.png')
                    text_iterator = start_typing(parts.pop(0))
                else:
                    is_finished = True
                    if area == 'start':
                        options_text = 'Press enter to continue'
                    elif area == 'intro':
                        options_text = 'Choose to "talk" or "walk" away'
                    elif options_text_bolean == True:
                        options_text = 'Choose who to talk to. "jens", "daniil" or "hightower" '

    window.fill((255, 255, 255))

    pygame.draw.rect(window, (200, 200, 200), text_area)
    pygame.draw.rect(window, (0, 200, 200), image_box)
    pygame.draw.rect(window, (200, 200, 0), input_box)

    lines = split_text(game_text, MAX_LENGTH)
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (0, 0, 0))
        window.blit(text_surface, (10, 10 + i*font.get_height()))

    
    option_lines = split_text(options_text,MAX_LENGTH / 2 )
    for i, line in enumerate(option_lines):
        text_surface = font.render(line, True, (0, 0, 0))
        window.blit(text_surface, (WIDTH / 2, TEXT_HEIGHT + (i + 1)*font.get_height()))


    image = pygame.transform.scale(image, (BOX_WIDTH, BOX_HEIGHT))
    window.blit(image, (0, TEXT_HEIGHT))

    input_surface = font.render(user_input, True, (0, 0, 0))
    window.blit(input_surface, (WIDTH / 2, TEXT_HEIGHT ))


    

    pygame.display.update()
