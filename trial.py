import serial
import pygame
import random
import time
import librosa
import numpy as np
import librosa.beat
import os

pygame.init()

display_width = 600
display_height = 800

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
grey = (100, 100, 100)

gap = 2
tile_width = (display_width - 10) / 4
tile_height = display_height * 0.25 - gap  # tile_width * 1.5
grid = [gap,
        (tile_width + gap * 2),
        (tile_width * 2 + gap * 3),
        (tile_width * 3 + gap * 4)]

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Beat Step")
clock = pygame.time.Clock()


class Tiles:
    posy = -tile_height
    posx = random.choice(grid)
    pressed = False

    def tile(self):

        if self.pressed is True:
            color = grey
        else:
            color = black

        posx_int = int(self.posx)
        posy_int = int(self.posy)
        width_int = int(tile_width) 
        height_int = int(tile_height)

        pygame.draw.rect(gameDisplay, color, [posx_int, posy_int, width_int, height_int])


def quitgame(ser):
    ser.close()
    pygame.quit()
    quit()


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def text(x, y, message, size, type, color):
    font = pygame.font.Font(type, size)
    text_surf, text_rect = text_objects(message, font, color)
    text_rect.center = (x, y)
    gameDisplay.blit(text_surf, text_rect)


def button(msg, x, y, width, height, icolor, acolor, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, acolor, (x, y, width, height))
        if click[0] == 1:  # and action is not None 
            action()

    else:
        pygame.draw.rect(gameDisplay, icolor, (x, y, width, height))

    text((x + (width / 2)), (y + (height / 2)), msg, 20, "resources/FreeSansBold.ttf", white)


def gameover(ser):
    ser.close()
    text((display_width / 2), (display_height / 2), "Game Over", 100, "resources/ARCADE.TTF", red)
    pygame.display.update()
    pygame.mixer.stop()
    time.sleep(2)
    start_menu()

selected_song = None
current_song_index = 0

selected_song = None
current_song_index = 0
song_list = None  # Declare song_list as a global variable

def start_menu():
    global selected_song, current_song_index, song_list
    song_directory = "songs"
    song_list = [os.path.join(song_directory, file) for file in os.listdir(song_directory) if file.endswith(".mp3")]
    selected_song = song_list[current_song_index]
    print(song_list)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(white)
        text((display_width / 2), (display_height / 2 - 50), "Beat Step", 115, "resources/ARCADE.TTF", black)
        button("Go!", (display_width / 2 - 100), (display_height * 0.65), 150, 50, black, grey, lambda: game(selected_song))
        button("Change Song", (display_width - 225), (display_height * 0.1), 150, 50, black, grey, change_song)  # Adjusted coordinates
        button("Exit", (display_width / 2 -100), (display_height * 0.75), 150, 50, black, grey, quitgame)

        pygame.display.update()
        clock.tick(15)


def change_song():
    global selected_song, current_song_index, song_list
    current_song_index = (current_song_index + 1) % len(song_list)
    selected_song = song_list[current_song_index]
    print(selected_song)




def load_audio(file_path):
    audio_data, sample_rate = librosa.load(file_path)
    return audio_data, sample_rate


def get_audio_energy(audio_data, sample_rate, frame_length=2048, hop_length=512):
    energy = librosa.feature.rms(y=audio_data, frame_length=frame_length, hop_length=hop_length)
    return energy
def get_serial_input(ser):
    # Check if there's data available to read
    if ser.in_waiting > 0:
        return ser.readline().decode('utf-8').strip()
    else:
        return None

def game(song = 'songs/JVKE - golden hour (official music video).mp3'): 
    print(song)
    tile1 = Tiles()
    tile2 = Tiles()
    tile3 = Tiles()
    tile4 = Tiles()
    tile5 = Tiles()
    tile_list = [tile1, tile2, tile3, tile4, tile5]
    mult = 1
    accelerator = 1
    serial_port = "COM6"
    baud_rate = 9600

    ser = serial.Serial(serial_port, baud_rate)

    for tile in tile_list:
        tile.posx = random.choice(grid)
        tile.posy += -tile_height * mult - gap * (mult + 1)
        mult += 1

    base_tile_speed = 4
    tile_speed = base_tile_speed
    score = 0

    # Prompt the user to select an audio file
    audio_file = song

    if audio_file:
        # Stop any previously playing audio
        pygame.mixer.stop()

        audio_data, sample_rate = load_audio(audio_file)
        audio_energy = get_audio_energy(audio_data, sample_rate)
        energy_scale_factor = 10  # Adjust this value to control the influence of audio energy

        # Detect beat times
        tempo, beat_times = librosa.beat.beat_track(y=audio_data, sr=sample_rate)

        # Initialize audio playback
        pygame.mixer.init()
        sound = pygame.mixer.Sound(audio_file)
        sound.play(loops=-1)  # Loop the audio

        frame_index = 0
        beat_index = 0
        penalty = 5

    while True:
        tileposy_list = []

        for tile in tile_list:

            if tile.pressed is False:
                tileposy_list.append(tile.posy)

        tileposy_list.sort()
        tileposy_list.reverse()
        line = get_serial_input(ser)
        print(line)
        if line =="a0":
            if tile1.posx == grid[0] and tile1.posy == tileposy_list[0]:
                tile1.pressed = True
                score += 1

            elif tile2.posx == grid[0] and tile2.posy == tileposy_list[0]:
                tile2.pressed = True
                score += 1

            elif tile3.posx == grid[0] and tile3.posy == tileposy_list[0]:
                tile3.pressed = True
                score += 1

            elif tile4.posx == grid[0] and tile4.posy == tileposy_list[0]:
                tile4.pressed = True
                score += 1

            elif tile5.posx == grid[0] and tile5.posy == tileposy_list[0]:
                tile5.pressed = True
                score += 1
            else:
                score -=1
                    
        if line == "a1":
                        if tile1.posx == grid[1] and tile1.posy == tileposy_list[0]:
                            tile1.pressed = True
                            score += 1

                        elif tile2.posx == grid[1] and tile2.posy == tileposy_list[0]:
                            tile2.pressed = True
                            score += 1

                        elif tile3.posx == grid[1] and tile3.posy == tileposy_list[0]:
                            tile3.pressed = True
                            score += 1

                        elif tile4.posx == grid[1] and tile4.posy == tileposy_list[0]:
                            tile4.pressed = True
                            score += 1

                        elif tile5.posx == grid[1] and tile5.posy == tileposy_list[0]:
                            tile5.pressed = True
                            score += 1
                        else:
                            score -=1


        if line == "a2":
                        if tile1.posx == grid[2] and tile1.posy == tileposy_list[0]:
                            tile1.pressed = True
                            score += 1

                        elif tile2.posx == grid[2] and tile2.posy == tileposy_list[0]:
                            tile2.pressed = True
                            score += 1

                        elif tile3.posx == grid[2] and tile3.posy == tileposy_list[0]:
                            tile3.pressed = True
                            score += 1

                        elif tile4.posx == grid[2] and tile4.posy == tileposy_list[0]:
                            tile4.pressed = True
                            score += 1

                        elif tile5.posx == grid[2] and tile5.posy == tileposy_list[0]:
                            tile5.pressed = True
                            score += 1
                        else:
                             score -= 1


        if line == "a3":
                        if tile1.posx == grid[3] and tile1.posy == tileposy_list[0]:
                            tile1.pressed = True
                            score += 1

                        elif tile2.posx == grid[3] and tile2.posy == tileposy_list[0]:
                            tile2.pressed = True
                            score += 1

                        elif tile3.posx == grid[3] and tile3.posy == tileposy_list[0]:
                            tile3.pressed = True
                            score += 1

                        elif tile4.posx == grid[3] and tile4.posy == tileposy_list[0]:
                            tile4.pressed = True
                            score += 1

                        elif tile5.posx == grid[3] and tile5.posy == tileposy_list[0]:
                            tile5.pressed = True
                            score += 1
                        else:
                             score -= 1
        if line is None:
            # If no tile in any column matches the input line, decrease the score
            if all(tile.posy != tileposy_list[0] for tile in tile_list):
                score -= 1
        elif line[0] == "a":
            if all(tile.posx != grid[int(line[1])] or tile.posy != tileposy_list[0] for tile in tile_list):
                score -= 1


        gameDisplay.fill(white)

        for tile in tile_list:
            tile.tile()
            if audio_file and beat_index < len(beat_times) and time.time() >= beat_times[beat_index]:
                tile.posy += tile_speed
                beat_index += 1
            tile.posy += tile_speed

        text(35, 15, "Score: " + str(score), 15, "resources/FreeSansBold.ttf", red)

        for tile in tile_list:

            if tile.posy > display_height:
                    tile_index = tile_list.index(tile)
                    tile.posy = tile_list[tile_index - 1].posy - tile_height - gap
                    tile.posx = random.choice(grid)
                    tile.pressed = False
                    if score <-10:
                         gameover(ser)
                    if score < 20:
                        continue
                    elif score % 20 == 0:
                        tile_speed += accelerator

        text((grid[0] + (tile_width / 2)), (display_height - 30), "Tile 1", 30, "resources/FreeSansBold.ttf", black)
        text((grid[1] + (tile_width / 2)), (display_height - 30), "Tile 2", 30, "resources/FreeSansBold.ttf", black)
        text((grid[2] + (tile_width / 2)), (display_height - 30), "Tile 3", 30, "resources/FreeSansBold.ttf", black)
        text((grid[3] + (tile_width / 2)), (display_height - 30), "Tile 4", 30, "resources/FreeSansBold.ttf", black)

        # Get the current audio energy level
        if audio_file:
            current_energy = audio_energy[:, frame_index]
            frame_index = (frame_index + 1) % audio_energy.shape[1]

            # Map the audio energy to tile speed
            tile_speed = base_tile_speed + current_energy * energy_scale_factor

        pygame.display.update()
        clock.tick(60)


start_menu()
