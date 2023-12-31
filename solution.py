import pygame
import neat
import os

pygame.init()

# Initialize pygame
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 55)
WINNER = 10
WIN_FONT = pygame.font.SysFont("comicsans", 75)

class Paddle:
    
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width  = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    
    def reset(self):
        self.y = HEIGHT//2 - self.height//2

class Ball:
    COLOR = WHITE
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.x_vel *= -1
        self.y_vel = 0

def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(str(left_score), 1, WHITE)
    right_score_text = SCORE_FONT.render(str(right_score), 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 10))
    win.blit(right_score_text, (WIDTH - WIDTH//4 - right_score_text.get_width()//2, 10))
    for paddle in paddles:
        paddle.draw(win)
    for i in range(10, HEIGHT, HEIGHT//20):
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 2, i, 4, HEIGHT//40))
    ball.draw(win)
    pygame.display.update()

def handle_collisions(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                ball.y_vel = (ball.y - (left_paddle.y + left_paddle.height//2))//10
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                ball.y_vel = (ball.y - (right_paddle.y + right_paddle.height//2))//10
    

    
def handle_keys(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 2:
        left_paddle.move()
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL <= HEIGHT - left_paddle.height - 2:
        left_paddle.move(False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 2:
        right_paddle.move()
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL <= HEIGHT - right_paddle.height - 2:
        right_paddle.move(False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    right_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_keys(keys, left_paddle, right_paddle)
        ball.move()
        handle_collisions(ball, left_paddle, right_paddle)

        if ball.x - ball.radius <= 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif ball.x + ball.radius >= WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        won = False

        if left_score >= WINNER:
            won = True
            win_text = 'Left Player Wins!'
        elif right_score >= WINNER:
            won = True
            win_text = 'Right Player Wins!'
        
        if won:
            text = WIN_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
    
    pygame.quit()

#def eval_genomes(genomes, config):
            
def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    #winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    main()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    run_neat(config)