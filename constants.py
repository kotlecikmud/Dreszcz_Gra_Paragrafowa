import pygame
import json
import os
from colorama import Fore

# /// initiators
audio_ext = '.mp3'
potion = None
count = 0  # Counter
potion_count = 2  # num of potions
choice_count = 0  # num of choices (universal)
gold_amount = 0  # initial gold amount
p_luck = None  # Player's luck
player_name = None  # Player's name
init_round_count = 0  # Initial num of rounds
round_count = 0  # Round counter
s_count = s_init = 0  # Action points counter: luck
w_count = w_init = 0  # Action points counter: stamina
z_count = z_init = 0  # Action points counter: dexterity
init_eatables_count = eatables_count = 8  # Initial number of meals
eatable_W_load = 4  # How many load of stamina in one meal

# /// constants
and_his_name_is = '''
        ZZZZZZZ    BBBBBB       YYY     YYY     SSSSSS      ZZZZZZZZ      K     K     OOOOO     
              Z     B     B      YYY   YYY     S                  Z       K    K     O     O    
             Z      B     B       YYY YYY       SSS              Z        K   K     O       O    
            Z       BBBBBB         YYYYY             S          Z          KKK      O       O    
          Z         B     B         YYY            SSSS        Z          K   K     O       O    
         Z          B     B         YYY              S        Z           K    K     O     O    
        ZZZZZZZ    BBBBBB           YYY        SSSSSS        ZZZZZZZZ     K     K     OOOOO     
        '''
input_sign = '>>> '  # sign indicating that the user should provide an input
delay = 0.2  # time delay in seconds between printing each character in text
entity_hit_mult = 1  # multiplier for entity level (default level is '1')
p_mult = 1  # player multiplier for damage calculation
p_hit_val_ = -2 * entity_hit_mult - 100  # player hit value
e_hit_val_ = -2 * entity_hit_mult  # enemy hit value
def_txt_clr = Fore.LIGHTWHITE_EX  # default text color
entity_txt_clr = Fore.LIGHTRED_EX  # color for entities
special_txt_clr = Fore.LIGHTMAGENTA_EX  # color for headlines and particular special texts
combat_txt_clr = Fore.LIGHTCYAN_EX  # color for combat text
debug_txt_clr = Fore.LIGHTBLACK_EX  # color for debug messages
error_txt_clr = Fore.RED  # color for error messages

"""
/// PATHS
This section contains path definitions and lists of audio files used in the game.

Paths:
- assets_audio_pth: Path to the directory containing audio files.
- assets_audio_effects_pth: Path to the directory containing sound effects.
- assets_audio_music_pth: Path to the directory containing music files.
- game_state_dir_name: Name of the directory used for game state saves.
- setup_name: Name of the setup script file.

Music Lists:
- music_combat: List of music tracks used in combat .
- music_main: List of main music tracks.
- music_menu: List of menu music tracks.
"""

assets_audio_pth = 'Assets/Audio'  # Path to audio files
assets_audio_effects_pth = 'Assets/Audio/fx'  # Path to sound effects
assets_audio_music_pth = 'Assets/Audio/music'  # Path to music
game_state_dir_name = "Dreszcz_saves"
setup_name = "setup.json"  # Get the setup script's name and or location

music_categories = ['menu', 'main', 'combat']
music_tracks = {}

for category in music_categories:
    category_path = os.path.join(assets_audio_music_pth, category)
    music_tracks[category] = []

    for filename in os.listdir(category_path):
        file_path = os.path.join(category_path, filename)
        if os.path.isfile(file_path):
            music_tracks[category].append(file_path)

# /// pygame mixer setup

pygame.mixer.init(frequency=44100, size=-16, channels=1,
                  buffer=2 ** 12)  # Initialize the mixer module with the specified settings
action_volume = 1  # Default volume for action sounds
sfx_volume = 0.8  # Default volume for sound effects
bckg_volume = 0.8  # Default volume for background music

# /// equipment list

# main equipment
main_eq = {"plecak na Prowiant": "",
           "prowiant": eatables_count,
           "tarcza": "",
           "miecz": "",
           }

# /// dictionaries
choices_115 = {'Miecz': '_232()',
               'Kościany kordelas': '_324()',
               'Rękawice': '_95()',
               'Tarcza': '_37()',
               'Hełm': '_298()',
               'Młot': '_324()',
               }

difficulty_levels = {"easy": 1, "medium": 1.3, "hard": 1.6}

"""
/// SETUP ///

The code defines and loads various setup parameters for a game from a JSON file.

The loaded parameters include:

active_gameplay: bool
    Stores the localization of the active game state file.

translation: str
    Stores the translation setting.

dev_mode: bool
    Enables exclusive mechanics while playing and additional debug information.

debug_msg: bool
    Enables debug messages in between gameplay.

use_dummy: bool
    Enables the use of dummy player and dummy data for testing purposes.

show_start_sequence: bool
    Determines if the start sequence should be shown.

manual_battle: bool
    If False, allows input of "a" and "b" values during combat round.

category: str
    Stores the category information.

allow_dialog_skipping: bool
    Determines whether dubbing will be skipped.

get_music: bool
    Determines whether music playing is enabled.

ver_num: str
    Stores the version number.

difficulty: str
    Placeholder for difficulty setting (currently not implemented).

The setup data is loaded from the JSON file specified by the setup_name variable located in the ///PATHS section above.
The values are assigned to their respective variables using the get() method of the loaded_setup dictionary.
"""

# load setup data from json file
with open(setup_name, "r") as f:
    loaded_setup = json.load(f)

active_gameplay = loaded_setup.get("active_gameplay")
translation = loaded_setup.get("translation")
dev_mode = loaded_setup.get("dev_mode")
debug_msg = loaded_setup.get("debug_msg")
use_dummy = loaded_setup.get("use_dummy")
show_start_sequence = loaded_setup.get("show_start_sequence")
manual_battle = loaded_setup.get("manual_battle")
allow_dialog_skipping = loaded_setup.get("allow_dialog_skipping")
get_music = loaded_setup.get("get_music")
ver_num = loaded_setup.get("ver_num")
difficulty = loaded_setup.get("difficulty")

# further auto config:
if use_dummy:
    game_state_exists = True  # enables 'Continue' and 'Load game' options in main menu
else:
    game_state_exists = False # disables the above
if dev_mode:
    template = "({}) {} - {}"  # - version with enabled annotations
else:
    template = "({}) {}"  # template for list printing (if dev_mode: explainer lines)
