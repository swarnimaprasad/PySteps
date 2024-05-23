import pygame
import sys
import numpy as np
import pyaudio
from math import pi, sin, cos  # for 3D calculations

# Define colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
DARK_GREY = (64, 64, 64)
BLACK = (0, 0, 0)

# Define audio files for each pad (replace with your actual audio files)
PAD_SOUNDS = {
    'Pad1': 'badumtss.wav',
    'Pad2': 'basedrum.wav',
    'Pad3': 'baseNsnare.wav',
    'Pad4': 'clap.wav',
    'Pad5': 'crash.wav',
    'Pad6': 'snare.wav',
    'Pad7': 'tom.wav',
    'Pad8': 'snareroll.wav'
}

# Key bindings for each pad
KEY_BINDINGS = {
    'Pad1': pygame.K_q,
    'Pad2': pygame.K_w,
    'Pad3': pygame.K_e,
    'Pad4': pygame.K_r,
    'Pad5': pygame.K_a,
    'Pad6': pygame.K_s,
    'Pad7': pygame.K_d,
    'Pad8': pygame.K_f
}

# Color mappings for sound visualization
SOUND_COLORS = {
    pygame.K_q: (255, 0, 0),    # Red
    pygame.K_w: (0, 255, 0),    # Green
    pygame.K_e: (0, 0, 255),    # Blue
    pygame.K_r: (255, 255, 0),  # Yellow
    pygame.K_a: (255, 0, 255),  # Magenta
    pygame.K_s: (0, 255, 255),  # Cyan
    pygame.K_d: (255, 165, 0),  # Orange
    pygame.K_f: (128, 0, 128)   # Purple
}

# Initialize pygame and PyAudio
pygame.init()
pygame.mixer.init()
p = pyaudio.PyAudio()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PAD_SIZE = 100
PADDING = 50

DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Octapad')

clock = pygame.time.Clock()

# Function to draw pads
def draw_pads(pads_state):
    DISPLAY.fill(BLACK)

    for i, (pad, state) in enumerate(pads_state.items()):
        # Define 3D positions of pads in a grid-like pattern
        x = PADDING + (i % 4) * (PAD_SIZE + PADDING)
        y = PADDING + (i // 4) * (PAD_SIZE + PADDING)
        z = 0  # Depth (in this case, all pads are at the same depth)

        # Apply perspective transformation to 3D coordinates
        # Here, we simply reduce the y-coordinate to simulate the 45-degree angle view
        y -= z * 0.5

        # Render the pads
        color = DARK_GREY if state else GREY
        pygame.draw.rect(DISPLAY, color, (x, y, PAD_SIZE, PAD_SIZE))

        font = pygame.font.SysFont(None, 36)    
        text = font.render(pad, True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (x + PAD_SIZE // 2, y + PAD_SIZE // 2)
        DISPLAY.blit(text, text_rect)

# Function to draw sound visualization
def draw_sound_visualization(audio_data, pressed_key):
    DISPLAY.fill(BLACK)

    # Visualize the audio data
    bar_width = 10
    bar_spacing = 5
    num_bars = WINDOW_WIDTH // (bar_width + bar_spacing)

    for i in range(num_bars):
        bar_height = int(abs(audio_data[i * (len(audio_data) // num_bars)]) * WINDOW_HEIGHT // 2)
        x = i * (bar_width + bar_spacing)
        y = WINDOW_HEIGHT // 2 - bar_height // 2
        color = SOUND_COLORS.get(pressed_key, WHITE)
        pygame.draw.rect(DISPLAY, color, (x, y, bar_width, bar_height))

# Function to draw tutoring screen
def draw_tutoring_screen():
    DISPLAY.fill(BLACK)

    # Add tutoring content here
    font = pygame.font.SysFont(None, 36)
    text = font.render("Tutoring Screen", True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    DISPLAY.blit(text, text_rect)

# Function to play a sound
def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

# Main loop
def main():
    pads_state = {pad: False for pad in PAD_SOUNDS}
    keys_pressed = set()
    current_screen = 'pads'

    # Set up PyAudio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    stream = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stream.stop_stream()
                stream.close()
                p.terminate()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Get key pressed and toggle pad state
                for pad, key in KEY_BINDINGS.items():
                    if event.key == key:
                        sound_file = PAD_SOUNDS[pad]
                        play_sound(sound_file)
                        pads_state[pad] = True
                        keys_pressed.add(key)
                # Switch between screens
                if event.key == pygame.K_t:
                    if current_screen == 'pads':
                        current_screen = 'visualization'
                    elif current_screen == 'visualization':
                        current_screen = 'tutoring'
                    elif current_screen == 'tutoring':
                        current_screen = 'pads'
            elif event.type == pygame.KEYUP:
                # Get key released and reset pad state
                for pad, key in KEY_BINDINGS.items():
                    if event.key == key:
                        pads_state[pad] = False
                        keys_pressed.remove(key)

        # Get audio data from the microphone
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Draw the appropriate screen
        if current_screen == 'pads':
            draw_pads(pads_state)
        elif current_screen == 'visualization':
            if len(keys_pressed) > 0:
                # Get the most recently pressed key
                pressed_key = list(keys_pressed)[-1]
                draw_sound_visualization(audio_data, pressed_key)
            else:
                draw_sound_visualization(audio_data, None)
        elif current_screen == 'tutoring':
            draw_tutoring_screen()

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
