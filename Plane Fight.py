import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from random import *
from pygame.locals import *

# 生成主界面
pygame.init()
pygame.mixer.init()
bg_size = width, height = 500, 600
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机小游戏")

# 加载图片资源
bg = pygame.image.load("image/background.png").convert()
bg2 = pygame.image.load("image/background.png").convert()
start = pygame.image.load("image/start.png").convert_alpha()
start2 = pygame.image.load("image/start2.png").convert_alpha()
end = pygame.image.load("image/end.png").convert_alpha()
end2 = pygame.image.load("image/end2.png").convert_alpha()

# 加载声音资源
pygame.mixer.music.load("sound/bgm.mp3")
pygame.mixer.music.set_volume(0.3)
select = pygame.mixer.Sound("sound/单击.wav")
select.set_volume(0.1)
upgrade_sound = pygame.mixer.Sound("sound/upgrade_sound.wav")
upgrade_sound.set_volume(0.5)
ult_sound = pygame.mixer.Sound("sound/炸弹.wav")
ult_sound.set_volume(0.3)
shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
shoot_sound.set_volume(0.1)
s_enemy_die = pygame.mixer.Sound("sound/pop.wav")
s_enemy_die.set_volume(0.5)
m_enemy_die = pygame.mixer.Sound("sound/中敌人.wav")
m_enemy_die.set_volume(0.5)
b_enemy_die = pygame.mixer.Sound("sound/大敌人.wav")
b_enemy_die.set_volume(0.5)
get_bullet_sound = pygame.mixer.Sound("sound/子弹补给.wav")
get_bullet_sound.set_volume(0.5)
get_ult_sound = pygame.mixer.Sound("sound/大招补给.wav")
get_ult_sound.set_volume(0.5)


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)


def ui():
    # 开始菜单
    while 1:
        screen.blit(pygame.transform.scale(bg, bg_size), (0, 0))
        screen.blit(start, (180, 350))
        screen.blit(end, (193, 430))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                """"print('[mouse motion]', ' #', event.pos, event.rel, event.buttons)"""
                if event.pos[0] in range(220, 294) and event.pos[1] in range(453, 480):
                    screen.blit(end2, (193, 430))
                    select.play()
                if event.pos[0] in range(205, 308) and event.pos[1] in range(371, 401):
                    screen.blit(start2, (180, 350))
                    select.play()
                pygame.display.flip()
            elif event.type == MOUSEBUTTONDOWN:
                if event.pos[0] in range(220, 294) and event.pos[1] in range(453, 480):
                    pygame.quit()
                if event.pos[0] in range(205, 308) and event.pos[1] in range(371, 401) and event.button:
                    main()


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.MidEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    # 播放背景音乐
    pygame.mixer.music.play(-1)
    # 生成我方飞机
    me = myplane.MyPlane(bg_size)
    enemies = pygame.sprite.Group()
    # 生成敌方小飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    # 生成敌方中飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 8)
    # 生成敌方大飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 5)
    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 3
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 6
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx + 6, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx - 15, me.rect.centery)))
    clock = pygame.time.Clock()
    # 统计得分
    score = 0
    score_font = pygame.font.Font('font/msyhbd.ttc', 20)
    # 暂停功能
    pause = False
    pause_btn = pygame.image.load('image/暂停.png').convert_alpha()
    pause_btn2 = pygame.image.load('image/暂停2.png').convert_alpha()
    resume_btn = pygame.image.load('image/恢复.png').convert_alpha()
    resume_btn2 = pygame.image.load('image/恢复2.png').convert_alpha()
    pause_rect = pause_btn.get_rect()
    pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
    pause_image = pause_btn

    # 设置难度等级
    level = 1

    # 全屏大招
    ult_image = pygame.image.load('image/大招.png').convert_alpha()
    ult_rect = ult_image.get_rect()
    ult_font = pygame.font.Font('font/msyhbd.ttc', 30)
    ult_num = 3

    # 30秒发一个补给(调试-1s一个)
    bullet_supply = supply.Bullet_Supply(bg_size)
    ult_supply = supply.Ult_Supply(bg_size)
    supply_time = USEREVENT
    pygame.time.set_timer(supply_time, 30 * 1000)

    # 子弹时常定时器
    bullet2_time = USEREVENT + 1
    # 切换子弹
    is_bullet2 = False
    # 解除无敌计时器
    INVINCIBLE_TIME = USEREVENT +2
    # 生命数量
    life_image = pygame.image.load('image/生命.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3
    # 组织重复存档
    recorded = False
    # 用来延迟
    delay = 100

    running = True

    while running:
        # 生成战斗背景
        screen.blit(pygame.transform.scale(bg2, bg_size), (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    pause = not pause
                    if pause:
                        pygame.time.set_timer(supply_time, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(supply_time, 30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause_image = resume_btn2
                    else:
                        pause_image = pause_btn2
                else:
                    if pause:
                        pause_image = resume_btn
                    else:
                        pause_image = pause_btn
            # 大招
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if ult_num:
                        ult_num -= 1
                        ult_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == supply_time:
                if choice([True, False]):
                    ult_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == bullet2_time:
                is_bullet2 = False
                pygame.time.set_timer(bullet2_time, 0)
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)
        # 根据得分增加难度
        if level == 1 and score > 10000:
            level = 2
            upgrade_sound.play()
            # 增加3架小型敌人，2架中型敌人，1架大型敌人
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(small_enemies, enemies, 2)
            add_big_enemies(small_enemies, enemies, 1)
            # 提升小型敌人速度
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 30000:
            level = 3
            upgrade_sound.play()
            # 增加5架小型敌人，3架中型敌人，2架大型敌人
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(small_enemies, enemies, 3)
            add_big_enemies(small_enemies, enemies, 2)
            # 提升小型敌人速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 100000:
            level = 4
            upgrade_sound.play()
            # 增加5架小型敌人，3架中型敌人，2架大型敌人
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(small_enemies, enemies, 3)
            add_big_enemies(small_enemies, enemies, 2)
            # 提升小型敌人速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 300000:
            level = 5
            upgrade_sound.play()
            # 增加5架小型敌人，3架中型敌人，2架大型敌人
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(small_enemies, enemies, 3)
            add_big_enemies(small_enemies, enemies, 2)
            # 提升小型敌人速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        if life_num and not pause:
            # 玩家操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveup()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.movedown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveleft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveright()

            # 绘制大招补给
            if ult_supply.active:
                screen.blit(ult_supply.image, ult_supply.rect)
                ult_supply.move()
                if pygame.sprite.collide_rect(ult_supply, me):
                    get_ult_sound.play()
                    if ult_num < 3:
                        ult_num += 1
                    ult_supply.active = False
            # 绘制子弹补给
            if bullet_supply.active:
                screen.blit(bullet_supply.image, bullet_supply.rect)
                bullet_supply.move()
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_bullet2 = True
                    pygame.time.set_timer(bullet2_time, 18*1000)
                    bullet_supply.active = False
            # 发射子弹
            if not(delay % 10):
                shoot_sound.play()
                if is_bullet2:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx + 6, me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx - 15, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset((me.rect[0] + 11, me.rect[1] - 10))
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False,)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            # 绘制大敌人
            for each in big_enemies:
                if each.active:
                    each.move()
                    screen.blit(pygame.transform.scale(each.image, (100, 100)), each.rect)
                    # 血条
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left, each.rect.top - 5),
                                     2)
                    # 生命大于20%显示绿血，否则红
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5), 2)
                else:
                    # 坠毁
                    b_enemy_die.play()
                    score += 5000
                    score_b = score_font.render('5000', True, RED)
                    screen.blit(score_b, (each.rect.left, each.rect.top))
                    each.reset()

            # 绘制中敌人
            for each in mid_enemies:
                if each.active:
                    each.move()
                    screen.blit(pygame.transform.scale(each.image, (50, 50)), each.rect)
                    # 血条
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left, each.rect.top - 5),
                                     2)
                    # 生命大于20%显示绿血，否则红
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5), 2)
                else:
                    # 坠毁
                    m_enemy_die.play()
                    score += 1000
                    score_m = score_font.render('1000', True, GREEN)
                    screen.blit(score_m, (each.rect.left, each.rect.top))
                    each.reset()

            # 绘制小敌人
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(pygame.transform.scale(each.image, (30, 30)), each.rect)
                else:
                    # 坠毁
                    score += 500
                    score_s = score_font.render('500', True, WHITE)
                    screen.blit(score_s, (each.rect.left, each.rect.top))
                    s_enemy_die.play()
                    each.reset()

            # 碰撞检测
            enemy_down = pygame.sprite.spritecollide(me, enemies, False,)
            if enemy_down and not me.invincible:
                me.active = False
                for e in enemy_down:
                    e.active = False
            # 绘制主角飞机
            if me.active:
                screen.blit(me.image, me.rect)
            else:
                # 坠毁
                life_num -= 1
                me.reset()
                pygame.time.set_timer(INVINCIBLE_TIME, 3*1000)
            # 难度条
            pygame.draw.line(screen, WHITE,
                             (200, 30),
                             (314, 30),
                             8)
            # 根据等级绘制难度条
            if level == 1:
                level_length = score / 10000
                level_color = BLACK
            elif level == 2:
                level_length = (score-10000) / 20000
                level_color = GREEN
            elif level == 3:
                level_length = (score-20000) / 80000
                level_color = RED
            elif level == 4:
                level_length = 1
                level_color = PURPLE
            pygame.draw.line(screen, level_color,
                             (200, 30),
                             (200 + 114 * level_length, 30),
                             4)
            # 绘制生命数
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,
                                (width - 10 - (i+1)*life_rect.width,
                                 height - 10 - life_rect.height))
            # 绘制大招数量
            ult_text = ult_font.render('× %d [space]' % ult_num, True, WHITE)
            text_rect = ult_text.get_rect()
            screen.blit(ult_image, (10, height - 10 - ult_rect.height))
            screen.blit(ult_text, (20 + ult_rect.width, height - 5 - text_rect.height))

            # 绘制难度等级
            up_font = pygame.font.Font('font/msyhbd.ttc', 18)
            up_text = up_font.render('难度等级 : × %d' % level, True, WHITE)
            screen.blit(up_text, (int(width / 2 - 50), 0))

        # 绘制游戏结束画面
        elif life_num == 0:
            # 音乐停止
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(supply_time, 0)
            # 好懒不想写结束界面，返回主界面。。。
            ui()

        # 绘制得分
        score_text = score_font.render('score : %s' % str(score), True, WHITE)
        screen.blit(score_text, (10, 0))
        # 绘制暂停按钮
        screen.blit(pause_image, pause_rect)

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        ui()
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
