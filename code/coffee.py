from settings import *

class Coffee(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'coffee', 'coffee2.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
