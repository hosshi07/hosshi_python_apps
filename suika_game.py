import pygame
import pymunk
import pymunk.pygame_util

# --- 設定 ---
WIDTH, HEIGHT = 400, 600
FPS = 60
# フルーツのサイズと色の定義 (段階的に大きくする)
FRUIT_TYPES = [
    {"radius": 15, "color": (255, 0, 0), "score": 10},   # さくらんぼ
    {"radius": 25, "color": (255, 165, 0), "score": 20}, # いちご
    {"radius": 35, "color": (138, 43, 226), "score": 40},# ぶどう
    {"radius": 50, "color": (255, 255, 0), "score": 60}, # デコポン
    {"radius": 70, "color": (255, 69, 0), "score": 80},  # かき
]

class Fruit:
    def __init__(self, space, pos, level):
        self.level = level
        self.radius = FRUIT_TYPES[level]["radius"]
        self.color = FRUIT_TYPES[level]["color"]
        
        # 物理体の設定
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.5
        self.shape.friction = 0.5
        self.shape.collision_type = 1 # 衝突判定用ID
        self.shape.fruit_level = level # カスタム属性でレベルを保持
        
        space.add(self.body, self.shape)

def setup_space():
    space = pymunk.Space()
    space.gravity = (0, 900) # 重力の設定
    
    # 壁の作成 (左、右、下)
    static_lines = [
        pymunk.Segment(space.static_body, (50, 100), (50, 550), 5),
        pymunk.Segment(space.static_body, (350, 100), (350, 550), 5),
        pymunk.Segment(space.static_body, (50, 550), (350, 550), 5)
    ]
    for line in static_lines:
        line.elasticity = 0.5
        space.add(line)
    return space

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    
    space = pymunk.Space()
    space.gravity = (0, 900)

    # 壁の作成
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (50, 100), (50, 550), 5),
        pymunk.Segment(static_body, (350, 100), (350, 550), 5),
        pymunk.Segment(static_body, (50, 550), (350, 550), 5)
    ]
    for wall in walls:
        wall.elasticity = 0.5
        space.add(wall)

    fruits = []
    to_remove = []
    to_add = []

    # 衝突時に呼ばれる関数
    def post_solve_collision(arbiter, space, data):
        s1, s2 = arbiter.shapes
        if hasattr(s1, "fruit_level") and hasattr(s2, "fruit_level"):
            if s1.fruit_level == s2.fruit_level and s1.fruit_level < len(FRUIT_TYPES) - 1:
                # 衝突座標を取得して新しいフルーツを作成
                pos = (s1.body.position + s2.body.position) / 2
                level = s1.fruit_level + 1
                # 削除と追加を予約
                to_add.append((pos, level))
                to_remove.extend([s1, s2])

    # 新しいメソッド「on_collision」を使用
    space.on_collision(1, 1, post_solve=post_solve_collision)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, _ = pygame.mouse.get_pos()
                # 左右の壁の内側に制限
                x = max(65, min(335, x))
                fruits.append(Fruit(space, (x, 120), 0))

        space.step(1/FPS)

        # 合成処理（物理演算ループの外で行う）
        for shape in set(to_remove): # setで重複削除
            if shape.body in space.bodies:
                space.remove(shape, shape.body)
        for pos, lvl in to_add:
            fruits.append(Fruit(space, pos, lvl))
        to_remove.clear()
        to_add.clear()

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()