import pygame
import sys
import traceback
import myplane
import ult
import enemy
import bullet
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
pygame.mixer.music.set_volume(0.1)
select = pygame.mixer.Sound("sound/单击.wav")
select.set_volume(0.1)
upgrade_sound = pygame.mixer.Sound("sound/pop.wav")
upgrade_sound.set_volume(0.5)
ult_sound = pygame.mixer.Sound("sound/ult_sound.wav")
ult_sound.set_volume(0.1)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


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

    # 大招
    ulto = ult.Ult(bg_size)

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
                    if ulto.num:
                        ulto.num -= 1
                        ult_sound.play()
                        for each in enemies:
                            screen.blit(ulto.image, ulto.rect)
                            ult_down = pygame.sprite.spritecollide(each, ulto, False, )
                            if ult_down:
                                each.active = False
        # 根据得分增加难度
        if level == 1 and score > 5000:
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

        if not pause:
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

            # 发射子弹
            if not(delay % 10):
                bullet1[bullet1_index].reset((me.rect[0] + 11, me.rect[1] - 10))
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM
            # 检测子弹是否击中
            for b in bullet1:
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

                    each.reset()

            # 碰撞检测
            enemy_down = pygame.sprite.spritecollide(me, enemies, False,)
            if enemy_down:
                me.active = False
                for e in enemy_down:
                    e.active = False
            # 绘制我方飞机
            if me.active:
                screen.blit(pygame.transform.scale(me.image, (30, 30)), me.rect)
            else:
                # 坠毁
                me.reset()

        score_text = score_font.render('score : %s' % str(score), True, WHITE)
        screen.blit(score_text, (10, -5))
        # 暂停按钮
        screen.blit(pause_image, pause_rect)

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        # ui()
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
