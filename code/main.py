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

        # coffee tracking
        self.coffee_count = 0
        self.coffees = []
        self.total_coffees = 5  # update if you want to count dynamically
        self.show_coffee_message = False
        self.coffees_spawned = False
        self.show_return_message = True
    def spawn_coffees(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Coffee':
                coffee = Coffee((obj.x, obj.y), (self.all_sprites, self.collision_sprites))
                self.coffees.append(coffee)
                

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
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # Spawn coffees after dialogue1 is finished, only once
            if hasattr(self.dog, 'dialogue1_finished') and self.dog.dialogue1_finished and not self.coffees and not self.coffees_spawned:
                self.spawn_coffees()
                self.show_coffee_message = True
                self.coffees_spawned = True

            # Coffee collection logic
            for coffee in self.coffees[:]:
                if self.player.rect.colliderect(coffee.rect):
                    self.coffees.remove(coffee)
                    coffee.kill()
                    self.coffee_count += 1
                    self.show_coffee_message = False

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            # Draw coffee count in top-left corner
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Cappuccinos: {self.coffee_count}/{self.total_coffees}", True, (255, 255, 255))
            self.display_surface.blit(text, (20, 20))

            # Show message after coffees appear
            if self.show_coffee_message:
                msg_font = pygame.font.SysFont(None, 40)
                msg_text = msg_font.render("Collect all the cappuccinos!", True, (255, 223, 186))
                msg_rect = msg_text.get_rect(center=(WINDOW_WIDTH//2, 60))
                self.display_surface.blit(msg_text, msg_rect)

            # Show message when all cappuccinos are collected
            if self.coffee_count == self.total_coffees:
                self.dog.all_coffee_collected = True
                if self.show_return_message:
                    win_font = pygame.font.SysFont(None, 40)
                    win_text = win_font.render("Return to Tobi!", True, (186, 255, 223))
                    win_rect = win_text.get_rect(center=(WINDOW_WIDTH//2, 100))
                    self.display_surface.blit(win_text, win_rect)
                # Only start dialogue2 when player collides AND presses SPACE
                keys = pygame.key.get_pressed()
                if self.player.rect.colliderect(self.dog.rect) and keys[pygame.K_SPACE]:
                    self.dog.speaking = True
                    self.show_return_message = False
            
            if self.dog.dialogue2_finished:
                self.dog.speaking = False
                # Try to load a cute background image
                try:
                    bg_image = pygame.image.load(join('images', 'lalele', 'lalele.jpg')).convert()
                    bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    self.display_surface.blit(bg_image, (0, 0))
                except Exception:
                    self.display_surface.fill((255, 223, 238))

                font_big = pygame.font.SysFont(None, 60)
                font_small = pygame.font.SysFont(None, 40)
                msg1 = font_big.render("Happy Birthday, Anastasija!", True, (255, 105, 180))
                msg2 = font_small.render("You the most important person for me trust me and I want to give my all to make you happy", True, (255, 20, 147))
                msg3 = font_small.render("I love you the most and the words are simply too small for the all the love I have for you!", True, (186, 85, 211))
                msg4 = font_small.render("Volim te! Te iubesc! I hope you feel all the love today!", True, (255, 20, 147))
                self.display_surface.blit(msg1, msg1.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60)))
                self.display_surface.blit(msg2, msg2.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)))
                self.display_surface.blit(msg3, msg3.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60)))
                self.display_surface.blit(msg4, msg4.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 120)))

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()  