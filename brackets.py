import pygame
import os
from os import listdir
from random import randint
from random import shuffle
import tkinter
from tkinter import ttk
from tkinter import StringVar

config_list = []

directory_list = []
for element in os.listdir():
    if os.path.isdir(os.path.join(element)):
        if element != "__pycache__":
            directory_list.append(element)

def donnees():
    global config_list
    config_list = []
    directory = directory_combobox.get()
    mode = photos_combobox.get()
    fps = fps_spinbox.get()
    width = width_spinbox.get()
    height = height_spinbox.get()
    config_list.append(directory)
    config_list.append(mode)
    config_list.append(fps)
    config_list.append(width)
    config_list.append(height)
    fullscreen = fullscreen_var.get()
    config_list.append(fullscreen)
    config.destroy()
    

config = tkinter.Tk()
config.title("Settings")
try:
    config.iconbitmap("icon.ico")
except:
    pass

frame = tkinter.Frame(config)
frame.pack()

directory_frame = tkinter.LabelFrame(frame, text = "Game settings")
directory_frame.grid(row = 0, column = 0, padx = 20, pady = 20)

directory_label = tkinter.Label(directory_frame, text="Directory : ")
directory_label.grid(row = 0, column = 0)
photos_label = tkinter.Label(directory_frame, text = "Number of images : ")
photos_label.grid(row = 1, column = 0)
directory_combobox = ttk.Combobox(directory_frame, values = directory_list, state = "readonly")
directory_combobox.grid(row = 0, column = 1)
photos_combobox = ttk.Combobox(directory_frame, values = [2**i for i in range(10)], state = "readonly")
photos_combobox.grid(row = 1, column = 1)

for widget in directory_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 10)

graphic_frame = tkinter.LabelFrame(frame, text = "Graphics settings")
graphic_frame.grid(row = 1, column = 0, sticky = "news", padx = 20, pady = 10)

fps_var = StringVar(config)
fps_label = tkinter.Label(graphic_frame, text = "FPS : ")
fps_spinbox = tkinter.Spinbox(graphic_frame, from_ = 1, to = 540, textvariable = fps_var)
fps_label.grid(row = 0, column = 0)
fps_spinbox.grid(row = 0, column = 1)
fps_spinbox.grid_configure(padx = 10, pady = 10)
fps_var.set("60")

width_label = tkinter.Label(graphic_frame, text = "Window width : ")
width_label.grid(row = 1, column = 0)
height_label = tkinter.Label(graphic_frame, text = "Window height : ")
height_label.grid(row = 2, column = 0)

width_var = StringVar(config)
height_var = StringVar(config)
width_spinbox = tkinter.Spinbox(graphic_frame, from_ = 100, to = 7680, textvariable = width_var)
height_spinbox = tkinter.Spinbox(graphic_frame, from_ = 100, to = 4320, textvariable = height_var)
width_spinbox.grid(row = 1, column = 1)
height_spinbox.grid(row = 2, column = 1)
width_var.set("1600")
height_var.set("900")

fullscreen_var = StringVar(value = False)
fullscreen_check = tkinter.Checkbutton(graphic_frame, text = "Fullscreen ", variable = fullscreen_var, onvalue = 1, offvalue = 0)
fullscreen_check.grid(row = 3, column = 0)
fullscreen_check.grid_configure(padx = 10, pady = 10)



button = tkinter.Button(frame, text = "Start", command = donnees)
button.grid(row = 3, column = 0, sticky = "news", padx = 20, pady = 10)

config.resizable(False, False)
config.mainloop()

pygame.init()

if config_list == []:
    width = 1600
    height = 900
    fps = 60
    directory = None
    mode = None
    dimensions = (width, height)
else:
    width = int(config_list[3])
    height = int(config_list[4])
    if config_list[5] == "1":
        dimensions = (0, 0)
    else:
        dimensions = (width, height)
    fps = int(config_list[2])
    if config_list[0] == '':
        directory = None
    else:
        directory = config_list[0]
    if config_list[1] == '':
        mode = None
    else:
        mode = int(config_list[1])
timer = pygame.time.Clock()
window = pygame.display.set_mode(dimensions, pygame.RESIZABLE, pygame.FULLSCREEN)
pygame.display.set_caption("Brackets")
try:
    pygame_icon = pygame.image.load("game.ico")
    pygame.display.set_icon(pygame_icon)
except:
    pass



def init_images(directory):
    d_images = {}
    for image_name in os.listdir(directory):
        d_images[image_name] = pygame.image.load(directory + "/" + image_name).convert_alpha()
    return d_images

def init_brackets(directory, mode):
    game = []
    images = []
    p = 1
    for image_name in os.listdir(directory):
        images.append(image_name)
    n = len(images)
    while len(images) < mode:
        images.append(None)
    while len(game) != mode:
        if (p % 2 == 0) and (None in images):
            game.append(None)
            images.pop(-1)
        else:
            index = randint(0, n - 1)
            game.append(images.pop(index))
            n -= 1
        p += 1
    return game

def image_size(image):
    image_height = image.get_height()
    image_width = image.get_width()
    ratio = image_width/image_height
    new_width = width//2
    new_height = new_width/ratio
    if new_height > height:
        new_height = height
        new_width = new_height*ratio 
    return (new_width, new_height)

def image_pos(image, size):
    if size[0] == width//2:
        posX = 0
        posY = height//2 - size[1]//2
    else:
        posX = width//4 - size[0]//2
        posY = 0
    return (posX, posY)

def display_image(name, row):
    if name != None:
        global d_images
        image = d_images[name]
        (image_width, image_height) = image_size(image)
        image = pygame.transform.scale(image, (image_width, image_height))
        (posX, posY) = image_pos(image, (image_width, image_height))
        posX = posX + width//2 * row
        window.blit(image, (posX,posY))

def display_text(text, row, backround_color):
    if text != None:
        while text[-1] != ".":
            text = text[:-1]
        text = text[:-1]  
        global width
        global height
        if backround_color == "black":
            rect_color = (20,20,20)
            couleur_text = (255, 255, 255)
        elif backround_color == "white":
            rect_color = (200, 200, 200)
            couleur_text = (40, 40, 40)
        font_text = pygame.font.SysFont("Franklin Gothic Medium", height//24)
        img = font_text.render(text, True, couleur_text)
        (width_text, height_text) = font_text.size(text)
        posX_rectangle = width//4 - width_text//2 + width//2 * row - height_text//10
        posY_rectangle = height - height_text - height_text//10
        pygame.draw.rect(window, rect_color, (posX_rectangle, posY_rectangle, width_text + height_text//5, height_text + height_text//5))
        window.blit(img, (posX_rectangle + height_text//10, posY_rectangle))

def display_round(round_, stage):
    global width
    global height
    font_text = pygame.font.SysFont("Franklin Gothic Medium", height//25)
    if round_ == stage == 0:
        text = "Winner"
    else:
        text = str(round_ + 1) + "/" + str(stage)
    img = font_text.render(text, True, (255, 255, 255))
    (width_text, height_text) = font_text.size(text)
    posX_rectangle = width//2 - width_text//2 - height_text//10
    posY_rectangle = 0
    pygame.draw.rect(window, (20, 20, 20), (posX_rectangle, posY_rectangle, width_text + height_text//5, height_text))
    window.blit(img, (posX_rectangle + height_text//10, posY_rectangle))

main = True
if directory == None or mode == None:
    main = False
else:
    click_count = 0
    try:
        game = init_brackets(directory, mode)
        d_images = init_images(directory)
    except:
        main = False
    game2 = []
    i = 0
while main:
    width, height = window.get_size()
    window.fill("black")
    timer.tick(fps)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main = False

    if len(game) == 1:
        display_image(game[0], 0.5)
        display_text(game[0], 0.5, "black")
        display_round(0, 0)
    else:
        display_image(game[2 * i], 0)
        display_image(game[2 * i + 1], 1)
        if mouse_pos[0] < width//2:
            display_text(game[2 * i], 0, "white")
        else:
            display_text(game[2 * i], 0, "black")
        if mouse_pos[0] > width//2 :
            display_text(game[2 * i + 1], 1, "white")
        else:
            display_text(game[2 * i + 1], 1, "black")
        display_round(i, len(game)//2)

    click = pygame.mouse.get_pressed()[0]
    if click:
        click_count += 1
    if click == False and click_count != 0:
        mouse_pos = pygame.mouse.get_pos()
        click_count = 0
        if len(game) == 1:
            main = False
        elif mouse_pos[0] < width//2:
            game2.append(game[2 * i])
        else:
            game2.append(game[2 * i + 1])
        i += 1
        if i >= len(game)/2:
            game, game2 = game2, []
            i = 0
            shuffle(game)
    pygame.display.update()

pygame.quit()

