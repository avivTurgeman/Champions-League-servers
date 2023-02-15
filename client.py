import pygame

# import button

pygame.init()

fps = 30
screen_w = 1000
screen_h = 600
clock = pygame.time.Clock()

# colors
purple = (155, 70, 239)
light_purple = (176, 156, 217)
black = (0, 0, 0)
red = (200, 30, 30)
light_red = (220, 0, 0)
green = (0, 120, 100)
light_green = (0, 200, 100)
blue = (0, 50, 120)
light_blue = (0, 50, 200)

screen = pygame.display.set_mode((screen_w, screen_h))

big_font = pygame.font.Font('freesansbold.ttf', 80)
med_font = pygame.font.Font('freesansbold.ttf', 50)
small_font = pygame.font.Font('freesansbold.ttf', 20)

pygame.display.set_caption("SQL project")


# background_img = pygame.image.load("background_leve1.png")

class button:
    def __init__(self, surface, text, x, y, width, height, name, text_size=17, active_color=light_purple,
                 inactive_color=purple, text_color=black):
        self.screen = surface
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font('freesansbold.ttf', text_size)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.clicked = False
        self.name = name

    def text_to_button(self):
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (self.x + (self.width / 2), self.y + (self.height / 2))
        self.screen.blit(text, text_rect.topleft)

    def click(self):
        global run
        if self.name == "chart":
            chart()
            run = True
        if self.name == "queries":
            queries()
            run = True
        if self.name == "back":
            run = False

    def is_clicked(self):
        click = self.clicked
        self.clicked = False
        return click

    def draw(self):
        cur = pygame.mouse.get_pos()
        if (self.x <= cur[0] <= self.x + self.width) and (self.y <= cur[1] <= self.y + self.height):
            if pygame.mouse.get_pressed()[0] == 1:
                if not self.clicked:
                    self.click()
                    self.clicked = True
            else:
                self.clicked = False
            pygame.draw.rect(self.screen, self.active_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.screen, self.inactive_color, (self.x, self.y, self.width, self.height))
        self.text_to_button()


# buttons
center_x = screen_w / 2
chart_button = button(screen, "full chart", center_x - 200 - 50, 400, 120, 70, "chart", 20, light_green, green)
queries_button = button(screen, "queries", center_x + 200 - 50, 400, 120, 70, "queries", 20, light_blue, blue)
back_button = button(screen, "back", 8, 8, 100, 50, "back", 20, light_red, red)

run = True


def start_screen():
    global run
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # background
        screen.fill((255, 255, 255))

        # text
        text1 = "Welcome!"
        text1 = big_font.render(text1, True, black)
        rect1 = text1.get_rect()
        rect1.center = (center_x, screen_h / 6)
        screen.blit(text1, rect1.topleft)

        # buttons
        chart_button.draw()
        queries_button.draw()

        pygame.display.update()
        clock.tick(fps)


def queries():
    global run
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # background
        screen.fill((0, 0, 0))

        # buttons
        back_button.draw()

        pygame.display.update()
        clock.tick(fps)


mat = [["alon", "suissa", "100"], ["aviv", "turgeman", "200"], ["noam", "levi", "300"], ["avi", "chen", "500"]]
titles = ["first name", "last name", "salary"]


def print_table(matrix, y_title):
    chunk_x = screen_w / 10
    chunk_y = screen_h / 10

    # lines
    for i in range(1, len(matrix[0])):
        pygame.draw.line(screen, black, (chunk_x * i, 60), (chunk_x * i, chunk_y * (len(matrix) + 2)))
    for i in range(2, len(matrix) + 2):
        pygame.draw.line(screen, black, (0, chunk_y * i), (chunk_x * (len(matrix[0])), chunk_y * i))

    # titles
    title_font = pygame.font.Font('freesansbold.ttf', 18)
    for i in range(0, len(titles)):
        text = title_font.render(titles[i], True, green)
        rect = text.get_rect()
        rect.center = (int(chunk_x * (0.5 + i)), int(60 + chunk_y / 2))
        screen.blit(text, rect.topleft)

    # values
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            text = small_font.render(matrix[i][j], True, black)
            rect = text.get_rect()
            rect.center = (int(chunk_x * (j + 0.5)), int(chunk_y * (i + 1.5) + 60))
            screen.blit(text, rect.topleft)


def chart():
    global run
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # background
        screen.fill((255, 255, 255))

        # chart
        print_table(mat, titles)

        # buttons
        back_button.draw()

        pygame.display.update()
        clock.tick(fps)


start_screen()
