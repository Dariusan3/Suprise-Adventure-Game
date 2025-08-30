from settings import *

class Coffee(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        from main import resource_path
        import os
        self.image = pygame.image.load(resource_path(os.path.join('images', 'coffee', 'coffee2.png'))).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
