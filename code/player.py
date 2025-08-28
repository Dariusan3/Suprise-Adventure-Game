from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -60)
        self.hitbox_rect.center = self.rect.center
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)  # store position as float

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox_rect.x = round(self.pos.x)
        self.rect.x = self.hitbox_rect.x
        self.collision('horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox_rect.y = round(self.pos.y)
        self.rect.y = self.hitbox_rect.y
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                        self.pos.x = self.hitbox_rect.x
                        self.rect.x = self.hitbox_rect.x
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                        self.pos.x = self.hitbox_rect.x
                        self.rect.x = self.hitbox_rect.x
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                        self.pos.y = self.hitbox_rect.y
                        self.rect.y = self.hitbox_rect.y
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.pos.y = self.hitbox_rect.y
                        self.rect.y = self.hitbox_rect.y

    def update(self, dt):
        self.input()
        self.move(dt)