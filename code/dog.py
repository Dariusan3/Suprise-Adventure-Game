from settings import *

class Dog(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'idle', 0
        self.image = pygame.image.load(join('images', 'dog', 'idle', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.Vector2()

    def load_images(self):
        self.frames = {'idle': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'dog', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda x: int(x.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        print(full_path)  # Debugging line to check file paths
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