import pygame
import math
from .Space import *
import torch

pygame.init()
pygame.mixer.init()
pygame.event.pump()
pygame.mixer_music.load("Assets/Whoosh Sound Effect.mp3")
scene1 = pygame.Surface((1920*4, 1080*4))
screen1 = pygame.display.set_mode((1920, 1080))
running = False
clock =  pygame.time.Clock()
draw_options1 = pymunk.pygame_util.DrawOptions(scene1)
bg = "purple"
scene_bg = "blue"
speed = 10
keys = {pygame.K_a: [+speed, 0], pygame.K_d: [-speed, 0], pygame.K_w: [0, +speed], pygame.K_s: [0, -speed], pygame.K_q: [(math.sqrt(2)/2)*speed, (math.sqrt(2)/2)*speed], pygame.K_e: [(math.sqrt(2)/2)*(-speed), (math.sqrt(2)/2)*speed], pygame.K_y: [(math.sqrt(2)/2)*speed, (math.sqrt(2)/2)*(-speed)], pygame.K_c: [(math.sqrt(2)/2)*(-speed), (math.sqrt(2)/2)*(-speed)]}

def camera_manager(scene, camera_position):
    for i, x in keys.items():
        if pygame.key.get_pressed()[i] == True:
            camera_position[0] += x[0]
            camera_position[1] += x[1]
    if pygame.key.get_pressed()[pygame.K_PLUS] == True:
        return pygame.transform.scale(scene, (scene.get_size()[0] * 5, scene.get_size()[1] * 5))
    else:
        return scene

def motor_manager(draw_options, scene, screen, camera_position, self_control, i, speed = None):
    position = body3.position[0]
    angle = body2.angle
    if speed != None:
        motor_rate = motor(speed/10, space, body3, body1, i)
    elif self_control:
        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            motor_rate = motor(speed  * 1, space, body3, body1, i)
        elif pygame.key.get_pressed()[pygame.K_LEFT] == True:
            motor_rate = motor(speed * -1, space, body3, body1, i)
        else:
            motor_rate = motor(speed*0, space, body3, body1, i)

    if angle <= 0:
        reward = angle * 10 + position
    elif angle > 0:
        reward = angle * -10 + position
    reward += 0.825



    done = True


    # New state representation (for the neural net)
    next_state = torch.tensor([angle, 0.00], dtype=torch.float)

    scene.fill(scene_bg)
    screen.fill(bg)
    space.debug_draw(draw_options)
    camera_manager(scene, camera_position)
    screen.blit(camera_manager(scene, camera_position), (camera_position[0], camera_position[1]))
    pygame.display.flip()
    clock.tick(60)
    space.step(1/60)
    return reward, space


def control_self(camera_position, i):

    pygame.init()

    scene1 = pygame.Surface((1920*4, 1080*4))
    screen1 = pygame.display.set_mode((1920, 1080))
    draw_options1 = pymunk.pygame_util.DrawOptions(scene1)
    running = True

    while running == True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        motor_manager(draw_options1, scene1, screen1, camera_position, i, self_control = True)

    pygame.quit()

