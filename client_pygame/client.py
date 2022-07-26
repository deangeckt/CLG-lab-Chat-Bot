import pygame
from chat import Chat
from bot import Bot, q
from utils import user_obj_color_stand, user_obj_color_press

pygame.init()
pygame.display.set_caption('Map task')
print(pygame.font.get_fonts())

image = pygame.image.load(r'map1.png')
image_width, image_height = image.get_size()
image_scale = 0.8  # TODO param from outside

image_width *= image_scale
image_height *= image_scale
image = pygame.transform.scale(image, (image_width, image_height))

chat_width = 400
screen_width = image_width + chat_width
screen_height = image_height
screen = pygame.display.set_mode([screen_width, screen_height])

chat = Chat(q, chat_width, image_height, image_width)
bot = Bot(chat)

p1 = 1104  # TODO start pos per image or map
p2 = 102
step = 2

user_obj_color = user_obj_color_stand
user_object_surface = screen

running = True
while running:

    screen.blit(image, (0, 0))
    user_ojb = pygame.draw.circle(user_object_surface, user_obj_color, (p1, p2), 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0] and event.type == pygame.MOUSEMOTION:
            if user_ojb.collidepoint(event.pos):
                mouse_cords = pygame.mouse.get_pos()
                p1, p2 = mouse_cords
                user_obj_color = user_obj_color_press
                user_object_surface = image

        if event.type == pygame.MOUSEBUTTONUP and user_obj_color == user_obj_color_press:
            user_obj_color = user_obj_color_stand
            user_object_surface = screen

        chat.on_event(event)

    chat.on_frame(screen)
    # print(p1, p2)
    pygame.display.flip()

pygame.quit()
