import random
import sys
import pygame as pg
import time



WIDTH, HEIGHT = 1000, 600

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kkk_img = pg.image.load("ex02/fig/8.png") # kkk_imgでこうかとんがばくだんに触れたときに変更後の画像を置いている 
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kkk_img = pg.transform.rotozoom(kkk_img, 0, 2.0)
    kkk_rct = kkk_img.get_rect()
    
    kk_rct = kk_img.get_rect()  # 練習3
    kk_rct.center = 900, 400

    

    bb_img = pg.Surface((20, 20))  # 練習1
    bb_img.set_colorkey((0, 0, 0))  # 練習1
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)

    bb_rct = bb_img.get_rect()  # 練習2
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
           
        if kk_rct.colliderect(bb_rct):
            kk_img = kkk_img
            print("Game Over")
            screen.blit(kk_img, kk_rct)
            pg.display.update()
            time.sleep(3)
            return
        
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]


        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) 
        
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) 
        #rotated_kk_img = pg.transform.rotozoom(kk_img, tmr % 360, 2.0)
        screen.blit(kk_img, kk_rct)
    

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx, vy)
            
        screen.blit(bb_img, bb_rct)

    
        pg.display.update()
        tmr += 1
        clock.tick(20)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()