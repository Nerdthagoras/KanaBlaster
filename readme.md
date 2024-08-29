Here's a README for the code you provided:

---

# Kana Blaster

**Kana Blaster** is a game built using the Python `pygame` library. The game is designed to transition through various game states, manage music, and handle collision detection and event handling. This README provides an overview of the code structure and usage.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Game States](#game-states)
- [Music Handling](#music-handling)
- [Event Handling and Collision Detection](#event-handling-and-collision-detection)
- [License](#license)

## Overview

The game transitions between different states such as `intro`, `menu`, `gameplay`, `boss`, and `game over`. Depending on the state, different background music is played. The game uses `pygame` to manage screen updates, collision detection, and event handling.

## Prerequisites

Before running the game, ensure you have the following installed:

- Python 3.x
- Pygame library (`pip install pygame`)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Nerdthagoras/KanaBlaster.git
    ```
2. Navigate to the project directory:
    ```bash
    cd KanaBlaster
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the game, execute the main script:

```bash
python Kanablaster.py
```

The game will start, and the initial state will be the `intro_state`. The game will transition between states based on player progress and game logic.

## Game States

The game consists of several states managed by the `Game_States` module:

- **Intro State (`intro_state`)**: The initial state of the game.
- **Menu State (`menu_state`)**: The main menu where the player can start the game.
- **Game State (`game_state`)**: The main gameplay state.
- **Boss State (`boss_state`)**: The state when the player encounters a boss.
- **Game Over State (`gameover_state`)**: The state after the player loses.

The current state is updated based on game progress, and the corresponding music track is loaded and played.

## Music Handling

Music is dynamically loaded and played based on the current game state. The following tracks are used:

- `GameIntro.wav` for the intro and menu states.
- `TimeDilation.wav` for the main gameplay.
- `ColinTheme.wav` for the boss fight and game over states.

Music volume is controlled by the `Variables.musicvolume` variable, which can be adjusted during runtime.

## Event Handling and Collision Detection

The game loop continuously checks for user input (such as key presses) and updates the game state accordingly. Collision detection is performed in the `current_state.collision()` method, ensuring that game objects interact correctly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to modify this README as needed to better suit your project or personal preferences!
