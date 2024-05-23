# Leg-Based Game Controller Using Piezo Sensors

## Overview
This project involves the development of a leg-based game controller utilizing piezo sensors to interact with digital games such as Piano Tiles, Subway Surfers, and Pacman. The primary goal is to create an interactive gaming experience that promotes physical activity and can even be used to learn dance steps. The controller interfaces with games developed in Pygame, an open-source library for making multimedia applications.

## Components
- **Piezo Sensors**: These sensors are placed on a mat or wearable straps around the legs. They detect pressure changes and convert them into electrical signals.
- **Microcontroller**: A microcontroller (e.g., Arduino) processes the signals from the piezo sensors and communicates with the computer via USB or Bluetooth.
- **Pygame Interface**: Custom code written in Pygame for games like Piano Tiles interprets the signals from the microcontroller to control the game.

## Functionality

### Piano Tiles Game
- Players tap their feet on the corresponding tiles on a mat to match the tiles displayed on the screen.
- The piezo sensors detect the foot taps and send signals to the Pygame application to register the input.

### Subway Surfers and Pacman
- Players can use their feet to simulate movements (e.g., jump, slide, turn left/right for Subway Surfers, and directional controls for Pacman).
- Different piezo sensors or combinations of sensors can be mapped to specific game controls.

## Benefits
- **Promotes Physical Activity**: Unlike traditional hand-held controllers, this system encourages players to move their legs, promoting exercise and physical engagement.
- **Interactive Learning**: The controller can be adapted to educational games that teach rhythm and dance steps, making learning fun and interactive.
- **Versatility**: While optimized for Piano Tiles, the controller’s design allows it to be adapted for various other games, enhancing the gaming experience and offering a new way to interact with digital entertainment.

## Implementation Steps

### Hardware Setup
1. Place piezo sensors on a mat or create wearable leg straps with integrated sensors.
2. Connect the sensors to a microcontroller (Arduino is a good choice for prototyping).

### Microcontroller Programming
1. Write code to read the piezo sensor signals and send them to the computer.
2. Map the sensor inputs to specific keyboard or mouse inputs that correspond to game controls.

### Pygame Integration
1. Modify the Pygame code of the desired game to accept inputs from the microcontroller.
2. Implement a calibration function to adjust the sensitivity of the sensors based on user preferences.

### Testing and Calibration
1. Test the setup with the targeted games (Piano Tiles, Subway Surfers, Pacman) and fine-tune the sensor sensitivity and response time.
2. Ensure that the input mapping is accurate and responsive to provide a seamless gaming experience.



## Conclusion
The leg-based game controller using piezo sensors is a novel way to interact with digital games, making them more engaging and physically stimulating. It not only enhances the gaming experience but also promotes physical activity and learning through interactive play. This project showcases the potential of combining hardware and software to create innovative solutions that bridge the gap between digital entertainment and physical exercise.



## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

This README provides an overview of the project, explains the components, functionality, benefits, and detailed steps for implementation, along with an example code snippet for integration with Pygame.
