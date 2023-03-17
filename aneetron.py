import random
import time
import numpy as np
import pyautogui
import cv2
import csv
import pyperclip
import sys
import os
import glob

min_duration = 0.1  # in seconds
max_duration = 0.23  # in seconds
duration = random.uniform(min_duration, max_duration)
loaded_items = {}
image_data = {}
file_names_csv = []
file_names_png = []
csv_list = []

def read_csv_file(filename):
    rows = []
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            rows.append(row)
    return rows

def delay(min_time=2, max_time=5):
    min_time = int(min_time)
    max_time = int(max_time)
    time.sleep(random.randint(min_time, max_time))

def simulate_scroll(pixels):
    pixels = int(pixels)
    pyautogui.scroll(pixels)

def find_image(pattern_img, threshold=0.8):
    screen_img = pyautogui.screenshot()
    screen_img = screen_img.crop((0, 72, screen_img.width, screen_img.height))
    screen_img = cv2.cvtColor(np.array(screen_img), cv2.COLOR_RGB2GRAY)
    result = cv2.matchTemplate(screen_img, pattern_img, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    if len(loc[0]) > 0:
        index = random.randint(0, len(loc[0])-1)
        pyautogui.moveTo(loc[1][index] + 20, loc[0][index] + 20 + 72)
        pyautogui.moveTo(loc[1][index] + 12, loc[0][index] + 12 + 72)
        pyautogui.moveTo(loc[1][index] + 20, loc[0][index] + 20 + 72)
        delay(0, 3)
        return True
    return False


def load_csv_files(file_names, loaded_items, folder_path):
    print('load_csv_files')
    for name in file_names:
        csv_values = read_csv_file(folder_path + name)
        csv_name = os.path.splitext(name)[0]
        # checking if a dict is None and exists with a specific key
        if loaded_items and name in loaded_items:
            # Perform your desired operation after ensuring that the object is valid, and key exists
            if loaded_items[csv_name]:
                loaded_items[csv_name] += csv_values
        else:
            loaded_items[csv_name] = csv_values
    return loaded_items


def load_images(file_names, folder_path):
    print('load_images')
    image_data = {}  # creating empty dict to hold images
    for name in file_names:
        img_name = os.path.splitext(name)[0]
        print(img_name)
        image = cv2.imread(folder_path + name, cv2.IMREAD_GRAYSCALE)
        image_data[img_name] = image
    return image_data


def get_file_names(folder_path, extension):
    print('get_file_names')
    file_names = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith("." + extension):
            file_names.append(file_name)
    print(file_names)
    return file_names


def get_keys(obj):
    keys = obj.keys()
    return keys


def findImage(name):
    if find_image(images_list.get(name)):
        delay(0, 3)
        return True
    return False

def click():
    print('click')
    pyautogui.click(duration=duration)

def right_click(duration=0.0):
    print('r_click')
    pyautogui.mouseDown(button='right')
    pyautogui.mouseUp(button='right', duration=duration)

def generate_tweet(*args):
    tweet = args[0]
    hashtags = args[1:]
    hashtag_string = " ".join([f"#{ht}" for ht in hashtags])
    return f"{tweet} {hashtag_string}"

def random_choice_from_csv(csv_list: dict, name: str) -> str:
    return random.choice(random.choice(csv_list.get(name)))

def pick_text(*csv_file_names):
    message = ""
    for name in csv_file_names:
        message += random_choice_from_csv(csv_list, name)
    pyperclip.copy(message)

def exact_choice_from_csv(name: str, row, col) -> str:
    return csv_list.get(name)[row][col]

def paste_text():
    pyautogui.hotkey('ctrl', 'v')

def copy_text():
    pyautogui.hotkey('ctrl', 'c')

def cut_text():
    pyautogui.hotkey('ctrl', 'x')

def refresh():
    pyautogui.hotkey('f5')

def key_press(*args):
    pyautogui.hotkey(*args)

file_names_png = get_file_names("./images/", "png")
images_list = load_images(file_names_png, './images/')
print('file_names_png', images_list) 

file_names_csv = get_file_names("./csv/", "csv")
print('file_names_csv', file_names_csv) 
csv_list = load_csv_files(file_names_csv, loaded_items,  './csv/')
print('csv_list', csv_list) 
imagesKeys = get_keys(images_list)
csvKeys = get_keys(csv_list)

commands = {
    'click': click,
    'rclick': right_click,
    'delay': delay,
    'findImage': findImage,
    'scroll': simulate_scroll,
    'pickText': pick_text,
    'paste': paste_text,
    'copy': copy_text,
    'cut': cut_text,
    'refresh': refresh,
    'keyPress': key_press,
}

while True:
    data = read_csv_file('./csv/commands.csv')
    for row in data:
        action = commands.get(row[0])
        if action:
            if len(row) > 1:
                print(row)
                action(*row[1:])
            else:
                print(row)
                action()