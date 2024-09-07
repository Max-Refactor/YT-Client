from Main import *
import os

def Main():
    download_video(input('Enter URL: '), 'test.mp4')
    os.system(f'videogrep --input test.mp4 --search \'{input("Enter search query: ")}\' --output output.mp4')
    # os.remove('test.mp4')

if __name__ == '__main__':
    Main()