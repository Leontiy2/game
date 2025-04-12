from collections import defaultdict

import pygame as pg
import random
import numpy as np


def draw_message(text, color):
    font = pg.font.SysFont(None, 36)
    message = font.render(text, True,color)
    screen.blit(message, (350, 150))
    pg.display.flip()
    pg.time. delay(1500)


def draw():
    if learned:
        pg.time.delay(10)
    # screen.fill(background_color)
    screen.blit(images_dict['bg'], (0, 0))

    screen.blit(parking_img, parking_rect)
    screen.blit(images_dict['player'][player_view], player_rect)
    screen.blit(hotel_img, hotel_rect)
    screen.blit(passenger_img, passenger_rect)


    pg.display.flip()


def apply_action(action):
    global player_view
    x_direction = 0
    y_direction = 0
    if action == 0:
        x_direction = 1
        player_view = 'right'
    elif action == 1:
        x_direction = -1
        player_view = 'left'
    elif action == 2:
        y_direction = -1
        player_view = 'rear'
    elif action == 3:
        y_direction = 1
        player_view = 'front'

    # player_rect.x += player_rect.width * x_direction
    # player_rect.y += player_rect.height * y_direction
    new_x = player_rect.x + player_rect.width * x_direction
    new_y = player_rect.y + player_rect.height * y_direction

    if 0 + player_rect.width < new_x < width - 2 * player_rect.width:
        player_rect.x = new_x
    if 0 + player_rect.height < new_y < height - 2 * player_rect.height:
        player_rect.y = new_y


def is_crash():
    for x in range(player_rect.x, player_rect.topright[0], 1):
        for y in range(player_rect.y, player_rect.bottomleft[1], 1): #в range за змовчуванням є одиничка крок
            try:
                if screen.get_at((x, y)) == (220, 215, 177):
                    return True
            except IndexError:
                print("pixel index out of range")

    return False


width = 700
height = 450
# size = [700, 450]
FPS = 60
background_color = (255, 255, 255)

images_dict = {
    'bg': pg.image.load('img/Background.png'),
    'player': {
        'rear': pg.image.load('img/cab_rear.png'),
        'left': pg.image.load('img/cab_left.png'),
        'front': pg.image.load('img/cab_front.png'),
        'right': pg.image.load('img/cab_right.png'),
    },
    # '': pg.image.load('img/'),
    'hole': pg.image.load('img/hole.png'),
    'hotel': pg.transform.scale(pg.image.load('img/hotel.png'), (80, 80)),
    'passenger': pg.image.load('img/passenger.png'),
    'taxi_background': pg.transform.scale(pg.image.load('img/taxi_background.png'), (80, 45)),
    'parking': pg.transform.scale(pg.image.load('img/parking.png'), (80, 45)),
}

def start_positions():
    global player_view
    player_view = 'rear'
    player_rect.x = 300
    player_rect.y = 300

    hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)

    parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height

    passenger_rect.x, passenger_rect.y = random.choice(hotel_positions)
    while (passenger_rect.x, passenger_rect.y) == (hotel_rect.x, hotel_rect.y):
        pass
    passenger_rect.y += hotel_rect.height


# taxi
player_view = 'rear'
player_rect = images_dict['player'][player_view].get_rect()
# player_rect.x = 300
# player_rect.y = 300

#hotel
hotel_img = images_dict['hotel']
hotel_rect = hotel_img.get_rect()
hotel_positions = [
    (60, 30),
    (555, 30),
    (60, 250),
    (555, 250)
]
# hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)

# parking
parking_img = images_dict['parking']
parking_rect = parking_img.get_rect()
# parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height

# passenger
passenger_img = images_dict['passenger']
passenger_rect = passenger_img.get_rect()

# passenger_rect.x, passenger_rect.y = random.choice(hotel_positions)
# while (passenger_rect.x, passenger_rect.y) == (hotel_rect.x, hotel_rect.y):
#     pass
# passenger_rect.y += hotel_rect.height

########################################################################
actions = [0, 1, 2, 3] # 0 - right; 1 - left; 2 - up; 3- down
Q_table = defaultdict(lambda: [0, 0, 0, 0]) # (300, 300) : [-2, -3, 5, 3]

learning_rate = 0.9
discount_factor = 0.9
epsilon = 0.1


def choose_action(state):
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        return np.argmax(Q_table[state])

def update_q(state, action, reward, next_state):
    best_next = max(Q_table[next_state])
    Q_table[state][action] += learning_rate * (reward + discount_factor * best_next - Q_table[state][action])


def make_step():
    current_state = (player_rect.x, player_rect.y)

    action = choose_action(current_state)

    apply_action(action)

    draw()

    reward = -1
    episode_end = False
    success = False

    if is_crash():
        reward = -100
        episode_end = True

    if parking_rect.contains(player_rect):
        print("Перемога!")
        # Перемога, то ж винагорода = 100
        reward = 100
        episode_end = True
        success = True

    next_state = (player_rect.x, player_rect.y)

    update_q(current_state, action, reward, next_state)

    return (episode_end, success)

pg.init()
screen = pg.display.set_mode([width,height])

# Основний цикл навчання
num_episodes = 300
max_step = 50
start_positions()
learned = False
draw()
for episode in range(num_episodes):
    player_view = 'rear'
    player_rect.x = 300
    player_rect.y = 300
    for step in range(max_step):
        (episode_end, success) = make_step()
        if episode_end:
            # draw_message(str(success), pg.Color('red'))
            print(success)
            break

learned = True
print (Q_table)
draw_message("Finished!", pg.Color('blue'))

########################################################################



timer = pg.time.Clock()

start_positions()

run = True
while run:
    timer.tick(FPS)
    # Обробка подій
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Поновлення

    current_state = (player_rect.x, player_rect.y)
    action = choose_action(current_state)
    apply_action(action)


    if is_crash():
        print("IS CRASH")
        draw_message("IS CRASH!", pg.Color('red'))
        start_positions()
        continue

    if player_rect.colliderect(passenger_rect):
        passenger_rect.x, passenger_rect.y = player_rect.x, player_rect.y

    if parking_rect.contains(player_rect):
        draw_message("You win!!", pg.Color('green'))
        start_positions()
        continue

    # Відображення

pg.quit()
