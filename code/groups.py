from dog import Dog
from player import Player
from settings import *
from coffee import Coffee

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

        
    def draw_speech_bubble(self, screen, text, text_color, bg_color, pos, size):
        font = pygame.font.SysFont(None, size)

        text_surface = font.render(text, True, text_color)
        # For debug, use a fixed position
        text_rect = text_surface.get_rect(midbottom=pos)

        # background
        bg_rect = text_rect.copy()
        bg_rect.inflate_ip(10, 10)

        # frame
        frame_rect = bg_rect.copy()
        frame_rect.inflate_ip(4, 4)

        pygame.draw.rect(screen, text_color, frame_rect)
        pygame.draw.rect(screen, bg_color, bg_rect)
        screen.blit(text_surface, text_rect)


    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        ground_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self.sprites() if not hasattr(sprite, 'ground')]
        
        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
                # Dialogue system: dog and player can speak
                if hasattr(sprite, "dialogue") and sprite.speaking:
                    if sprite.speech_index < len(sprite.dialogue):
                        current = sprite.dialogue[sprite.speech_index]
                        if current["speaker"] == "dog":
                            bubble_pos = sprite.rect.topleft + self.offset + pygame.Vector2(0, -20)
                        else:  # "player"
                            player_sprite = next((s for s in self.sprites() if isinstance(s, Player)), None)
                            if player_sprite:
                                bubble_pos = player_sprite.rect.topleft + self.offset + pygame.Vector2(0, -20)
                        self.draw_speech_bubble(self.display_surface, current["text"], (0, 0, 0), (255, 255, 255), bubble_pos, 32)
                    else:
                        sprite.dialogue_finished = True
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            sprite.speech_index = (sprite.speech_index + 1)
