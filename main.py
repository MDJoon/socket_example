import pygame
import socket
from _thread import *


HOST = input("ip:")
PORT = 9999

pygame.init()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
size = [1100, 700]
player_size = 50
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (player_size, player_size))

scd_player = pygame.image.load('scdplayer.png')
scd_player = pygame.transform.scale(scd_player, (player_size, player_size))
scd_players = {}

def checkPlayerLocation(x, y):
    left_up_side = [x, y]
    right_up_side = [x+player_size, y]
    left_down_side = [x, y+player_size]
    right_down_side = [x+player_size, y+player_size]

    if(left_up_side[0] < 0 or left_up_side[1] < 0): return False
    if(right_up_side[0] > size[0] or right_up_side[1] < 0): return False
    if(left_down_side[0] < 0 or left_down_side[1] > size[1]): return False
    if(right_down_side[0] > size[0] or right_down_side[1] > size[1]): return False
    return True

def recv_data(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            player_list = data.decode().split(",")
            scd_players[player_list[2]] = [player_list[0], player_list[1]]
                
        except:
            print('>> Disconnected')
            break
        

start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')

def run():
    global done
    player_x, player_y = 0, 0
    player_speed = 10

    left, right, up, down = False, False, False, False

    while not done:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                done = True

            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_UP:
                    up = True
                elif key == pygame.K_DOWN:
                    down = True
                elif key == pygame.K_LEFT:
                    left = True
                elif key == pygame.K_RIGHT:
                    right = True

            if event.type == pygame.KEYUP:
                key = event.key
                if key == pygame.K_UP:
                    up = False
                elif key == pygame.K_DOWN:
                    down = False
                elif key == pygame.K_LEFT:
                    left = False
                elif key == pygame.K_RIGHT:
                    right = False
        if(up):
            y = player_y - player_speed
            if(checkPlayerLocation(player_x, y)):
                player_y -= player_speed
        if(down):
            y = player_y + player_speed
            if(checkPlayerLocation(player_x, y)):
                player_y += player_speed
        if(left):
            x = player_x - player_speed
            if(checkPlayerLocation(x, player_y)):
                player_x -= player_speed
        if(right):
            x = player_x + player_speed
            if(checkPlayerLocation(x, player_y)):
                player_x += player_speed

        location = ','.join([str(player_x), str(player_y)])

        client_socket.send(location.encode())

        screen.blit(player, (player_x, player_y))
        for val in scd_players.values():
            screen.blit(scd_player, (int(val[0]), int(val[1])))
        scd_players.clear()
        pygame.display.update()
    client_socket.close()

run()
pygame.quit()
