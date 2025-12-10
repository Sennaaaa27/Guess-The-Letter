# dictionary.py

# ---------------------------
# WORDS BY DIFFICULTY
# ---------------------------
EASY_WORDS = [
    "cat", "dog", "car", "cup", "sun", "star", "book", "key", "hat", "sky",
    "pen", "ball", "fish", "tree", "milk", "door", "leaf", "egg", "shoe", "bag",
    "moon", "bird", "hat", "sock", "fork", "glass", "chair", "clock", "ring", "fan"
]

MEDIUM_WORDS = [
    "apple", "train", "house", "phone", "plant", "light", "smile", "cookie", "table", "monitor",
    "pencil", "garden", "window", "button", "camera", "bottle", "rabbit", "candle", "shirt", "laptop",
    "bicycle", "balloon", "letter", "flower", "mirror", "pillow", "clock", "basket", "keypad", "rocket"
]

HARD_WORDS = [
    "advance", "network", "battery", "question", "computer",
    "elephant", "slippers", "umbrella", "bluebird", "strength",
    "dictionary", "keyboard", "microscope", "telephone", "pineapple",
    "chocolate", "adventure", "backpack", "hospital", "sandwich",
    "pinecone", "fireplace", "astronaut", "blackboard", "sunflower",
    "refrigerator", "volleyball", "compass", "helicopter", "telescope"
]

# ---------------------------
# LETTER TO EMOJI MAP
# ---------------------------
LETTER_EMOJI_MAP = {
    'A': ["🍎","✈️","🅰️","😡"],
    'B': ["🍌","🦋","🐝","📚"],
    'C': ["🐱","🍪","🌽","🍰"],
    'D': ["🐶","🍩","🎯","☢️"],
    'E': ["🥚","🐘","🦅","✉️"],
    'F': ["🐸","🍟","🌸","🏳️"],
    'G': ["🦒","🍇","🎮","💎"],
    'H': ["🏠","🎩","❤️","😆"],
    'I': ["🍦","🏝️","🧊","💉"],
    'J': ["👖","🃏","🤹","🎌"],
    'K': ["🔑","⌨️","🪁","🔪"],
    'L': ["🦁","💡","🍋","🐞"],
    'M': ["🐒","💵","🌚","🎖️"],
    'N': ["🎶","🪺","💅🏼","🥜"],
    'O': ["🦉","🍊","⭕","🐙"],
    'P': ["🍑","🐧","🥞","🏓"],
    'Q': ["❓","👸","🏳️‍🌈","🇶"],
    'R': ["🌈","🐇","🤖","🌧️"],
    'S': ["🐍","🌟","🍓","🌞"],
    'T': ["🌮","🩺","🌳","🕒"],
    'U': ["☂️","🌍","🦄","🔝"],
    'V': ["🎻","🏐","🌋","🏺"],
    'W': ["🌊","🍉","♿","💦"],
    'X': ["❌","🩻","🖾","🙅"],
    'Y': ["🧶","☯","🛥️"],
    'Z': ["🧟‍♂️","🦓","🤐","😴"],
}

# ---------------------------
# WORD TO IMAGE MAP
# ---------------------------
WORD_IMAGES = {
    # EASY
    "cat": "images/cat.jpg",
    "dog": "images/dog.jpg",
    "car": "images/car.jpg",
    "cup": "images/cup.jpg",
    "sun": "images/sun.jpg",
    "star": "images/star.jpg",
    "book": "images/book.jpg",
    "key": "images/key.jpg",
    "hat": "images/hat.jpg",
    "sky": "images/sky.jpg",
    "pen": "images/pen.jpg",
    "ball": "images/ball.jpg",
    "fish": "images/fish.jpg",
    "tree": "images/tree.jpg",
    "milk": "images/milk.jpg",
    "door": "images/door.jpg",
    "leaf": "images/leaf.jpg",
    "egg": "images/egg.jpg",
    "shoe": "images/shoe.jpg",
    "bag": "images/bag.jpg",
    "moon": "images/moon.jpg",
    "bird": "images/bird.jpg",
    "sock": "images/sock.jpg",
    "fork": "images/fork.jpg",
    "glass": "images/glass.jpg",
    "chair": "images/chair.jpg",
    "clock": "images/clock.jpg",
    "ring": "images/ring.jpg",
    "fan": "images/fan.jpg",

    # MEDIUM
    "apple": "images/apple.jpg",
    "train": "images/train.jpg",
    "house": "images/house.jpg",
    "phone": "images/phone.jpg",
    "plant": "images/plant.jpg",
    "light": "images/light.jpg",
    "smile": "images/smile.jpg",
    "cookie": "images/cookie.jpg",
    "table": "images/table.jpg",
    "monitor": "images/monitor.jpg",
    "pencil": "images/pencil.jpg",
    "garden": "images/garden.jpg",
    "window": "images/window.jpg",
    "button": "images/button.jpg",
    "camera": "images/camera.jpg",
    "bottle": "images/bottle.jpg",
    "rabbit": "images/rabbit.jpg",
    "candle": "images/candle.jpg",
    "shirt": "images/shirt.jpg",
    "laptop": "images/laptop.jpg",
    "bicycle": "images/bicycle.jpg",
    "balloon": "images/balloon.jpg",
    "letter": "images/letter.jpg",
    "flower": "images/flower.jpg",
    "mirror": "images/mirror.jpg",
    "pillow": "images/pillow.jpg",
    "crown": "images/crown.jpg",
    "basket": "images/basket.jpg",
    "keypad": "images/keypad.jpg",
    "rocket": "images/rocket.jpg",

    # HARD
    "advance": "images/advance.jpg",
    "network": "images/network.jpg",
    "battery": "images/battery.jpg",
    "question": "images/question.jpg",
    "computer": "images/computer.jpg",
    "elephant": "images/elephant.jpg",
    "slippers": "images/slippers.jpg",
    "umbrella": "images/umbrella.jpg",
    "bluebird": "images/bluebird.jpg",
    "strength": "images/strength.jpg",
    "dictionary": "images/university.jpg",
    "keyboard": "images/keyboard.jpg",
    "microscope": "images/microscope.jpg",
    "telephone": "images/telephone.jpg",
    "pineapple": "images/pineapple.jpg",
    "chocolate": "images/chocolate.jpg",
    "adventure": "images/adventure.jpg",
    "backpack": "images/backpack.jpg",
    "hospital": "images/hospital.jpg",
    "sandwich": "images/sandwich.jpg",
    "pinecone": "images/pinecone.jpg",
    "fireplace": "images/fireplace.jpg",
    "astronaut": "images/astronaut.jpg",
    "blackboard": "images/blackboard.jpg",
    "sunflower": "images/sunflower.jpg",
    "refrigerator": "images/refrigerator.jpg",
    "volleyball": "images/volleyball.jpg",
    "compass": "images/compass.jpg",
    "helicopter": "images/helicopter.jpg",
    "telescope": "images/telescope.jpg"
}

# ---------------------------
# FALLBACK EMOJI
# ---------------------------
FALLBACK_EMOJI = "❓"

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def get_emoji_for_letter(letter):
    """Return a random emoji for a given letter"""
    if not letter:
        return FALLBACK_EMOJI
    letter = letter.upper()
    return random.choice(LETTER_EMOJI_MAP.get(letter, [FALLBACK_EMOJI]))


#def WORD_EMOJI_MAP():
    return None