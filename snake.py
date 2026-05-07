import random
import turtle

# ------------------------
# 配置
# ------------------------
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
MOVE_STEP = 20
INITIAL_DELAY_MS = 120


class SnakeGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("贪吃蛇")
        self.screen.bgcolor("black")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)

        self.delay = INITIAL_DELAY_MS
        self.running = True

        # 蛇头
        self.head = turtle.Turtle("square")
        self.head.color("lime")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"

        # 食物
        self.food = turtle.Turtle("circle")
        self.food.color("red")
        self.food.penup()
        self.relocate_food()

        # 身体
        self.segments = []

        # 分数显示
        self.score = 0
        self.high_score = 0
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.goto(0, SCREEN_HEIGHT // 2 - 40)
        self.update_score()

        self.bind_keys()

    def bind_keys(self):
        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction("up"), "Up")
        self.screen.onkeypress(lambda: self.set_direction("down"), "Down")
        self.screen.onkeypress(lambda: self.set_direction("left"), "Left")
        self.screen.onkeypress(lambda: self.set_direction("right"), "Right")
        self.screen.onkeypress(self.restart, "r")

    def set_direction(self, direction):
        # 防止直接反向
        opposite = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        if self.head.direction != opposite.get(direction):
            self.head.direction = direction

    def relocate_food(self):
        x = random.randrange(-SCREEN_WIDTH // 2 + MOVE_STEP, SCREEN_WIDTH // 2 - MOVE_STEP, MOVE_STEP)
        y = random.randrange(-SCREEN_HEIGHT // 2 + MOVE_STEP, SCREEN_HEIGHT // 2 - MOVE_STEP, MOVE_STEP)
        self.food.goto(x, y)

    def update_score(self):
        self.pen.clear()
        self.pen.write(
            f"分数: {self.score}  最高分: {self.high_score}   (方向键移动，R 重新开始)",
            align="center",
            font=("Arial", 14, "normal"),
        )

    def move_head(self):
        x, y = self.head.xcor(), self.head.ycor()
        if self.head.direction == "up":
            self.head.sety(y + MOVE_STEP)
        elif self.head.direction == "down":
            self.head.sety(y - MOVE_STEP)
        elif self.head.direction == "left":
            self.head.setx(x - MOVE_STEP)
        elif self.head.direction == "right":
            self.head.setx(x + MOVE_STEP)

    def hit_wall(self):
        half_w = SCREEN_WIDTH // 2
        half_h = SCREEN_HEIGHT // 2
        return (
            self.head.xcor() > half_w - MOVE_STEP
            or self.head.xcor() < -half_w + MOVE_STEP
            or self.head.ycor() > half_h - MOVE_STEP
            or self.head.ycor() < -half_h + MOVE_STEP
        )

    def hit_self(self):
        for seg in self.segments:
            if seg.distance(self.head) < 1:
                return True
        return False

    def reset_snake(self):
        for seg in self.segments:
            seg.goto(1000, 1000)
        self.segments.clear()
        self.head.goto(0, 0)
        self.head.direction = "stop"

    def game_over(self):
        self.running = False
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.update_score()
        self.reset_snake()
        self.delay = INITIAL_DELAY_MS
        self.running = True

    def restart(self):
        self.game_over()

    def grow(self):
        seg = turtle.Turtle("square")
        seg.color("green")
        seg.penup()
        self.segments.append(seg)

    def move_segments(self):
        # 从尾巴开始，跟随前一节
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)

        # 第一节跟随蛇头
        if self.segments:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

    def tick(self):
        if self.running:
            self.screen.update()

            # 吃到食物
            if self.head.distance(self.food) < 15:
                self.relocate_food()
                self.grow()
                self.score += 10
                if self.score > self.high_score:
                    self.high_score = self.score
                self.update_score()
                # 每次加速一点，最低 60ms
                self.delay = max(60, self.delay - 2)

            self.move_segments()
            self.move_head()

            if self.hit_wall() or self.hit_self():
                self.game_over()

        self.screen.ontimer(self.tick, self.delay)

    def run(self):
        self.tick()
        self.screen.mainloop()


if __name__ == "__main__":
    SnakeGame().run()
