import pygame
import pymunk
import random

# --- 設定 ---
WIDTH, HEIGHT = 400, 650
FPS = 60

# フルーツの定義（半径、色、スコア）
FRUIT_TYPES = [
    {"radius": 15, "color": (255, 50, 50), "score": 1},    # さくらんぼ
    {"radius": 22, "color": (255, 100, 150), "score": 3},  # いちご
    {"radius": 30, "color": (150, 50, 255), "score": 6},   # ぶどう
    {"radius": 40, "color": (255, 180, 0), "score": 10},   # デコポン
    {"radius": 52, "color": (255, 120, 0), "score": 15},   # かき
    {"radius": 65, "color": (255, 50, 0), "score": 21},    # りんご
    {"radius": 78, "color": (255, 230, 100), "score": 28}, # なし
    {"radius": 92, "color": (255, 200, 200), "score": 36}, # もも
    {"radius": 105, "color": (200, 255, 100), "score": 45},# パイナップル
    {"radius": 120, "color": (50, 200, 50), "score": 55},  # メロン
    {"radius": 140, "color": (0, 150, 0), "score": 66},    # スイカ
]

class Fruit:
    def __init__(self, space, pos, level):
        self.level = level
        conf = FRUIT_TYPES[level]
        mass = 1 + level * 0.5 # 大きいほど少し重くする
        moment = pymunk.moment_for_circle(mass, 0, conf["radius"])
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, conf["radius"])
        self.shape.elasticity = 0.2
        self.shape.friction = 0.8
        self.shape.collision_type = 1
        self.shape.fruit_level = level
        space.add(self.body, self.shape)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("図形で作るスイカゲーム")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    space = pymunk.Space()
    space.gravity = (0, 900)

    # 壁の設定（(x, y)座標）
    WALL_LEFT, WALL_RIGHT, WALL_BOTTOM = 50, 350, 600
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (WALL_LEFT, 150), (WALL_LEFT, WALL_BOTTOM), 5),
        pymunk.Segment(static_body, (WALL_RIGHT, 150), (WALL_RIGHT, WALL_BOTTOM), 5),
        pymunk.Segment(static_body, (WALL_LEFT, WALL_BOTTOM), (WALL_RIGHT, WALL_BOTTOM), 5)
    ]
    for wall in walls:
        wall.elasticity = 0.5
        space.add(wall)

    to_remove = []
    to_add = []
    score = 0
    next_level = random.randint(0, 2) # 最初は小さいのだけ

    # 衝突ハンドラー
    def post_solve_collision(arbiter, space, data):
        nonlocal score
        s1, s2 = arbiter.shapes
        if hasattr(s1, "fruit_level") and hasattr(s2, "fruit_level"):
            if s1.fruit_level == s2.fruit_level and s1.fruit_level < len(FRUIT_TYPES) - 1:
                if s1 not in to_remove and s2 not in to_remove:
                    pos = (s1.body.position + s2.body.position) / 2
                    level = s1.fruit_level + 1
                    to_add.append((pos, level))
                    to_remove.extend([s1, s2])
                    score += FRUIT_TYPES[s1.fruit_level]["score"]

    space.on_collision(1, 1, post_solve=post_solve_collision)
    game_over = False
    deadline_y = 150  # このラインを超えたら警告
    over_time_counter = 0  # ラインを超えている時間（フレーム数）
    LIMIT_TIME = FPS * 2  # 2秒間超え続けたらゲームオーバー
    

    running = True
    while running:
        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mx, _ = pygame.mouse.get_pos()
                r = FRUIT_TYPES[next_level]["radius"]
                drop_x = max(WALL_LEFT + 7 + r, min(WALL_RIGHT - 7 - r, mx))
                Fruit(space, (drop_x, 140), next_level)
                next_level = random.randint(0, 2)
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main() # 関数を再帰呼び出ししてリセット
                    return

        # --- 物理演算 ---
        if not game_over:
            space.step(1/FPS)

        # --- ゲームオーバー判定ロジック ---
        highest_y = HEIGHT # 画面の一番下が基準
        
        # 合成処理
        for shape in set(to_remove):
            if shape.body in space.bodies:
                space.remove(shape, shape.body)
        for pos, lvl in to_add:
            Fruit(space, pos, lvl)
        to_remove.clear()
        to_add.clear()

        # --- 描画 ---
        screen.fill((255, 250, 240)) # 背景：アイボリー
        line_color = (255, 0, 0) if over_time_counter > 0 else (200, 200, 200)
        pygame.draw.line(screen, line_color, (WALL_LEFT, deadline_y), (WALL_RIGHT, deadline_y), 2)
        
        # 容器の描画
        pygame.draw.rect(screen, (139, 69, 19), (WALL_LEFT-5, 150, 5, 455)) # 左壁
        pygame.draw.rect(screen, (139, 69, 19), (WALL_RIGHT, 150, 5, 455)) # 右壁
        pygame.draw.rect(screen, (139, 69, 19), (WALL_LEFT-5, WALL_BOTTOM, 310, 5)) # 底

        # フルーツの描画
        current_highest_y = HEIGHT
        for shape in space.shapes:
            if hasattr(shape, "fruit_level"):
                pos = shape.body.position
                angle = shape.body.angle
                level = shape.fruit_level
                conf = FRUIT_TYPES[level]
                # radius = FRUIT_TYPES[level]["radius"]
                
                # 本体
                pygame.draw.circle(screen, conf["color"], (int(pos.x), int(pos.y)), conf["radius"])
                # 輪郭
                pygame.draw.circle(screen, (50, 50, 50), (int(pos.x), int(pos.y)), conf["radius"], 2)
                # 光沢（少し立体的に）
                shiny_x = pos.x - conf["radius"] * 0.3
                shiny_y = pos.y - conf["radius"] * 0.3
                pygame.draw.circle(screen, (255, 255, 255), (int(shiny_x), int(shiny_y)), conf["radius"] * 0.2)
                top_y = shape.body.position.y - shape.radius
                if top_y < highest_y:
                    highest_y = top_y

        # 投下待ちフルーツのガイド表示
        if not game_over:
            mx, _ = pygame.mouse.get_pos()
            r = FRUIT_TYPES[next_level]["radius"]
            guide_x = max(WALL_LEFT+ 7 + r, min(WALL_RIGHT - 7 - r, mx))
            pygame.draw.circle(screen, FRUIT_TYPES[next_level]["color"], (guide_x, 120), r, 2)
            pygame.draw.line(screen, (200, 200, 200), (guide_x, 120), (guide_x, 150), 1)

        if highest_y < deadline_y:
            over_time_counter += 1
            if over_time_counter >= LIMIT_TIME:
                game_over = True
        else:
            # ラインを下回っていればカウンターをリセット
            over_time_counter = 0
        # スコア表示
        score_text = font.render(f"Score: {score}", True, (50, 50, 50))
        screen.blit(score_text, (20, 20))
        # ゲームオーバー画面の表示
        if game_over:
            # 背景を少し暗くするオーバーレイ
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            go_text = font.render("GAME OVER", True, (255, 255, 255))
            retry_text = font.render("Press 'R' to Restart", True, (200, 200, 200))
            screen.blit(go_text, (WIDTH//2 - 80, HEIGHT//2 - 20))
            screen.blit(retry_text, (WIDTH//2 - 100, HEIGHT//2 + 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()