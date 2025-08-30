from settings import *

class Dog(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'idle', 0
        self.image = pygame.image.load(join('images', 'dog', 'idle', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.Vector2()
        self.speaking = False
        self.dialogue1 = [
            {"speaker": "dog", "text": "Woof woof! Anastasija! Happy Birthday!"},
            {"speaker": "player", "text": "Hi Tobi! Thank you, my sweet poodle friend!"},
            {"speaker": "dog", "text": "I have a very important mission for you today!"},
            {"speaker": "player", "text": "Oh? What kind of mission?"},
            {"speaker": "dog", "text": "I need you to find cappuccinos! Lots of them!"},
            {"speaker": "player", "text": "Cappuccinos? That's my favorite also!"},
            {"speaker": "dog", "text": "I love the smell too! It makes me so energetic!"},
            {"speaker": "player", "text": "Of course! Let's go find them!"},
            {"speaker": "dog", "text": "You're the best! Adventure time!"}
        ]
        self.speech1_index = 0
        self.dialogue1_finished = False

        self.all_coffee_collected = False

        self.dialogue2 = [
        {"speaker": "Tobi", "text": "Woof woof! You're back!"},
        {"speaker": "Anastasija", "text": "I got all 5 cappuccinos, Tobi!"},
        {"speaker": "Tobi", "text": "*sniff sniff* Oh wow! They smell amazing!"},
        {"speaker": "Tobi", "text": "You're the most wonderful birthday girl ever!"},
        {"speaker": "Anastasija", "text": "Aww, thank you Tobi!"},
        {"speaker": "Tobi", "text": "Now I have the perfect surprise for you..."},
        ]
        self.speech2_index = 0
        self.dialogue2_finished = False

    def load_images(self):
        self.frames = {'idle': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'dog', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda x: int(x.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def animate(self, dt):
        # always use idle state since only idle frames exist
        self.state = 'idle'
        self.frame_index = self.frame_index + 2.5 * dt
        if self.frames['idle']:
            self.image = self.frames['idle'][int(self.frame_index) % len(self.frames['idle'])]

    def update(self, dt):
        self.animate(dt)