import threading
import time

import pygame
from pygame import mixer
import socket
import pickle
from PL_player import PL_player
import query_object
import functions

# defines
protocol = "UDP"
LEN_SIZE_HEADER = 8  # for tcp
FORMAT = 'utf-8'  # the format that the messages decode/encode
CHUNK = 32

# server defines
SERVER_PORT = 30015
SERVER_IP = socket.gethostbyname(socket.gethostname())  # getting the ip of the computer
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
DISCONNECT_MESSAGE = [query_object.query_obj("Exit", True)]

# client defines
CLIENT_PORT = 20351  # (for UDP)
CLIENT = 1  # changing later to socket (when the user will choose TCP or UDP protocol)

# dhcp defines
DISCONNECT_MESSAGE_DHCP = "EXIT"
CONNECTION_MESSAGE = "PLEASE CONNECT ME"
DHCP_IP = socket.gethostbyname(socket.gethostname())
DHCP_PORT = 4836

# dns defines
DNS_IP = 1  # will change later (when we will get it from the DHCP SERVER)
DNS_PORT = 1  # will change later (when we will get it from the DHCP SERVER)
SERVER_ADDR_REQUEST = "SERVER"
DISCONNECT_MESSAGE_DNS = "EXIT"

# init
pygame.init()
pygame.font.init()

titles = ["Name", "Rating", "Team", "Position", "Goals", "Assists"]

# icon
icon = pygame.image.load('sql_icon.png')
pygame.display.set_icon(icon)

# sound
# mixer.music.set_volume(0.3)
# mixer.music.load('background_Sound.mp3')
mixer.music.play(-1, fade_ms=5000)
click_sound = pygame.mixer.Sound("Mouse_Click_2-fesliyanstudios.com.mp3")

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
gray = (40, 40, 40)
light_pink = (255, 190, 203)
pink = (255, 100, 147)
white = (255, 255, 255)
background_color = (0, 0, 80)  # deep blue

text_color = white

background_img = "champions_league_background2.png"

screen = pygame.display.set_mode((screen_w, screen_h))

# universal text
welcome_text1 = "Champions League"
aviv = "Aviv Turgeman - 208007351"
alon = "Alon Suissa - 211344015"

# fonts
fonts = pygame.font.get_fonts()
big_font = pygame.font.Font('freesansbold.ttf', 100)
med_font = pygame.font.Font('freesansbold.ttf', 60)
special_small_font = pygame.font.Font(pygame.font.match_font(fonts[14]), 50)
regular_small_font = pygame.font.Font('freesansbold.ttf', 30)
extra_small_font = pygame.font.Font('freesansbold.ttf', 20)

chart_font = pygame.font.Font(pygame.font.match_font(fonts[8]), 18)

pygame.display.set_caption("SQL project")


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

    def is_hover(self):
        cur = pygame.mouse.get_pos()
        return (self.x <= cur[0] <= self.x + self.width) and (self.y <= cur[1] <= self.y + self.height)

    def click(self):
        click_sound.play()
        global run
        if self.name == "chart":
            full_q = [query_object.query_obj("full")]
            send_queries(full_q)
            run = True
        if self.name == "queries":
            queries_categories()
            run = True
        if self.name == "back":
            run = False
        if self.name == "exit":
            _quit()
        if self.name == "UDP" or self.name == "TCP":
            global protocol
            print(protocol, "->", end=" ")
            protocol = self.name
            print(protocol)
            connect_to_socket()
            start_screen()

    def is_clicked(self):
        click = self.clicked
        self.clicked = False
        return click

    def draw(self):
        if self.visible:
            if self.is_hover():
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
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


class explain_button(button):

    def __init__(self, surface, text, x, y, width, height, name, active_color=light_purple, inactive_color=purple,
                 text_color=black, text_size=35, visible=True):
        super().__init__(surface, text, x, y, width, height, name, active_color, inactive_color, text_color, text_size,
                         visible)

    def click(self):
        None

    def draw(self):
        if self.visible:
            if self.is_hover():
                text1 = "Use UP/DOWN buttons for scrolling"
                text2 = "Use LEFT/RIGHT to decrease/increase scroll speed"
                text1 = regular_small_font.render(text1, True, black)
                text2 = regular_small_font.render(text2, True, black)
                text1_rect = text1.get_rect()
                text1_rect.center = (center_x, screen_h / 2)

                text2_rect = text2.get_rect()
                text2_rect.center = (center_x, screen_h / 2 + 100)

                pygame.draw.rect(screen, black, (text2_rect.x - 20, text1_rect.y - 20, text2_rect.width + 40,
                                                 (text2_rect.y - text1_rect.y) + text2_rect.height + 40))
                pygame.draw.rect(screen, green, (text2_rect.x - 15, text1_rect.y - 15, text2_rect.width + 30,
                                                 (text2_rect.y - text1_rect.y) + text2_rect.height + 30))

                self.screen.blit(text1, text1_rect.topleft)
                self.screen.blit(text2, text2_rect.topleft)
                pygame.draw.rect(self.screen, self.inactive_color, (self.x, self.y, self.width, self.height))
                self.text_to_button()
            else:
                pygame.draw.rect(self.screen, self.active_color, (self.x, self.y, self.width, self.height))
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
        click_sound.play()
        q1 = None
        q2 = None
        q3 = None
        q4 = None
        q5 = None
        q6 = None
        global run
        if self.name == "Team":
            button_w = 170
            button_h = 80
            q1 = query_button(screen, "Liverpool", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                              "Liverpool", 21, light_green, green)
            q2 = query_button(screen, "MCFC", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                              "MCFC", 12, light_green, green)
            q3 = query_button(screen, "Real Madrid", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                              "Real Madrid", 13, light_green, green)
            q4 = query_button(screen, "PSG", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                              "PSG", 14, light_green, green)
            q5 = query_button(screen, "Bayren Munich", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                              "Bayren Munich", 15, light_green, green)
            q6 = query_button(screen, "Porto", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                              "Porto", 16, light_green, green)

        if self.name == "Goals":
            button_w = 150
            button_h = 75
            q1 = query_button(screen, "no goals", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                              "no goals", 21, light_green, green)
            q2 = query_button(screen, "Goals >= 2", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                              "goals >= 2", 22, light_green, green)
            q3 = query_button(screen, "Goals < 4", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                              "goals < 4", 23, light_green, green)
            q4 = query_button(screen, "top scorer", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                              "top scorer", 24, light_green, green)
            q5 = query_button(screen, "top 10 scorers", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                              "top 10 scorers", 25, light_green, green)
            q6 = query_button(screen, "top 5 scorers", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                              "top 5 scorers", 26, light_green, green)

        if self.name == "Assists":
            button_w = 170
            button_h = 80
            q1 = query_button(screen, "no Assists", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                              "no assists", 31, light_green, green)
            q2 = query_button(screen, "Assists >= 2", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                              "assists >= 2", 32, light_green, green)
            q3 = query_button(screen, "Assists < 4", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                              "assists < 4", 33, light_green, green)
            q4 = query_button(screen, "top Assistive", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                              "top assistive", 34, light_green, green)
            q5 = query_button(screen, "top 10 Assistive", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                              "top 10 assistive", 35, light_green, green)
            q6 = query_button(screen, "top 5 Assistive", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                              "top 5 assistive", 36, light_green, green)

        if self.name == "Rating":
            button_w = 150
            button_h = 75
            q1 = query_button(screen, "Rating > 3.5", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                              "rating > 3.5", 41, light_green, green)
            q2 = query_button(screen, "Rating < 7.0", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                              "rating < 7.0", 42, light_green, green)
            q3 = query_button(screen, "Rating < 6.2", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                              "rating < 6.2", 43, light_green, green)
            q4 = query_button(screen, "Rating > 7.5", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                              "rating > 7.5", 44, light_green, green)
            q5 = query_button(screen, "top 10 Rating", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                              "top 10 rating", 45, light_green, green)
            q6 = query_button(screen, "top 5 Rating", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                              "top 5 rating", 46, light_green, green)

        if self.name == "Position":
            button_w = 150
            button_h = 75
            q1 = query_button(screen, "Goalkeepers", screen_w / 2 - 200 - button_w / 2, 250, button_w, button_h,
                              "Goalkeepers", 61, light_green, green)
            q2 = query_button(screen, "Defenders", screen_w / 2 - button_w / 2, 250, button_w, button_h,
                              "Defenders", 62, light_green, green)
            q3 = query_button(screen, "midfielders", screen_w / 2 + 200 - button_w / 2, 250, button_w, button_h,
                              "midfielders", 63, light_green, green)
            q4 = query_button(screen, "Forwards", screen_w / 2 - 200 - button_w / 2, 375, button_w, button_h,
                              "Forwards", 64, light_green, green)
            q5 = query_button(screen, "Left Wing", screen_w / 2 - button_w / 2, 375, button_w, button_h,
                              "Left Wing", 65, light_green, green)
            q6 = query_button(screen, "Right Wing", screen_w / 2 + 200 - button_w / 2, 375, button_w, button_h,
                              "Right Wing", 66, light_green, green)
        queries_list = [q1, q2, q3, q4, q5, q6]
        send_ = send_button(screen, "send", screen_w / 2 - 50, 500, 100, 50, "send", queries_list, black, gray,
                            text_color=(255, 255, 255))
        buttons_list = [q1, q2, q3, q4, q5, q6, send_]
        queries_draw(buttons_list)
        run = True


class query_button(button):

    def __init__(self, surface, text, x, y, width, height, name, index, active_color=light_purple,
                 inactive_color=purple,
                 text_color=black, text_size=35, visible=True):
        super().__init__(surface, text, x, y, width, height, name, active_color, inactive_color, text_color, text_size,
                         visible)
        self.index = index

    def query(self):
        return query_object.query_obj(self.name)

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
                pygame.draw.rect(self.screen, text_color,
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
        click_sound.play()
        queries_to_send = []
        for query in self.queries:
            # if the button is clicked right now
            if query.click_on_index == 1:
                # add that query to the sending query
                queries_to_send.insert(0, query.query())

        print("sending: ", end=" [")
        for i, q in enumerate(queries_to_send):
            if i == 0:
                print(q.query_name, end="")
            else:
                print(",", q.query_name, end="")
        print("]")
        send_queries(queries_to_send)


def tcp_send(queries_l: list):
    global run
    #  sending queries
    to_send = pickle.dumps(queries_l)
    to_send = bytes(f'{len(to_send) :< {LEN_SIZE_HEADER}}', FORMAT) + to_send
    CLIENT.send(to_send)

    # receive answer
    new_msg = True
    answer = b''
    msg_len = 0
    get_size = LEN_SIZE_HEADER
    while True:
        msg = CLIENT.recv(get_size)
        if new_msg:
            msg_len = int(msg[:LEN_SIZE_HEADER])
            new_msg = False
            get_size = CHUNK
        else:
            answer += msg
        if len(answer) == msg_len:
            answer = pickle.loads(answer)
            break
    chart(answer)
    run = True


def udp_send(queries_l: list):
    global run

    # sending the queries
    functions.send_with_cc(CLIENT, SERVER_ADDR, queries_l)

    # receive answer
    answer = functions.receive(CLIENT, SERVER_ADDR)

    chart(answer)
    run = True


def send_queries(queries_to_send: list):
    if protocol == "TCP":
        tcp_send(queries_to_send)
    if protocol == "UDP":
        udp_send(queries_to_send)


def queries_draw(buttons: list[button]):
    global run
    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _quit()

        # background
        intro_background_img = pygame.image.load(background_img)
        img = pygame.transform.scale(intro_background_img, (screen_w, screen_h))
        screen.blit(img, (0, 0))

        # text
        txt = "Choose Your Queries"
        txt = med_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.center = (center_x, screen_h / 6)
        screen.blit(txt, rect1.topleft)

        txt = "if you choose more then one its with && operation between them"
        txt = extra_small_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.center = (center_x, screen_h / 6 + 70)
        screen.blit(txt, rect1.topleft)

        # buttons
        hover = False
        for b in buttons:
            b.draw()
            hover = hover or b.is_hover()
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        exit_button.draw()
        back_button.draw()

        pygame.display.update()
        clock.tick(fps)


# universal buttons
center_x = screen_w / 2
back_button = button(screen, "back", 8, 8, 100, 50, "back", pink, light_pink)
exit_button = button(screen, "exit", screen_w - 8 - 100, 8, 100, 50, "exit", pink, light_pink)

run = True


def intro():
    udp_button = button(screen, "RUDP", 50, 450, 120, 70, "UDP", blue, light_blue)
    tcp_button = button(screen, "TCP", 50 + 200, 450, 120, 70, "TCP", blue, light_blue)
    global run, welcome_text1
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _quit()

        # background
        intro_background_img = pygame.image.load(background_img)
        img = pygame.transform.scale(intro_background_img, (screen_w, screen_h))
        screen.blit(img, (0, 0))

        # text
        txt = welcome_text1
        txt = med_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.topleft = (50, screen_h / 6 - 50)
        screen.blit(txt, rect1.topleft)

        sql_text = "Players SQL"
        sql_text = med_font.render(sql_text, True, text_color)
        screen.blit(sql_text, (50, screen_h / 6 + 50))

        txt = aviv
        txt = special_small_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.topleft = (50, screen_h / 6 + 150)
        screen.blit(txt, rect1.topleft)

        txt = alon
        txt = special_small_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.topleft = (50, screen_h / 6 + 250)
        screen.blit(txt, rect1.topleft)

        # buttons
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        udp_button.draw()
        tcp_button.draw()
        exit_button.draw()

        pygame.display.update()
        clock.tick(fps)


def dhcp_connection():
    global CLIENT_PORT, DNS_PORT, DNS_IP
    try:
        # connection
        DHCP_ADDR = (DHCP_IP, DHCP_PORT)
        dhcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dhcp_sock.connect(DHCP_ADDR)

        # request
        print("sending request to the DHCP SERVER")
        msg = pickle.dumps(CONNECTION_MESSAGE)
        msg = bytes(f'{len(msg) :< {LEN_SIZE_HEADER}}', FORMAT) + msg
        dhcp_sock.send(msg)

        # receive answer
        new_msg = True
        answer = b''
        msg_len = 0
        get_size = LEN_SIZE_HEADER
        while True:
            msg = dhcp_sock.recv(get_size)
            if new_msg:
                msg_len = int(msg[:LEN_SIZE_HEADER])
                new_msg = False
                get_size = CHUNK
            else:
                answer += msg
            if len(answer) == msg_len:
                answer = pickle.loads(answer)
                break

        port = answer[0][1]
        print("answer:", answer)
        print("my port:", port, end="\n\n")
        print("DNS address:", answer[1], end="\n\n")
        CLIENT_PORT = port
        DNS_IP = answer[1][0]
        DNS_PORT = answer[1][1]

        # close connection
        msg = pickle.dumps(DISCONNECT_MESSAGE_DHCP)
        msg = bytes(f'{len(msg) :< {LEN_SIZE_HEADER}}', FORMAT) + msg
        dhcp_sock.send(msg)
        dhcp_sock.close()

    except ConnectionRefusedError as error:
        print("U SHOULD RUN THE DHCP SERVER FIRST")
        print(error)


def dns():
    global SERVER_ADDR, SERVER_IP, SERVER_PORT
    try:
        # connection
        dns_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dns_sock.connect((DNS_IP, DNS_PORT))

        # request
        print("sending request to the DNS SERVER")
        msg = pickle.dumps(SERVER_ADDR_REQUEST)
        msg = bytes(f'{len(msg) :< {LEN_SIZE_HEADER}}', FORMAT) + msg
        dns_sock.send(msg)

        # receive answer
        new_msg = True
        answer = b''
        msg_len = 0
        get_size = LEN_SIZE_HEADER
        while True:
            msg = dns_sock.recv(get_size)
            if new_msg:
                msg_len = int(msg[:LEN_SIZE_HEADER])
                new_msg = False
                get_size = CHUNK
            else:
                answer += msg
            if len(answer) == msg_len:
                answer = pickle.loads(answer)
                break
        print("DNS answer:", answer, end="\n\n")
        SERVER_ADDR = answer
        SERVER_IP = answer[0]
        SERVER_PORT = answer[1]

        # close connection
        msg = pickle.dumps(DISCONNECT_MESSAGE_DNS)
        msg = bytes(f'{len(msg) :< {LEN_SIZE_HEADER}}', FORMAT) + msg
        dns_sock.send(msg)
        dns_sock.close()
    except ConnectionRefusedError as error:
        print("U SHOULD RUN THE DNS SERVER FIRST")
        print(error)


def connect_to_socket():
    global SERVER_ADDR, CLIENT, SERVER_PORT
    # dhcp connection
    dhcp_connection()

    # dns connection
    dns()

    # socket
    if protocol == "TCP":
        try:
            SERVER_ADDR = (SERVER_IP, SERVER_PORT)
            CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CLIENT.connect(SERVER_ADDR)
        except ConnectionRefusedError as error:
            print("U SHOULD RUN THE TCP SERVER FIRST")
            print(error)
        else:
            print("TCP connection established")

    elif protocol == "UDP":
        CLIENT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
        CLIENT.bind((socket.gethostbyname(socket.gethostname()), CLIENT_PORT))  # binding the address

        flag = 1
        temp_pair = 0
        CLIENT.setblocking(False)

        while flag:
            # sending start message (syn)
            if flag == 1:
                CLIENT.settimeout(0.2)
                print(f'sending start message')
                CLIENT.sendto(pickle.dumps("syn"), SERVER_ADDR)
                flag = 2

            # recv start massage and change the address
            if flag == 2:
                temp_pair = 0
                try:
                    if temp_pair == 0:
                        temp_pair = CLIENT.recvfrom(100)
                except socket.timeout as e:
                    continue
                if temp_pair != 0:
                    flag = 3
                    SERVER_ADDR = temp_pair[1]
                    print("!=0 case, temp pair:", temp_pair, ".")
                else:
                    print(" ==0 case, temp pair:", temp_pair, ".")
                    flag = 1
            # ack
            if flag == 3:
                CLIENT.sendto(pickle.dumps("ack"), SERVER_ADDR)
                print("sent ack")
                msg2 = 0
                try:
                    msg2 = CLIENT.recvfrom(1000)[0]
                    if msg2 == 0:
                        msg2 = pickle.loads(msg2)
                except socket.timeout as e:
                    continue

                if msg2 == 0:
                    flag = 0
                else:  # if I got somthing that's mean the server still trying to complete the sync
                    flag = 1
        CLIENT.setblocking(True)
        CLIENT.settimeout(30.0)
        print("RUDP connection established")


def start_screen():
    chart_button = button(screen, "full chart", 50, 450, 120, 70, "chart", blue, light_blue)
    queries_button = button(screen, "queries", 50 + 200, 450, 120, 70, "queries", blue, light_blue)
    global run, welcome_text1
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _quit()

        # background
        intro_background_img = pygame.image.load(background_img)
        img = pygame.transform.scale(intro_background_img, (screen_w, screen_h))
        screen.blit(img, (0, 0))

        # text
        txt = welcome_text1
        txt = med_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.topleft = (50, screen_h / 6 - 50)
        screen.blit(txt, rect1.topleft)

        sql_text = "Players SQL"
        sql_text = med_font.render(sql_text, True, text_color)
        screen.blit(sql_text, (50, screen_h / 6 + 50))

        txt = aviv
        txt = special_small_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.topleft = (50, screen_h / 6 + 150)
        screen.blit(txt, rect1.topleft)

        txt = alon
        txt = special_small_font.render(txt, True, text_color)
        rect1 = txt.get_rect()
        rect1.topleft = (50, screen_h / 6 + 250)
        screen.blit(txt, rect1.topleft)

        # buttons
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        chart_button.draw()
        queries_button.draw()
        exit_button.draw()

        pygame.display.update()
        clock.tick(fps)


def queries_categories():
    button_w = 150
    button_h = 75
    category1_Teams = category_button(screen, "Team", screen_w / 2 - button_w / 2 - 200, 250,
                                      button_w, button_h, "Team", light_green, green)

    category2_Goals = category_button(screen, "Goals", screen_w / 2 - button_w / 2, 250,
                                      button_w, button_h, "Goals", light_green, green)
    category3_Assists = category_button(screen, "Assists", screen_w / 2 - button_w / 2 + 200, 250,
                                        button_w, button_h, "Assists", light_green, green)

    category4_Rate = category_button(screen, "Rating", center_x - button_w / 2 - 100, 375,
                                     button_w, button_h, "Rating", light_green, green)

    category5_Position = category_button(screen, "Position", screen_w / 2 - button_w / 2 + 100, 375,
                                         button_w, button_h, "Position", light_green, green)
    global run
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _quit()

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
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        back_button.draw()
        exit_button.draw()
        category2_Goals.draw()
        category3_Assists.draw()
        category1_Teams.draw()
        category4_Rate.draw()
        category5_Position.draw()

        pygame.display.update()
        clock.tick(fps)


# ["name", "Rating", "Team", "position", "goals", "assists"]

def print_table(data: list[PL_player], delta_y):
    matrix = [[data[i].get_name(), str(data[i].get_rate()), data[i].get_team(), data[i].get_position(),
               str(data[i].get_goals()), str(data[i].get_assists())] for i in range(len(data))]
    chunk_x = screen_w / 6
    chunk_y = screen_h / 10

    # boundaries
    down_boundary = 540
    if len(data) <= 8:
        delta_y = 0
    if delta_y < 0 and ((chunk_y * 2) - delta_y >= 120):
        delta_y = 0
    elif delta_y > 0 and (chunk_y * 2) - delta_y < 0 and (chunk_y * (len(matrix) + 2) - delta_y) < down_boundary:
        delta_y = chunk_y * (len(matrix) + 2) - down_boundary

    # lines
    for i in range(2, len(matrix) + 2):
        pygame.draw.line(screen, text_color, (0, (chunk_y * i) - delta_y),
                         (chunk_x * (len(matrix[0])), (chunk_y * i) - delta_y))
    for i in range(1, 6):
        pygame.draw.line(screen, text_color, (chunk_x * i, 60 - delta_y),
                         (chunk_x * i, chunk_y * (len(matrix) + 2) - delta_y))
    if len(matrix) == 0:
        pygame.draw.line(screen, text_color, (0, (chunk_y * 2) - delta_y),
                         (chunk_x * 6, (chunk_y * 2) - delta_y))

    # titles
    title_font = pygame.font.Font('freesansbold.ttf', 20)
    for i in range(0, len(titles)):
        text = title_font.render(titles[i], True, white)
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


def chart(table):
    global run
    exp_button = explain_button(screen, "?", screen_w - 40, screen_h - 40, 40, 50, "explain", black, (50, 50, 50),
                                white,
                                text_size=55)
    run = True
    delta_y = 0
    scroll_speed = 4
    down = False
    up = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _quit()

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
            delta_y += scroll_speed
        elif up:
            delta_y -= scroll_speed
        # background
        screen.fill(background_color)

        # chart
        delta_y = print_table(table, delta_y)

        # buttons
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        back_button.draw()
        exit_button.draw()
        exp_button.draw()

        pygame.display.update()
        clock.tick(fps)


def _quit():
    print("SENDING EXIT MESSAGE")

    if protocol == "TCP":
        to_send = pickle.dumps(DISCONNECT_MESSAGE)
        to_send = bytes(f'{len(to_send) :< {LEN_SIZE_HEADER}}', FORMAT) + to_send
        CLIENT.send(to_send)
    if protocol == "UDP":
        functions.send_with_cc(CLIENT, SERVER_ADDR, DISCONNECT_MESSAGE)
    print("EXITING...")
    pygame.quit()
    quit()


intro()
