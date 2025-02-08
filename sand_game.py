import os
import sys
import time
import random
import pygame
import json

pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
TILE_SIZE = 100
MENU_WIDTH = 275
MENU_PADDING = 10
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HP_COLOR = RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

def load_image(name, colorkey=None):
    fullname = os.path.join('../pygamehoi5test/data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

player_card = load_image(resource_path('data/green_toy.png'))
enemy_card = load_image(resource_path('data/red_toy.png'))
dirt_tile = load_image(resource_path('data/dirt.png'))
placable_tile = load_image(resource_path('data/placable_dirt.png'))
parking_lot_tile = load_image(resource_path('data/parking_lot.png'))
supply_truck = load_image(resource_path('data/truck.png'))
bunker = load_image(resource_path('data/bunker_gray.png'))
tile_images = {
    "trencher": pygame.transform.scale(parking_lot_tile, (TILE_SIZE, TILE_SIZE)),
    "trench": pygame.transform.scale(placable_tile, (TILE_SIZE, TILE_SIZE)),
    "dirt": pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))
}

def load_sound(name):
    fullname = os.path.join('../pygamehoi5test/data', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        return None
    return pygame.mixer.Sound(fullname)

SOUNDS = {
    "pause": load_sound(resource_path('data/pause_button.wav')),
    "button": load_sound(resource_path('data/button_press.wav')),
    "restart": load_sound(resource_path('data/restart.wav')),
    "enemy_spawn": load_sound(resource_path('data/enemy_spawn.wav')),
    "card_place": load_sound(resource_path('data/card_place.wav')),
    "truck_place": load_sound(resource_path('data/truck_place.wav')),
    "bunker_place": load_sound(resource_path('data/bunker_place.wav'))
}

def load_settings():
    try:
        with open( resource_path("settings.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"volume": 100}

def save_settings(settings):
    with open(resource_path("settings.json"), "w") as file:
        json.dump(settings, file)

class Button:
    def __init__(self, rect, text, font, bg_color=GRAY, border_color=WHITE, text_color=WHITE, border_width=2):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.border_width = border_width
        self.render_text()

    def render_text(self):
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, event, offset=(0, 0)):
        adjusted_rect = self.rect.move(offset)
        return event.type == pygame.MOUSEBUTTONDOWN and adjusted_rect.collidepoint(event.pos)

class ImageButton:
    def __init__(self, rect, image_path, text, font, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.image = pygame.transform.scale(load_image(image_path), (self.rect.width, self.rect.height))
        self.text = text
        self.font = font
        self.text_color = text_color
        self.render_text()

    def render_text(self):
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

def starting_screen():
    pygame.display.set_caption("Sand Line")
    icon = load_image(resource_path('data/icon.png'))
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    background = pygame.transform.scale(load_image(resource_path('data/starting_screen.jpg')), (SCREEN_WIDTH, SCREEN_HEIGHT))
    logo = pygame.transform.scale(load_image(resource_path('data/up_logo.png')), (600, 190))
    logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    font = pygame.font.Font(resource_path('data/KarmaticArcade-6Yrp1.ttf'), 36)

    button_width, button_height = 265, 65
    play_button = ImageButton(((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2, button_width, button_height), resource_path('data/starting_screen_button.png'), "Play", font, BLACK )
    settings_button = ImageButton(((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 75, button_width, button_height), resource_path('data/starting_screen_button.png'), "Settings", font, BLACK )
    exit_button = ImageButton(((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 150, button_width, button_height), resource_path('data/starting_screen_button.png'), "Exit", font, BLACK )
    settings_icon_button = ImageButton((50, 500, 50, 50), resource_path('data/settings_icon.png'), "", font)

    while True:
        screen.blit(background, (0, 0))
        screen.blit(logo, logo_rect)
        play_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)
        settings_icon_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif play_button.is_clicked(event):
                if SOUNDS["pause"]:
                    SOUNDS["pause"].play()
                return

            elif settings_button.is_clicked(event):
                if SOUNDS["pause"]:
                    SOUNDS["pause"].play()
                settings_screen(screen)
            elif exit_button.is_clicked(event):
                if SOUNDS["pause"]:
                    SOUNDS["pause"].play()
                pygame.quit()
                sys.exit()
            elif settings_icon_button.is_clicked(event):
                if SOUNDS["pause"]:
                    SOUNDS["pause"].play()
                settings_screen(screen)


        pygame.display.flip()
        clock.tick(FPS)

def settings_screen(screen, on_back_callback=None):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    font_arc = pygame.font.Font(resource_path('data/KarmaticArcade-6Yrp1.ttf'), 60)
    back_button = Button((50, 50, 150, 50), "Back", font)
    main_menu_button = Button((50, 120, 150, 50), "Menu", font)
    background = pygame.transform.scale(load_image(resource_path('data/settings_fon.jpg')), (SCREEN_WIDTH, SCREEN_HEIGHT))
    settings = load_settings()
    current_volume = settings["volume"]

    slider_width = 200
    slider_height = 20
    slider_x = SCREEN_WIDTH // 2 - slider_width // 2
    slider_y = SCREEN_HEIGHT // 2
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    handle_radius = 10
    handle_x = slider_x + (current_volume / 100) * slider_width

    dragging = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings["volume"] = current_volume
                    save_settings(settings)
                    if on_back_callback:
                        on_back_callback()
                    return
            elif main_menu_button.is_clicked(event):
                if SOUNDS["button"]:
                    SOUNDS["button"].play()
                save_settings(settings)
                starting_screen()
                if on_back_callback:
                    on_back_callback()
                return
            elif back_button.is_clicked(event):
                if SOUNDS["pause"]:
                    SOUNDS["pause"].play()
                settings["volume"] = current_volume
                save_settings(settings)
                if on_back_callback:
                    on_back_callback()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(event.pos):
                    dragging = True
                    if SOUNDS["button"]:
                        SOUNDS["button"].play()
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                handle_x = max(slider_x, min(event.pos[0], slider_x + slider_width))
                current_volume = int(((handle_x - slider_x) / slider_width) * 100)
                for sound in SOUNDS.values():
                    if sound:
                        sound.set_volume(current_volume / 100)

        screen.blit(background, (0, 0))
        text = font_arc.render("Settings", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
        pygame.draw.rect(screen, GRAY, slider_rect)
        pygame.draw.circle(screen, BLACK, (int(handle_x), slider_y + slider_height // 2), handle_radius)
        volume_text = font.render(f"Volume: {current_volume}%", True, WHITE)
        screen.blit(volume_text, (slider_x, slider_y + slider_height + 10))
        back_button.draw(screen)
        main_menu_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

TILE_TYPES = {
    "trencher": pygame.transform.scale(parking_lot_tile, (TILE_SIZE, TILE_SIZE)),
    "trench": pygame.transform.scale(placable_tile, (TILE_SIZE, TILE_SIZE)),
    "dirt": pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__()
        self.tile_type = tile_type
        self.image = TILE_TYPES[tile_type]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.upgrade_type = None
        self.protected = False

    def apply_upgrade(self, upgrade_type, resources):
        if upgrade_type == "supply":
            resources["supply"] += 1
            self.upgrade_type = upgrade_type
        elif upgrade_type == "bunker":
            self.protected = True
            self.upgrade_type = upgrade_type

class Grid:
    def __init__(self, screen_width, screen_height, tile_size):
        self.tile_size = tile_size
        self.tile_group = pygame.sprite.Group()
        for y in range(0, screen_height, tile_size):
            for x in range(0, screen_width, tile_size):
                if x < tile_size:
                    tile_type = "trencher"
                elif x < tile_size * 4:
                    tile_type = "trench"
                else:
                    tile_type = "dirt"
                new_tile = Tile(tile_type, x, y)
                self.tile_group.add(new_tile)

    def draw(self, screen):
        self.tile_group.draw(screen)
        for tile in self.tile_group:
            pygame.draw.rect(screen, WHITE, tile.rect, 1)

class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, hp=100):
        super().__init__()
        self.hp = hp
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass

    def draw_hp_bar(self, screen):
        bar_width = TILE_SIZE - 10
        bar_height = 10
        bar_x = self.rect.x + 5
        bar_y = self.rect.y + TILE_SIZE - bar_height - 5
        hp_ratio = max(self.hp / 100, 0)
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        inner_width = int(bar_width * hp_ratio)
        pygame.draw.rect(screen, HP_COLOR, (bar_x, bar_y, inner_width, bar_height))

class PlayerCard(Card):
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.image = pygame.transform.scale(player_card, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class EnemyCard(Card):
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.image = pygame.transform.scale(enemy_card, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Upgrade(pygame.sprite.Sprite):
    def __init__(self, x, y, cost):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cost = cost

    def update(self):
        pass

    def draw_hp_bar(self, screen):
        pass

class TruckUpgrade(Upgrade):
    def __init__(self, x, y):
        super().__init__(x, y, cost=150)
        self.image = pygame.transform.scale(supply_truck, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.directions = [(0, 1), (0, -1)]

class BunkerUpgrade(Upgrade):
    def __init__(self, x, y):
        super().__init__(x, y, cost=300)
        self.image = pygame.transform.scale(bunker, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.directions = []

class SlidingMenu:
    def __init__(self, width, screen_height, padding=10):
        self.width = width
        self.height = screen_height
        self.padding = padding
        self.x = -width
        self.target_x = -width
        self.open = False

    def toggle(self):
        self.open = not self.open
        self.target_x = 0 if self.open else -self.width
        if SOUNDS["button"]:
            SOUNDS["button"].play()

    def update(self):
        speed = 30
        if self.x < self.target_x:
            self.x = min(self.x + speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - speed, self.target_x)

    def draw(self, screen, resources, font):
        menu_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        menu_surface.fill((0, 0, 0, 128))
        truck_icon = pygame.transform.scale(supply_truck, (TILE_SIZE, TILE_SIZE))
        truck_icon_rect = truck_icon.get_rect(topleft=(20, 150))
        menu_surface.blit(truck_icon, truck_icon_rect.topleft)
        truck_text = font.render("Supply Truck", True, WHITE)
        menu_surface.blit(truck_text, (truck_icon_rect.right + 10, truck_icon_rect.y))
        resource_icon_size = 20
        resource_icon1 = pygame.transform.scale(load_image(resource_path("data/png3.png")),
                                                (resource_icon_size, resource_icon_size))
        menu_surface.blit(resource_icon1, (truck_icon_rect.right + 10, truck_icon_rect.y + 30))
        resource_text1 = font.render("150", True, WHITE)
        menu_surface.blit(resource_text1, (truck_icon_rect.right + 10 + resource_icon_size + 5, truck_icon_rect.y + 30))

        bunker_icon = pygame.transform.scale(bunker, (TILE_SIZE, TILE_SIZE))
        bunker_icon_rect = bunker_icon.get_rect(topleft=(20, truck_icon_rect.bottom + 20))
        menu_surface.blit(bunker_icon, bunker_icon_rect.topleft)
        bunker_text = font.render("Bunker", True, WHITE)
        menu_surface.blit(bunker_text, (bunker_icon_rect.right + 10, bunker_icon_rect.y))
        resource_icon2 = pygame.transform.scale(load_image(resource_path("data/png3.png")),
                                                (resource_icon_size, resource_icon_size))
        menu_surface.blit(resource_icon2, (bunker_icon_rect.right + 10, bunker_icon_rect.y + 30))
        resource_text2 = font.render("300", True, WHITE)
        menu_surface.blit(resource_text2,(bunker_icon_rect.right + 10 + resource_icon_size + 5, bunker_icon_rect.y + 30))

        screen.blit(menu_surface, (self.x, 0))
        pygame.draw.rect(screen, WHITE, (self.x, 0, self.width, self.height), 3)
        return truck_icon_rect.move(self.x, 0), bunker_icon_rect.move(self.x, 0)
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sand Line")
        icon = load_image(resource_path('data/icon.png'))
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.sound_popup = None
        self.current_volume = 25
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.upgrade_group = pygame.sprite.Group()
        self.placed_upgrades = pygame.sprite.Group()
        self.grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
        self.resources = {"supply": 1, "ammunition": 200, "prodpoint": 150}
        self.production_rate = {"ammunition": 4, "prodpoint": 5}
        self.last_update_time = time.time()
        self.dragging_card = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.dragging_card_original_pos = None
        self.enemy_spawn_time = time.time()
        self.enemy_move_time = time.time()
        self.popup_active = False
        self.debug_menu_active = False
        self.game_paused = False
        self.settings_active = False
        self.menu = SlidingMenu(MENU_WIDTH, SCREEN_HEIGHT, MENU_PADDING)
        self.menu_button = pygame.Rect(10, 4, 50, 30)
        self.game_speed_multiplier = 1.0
        self.active_speed_button = None
        self.restart_button = None

    def update_resources(self):
        if not self.game_paused:
            current_time = time.time()
            elapsed = (current_time - self.last_update_time) * self.game_speed_multiplier
            if elapsed >= 1:
                self.last_update_time = current_time
                self.resources["ammunition"] += self.production_rate["ammunition"] * self.resources["supply"]
                self.resources["prodpoint"] += self.production_rate["prodpoint"] * self.resources["supply"]

    def restart(self):
        if SOUNDS["restart"]:
            SOUNDS["restart"].play()
        for sprite in self.all_sprites:
            sprite.kill()
        self.popup_active = False
        self.resources = {"supply": 1, "ammunition": 200, "prodpoint": 150}
        self.enemy_spawn_time = time.time()
        self.enemy_move_time = time.time()

    def place_upgrade(self, upgrade, valid_tile):
        if isinstance(upgrade, BunkerUpgrade) and valid_tile.rect.x >= TILE_SIZE * 4:
            upgrade.kill()
            self.all_sprites.remove(upgrade)
            self.placed_upgrades.remove(upgrade)
            return
        if isinstance(upgrade, TruckUpgrade) and valid_tile.rect.x != 0:
            upgrade.kill()
            self.all_sprites.remove(upgrade)
            self.placed_upgrades.remove(upgrade)
            return
        if valid_tile and not any(upg.rect.topleft == valid_tile.rect.topleft for upg in self.placed_upgrades):
            if self.resources["prodpoint"] >= upgrade.cost:
                upgrade.rect.topleft = valid_tile.rect.topleft
                if isinstance(upgrade, TruckUpgrade):
                    valid_tile.apply_upgrade("supply", self.resources)
                    if SOUNDS["truck_place"]:
                        SOUNDS["truck_place"].play()
                elif isinstance(upgrade, BunkerUpgrade):
                    valid_tile.apply_upgrade("bunker", self.resources)
                    if SOUNDS["bunker_place"]:
                        SOUNDS["bunker_place"].play()
                self.resources["prodpoint"] -= upgrade.cost
                self.placed_upgrades.add(upgrade)
                upgrade.placed = True
                self.all_sprites.add(upgrade)
            else:
                self.all_sprites.remove(upgrade)
                self.placed_upgrades.remove(upgrade)
                upgrade.kill()
        else:
            self.all_sprites.remove(upgrade)
            self.placed_upgrades.remove(upgrade)
            upgrade.kill()

    def spawn_enemy(self):
        potential_rows = [y for y in range(0, SCREEN_HEIGHT, TILE_SIZE) if
                          sum(1 for enemy in self.enemy_group if enemy.rect.y == y) < 1]
        if potential_rows:
            y_pos = random.choice(potential_rows)
            new_enemy = EnemyCard(SCREEN_WIDTH - TILE_SIZE, y_pos)
            self.all_sprites.add(new_enemy)
            self.enemy_group.add(new_enemy)
            if SOUNDS["enemy_spawn"]:
                SOUNDS["enemy_spawn"].play()

    def move_enemies(self):
        for enemy in list(self.enemy_group):
            if enemy.hp <= 0:
                enemy.kill()
                continue
            target_x = enemy.rect.x - TILE_SIZE
            if target_x < 0:
                self.popup_active = True
                return
            if any(other.rect.y == enemy.rect.y and other.rect.x == target_x for other in self.enemy_group):
                continue
            target_player = None
            for card in self.player_group:
                if card.rect.x == target_x and card.rect.y == enemy.rect.y:
                    target_player = card
                    break
            if target_player:
                damage = 25
                for tile in self.grid.tile_group:
                    if tile.rect.topleft == target_player.rect.topleft and tile.protected:
                        damage = 12
                        break
                target_player.hp -= damage
                enemy.hp -= 40
                if target_player.hp <= 0:
                    target_player.kill()
                if enemy.hp <= 0:
                    enemy.kill()
            else:
                enemy.rect.x = target_x
                enemy.x = enemy.rect.x

    def handle_card_placement(self, pos):
        for tile in self.grid.tile_group:
            if tile.rect.collidepoint(pos):
                if 0 <= tile.rect.x < TILE_SIZE * 4:
                    occupied = any(card.rect.topleft == tile.rect.topleft for card in
                                   self.player_group.sprites() + self.enemy_group.sprites())
                    if not occupied and self.resources["ammunition"] >= 25 and self.resources["prodpoint"] >= 15:
                        new_card = PlayerCard(tile.rect.x, tile.rect.y)
                        self.all_sprites.add(new_card)
                        self.player_group.add(new_card)
                        self.resources["ammunition"] -= 25
                        self.resources["prodpoint"] -= 15
                        if SOUNDS["card_place"]:
                            SOUNDS["card_place"].play()
                        return
                for card in self.player_group:
                    if card.rect.collidepoint(pos):
                        self.dragging_card = card
                        self.dragging_card_original_pos = (card.rect.x, card.rect.y)
                        self.drag_offset_x = pos[0] - card.rect.x
                        self.drag_offset_y = pos[1] - card.rect.y
                        return

    def handle_card_drag(self, pos):
        if self.dragging_card:
            new_x = pos[0] - self.drag_offset_x
            new_y = pos[1] - self.drag_offset_y
            self.dragging_card.rect.topleft = (new_x, new_y)
            self.dragging_card.x = new_x
            self.dragging_card.y = new_y

    def handle_card_drop(self):
        if not self.dragging_card:
            return
        if isinstance(self.dragging_card, Upgrade):
            valid_tile = None
            for tile in self.grid.tile_group:
                if tile.rect.collidepoint(self.dragging_card.rect.center):
                    if not any(upg.rect.topleft == tile.rect.topleft for upg in self.placed_upgrades):
                        valid_tile = tile
                        break
            if valid_tile:
                self.place_upgrade(self.dragging_card, valid_tile)
            else:
                self.dragging_card.kill()
            self.dragging_card = None
            return
        original_x, original_y = self.dragging_card_original_pos
        valid_tile = None
        for tile in self.grid.tile_group:
            if tile.rect.collidepoint(self.dragging_card.rect.center):
                occupied = any((other.rect.x == tile.rect.x and other.rect.y == tile.rect.y)
                               for other in self.all_sprites if
                               other != self.dragging_card and not isinstance(other, Upgrade))
                if not occupied:
                    valid_tile = tile
                    break
        if not valid_tile:
            col = self.dragging_card.rect.centerx // TILE_SIZE
            row = self.dragging_card.rect.centery // TILE_SIZE
            candidates = []
            directions = [(0, -1), (0, -2), (-1, 0), (1, 0)]
            for d_row, d_col in directions:
                new_row = row + d_row
                new_col = col + d_col
                if new_row < 0 or new_col < 0 or new_row >= (SCREEN_HEIGHT // TILE_SIZE) or new_col >= (
                        SCREEN_WIDTH // TILE_SIZE):
                    continue
                tile_rect = pygame.Rect(new_col * TILE_SIZE, new_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                for tile in self.grid.tile_group:
                    if tile.rect.topleft == tile_rect.topleft:
                        occupied = any((other.rect.x == tile.rect.x and other.rect.y == tile.rect.y)
                                       for other in self.all_sprites if
                                       other != self.dragging_card and not isinstance(other, Upgrade))
                        if not occupied:
                            candidates.append(tile)
                        break
            if candidates:
                valid_tile = candidates[0]
        if valid_tile:
            if valid_tile.rect.x <= TILE_SIZE * 3:
                self.dragging_card.rect.topleft = valid_tile.rect.topleft
                self.dragging_card.x, self.dragging_card.y = valid_tile.rect.x, valid_tile.rect.y
            else:
                self.dragging_card.rect.topleft = (TILE_SIZE * 3, valid_tile.rect.y)
                self.dragging_card.x, self.dragging_card.y = TILE_SIZE * 3, valid_tile.rect.y
        else:
            self.dragging_card.rect.topleft = (original_x, original_y)
            self.dragging_card.x, self.dragging_card.y = original_x, original_y
        self.dragging_card = None

    def handle_menu_button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_button.collidepoint(event.pos):
                self.menu.toggle()

    def draw_menu_button(self):
        pygame.draw.rect(self.screen, GRAY, self.menu_button)
        pygame.draw.rect(self.screen, WHITE, self.menu_button, 2)
        text = self.font.render("Buy", True, WHITE)
        self.screen.blit(text, (self.menu_button.x + 7, self.menu_button.y + 7))

    def draw_popup(self):
        popup_surface = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), pygame.SRCALPHA)
        popup_surface.fill((0, 0, 0, 128))
        pygame.draw.rect(popup_surface, WHITE, (0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 3)
        text = self.font.render("You've capitulated!", True, WHITE)
        popup_surface.blit(text, (SCREEN_WIDTH // 4 - text.get_width() // 2, 50))

        self.restart_button = Button(
            (SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT // 4 + 50, 100, 50),
            "Restart", self.font, bg_color=RED
        )
        self.restart_button.draw(popup_surface)
        self.screen.blit(popup_surface, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

    def draw_top_ui(self):
        panel_x = 0
        panel_y = 0
        panel_width = SCREEN_WIDTH
        panel_height = 40
        ui_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        ui_surface.fill((0, 0, 0, 128))
        icon_size = 30
        margin = 10
        x = 70
        y = (panel_height - icon_size) // 2
        icon1 = pygame.transform.scale(load_image(resource_path("data/png1.png")), (icon_size, icon_size))
        ui_surface.blit(icon1, (x, y))
        supply_text = self.font.render(str(self.resources["supply"]), True, WHITE)
        ui_surface.blit(supply_text, (x + icon_size + margin, (panel_height - supply_text.get_height()) // 2))
        x += icon_size + margin + supply_text.get_width() + 2 * margin
        icon2 = pygame.transform.scale(load_image(resource_path("data/png2.png")), (icon_size, icon_size))
        ui_surface.blit(icon2, (x, y))
        amm_text = self.font.render(str(self.resources["ammunition"]), True, WHITE)
        ui_surface.blit(amm_text, (x + icon_size + margin, (panel_height - amm_text.get_height()) // 2))
        x += icon_size + margin + amm_text.get_width() + 2 * margin
        icon3 = pygame.transform.scale(load_image(resource_path("data/png3.png")), (icon_size, icon_size))
        ui_surface.blit(icon3, (x, y))
        prodpoint_text = self.font.render(str(self.resources["prodpoint"]), True, WHITE)
        ui_surface.blit(prodpoint_text, (x + icon_size + margin, (panel_height - prodpoint_text.get_height()) // 2))
        self.screen.blit(ui_surface, (panel_x, panel_y))

    def draw_speed_buttons(self):
        button_width = 40
        button_height = 40
        spacing = 10
        start_x = SCREEN_WIDTH - (3 * button_width + 2 * spacing)
        start_y = 10
        buttons = []
        labels = ["<<", "| |", ">>"]
        for i, label in enumerate(labels):
            rect = (start_x + i * (button_width + spacing), start_y, button_width, button_height)
            if label == "| |":
                color = RED if self.game_paused else GRAY
            elif label == ">>":
                color = RED if self.active_speed_button == ">>" else GRAY
            elif label == "<<":
                color = RED if self.active_speed_button == "<<" else GRAY
            else:
                color = GRAY
            button = Button(rect, label, self.font, bg_color=color)
            buttons.append((button, label))
            button.draw(self.screen)
        return buttons

    def handle_speed_buttons(self, event, buttons):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button, label in buttons:
                if button.is_clicked(event):
                    if label == "| |":
                        self.toggle_pause()
                    elif label == ">>":
                        if self.active_speed_button == ">>":
                            self.active_speed_button = None
                            self.game_speed_multiplier = 1.0
                            if SOUNDS["pause"]:
                                SOUNDS["pause"].play()
                        else:
                            self.active_speed_button = ">>"
                            self.game_speed_multiplier = 5.0
                    elif label == "<<":
                        if self.active_speed_button == "<<":
                            self.active_speed_button = None
                            self.game_speed_multiplier = 1.0
                            if SOUNDS["pause"]:
                                SOUNDS["pause"].play()
                        else:
                            self.active_speed_button = "<<"
                            self.game_speed_multiplier = 0.2

    def toggle_pause(self):
        self.game_paused = not self.game_paused
        if SOUNDS["pause"]:
            SOUNDS["pause"].play()

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_menu_button(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if SOUNDS["pause"]:
                        SOUNDS["pause"].play()
                    self.settings_active = not self.settings_active
                    self.game_paused = self.settings_active
                if event.key == pygame.K_r and self.popup_active:
                    self.restart()
                if event.key == pygame.K_s:
                    self.menu.toggle()
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    self.toggle_pause()
            if self.sound_popup:
                self.sound_popup.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.popup_active:
                    if self.restart_button:
                        if self.restart_button.is_clicked(event, offset=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)):
                            self.restart()
                elif self.menu.open:
                    truck_rect, bunker_rect = self.menu.draw(self.screen, self.resources, self.font)
                    if truck_rect.collidepoint(event.pos):
                        new_upgrade = TruckUpgrade(truck_rect.x, truck_rect.y)
                        self.all_sprites.add(new_upgrade)
                        self.upgrade_group.add(new_upgrade)
                        self.dragging_card = new_upgrade
                        self.dragging_card_original_pos = (new_upgrade.rect.x, new_upgrade.rect.y)
                        self.drag_offset_x = event.pos[0] - new_upgrade.rect.x
                        self.drag_offset_y = event.pos[1] - new_upgrade.rect.y
                        self.menu.toggle()
                        continue
                    elif bunker_rect.collidepoint(event.pos):
                        new_upgrade = BunkerUpgrade(bunker_rect.x, bunker_rect.y)
                        self.all_sprites.add(new_upgrade)
                        self.upgrade_group.add(new_upgrade)
                        self.dragging_card = new_upgrade
                        self.dragging_card_original_pos = (new_upgrade.rect.x, new_upgrade.rect.y)
                        self.drag_offset_x = event.pos[0] - new_upgrade.rect.x
                        self.drag_offset_y = event.pos[1] - new_upgrade.rect.y
                        self.menu.toggle()
                        continue
                    menu_rect = pygame.Rect(self.menu.x, 0, self.menu.width, self.menu.height)
                    if not menu_rect.collidepoint(event.pos) and not self.menu_button.collidepoint(event.pos):
                        self.menu.toggle()
                else:
                    self.handle_card_placement(event.pos)
                speed_buttons = self.draw_speed_buttons()
                self.handle_speed_buttons(event, speed_buttons)
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_card:
                    self.handle_card_drag(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_card_drop()

    def update(self):
        self.menu.update()
        tick_speed = 1.0 / self.game_speed_multiplier
        current_time = time.time()
        if not self.game_paused:
            if current_time - self.enemy_spawn_time > tick_speed:
                self.spawn_enemy()
                self.enemy_spawn_time = current_time
            if current_time - self.enemy_move_time > tick_speed:
                self.move_enemies()
                self.enemy_move_time = current_time
        self.update_resources()
        self.all_sprites.update()

    def draw(self):
        if self.settings_active:
            settings_screen(self.screen, on_back_callback=lambda: setattr(self, 'settings_active', False))
            return
        self.screen.fill(BLACK)
        self.grid.draw(self.screen)
        self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            if hasattr(sprite, 'draw_hp_bar'):
                sprite.draw_hp_bar(self.screen)
        self.menu.draw(self.screen, self.resources, self.font)
        self.draw_top_ui()
        self.draw_menu_button()
        self.draw_speed_buttons()
        if self.popup_active:
            self.draw_popup()
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            if not self.settings_active:
                self.update()
            self.draw()
            self.clock.tick(FPS)

def main():
    starting_screen()
    settings = load_settings()
    current_volume = settings["volume"]
    for sound in SOUNDS.values():
        if sound:
            sound.set_volume(current_volume / 100)
    game = Game()
    game.run()


if __name__ == "__main__":
    main()