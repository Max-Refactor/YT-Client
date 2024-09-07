from rich.console import Console
from colorama import Fore, init
from rich.panel import Panel

from io import BytesIO
from PIL import Image
import keyboard

import requests, msvcrt, pyfzf, art, sys, os

fzf = pyfzf.FzfPrompt()
console = Console()

def print_massage(message, title, subtitle):
    console.print(Panel(message, title=title, subtitle=subtitle))

def on_press(key):
    if key.name == 'f':
        # Ваш код здесь
        print('Клавиша F нажата')
    elif key.name == 'ctrl+q':
        sys.exit()

def create_keybinds():
    keyboard.on_press(on_press)

def wait(_print=False, _cls=False):
    if _cls:
        os.system('cls')

    if _print:
        print(Fore.BLUE + 'Press any key to continue...' + Fore.RESET)
    msvcrt.getch()

def print_titles(titles, sep='\n'):
    os.system('cls')

    for title in titles:
        print(art.text2art(title, font="big", sep=sep))

    wait()

def menu(items, question='Choose Channel', addback=True, addytube=False):
    try:
        if addback:
            if items[0] == 'Back': items.remove('Back')
            items.insert(0, 'Back')

        os.system('cls')
        answer = fzf.prompt(items)[0]
        # print(Fore.BLUE + answer + Fore.RESET)

        if addytube and answer != 'Back':
            return 'https://www.youtube.com/@' + answer
        else:
            return answer

    except Exception as e: exit()

def print_image_2_console(url):
    # Initialize colorama
    init()

    # Download the image from the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the image data from the response
        image_data = response.content

        # Create a Pillow Image object from the image data
        image = Image.open(BytesIO(image_data))

        # Resize the image to fit the console
        width, height = image.size
        aspect_ratio = width / height
        f = open('width.txt', 'r')
        new_width = int(f.read())
        f.close()
        new_height = int(new_width / aspect_ratio * 0.6)
        image = image.resize((new_width, new_height), resample=Image.LANCZOS)

        # Convert the image to a console-like representation
        image_str = ''
        for y in range(new_height):
            for x in range(new_width):
                pixel = image.getpixel((x, y))
                r, g, b = pixel
                # Convert the pixel to a color code
                color_code = f'\033[38;2;{r};{g};{b}m'
                image_str += color_code + '█'
            image_str += '\033[0m\n'

        # Display the image
        print(image_str.encode('utf-8').decode('utf-8'))
    else:
        print('Failed to download the image')