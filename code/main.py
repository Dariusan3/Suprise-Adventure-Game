from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from dog import Dog
from coffee import Coffee

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Anastasija's Surprise Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # audio
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.music.set_volume(0.07)
        self.music.play(loops = -1)

        self.setup()

        #sprites

    def check_coffee_collection(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        if self.dog.dialogue_finished:
            for obj in map.get_layer_by_name('Entities'):
                if obj.name == 'Coffee':
                    self.coffee = Coffee((obj.x, obj.y), (self.all_sprites, self.collision_sprites))

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprites((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprites((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), 
                             self.collision_sprites)
            
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                   self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            if obj.name == 'Dog':
                   self.dog = Dog((obj.x, obj.y), (self.all_sprites, self.collision_sprites))

    def run(self):
        while self.running:
            # dtsd
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)
            self.check_coffee_collection()

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()  