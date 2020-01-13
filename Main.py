import pygame
import os
import sys

pygame.init()

# TODO ПОПРАВИТЬ РАССТОЯНИЯ МЕЖДУ СПРАЙТАМИ / ВЫРЕЗАТЬ ИХ ПО ОТДЕЛЬНОСТИ
# Первостепенные константы

size = width, height = 800, 600
Display = pygame.display.set_mode(size)
tile_width = tile_height = 50
UP = 273
LEFT = 276
RIGHT = 275
ATTACK = pygame.K_a
GRAVITY = 0.15
PLAYER_ATTACKED = False

# Первостепенные функции


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, collorkey=None, transform=None):
    fullname = os.path.join('data\\sprites', name)
    image = pygame.image.load(fullname)
    if collorkey:
        if collorkey == -1:
            collorkey = image.get_at((0, 0))
        image.set_colorkey(collorkey)
    else:
        image = image.convert_alpha()
    return image

# группы


all_sprite = pygame.sprite.Group()
all_sprite_without_player = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bakcground_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tile_images = {'grass': load_image(
    'jungle_test.png'), 'dirt': load_image('jungle_dirt.png'), 'long': load_image('jungle_test_long.png')}
player_images = {'run_r': load_image('player_run_r.png'), 'run_l': load_image('player_run_l.png'), 'idle_r': load_image(
    'player_idle_r.png'), 'idle_l': load_image('player_idle_l.png'), 'attack_r': load_image('player_attack_r.png'),
    'attack_l': load_image('player_attack_l.png')}
player_image = load_image('knight_test_l.png')
enemy_images = {'run_r': load_image('skel_run_r.png'), 'run_l': load_image(
    'skel_run_l.png'), 'attack_r': load_image('skel_attack_r.png'), 'attack_l': load_image('skel_attack_l.png'),
    'dead_r': load_image('skel_dead_r.png'), 'dead_l': load_image('skel_dead_l.png')}

# классы


class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprite)
        self.cur_sprite = 0
        self.cur_sprite_attack = 0
        self.frames_run = [self.cut_shet(player_images['run_r'], 8, 1), self.cut_shet(
            player_images['run_l'], 8, 1)]
        self.frames_run[1].reverse()
        self.frame_idle = [self.cut_shet(player_images['idle_r'], 15, 1), self.cut_shet(
            player_images['idle_l'], 15, 1)]
        self.frame_idle[1].reverse()
        self.frame_attack = [self.cut_shet(player_images['attack_r'], 22, 1), self.cut_shet(
            player_images['attack_l'], 22, 1)]
        self.frame_attack[1].reverse()
        self.image = self.frame_idle[0][0]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.Right = False
        self.Left = False
        self.Up = False
        self.can_jump = True
        self.Attack = False
        self.DEAD = False
        self.last_direct = RIGHT
        self.speed_x = 300
        self.speed_y = 0

    def cut_shet(self, sheet, columns, rows):
        cur_frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() //
                                columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_loc = (self.rect.w * i, self.rect.h * j)
                cur_frames.append(sheet.subsurface(
                    pygame.Rect(frame_loc, self.rect.size)))
        for i in range(rows * columns):
            cur_frames[i] = pygame.transform.scale(cur_frames[i], (cur_frames[i].get_width(
            ) + tile_width, cur_frames[i].get_height() + tile_height))
        return cur_frames

    def action_on(self, *sides):

        for el in sides:
            if el == LEFT:
                self.Left = True

            elif el == RIGHT:
                self.Right = True

            if el == UP:
                self.Up = True

            if el == ATTACK:
                self.Attack = True

    def action_Off(self, *sides):
        for el in sides:
            if el == LEFT:
                self.Left = False

            elif el == RIGHT:
                self.Right = False

            if el == UP:
                self.Up = False

            if el == ATTACK:
                self.Attack = False

    def update(self):
        for el in pygame.sprite.groupcollide(enemy_group, player_group, False, False, pygame.sprite.collide_mask):
            if self.Attack:
                if (self.cur_sprite_attack >= 6 and self.cur_sprite_attack <= 8) or (self.cur_sprite_attack >= 1 and self.cur_sprite_attack <= 12) or (self.cur_sprite_attack >= 18 and self.cur_sprite_attack <= 19):
                    el.dead = True
                elif el.cur_sprite_attack >= 8 and el.cur_sprite_attack <= 10 and el.Attack:
                    self.DEAD = True

        if self.Right:
            self.rect = self.rect.move(-(-self.speed_x // FPS), 0)
            self.last_direct = RIGHT
            if pygame.sprite.spritecollideany(self, tiles_group, pygame.sprite.collide_mask):
                self.rect = self.rect.move(-self.speed_x // FPS, 0)

        elif self.Left:
            self.rect = self.rect.move(-self.speed_x // FPS, 0)
            self.last_direct = LEFT
            if pygame.sprite.spritecollideany(self, tiles_group, pygame.sprite.collide_mask):
                self.rect = self.rect.move(-(-self.speed_x // FPS), 0)

        if not self.can_jump:
            self.Up = False

        if self.Up and self.can_jump:
            self.speed_y = -6.2
            self.Up = False
            self.can_jump = False

        if not self.Up:
            self.rect = self.rect.move(0, self.speed_y)
            if pygame.sprite.spritecollideany(self, tiles_group, pygame.sprite.collide_mask):
                self.rect = self.rect.move(0, -self.speed_y)
                if self.speed_y >= 0:
                    self.can_jump = True
                    self.speed_y = 1
                if self.speed_y < 0:
                    self.speed_y = 0
            self.speed_y += GRAVITY
            if self.speed_y > 5:
                self.speed_y = 5

    def animation(self):
        if self.Right or self.Left:
            self.cur_sprite = (self.cur_sprite + 1) % len(self.frames_run[0])
            if self.Right:
                self.image = self.frames_run[0][self.cur_sprite]
            elif self.Left:
                self.image = self.frames_run[1][self.cur_sprite]

        else:
            self.cur_sprite = (self.cur_sprite + 1) % len(self.frame_idle[0])
            if self.last_direct == RIGHT:
                self.image = self.frame_idle[0][self.cur_sprite]
            else:
                self.image = self.frame_idle[1][self.cur_sprite]

        if self.Attack:
            self.cur_sprite_attack = (
                self.cur_sprite_attack + 1) % len(self.frame_attack[0])
            if self.last_direct == RIGHT:
                self.image = self.frame_attack[0][self.cur_sprite_attack]
            if self.last_direct == LEFT:
                self.image = self.frame_attack[1][self.cur_sprite_attack]
        else:
            self.cur_sprite_attack = 0
        prev_cen = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = prev_cen
        self.mask = pygame.mask.from_surface(self.image)


class Skelet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprite)
        self.cur_sprite = 0
        self.cur_sprite_attack = 0
        self.dead_spr = 0
        self.frames_run = [self.cut_shet(enemy_images['run_r'], 13, 1), self.cut_shet(
            enemy_images['run_l'], 13, 1)]
        self.frames_run[1].reverse()
        self.image = self.frames_run[0][0]
        self.frames_attack = [self.cut_shet(
            enemy_images['attack_r'], 18, 1), self.cut_shet(enemy_images['attack_l'], 18, 1)]
        self.dead_frames = [self.cut_shet(enemy_images['dead_r'], 15, 1), self.cut_shet(enemy_images['dead_l'], 15, 1)]
        self.dead_frames[1].reverse()
        self.frames_run[1].reverse()
        self.frames_attack[1].reverse()
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.frames_run[0][0])
        self.Right = False
        self.Left = True
        self.dead = False
        self.can_move = True
        self.Attack = False
        self.speed_x = 80
        self.speed_y = 0

    def cut_shet(self, sheet, columns, rows):
        cur_frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() //
                                columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_loc = (self.rect.w * i, self.rect.h * j)
                cur_frames.append(sheet.subsurface(
                    pygame.Rect(frame_loc, self.rect.size)))
        for i in range(rows * columns):
            cur_frames[i] = pygame.transform.scale(cur_frames[i], (cur_frames[i].get_width(
            ) + tile_width // 2, cur_frames[i].get_height() + tile_height // 2))
        return cur_frames

    def animation(self):
        if not self.dead:
            if self.Attack:
                if self.Right:
                    self.image = self.frames_attack[0][self.cur_sprite_attack]
                    self.cur_sprite_attack = (
                        self.cur_sprite_attack + 1) % len(self.frames_attack[0])
                else:
                    self.image = self.frames_attack[1][self.cur_sprite_attack]
                    self.cur_sprite_attack = (
                        self.cur_sprite_attack + 1) % len(self.frames_attack[0])

            else:
                self.cur_sprite = (self.cur_sprite +
                                   1) % len(self.frames_run[0])
                if self.Right:
                    self.image = self.frames_run[0][self.cur_sprite]
                elif self.Left:
                    self.image = self.frames_run[1][self.cur_sprite]
            x, y = self.rect.center
            y_b = self.rect.bottom
            self.rect = self.image.get_rect()

            if self.Attack:
                self.rect.center = (x, y)
                self.rect.bottom = (y_b)
            else:
                self.rect.center = (x, y)

            self.mask = pygame.mask.from_surface(self.image)
        else:
            if self.dead_spr < 15:
                if self.Right:
                    self.image = self.dead_frames[0][self.dead_fdead_sprrames]
                else:
                    self.image = self.dead_frames[1][self.dead_spr]
                self.dead_spr += 1
                x, y = self.rect.center
                y_b = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.center = (x, y)
                self.rect.bottom = (y_b)
                self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        if self.dead:
            self.cur_sprite_attack = 0
            pass

        else:
            rast = self.rect.centerx - player.rect.centerx
            self.can_move = True
            self.Attack = False

            if abs(rast) <= 50:
                if rast <= 0 and self.Right:
                    self.can_move = False
                    self.Attack = True

                elif rast >= 0 and self.Left:
                    self.can_move = False
                    self.Attack = True

            if self.can_move:
                self.Attack = False

                if self.Right:
                    self.rect = self.rect.move(-(-self.speed_x // FPS), 0)
                    if pygame.sprite.spritecollideany(self, tiles_group, pygame.sprite.collide_mask):
                        self.rect = self.rect.move(-self.speed_x // FPS, 0)
                        self.Right = False
                        self.Left = True

                elif self.Left:
                    self.rect = self.rect.move(-self.speed_x // FPS, 0)
                    if pygame.sprite.spritecollideany(self, tiles_group, pygame.sprite.collide_mask):
                        self.rect = self.rect.move(-(-self.speed_x // FPS), 0)
                        self.Right = True
                        self.Left = False

                self.rect = self.rect.move(0, self.speed_y)
                if pygame.sprite.spritecollideany(self, tiles_group, pygame.sprite.collide_mask):
                    self.rect = self.rect.move(0, -self.speed_y)
                    if self.speed_y < 0:
                        self.speed_y = 0
                self.speed_y += GRAVITY
                if self.speed_y > 5:
                    self.speed_y = 5


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, long=1):
        super().__init__(tiles_group, all_sprite, all_sprite_without_player)
        self.image = pygame.transform.smoothscale(
            tile_images[tile_type], (tile_width * long, tile_height))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        if obj in player_group:
            if player.Attack and player.cur_sprite_attack > 13 and player.cur_sprite_attack < 18:
                x, y = obj.rect.center
                if player.last_direct == RIGHT:
                    x += 1
                    obj.rect.center = (x, y)
                else:
                    x -= 1
                    obj.rect.center = (x, y)
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


# второстепенные функции (вспомогательные)


def load_level(filname):
    filname = 'data/levels/' + filname
    with open(filname, 'r') as MapFile:
        level_map = [line.strip() for line in MapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for i in range(5):
        back_sprit = pygame.sprite.Sprite(bakcground_group)
        back_sprit.image = pygame.transform.scale(
            load_image(f'plx-{i}.png'), size)
        back_sprit.rect = back_sprit.image.get_rect()
        back_sprit.rect.x = 0
        back_sprit.rect.y = 0
    spr_2_long = 1

    for y in range(len(level)):
        for x in range(len(level[y])):
            if spr_2_long != 1:
                spr_2_long -= 1
                continue
            if level[y][x] == '#':
                if x != len(level[y]) - 1:
                    if level[y][x + 1] == '#':
                        spr_2_long += 1
                        for z in range(x + 2, len(level[y])):
                            if level[y][z] == '#':
                                spr_2_long += 1
                                if spr_2_long == 7:
                                    break
                            else:
                                break
                Tile('long', x, y, spr_2_long)

            elif level[y][x] == '@':
                new_player = Player(x, y - 1)

            elif level[y][x] == 's':
                Skelet(x, y)

    return new_player, x, y


FPS = 200
Clock = pygame.time.Clock()
camera = Camera()

player, level_x, level_y = generate_level(load_level('level_1.txt'))
camera.update(player)


Is_game_on = True
Time_count = 0

while Is_game_on:
    if player.DEAD == True:
        break
    Display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            index = [index for index, value in enumerate(
                pygame.key.get_pressed()) if value == 1]
            player.action_on(*index)

        elif event.type == pygame.KEYUP:
            up_keys = []
            if event.key == UP:
                up_keys.append(UP)
            if event.key == LEFT:
                up_keys.append(LEFT)
            elif event.key == RIGHT:
                up_keys.append(RIGHT)
            if event.key == ATTACK:
                up_keys.append(ATTACK)
            player.action_Off(*up_keys)
    if Time_count >= 60:
        Time_count = 0
        player.animation()
        for el in enemy_group:
            el.animation()
    player_group.update()
    enemy_group.update()
    bakcground_group.draw(Display)
    all_sprite.draw(Display)
    pygame.display.flip()
    camera.update(player)
    for el in all_sprite:
        camera.apply(el)
    Time_count += Clock.tick(FPS)
