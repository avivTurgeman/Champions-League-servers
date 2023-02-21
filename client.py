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
med_font = pygame.font.Font('freesansbold.ttf', 60)
small_font = pygame.font.Font(pygame.font.match_font(fonts[14]), 50)
extra_small_font = pygame.font.Font('freesansbold.ttf', 20)

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
        self.clicked = True
        self.name = name
        self.visible = visible
        self.click_on_index = 0

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
            queries_categories()
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
                        self.click_on_index = (self.click_on_index + 1) % 2
                else:
                    self.clicked = False
                pygame.draw.rect(self.screen, self.active_color, (self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(self.screen, self.inactive_color, (self.x, self.y, self.width, self.height))
            self.text_to_button()


class and_or_buttons(button):

    def __init__(self, surface, text, x, y, width, height, name, active_color=light_purple, inactive_color=purple,
                 text_color=black, text_size=35, visible=True):
        super().__init__(surface, text, x, y, width, height, name, active_color, inactive_color, text_color, text_size,
                         visible)

    def text_to_button(self):
        super().text_to_button()

    def click(self):
        super().click()


class category_button(button):

    def __init__(self, surface, text, x, y, width, height, name, active_color=light_purple, inactive_color=purple,
                 text_color=black, text_size=35, visible=True):
        super().__init__(surface, text, x, y, width, height, name, active_color, inactive_color, text_color, text_size,
                         visible)

    def click(self):
        global run
        if self.name == "Team":
            button_w = 150
            button_h = 75
            gaol_q1 = query_button(screen, "query 11", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                                   "query11", 21, light_green, green)
            gaol_q2 = query_button(screen, "query 12", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                                   "query12", 12, light_green, green)
            gaol_q3 = query_button(screen, "query 13", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                                   "query13", 13, light_green, green)
            gaol_q4 = query_button(screen, "query 14", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                                   "query14", 14, light_green, green)
            gaol_q5 = query_button(screen, "query 15", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                                   "query15", 15, light_green, green)
            gaol_q6 = query_button(screen, "query 16", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                                   "query16", 16, light_green, green)
            queries_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6]
            send = send_button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", queries_list, black, gray,
                               text_color=(255, 255, 255))
            buttons_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6, send]
            queries_draw(buttons_list)
            run = True
        if self.name == "Goals":
            button_w = 150
            button_h = 75
            gaol_q1 = query_button(screen, "query 21", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                                   "query21", 21, light_green, green)
            gaol_q2 = query_button(screen, "query 22", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                                   "query22", 22, light_green, green)
            gaol_q3 = query_button(screen, "query 23", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                                   "query23", 23, light_green, green)
            gaol_q4 = query_button(screen, "query 24", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                                   "query24", 24, light_green, green)
            gaol_q5 = query_button(screen, "query 25", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                                   "query25", 25, light_green, green)
            gaol_q6 = query_button(screen, "query 26", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                                   "query26", 26, light_green, green)
            queries_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6]
            send = send_button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", queries_list, black, gray,
                               text_color=(255, 255, 255))
            buttons_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6, send]
            queries_draw(buttons_list)
            run = True
        if self.name == "Assists":
            button_w = 150
            button_h = 75
            gaol_q1 = query_button(screen, "query 31", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                                   "query31", 31, light_green, green)
            gaol_q2 = query_button(screen, "query 32", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                                   "query32", 32, light_green, green)
            gaol_q3 = query_button(screen, "query 33", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                                   "query33", 33, light_green, green)
            gaol_q4 = query_button(screen, "query 34", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                                   "query34", 34, light_green, green)
            gaol_q5 = query_button(screen, "query 35", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                                   "query35", 35, light_green, green)
            gaol_q6 = query_button(screen, "query 36", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                                   "query36", 36, light_green, green)
            queries_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6]
            send = send_button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", queries_list, black, gray,
                               text_color=(255, 255, 255))
            buttons_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6, send]
            queries_draw(buttons_list)
            run = True
        if self.name == "Age":
            button_w = 150
            button_h = 75
            gaol_q1 = query_button(screen, "query 41", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                                   "query41", 41, light_green, green)
            gaol_q2 = query_button(screen, "query 42", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                                   "query42", 42, light_green, green)
            gaol_q3 = query_button(screen, "query 43", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                                   "query43", 43, light_green, green)
            gaol_q4 = query_button(screen, "query 44", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                                   "query44", 44, light_green, green)
            gaol_q5 = query_button(screen, "query 45", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                                   "query45", 45, light_green, green)
            gaol_q6 = query_button(screen, "query 26", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                                   "query46", 46, light_green, green)
            queries_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6]
            send = send_button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", queries_list, black, gray,
                               text_color=(255, 255, 255))
            buttons_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6, send]
            queries_draw(buttons_list)
            run = True
        if self.name == "Number":
            button_w = 150
            button_h = 75
            gaol_q1 = query_button(screen, "query 51", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                                   "query51", 51, light_green, green)
            gaol_q2 = query_button(screen, "query 52", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                                   "query52", 52, light_green, green)
            gaol_q3 = query_button(screen, "query 53", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                                   "query53", 53, light_green, green)
            gaol_q4 = query_button(screen, "query 54", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                                   "query54", 54, light_green, green)
            gaol_q5 = query_button(screen, "query 55", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                                   "query55", 55, light_green, green)
            gaol_q6 = query_button(screen, "query 56", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                                   "query56", 56, light_green, green)
            queries_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6]
            send = send_button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", queries_list, black, gray,
                               text_color=(255, 255, 255))
            buttons_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6, send]
            queries_draw(buttons_list)
            run = True
        if self.name == "Position":
            button_w = 150
            button_h = 75
            gaol_q1 = query_button(screen, "query 61", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                                   "query21", 61, light_green, green)
            gaol_q2 = query_button(screen, "query 62", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                                   "query62", 62, light_green, green)
            gaol_q3 = query_button(screen, "query 63", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                                   "query63", 63, light_green, green)
            gaol_q4 = query_button(screen, "query 64", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                                   "query64", 64, light_green, green)
            gaol_q5 = query_button(screen, "query 65", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                                   "query65", 65, light_green, green)
            gaol_q6 = query_button(screen, "query 66", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                                   "query66", 66, light_green, green)
            queries_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6]
            send = send_button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", queries_list, black, gray,
                               text_color=(255, 255, 255))
            buttons_list = [gaol_q1, gaol_q2, gaol_q3, gaol_q4, gaol_q5, gaol_q6, send]
            queries_draw(buttons_list)
            run = True


def queries_draw(buttons: list[button]):
    global run
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
        txt = "Choose Your Query"
        txt = med_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.center = (center_x, screen_h / 6)
        screen.blit(txt, rect1.topleft)

        # buttons
        for b in buttons:
            b.draw()

        exit_button.draw()
        back_button.draw()

        pygame.display.update()
        clock.tick(fps)


class query_button(button):

    def __init__(self, surface, text, x, y, width, height, name, index, active_color=light_purple,
                 inactive_color=purple,
                 text_color=black, text_size=35, visible=True):
        super().__init__(surface, text, x, y, width, height, name, active_color, inactive_color, text_color, text_size,
                         visible)
        self.index = index

    def query(self):
        return self.index

    def draw(self):
        conditions = [False, True]
        click_on = conditions[self.click_on_index]
        if self.visible:
            cur = pygame.mouse.get_pos()
            if (self.x <= cur[0] <= self.x + self.width) and (self.y <= cur[1] <= self.y + self.height):
                # hover text:
                # text = "lncakjkasbcksabcskb"
                # text = small_font.render(text, True, gray)
                # rect = text.get_rect()
                # rect.center = (self.x + self.width/2 , self.y + self.height + 10)
                # self.screen.blit(text, rect.topleft)
                if pygame.mouse.get_pressed()[0] == 1:
                    if not self.clicked:
                        self.click()
                        self.clicked = True
                        self.click_on_index = (self.click_on_index + 1) % 2
                        click_on = conditions[self.click_on_index]
                else:
                    self.clicked = False
                pygame.draw.rect(self.screen, self.active_color, (self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(self.screen, self.inactive_color, (self.x, self.y, self.width, self.height))
            if click_on:
                pygame.draw.rect(self.screen, black,
                                 (self.x - 3, self.y - 3, self.width + 6, self.height + 6), 3)
            self.text_to_button()


class send_button(button):

    def __init__(self, surface, text, x, y, width, height, name, queries: list[query_button], active_color=light_purple,
                 inactive_color=purple,
                 text_color=black, text_size=35, visible=True):
        super().__init__(surface, text, x, y, width, height, name, active_color, inactive_color, text_color, text_size,
                         visible)
        self.queries = queries

    def click(self):
        queries_to_send = []
        for query in self.queries:
            # if the button is clicked right now
            if query.click_on_index == 1:
                # add that query to the sending query
                queries_to_send.insert(0, query.query())

        print("sending: ", queries_to_send)


# buttons
center_x = screen_w / 2
chart_button = button(screen, "full chart", center_x - 250 - 50, 400, 120, 70, "chart", blue, light_blue)
queries_button = button(screen, "queries", center_x + 250 - 50, 400, 120, 70, "queries", blue, light_blue)
back_button = button(screen, "back", 8, 8, 100, 50, "back", pink, light_pink)
exit_button = button(screen, "exit", screen_w - 8 - 100, 8, 100, 50, "exit", pink, light_pink)

button_w = 150
button_h = 75

category1_Teams = category_button(screen, "Team", screen_w / 2 - button_w / 2 - 200, 250,
                                  button_w, button_h, "Team", light_green, green)

category2_Goals = category_button(screen, "Goals", screen_w / 2 - button_w / 2, 250,
                                  button_w, button_h, "Goals", light_green, green)
category3_Assists = category_button(screen, "Assists", screen_w / 2 - button_w / 2 + 200, 250,
                                    button_w, button_h, "Assists", light_green, green)


category4_Age = category_button(screen, "Age", screen_w / 2 - button_w / 2 - 200, 375,
                                button_w, button_h, "Age", light_green, green)
category5_Number = category_button(screen, "Number", screen_w / 2 - button_w / 2, 375,
                                   button_w, button_h, "Number", light_green, green)
category6_Position = category_button(screen, "Position", screen_w / 2 - button_w / 2 + 200, 375,
                                     button_w, button_h, "Position", light_green, green)

queries = []
send = send_button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", queries, black, gray,
                   text_color=(255, 255, 255))

dont_button = button(screen, "DO NOT CLICK!", screen_w / 2 - 50, 400, 120, 70, "dont", blue, light_blue, text_size=21)


def blur_img(img, amount):
    scale = 1 / float(amount)
    surf_size = img.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(img, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


run = True

welcome_text = "Premier League Players SQL"
aviv = "Aviv Turgeman - 208007351"
alon = "Alon Suissa - 211344015"


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
        txt = med_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.center = (center_x, screen_h / 6)
        screen.blit(txt, rect1.topleft)

        txt = aviv
        txt = small_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.center = (center_x, screen_h / 6 + 100)
        screen.blit(txt, rect1.topleft)

        txt = alon
        txt = small_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.center = (center_x, screen_h / 6 + 200)
        screen.blit(txt, rect1.topleft)

        # buttons
        chart_button.draw()
        queries_button.draw()
        exit_button.draw()
        dont_button.draw()

        pygame.display.update()
        clock.tick(fps)


def queries_categories():
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

        # text
        txt = "Choose A Query Category"
        cur_font = pygame.font.Font(pygame.font.match_font(fonts[14]), 70)
        txt = cur_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.center = (center_x, screen_h / 6)
        screen.blit(txt, rect1.topleft)

        # buttons
        back_button.draw()
        exit_button.draw()
        category2_Goals.draw()
        category3_Assists.draw()
        category1_Teams.draw()
        category4_Age.draw()
        category5_Number.draw()
        category6_Position.draw()

        pygame.display.update()
        clock.tick(fps)


# example for a table
mat = [["Erling Haaland", "22", "MCFC", "CF", "26", "4"],
       ["Harry Kane", "29", "Spurs", "CF", "17", "2"],
       ["Ivan Toney", "26", "Brentford", "CF", "14", "3"],
       ["Bukayo Saka", "21", "Arsenal", "RF", "9", "8"]]
titles = ["name", "age", "Team", "position", "goals", "assissts"]


def print_table(matrix, delta_y):
    chunk_x = screen_w / 6
    chunk_y = screen_h / 10

    # boundaries
    if delta_y < 0 and (chunk_y * 2) - delta_y >= 120:
        delta_y = 0

    # lines
    for i in range(2, len(matrix) + 2):
        pygame.draw.line(screen, text_color, (0, (chunk_y * i) - delta_y),
                         (chunk_x * (len(matrix[0])), (chunk_y * i) - delta_y))

    for i in range(1, len(matrix[0])):
        pygame.draw.line(screen, text_color, (chunk_x * i, 60 - delta_y),
                         (chunk_x * i, chunk_y * (len(matrix) + 2) - delta_y))

    # titles
    title_font = pygame.font.Font('freesansbold.ttf', 20)
    for i in range(0, len(titles)):
        text = title_font.render(titles[i], True, gray)
        rect = text.get_rect()
        rect.center = (int(chunk_x * (0.5 + i)), int(60 + chunk_y / 2) - delta_y)
        screen.blit(text, rect.topleft)

    # values
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            text = chart_font.render(matrix[i][j], True, text_color)
            rect = text.get_rect()
            rect.center = (int(chunk_x * (j + 0.5)), int(chunk_y * (i + 1.5) + 60) - delta_y)
            screen.blit(text, rect.topleft)
    return delta_y


def chart():
    global run
    run = True
    delta_y = 0
    scroll_speed = 10
    down = False
    up = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_DOWN:
                    down = True
                if event.key == pygame.K_RIGHT:
                    scroll_speed += 2
                if event.key == pygame.K_LEFT:
                    scroll_speed -= 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down = False
                if event.key == pygame.K_UP:
                    up = False
            if scroll_speed <= 0:
                scroll_speed = 1

        if down:
            delta_y -= scroll_speed
        elif up:
            delta_y += scroll_speed
        # background
        into_background_img = pygame.image.load(background_img)
        img = pygame.transform.scale(into_background_img, (screen_w, screen_h))
        # img = blur_img(img, 100)
        screen.blit(img, (0, 0))

        # chart
        delta_y = print_table(mat, delta_y)

        # buttons
        back_button.draw()
        exit_button.draw()

        pygame.display.update()
        clock.tick(fps)


start_screen()
