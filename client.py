import pygame

# import button

pygame.init()
pygame.font.init()
fonts = pygame.font.get_fonts()

# icon
icon = pygame.image.load('sql_icon.png')
pygame.display.set_icon(icon)

fps = 30
screen_w = 1000
screen_h = 600
clock = pygame.time.Clock()

# colors
purple = (155, 70, 239)
light_purple = (176, 156, 217)
black = (0, 0, 0)
red = (180, 50, 50)
light_red = (220, 0, 0)
green = (0, 120, 100)
light_green = (0, 200, 100)
blue = (60, 170, 200)
light_blue = (36, 100, 113)
light_yellow = (255, 255, 0)
yellow = (180, 180, 0)
gray = (40, 40, 40)
light_pink = (255, 190, 203)
pink = (255, 100, 147)
white = (255, 255, 255)

text_color = black

background_img = "background2.jpg"

screen = pygame.display.set_mode((screen_w, screen_h))

big_font = pygame.font.Font('freesansbold.ttf', 100)
med_font = pygame.font.Font('freesansbold.ttf', 50)
small_font = pygame.font.Font('freesansbold.ttf', 20)

chart_font = pygame.font.Font(pygame.font.match_font(fonts[8]), 20)

pygame.display.set_caption("SQL project")


# background_img = pygame.image.load("background_leve1.png")

class button:
    def __init__(self, surface, text, x, y, width, height, name, active_color=light_purple,
                 inactive_color=purple, text_color=black, text_size=35, visible=True):
        self.screen = surface
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font(pygame.font.match_font(fonts[14]), text_size)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.clicked = False
        self.name = name
        self.visible = visible

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
        if self.name == "exit":
            pygame.quit()
            quit()
        if self.name == "send":
            print("sending")
        if self.name == "dont":
            global welcome_text, background_img, text_color
            welcome_text = "obviously..."
            background_img = "hell.jpg"
            text_color = white
            self.visible = False

    def is_clicked(self):
        click = self.clicked
        self.clicked = False
        return click

    def draw(self):
        if self.visible:
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
chart_button = button(screen, "full chart", center_x - 250 - 50, 400, 120, 70, "chart", blue, light_blue)
queries_button = button(screen, "queries", center_x + 250 - 50, 400, 120, 70, "queries", blue, light_blue)
back_button = button(screen, "back", 8, 8, 100, 50, "back", pink, light_pink)
exit_button = button(screen, "exit", screen_w - 8 - 100, 8, 100, 50, "exit", pink, light_pink)

query1 = button(screen, "query 1", screen_w / 6 * 1 - 50, 150, 100, 50, "query1", light_green, green)
query2 = button(screen, "query 2", screen_w / 6 * 2 - 50, 150, 100, 50, "query2", light_green, green)
query3 = button(screen, "query 3", screen_w / 6 * 3 - 50, 150, 100, 50, "query3", light_green, green)
query4 = button(screen, "query 4", screen_w / 6 * 4 - 50, 150, 100, 50, "query4", light_green, green)
query5 = button(screen, "query 5", screen_w / 6 * 5 - 50, 150, 100, 50, "query5", light_green, green)

query6 = button(screen, "query 6", screen_w / 6 * 1 - 50, 350, 100, 50, "query6", light_green, green)
query7 = button(screen, "query 7", screen_w / 6 * 2 - 50, 350, 100, 50, "query7", light_green, green)
query8 = button(screen, "query 8", screen_w / 6 * 3 - 50, 350, 100, 50, "query8", light_green, green)
query9 = button(screen, "query 9", screen_w / 6 * 4 - 50, 350, 100, 50, "query9", light_green, green)
query10 = button(screen, "query 10", screen_w / 6 * 5 - 50, 350, 100, 50, "query10", light_green, green)

send = button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", black, gray, text_color=(255, 255, 255))

dont_button = button(screen, "DO NOT CLICK!", screen_w / 2 - 50, 400, 120, 70, "dont", blue, light_blue, text_size=21)


def blur_img(img, amount):
    scale = 1 / float(amount)
    surf_size = img.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(img, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


run = True

welcome_text = "Welcome!"


def start_screen():
    global run, welcome_text
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # background
        intro_background_img = pygame.image.load(background_img)
        img = pygame.transform.scale(intro_background_img, (screen_w, screen_h))
        screen.blit(img, (0, 0))

        # text
        txt = welcome_text
        txt = big_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.center = (center_x, screen_h / 6)
        screen.blit(txt, rect1.topleft)

        # buttons
        chart_button.draw()
        queries_button.draw()
        exit_button.draw()
        dont_button.draw()

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
        into_background_img = pygame.image.load(background_img)
        img = pygame.transform.scale(into_background_img, (screen_w, screen_h))
        # img = blur_img(img, 100)
        screen.blit(img, (0, 0))

        # buttons
        back_button.draw()
        exit_button.draw()
        query1.draw()
        query2.draw()
        query3.draw()
        query4.draw()
        query5.draw()
        query6.draw()
        query7.draw()
        query8.draw()
        query9.draw()
        query10.draw()
        send.draw()

        pygame.display.update()
        clock.tick(fps)


# example for a table
mat = [["Erling Haaland", "22", "MCFC", "CF", "26", "4"],
       ["Harry Kane", "29", "Spurs", "CF", "17", "2"],
       ["Ivan Toney", "26", "Brentford", "CF", "14", "3"],
       ["Bukayo Saka", "21", "Arsenal", "RF", "9", "8"]]
titles = ["name","age", "Team", "position", "goals", "assissts"]


def print_table(matrix, y_title):
    chunk_x = screen_w / 6
    chunk_y = screen_h / 10

    # lines
    for i in range(1, len(matrix[0])):
        pygame.draw.line(screen, text_color, (chunk_x * i, 60), (chunk_x * i, chunk_y * (len(matrix) + 2)))
    for i in range(2, len(matrix) + 2):
        pygame.draw.line(screen, text_color, (0, chunk_y * i), (chunk_x * (len(matrix[0])), chunk_y * i))

    # titles
    title_font = pygame.font.Font('freesansbold.ttf', 20)
    for i in range(0, len(titles)):
        text = title_font.render(titles[i], True, gray)
        rect = text.get_rect()
        rect.center = (int(chunk_x * (0.5 + i)), int(60 + chunk_y / 2))
        screen.blit(text, rect.topleft)

    # values
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            text = chart_font.render(matrix[i][j], True, text_color)
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
        into_background_img = pygame.image.load(background_img)
        img = pygame.transform.scale(into_background_img, (screen_w, screen_h))
        # img = blur_img(img, 100)
        screen.blit(img, (0, 0))

        # chart
        print_table(mat, titles)

        # buttons
        back_button.draw()
        exit_button.draw()

        pygame.display.update()
        clock.tick(fps)


start_screen()
