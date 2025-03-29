from collections import defaultdict
from email.policy import default

import pygame as pg
import random

width = 700
height = 450
# size = [700, 450]
FPS = 60
background_color = (255, 255, 255)

x_direction = 0
y_direction = 0
player_speed = 2

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

# taxi
player_view = 'rear'
player_rect = images_dict['player'][player_view].get_rect()
player_rect.x = 300
player_rect.y = 300

#hotel
hotel_img = images_dict['hotel']
hotel_rect = hotel_img.get_rect()
hotel_positions = [
    (60, 30),
    (555, 30),
    (60, 250),
    (555, 250)
]
hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)

# parking
parking_img = images_dict['parking']
parking_rect = parking_img.get_rect()
parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height

# passendger
passenger_img = images_dict['passenger']
passenger_rect = passenger_img.get_rect()
# passenger_positions = [
#     (60, 30),
#     (555, 30),
#     (60, 250),
#     (555, 250)
# ]
passenger_rect.x, passenger_rect.y = random.choice(hotel_positions)
passenger_rect.y += hotel_rect.height
# while (passenger_rect.x, passenger_rect.y) == (hotel_rect.x, hotel_rect.y):
#     pass

def draw_message(text, color):
    font = pg.font.SysFont(None, 36)
    message = font.render(text, True,color)
    screen.blit(message, (350, 150))
    pg.display.flip()
    pg.time. delay(1500)

def is_crash():
    for x in range(player_rect.x, player_rect.topright[0], 1):
        for y in range(player_rect.y, player_rect.bottomleft[1], 1): #в range за змовчуванням є одиничка крок
            try:
                if screen.get_at((x, y)) == (220, 215, 177):
                    return True
            except IndexError:
                print("pixel index out of range")

    return False



pg.init()
screen = pg.display.set_mode([width,height])

timer = pg.time.Clock()

run = True
while run:
    timer.tick(FPS)
    # Обробка подій
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            # pg.quit()
            # exit()
        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_RIGHT:
        #         x_direction = 1
        #         player_view = 'right'
        #     elif event.key == pg.K_LEFT:
        #         x_direction = -1
        #         player_view = 'left'
        #     elif event.key == pg.K_UP:
        #         y_direction = -1
        #         player_view = 'rear'
        #     elif event.key == pg.K_DOWN:
        #         y_direction = 1
        #         player_view = 'front'

    keys_klava = pg.key.get_pressed()
    if keys_klava[pg.K_RIGHT]:
        x_direction = 1
        player_view = 'right'
    elif keys_klava[pg.K_LEFT]:
        x_direction = -1
        player_view = 'left'
    elif keys_klava[pg.K_UP]:
        y_direction = -1
        player_view = 'rear'
    elif keys_klava[pg.K_DOWN]:
        y_direction = 1
        player_view = 'front'


    # Поновлення
    player_rect.x += player_speed * x_direction
    player_rect.y += player_speed * y_direction
    x_direction = 0
    y_direction = 0

    if is_crash():
        print("IS CRASH")
        draw_message("IS CRASH!", pg.Color('red'))

        player_view = 'rear'
        player_rect.x = 300
        player_rect.y = 300

        hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)
        parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height
        passenger_rect.x, passenger_rect.y = random.choice(hotel_positions)
        passenger_rect.y += hotel_rect.height
        continue

    if player_rect.colliderect(passenger_rect):
        passenger_rect.x, passenger_rect.y = player_rect.x, player_rect.y

    if parking_rect.contains(player_rect):
        draw_message("You win!!", pg.Color('green'))
        player_view = 'rear'
        player_rect.x = 300
        player_rect.y = 300

        hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)
        parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height
        passenger_rect.x, passenger_rect.y = random.choice(hotel_positions)
        passenger_rect.y += hotel_rect.height
        continue

    # Відображеня
    screen.fill(background_color)
    screen.blit(images_dict['bg'], (0, 0))

    screen.blit(parking_img, parking_rect)
    screen.blit(images_dict['player'][player_view], player_rect)
    screen.blit(hotel_img, hotel_rect)
    screen.blit(passenger_img, passenger_rect)


    pg.display.flip()
pg.quit()
