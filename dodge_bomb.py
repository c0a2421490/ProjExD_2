import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectまたは爆弾Rect
    戻り値:判定結果タプル(横, 縦)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数:screen
    画面をブラックアウト,泣いているこうかとん画像と「Game Over」の文字列を5秒間表示
    """
    # ブラックアウト
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    screen.blit(bg_img,[0, 0])
    gg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(gg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    gg_img.set_alpha(200)
    gg_rect = gg_img.get_rect()
    screen.blit(gg_img, gg_rect)
    # テキスト
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",True, (255, 255, 255))
    txt_rect =txt.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(txt, txt_rect)
    # こうかとん
    kk81_img = pg.image.load("fig/8.png")
    kk81_rct = kk81_img.get_rect()
    kk81_rct.center = (WIDTH/2)-200, HEIGHT/2
    screen.blit(kk81_img, kk81_rct)

    kk82_img = pg.image.load("fig/8.png")
    kk82_rct = kk82_img.get_rect()
    kk82_rct.center = (WIDTH/2)+200, HEIGHT/2
    screen.blit(kk82_img, kk82_rct)

    pg.display.update()
    time.sleep(5)


def kakukaso(tmr) -> tuple[bool, bool]:
    """
    引数:時間
    戻り値:爆弾の大きさと加速度のタプル
    10段階の大きさ、加速度
    """
    # 爆弾移動速度
    vx = 5
    vy = 5
    # 加速度のリスト
    bb_accs = [a for a in range(1, 11)]
    # 拡大爆弾Surfaceのリスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    # 
    avx = vx*bb_accs[min(tmr//500, 9)]
    bb_img = bb_imgs[min(tmr//500, 9)]


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    # こうかとん初期化
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    # 爆弾移動速度
    vx = 5
    vy = 5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        # 背景
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        # こうかとん爆弾が衝突時
        if kk_rct.colliderect(bb_rct):
            gameover(screen)

        # こうかとん&爆弾
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key , mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]  += mv[0]  #上下方向
                sum_mv[1]  += mv[1] #左右方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # 画面外なら
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1]) # 画面内にもどす
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #左右どちらかはみでていたら
            vx *= -1
        if not tate: #上下どちらかはみでていたら
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
