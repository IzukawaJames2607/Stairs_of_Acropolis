import pygame
import os
import time
import pygame.gfxdraw
import colour
from colour import Color
import mysql.connector

pygame.init()
pygame.font.init()

#Set up frame and caption
width, height = 900, 700
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stairs of Acropolis")

#Upload the image
acropolis_temple = pygame.image.load('acropolis.png')
frame = pygame.image.load('Greek_Style_Border_Frame.png')
athena = pygame.image.load('athena_goddess.png')
cloud1 = pygame.image.load('cloud1.png')
cloud2 = pygame.image.load('cloud2.png')
pygame.display.set_icon(acropolis_temple)

#Set the size of image and draw it on the window
acropolis_temple_new_w = 300
acropolis_temple_new_h = 200
athena_new_w = 500
athena_new_h = 600
new_acropolis_temple = pygame.transform.scale(acropolis_temple, (acropolis_temple_new_w, acropolis_temple_new_h))
new_greek_frame = pygame.transform.scale(frame, (width, height))
new_athena = pygame.transform.scale(athena, (athena_new_w, athena_new_h))

#Set the title and its shadow effect on the window
title_font = pygame.font.SysFont("Times New Roman", 52, bold=True)
shadow_title = title_font.render("STAIRS OF ACROPOLIS", False, (255, 255, 240))
set_font_title = title_font.render("STAIRS OF ACROPOLIS", True, (0, 0, 0))

#Recognize each stair as a rectangle and set the size and location of the first stair
stairs_num = 12
first_stair_width = acropolis_temple_new_w
first_stair_height = height // stairs_num
first_stair_x = width//2 - first_stair_width//2
first_stair_y = height//2 - 1.2*acropolis_temple_new_h + acropolis_temple_new_h

#Upload the music for background music
background_music = os.path.join('Neverland(chosic.com).mp3')
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#Set the color of 12 stairs varying from bottom to top
stairs_bottom_color = (180, 180, 180)
stairs_top_color = (255, 255, 240)
base_color = [(
    int(stairs_bottom_color[0] + (stairs_top_color[0] - stairs_bottom_color[0]) * i / (stairs_num - 1)),
    int(stairs_bottom_color[1] + (stairs_top_color[1] - stairs_bottom_color[1]) * i / (stairs_num - 1)),
    int(stairs_bottom_color[2] + (stairs_top_color[2] - stairs_bottom_color[2]) * i / (stairs_num - 1))
) for i in range(stairs_num)]

#Set the colors varying for textbox
textbox_rect = pygame.Rect(100, 700, 180, 130)
textbox_rect2 = pygame.Rect(350, 700, 180, 130)
textbox_rect3 = pygame.Rect(600, 700, 180, 130)
textbox_color = (255, 10, 10)

#Set up function for drawing textbox
font_to_fill = pygame.font.SysFont('Arial', 16)

#Connect to database to save the information of player
player_db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port=3306,
    password="manhtuan2003",
    database="Stairs_of_Acropolis"
)

def sign_up_player_data(username, age_text, place_of_living, hobby, gender):
    """
    This is the docstring of function sign_up_player_data, which inserts a player's basic information into the database.
    """
    if username and age_text and place_of_living and hobby and gender:
        try:
            mycursor = player_db.cursor()
            sql = "INSERT INTO Player (username, age, place_of_living, hobby, gender) VALUES (%s, %s, %s, %s, %s)"
            val = (username, int(age_text), place_of_living, hobby, gender)
            mycursor.execute(sql, val)
            player_db.commit()
            print("User data saved successfully!")
        except mysql.connector.Error as err:
            print(err)
    else:
        return None
#Check whether player's username exists
def check_username_exist(username):
    """
    This is the docstring of function check_username_exist(username), which checks whether the username of a player already exists in database or not.
    """
    try:
        mycursor = player_db.cursor()
        mycursor.execute("SELECT COUNT(*) FROM Player WHERE username = %s", (username, ))
        count_username = mycursor.fetchone()[0]
        mycursor.close()
        return count_username > 0
    except mysql.connector.Error as err:
        print(err)

def pop_username():
    """
    This is the docstring of function pop_username(), which prints the username of current player.
    """
    try:
        mycursor = player_db.cursor()
        mycursor.execute("SELECT username FROM Player ORDER BY PlayerID DESC LIMIT 1")
        name_result = mycursor.fetchone()
        mycursor.close()
        return name_result
    except mysql.connector.Error as err:
        print(err)

def pop_points():
    """
    This is the docstring of function pop_points(), which print the current points a player have earned.
    """
    try:
        mycursor = player_db.cursor()
        mycursor.execute("SELECT points FROM Player ORDER BY PlayerID DESC LIMIT 1")
        point_result = mycursor.fetchone()
        mycursor.close()
        return point_result
    except mysql.connector.Error as err:
        print(err)

def pop_question_number():
    """
    This is the docstring of function pop_question_number(), which print the number of questions a player has answered.
    """
    try:
        mycursor = player_db.cursor()
        mycursor.execute("SELECT question_number FROM Player ORDER BY PlayerID DESC LIMIT 1")
        get_qnum = mycursor.fetchone()[0]
        mycursor.close()
        return get_qnum
    except mysql.connector.Error as err:
        print(err)

def pop_questions_gorgo(specialty):
    """
    This is the docstring of function pop_questions_gorgo, which extracts the question and its options and its correct answer in Gorgo Version.
    """
    try:
        mycursor = player_db.cursor()
        mycursor.execute("SELECT question, optionA, optionB, optionC, optionD, correct_answer FROM Acropolis_Questions_System WHERE specialty = %s AND question_type = 'Gorgo' ORDER BY RAND() LIMIT 1", (specialty, ))
        gorgo_question = mycursor.fetchone()
        player_db.close()
        return gorgo_question
    except mysql.connector.Error as err:
        print(err)

def pop_questions_sparta(specialty):
    """
    This is the docstring of function pop_questions_sparta, which extracts the question and its correct answer in Sparta Version.
    """
    try:
        mycursor = player_db.cursor()
        mycursor.execute("SELECT question, correct_answer FROM Acropolis_Questions_System WHERE specialty = %s AND question_type = 'Sparta' ORDER BY RAND() LIMIT 1", (specialty, ))
        player_db.close()
        return mycursor.fetchone()
    except mysql.connector.Error as err:
        print(err)

def interpolate_color(color1, color2, progress):
    r = int(color1[0] * (1 - progress) + color2[0] * progress)
    g = int(color1[1] * (1 - progress) + color2[1] * progress)
    b = int(color1[2] * (1 - progress) + color2[2] * progress)
    return (r, g, b)

class RoundRectTextbox:
    """
    This is the docstring of class Player, which represents a player joining game.
    
    Attributes:
    rx, ry, rw, rh (int): the size and coordinate of round rectangle textbox.
    start_color, end_color: initialize a range of color from start to end to fill the textbox.

    Functions:
    roundrectdraw(surface): draw the round rectangle textbox.
    render_text(): Align the text to be in the textbox only.
    roundrectfill(): Fill in the textbox with the text aligned.
    update_color(progress): Vary the color filling the textbox.

    """
    def __init__(self, rx=0, ry=0, rw=0, rh=0, start_color=(0,0,0), end_color=(0,0,0)):
        self.rx = rx
        self.ry = ry
        self.rw = rw
        self.rh = rh
        self.start_color = start_color
        self.end_color = end_color
        self.lines = []
    def roundrectdraw(self, surface):
        self.roundrect = pygame.Rect(self.rx, self.ry, self.rw, self.rh)
        pygame.draw.rect(surface, self.start_color, self.roundrect, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), self.roundrect, width=2, border_radius=10)
    def render_text(self, rrtext='', rrfont_name='', rrfontsize='', rrfontcolor=(0,0,0), is_bold=True):
        lines = []
        words = str(rrtext).split()
        max_width = self.rw
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            text_width, _ = pygame.font.SysFont(rrfont_name, rrfontsize).size(test_line)
            if text_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)
        rendered_lines = [pygame.font.SysFont(rrfont_name, rrfontsize, is_bold).render(line, True, rrfontcolor) for line in lines]
        return rendered_lines
    def roundrectfill(self, surface, rrtext='', rrfont_name='', rrfontsize='', rrfontcolor=(0,0,0), is_bold=True):
        self.lines = self.render_text(rrtext, rrfont_name, rrfontsize, rrfontcolor, is_bold)
        y = self.ry + (self.rh - sum(line.get_height() for line in self.lines)) // 2
        for line in self.lines:
            rr_text_rect = line.get_rect(center=(self.rx + self.rw // 2, y))
            surface.blit(line, rr_text_rect.topleft)
            y += line.get_height() + 2
    def update_color(self, progress):
        self.fill_color = interpolate_color(self.start_color, self.end_color, progress)

#Set pop-up animation
y_to_popup = 450
popup_speed = 5
def pop_up_animation(textbox_rect, y_to_popup, popup_speed):
    if textbox_rect.y > y_to_popup:
        textbox_rect.y -= popup_speed

#Fill the window with color varying in an identified range
def background_color(surface, top_color, bottom_color):
    """
    This is the docstring of function background_color, which shows the background color of every window calling it.
    """
    top_color = (135, 206, 235)
    bottom_color = (139, 69, 19)
    for y in range(height):
        color = [top_color[i] + (bottom_color[i] - top_color[i])*(y/height) for i in range(3)]
        pygame.draw.line(surface, color, (0, y), (width, y))

#Set a window to notify the player that their information is saved
def open_save_window():
    """
    This is the docstring of open_save_window(), which shows and notifies player about the information being saved in database.
    """
    save_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - Sign up')
    running_save_window = True
    username = ''
    save_confirm = pygame.Rect((width - 400)//2, 200, 400, 100)
    while running_save_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_save_window = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_new_game_window()
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_new_window()

        background_color(save_window, (135, 206, 235), (139, 69, 19))

        pygame.draw.rect(save_window, (0, 200, 0), save_confirm)
        pygame.draw.rect(save_window, (0, 0, 200), save_confirm, 5)
        if check_username_exist(username):
            save_title = pygame.font.SysFont('Arial', 24, bold=True).render('This username already exists!', True, (255, 255, 255))
            break
        else:
            save_title = pygame.font.SysFont('Arial', 24, bold=True).render('Welcome to Stairs of Acropolis!', True, (255, 255, 255))
        save_window.blit(save_title, save_title.get_rect(center=save_confirm.center))

        pygame.draw.rect(save_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        save_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))

        pygame.draw.rect(save_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        save_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.display.flip()
    pygame.quit()

#Set up cursor symbol in textbox
athena_rect = new_athena.get_rect()
flip_athena_rect = pygame.transform.flip(new_athena, True, False).get_rect()
cursor_timer = 0
cursor_visible = True
#Open a new window
def open_new_window():
    """
    This is the docstring of function open_new_window(), which shows the window where a player signs up in game for the first time.
    """
    new_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - Sign up')
    running_new_window = True
    username = ''
    age_text = ''
    place_of_living = ''
    hobby = ''
    gender = ''
    typing = False
    username_rect = pygame.Rect((width - 200)//2, 50, 200, 75)
    age_rect = pygame.Rect((width - 200)//2, 150, 200, 75)
    place_of_living_rect = pygame.Rect((width - 200)//2, 250, 200, 75)
    hobby_rect = pygame.Rect((width - 200)//2, 350, 200, 75)
    save_button_rect = pygame.Rect((width - 100)//2 + 80, 600, 100, 50)
    gender_rect = pygame.Rect((width - 200)//2, 450, 200, 75)
    center_box = pygame.Rect((width - 300)//2, 50, 300, 500)
    sub1 = ''
    sub2 = ''
    sub3 = ''
    sub4 = ''
    while running_new_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_new_window = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sign_up_player_data(username, age_text, place_of_living, hobby, gender)
                    username = ''
                    age_text = ''
                    place_of_living = ''
                    hobby = ''
                    gender = ''
                elif event.key == pygame.K_BACKSPACE:
                    if username_rect.collidepoint(pygame.mouse.get_pos()):
                        username = username[:-1]
                    elif age_rect.collidepoint(pygame.mouse.get_pos()):
                        age_text = age_text[:-1]
                    elif place_of_living_rect.collidepoint(pygame.mouse.get_pos()):
                        place_of_living = place_of_living[:-1]
                    elif hobby_rect.collidepoint(pygame.mouse.get_pos()):
                        hobby = hobby[:-1]
                    elif gender_rect.collidepoint(pygame.mouse.get_pos()):
                        gender = gender[:-1]
                elif typing:
                    if username_rect.collidepoint(pygame.mouse.get_pos()):
                        username += event.unicode
                    elif age_rect.collidepoint(pygame.mouse.get_pos()):
                        age_text += event.unicode
                    elif place_of_living_rect.collidepoint(pygame.mouse.get_pos()):
                        place_of_living += event.unicode
                    elif hobby_rect.collidepoint(pygame.mouse.get_pos()):
                        hobby += event.unicode
                    elif gender_rect.collidepoint(pygame.mouse.get_pos()):
                        gender += event.unicode
                else:
                    typing = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if save_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if not check_username_exist(username):
                        sign_up_player_data(username, age_text, place_of_living, hobby, gender)
                    open_save_window()
                if username_rect.collidepoint(pygame.mouse.get_pos()) and age_rect.collidepoint(pygame.mouse.get_pos()) and place_of_living_rect.collidepoint(pygame.mouse.get_pos()) and hobby_rect.collidepoint(pygame.mouse.get_pos()):
                    typing = True
                else:
                    typing = False
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    main_window()

        background_color(new_window, (135, 206, 235), (139, 69, 19))

        cursor_timer = 0
        cursor_visible = True
        cursor_timer += pygame.time.get_ticks()
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer %= 500

        new_window.blit(new_athena, (width//4 - 1.2*athena_new_w//2, 3*height//2 - 1.5*athena_new_h))
        new_window.blit(pygame.transform.flip(new_athena, True, False), (width//4 - 1.2*athena_new_w//2 + 1.2*width//2, 3*height//2 - 1.5*athena_new_h))

        pygame.draw.rect(new_window, (100, 100, 100), center_box)

        pygame.draw.rect(new_window, (92, 179, 255), username_rect)
        if not username and not typing:
            sub1 = font_to_fill.render("How may we call you?", (114, 114, 114), True)
            new_window.blit(sub1, sub1.get_rect(center=username_rect.center))
        username_blank = font_to_fill.render(username, True, (255, 255, 255))
        new_window.blit(username_blank, username_blank.get_rect(center=username_rect.center))

        pygame.draw.rect(new_window, (92, 179, 255), age_rect)
        if not age_text and not typing:
            sub2 = font_to_fill.render("How old are you?", (114, 114, 114), True)
            new_window.blit(sub2, sub2.get_rect(center=age_rect.center))
        age_blank = font_to_fill.render(age_text, True, (255, 255, 255))
        new_window.blit(age_blank, age_blank.get_rect(center=age_rect.center))

        pygame.draw.rect(new_window, (92, 179, 255), place_of_living_rect)
        if not place_of_living and not typing:
            sub3 = font_to_fill.render("Where do you live?", (114, 114, 114), True)
            new_window.blit(sub3, sub3.get_rect(center=place_of_living_rect.center))
        place_of_living_blank = font_to_fill.render(place_of_living, True, (255, 255, 255))
        new_window.blit(place_of_living_blank, place_of_living_blank.get_rect(center=place_of_living_rect.center))

        pygame.draw.rect(new_window, (92, 179, 255), hobby_rect)
        if not hobby and not typing:
            sub4 = font_to_fill.render("What is your hobby?", (114, 114, 114), True)
            new_window.blit(sub4, sub4.get_rect(center=hobby_rect.center))
        hobby_blank = font_to_fill.render(hobby, True, (255, 255, 255))
        new_window.blit(hobby_blank, hobby_blank.get_rect(center=hobby_rect.center))

        pygame.draw.rect(new_window, (92, 179, 255), gender_rect)
        if not gender and not typing:
            sub1 = font_to_fill.render("Are you men or women?", (114, 114, 114), True)
            new_window.blit(sub1, sub1.get_rect(center=gender_rect.center))
        gender_blank = font_to_fill.render(gender, True, (255, 255, 255))
        new_window.blit(gender_blank, gender_blank.get_rect(center=gender_rect.center))

        pygame.draw.rect(new_window, (34, 139, 34), save_button_rect)
        save_text = pygame.font.SysFont('Arial', 18).render('SAVE', True, (255, 255, 255))
        new_window.blit(save_text, save_text.get_rect(center=save_button_rect.center))

        pygame.draw.rect(new_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        new_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.display.flip()
    pygame.quit()

def open_gorgo_window():
    """
    This is the docstring of function open_gorgo_window(), which shows how Stairs of Acropolis in Gorgo Version works.
    """
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_gorgo = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    gorgo_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    stair_height = height//25
    GORGO_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (0, 201, 87),
        "INTERMEDIATE": (135, 206, 250),
        "HARD": (0, 51, 102),
        "EXPERT": (54, 69, 79)
    }
    running_gorgo = True
    i = 0
    while running_gorgo and i < 25:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    open_new_game_window()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)

        background_color(gorgo_window, (135, 206, 235), (139, 69, 19))

        width_in_process = (width//25)*(25 - i)
        start_stair_x = i*(width//25)
        start_stair_y = height - (i*stair_height)
        color_index = i // 5
        color_level = list(GORGO_COLORS.keys())[color_index % len(GORGO_COLORS)]
        color = GORGO_COLORS[color_level]
        pygame.draw.rect(gorgo_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))
        if progress < 1.0:
            username_written.rw += 2
            username_written.rx -= 1
            username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))
            progress += 0.01
            username_written.update_color(progress)

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))
        if progress < 1.0:
            points_written.rw += 2
            points_written.rx -= 1
            points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 18, (255, 255, 255))
            progress += 0.01
            points_written.update_color(progress)

        pygame.draw.rect(gorgo_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        gorgo_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(gorgo_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        gorgo_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))

        pygame.display.flip()

        i += 1
        pygame.time.wait(100)

    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    open_new_game_window()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin()

        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(GORGO_COLORS.keys())[color_index % len(GORGO_COLORS)]
            color = GORGO_COLORS[color_level]
            pygame.draw.rect(gorgo_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        introduction_gorgo.roundrectdraw(gorgo_window)
        introduction_word = ('Hello,', pop_username(), '! Welcome to the version of Stairs of Acropolis where you can feel much pleasant and less pressure, the Gorgo Version!')
        introduction_gorgo.roundrectfill(gorgo_window, ''.join(str(item) for item in introduction_word), 'Century Gothic', 30, (255, 255, 240), False)
        if progress < 1.0:
            introduction_gorgo.rw += 2
            introduction_gorgo.roundrectfill(gorgo_window, ''.join(str(item) for item in introduction_word), 'Century Gothic', 30, (255, 255, 240), False)
            progress += 0.01
            introduction_gorgo.update_color(progress)

        pygame.draw.rect(gorgo_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        gorgo_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(gorgo_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        gorgo_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))
        pygame.display.flip()

def open_gorgo_window_twin_docstring():
    """
    This is the docstring of function open_gorgo_window_twin_docstring(), which represents all twins of open_gorgo_window() to show how the host communicates with a player via Gorgo Version.
    """
    pass

def open_gorgo_window_twin():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_gorgo = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    gorgo_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    stair_height = height//25
    typed_effect_char = ''
    typing_speed = 50
    clock = pygame.time.Clock()
    index = 0
    start_time = time.time()
    GORGO_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (0, 201, 87),
        "INTERMEDIATE": (135, 206, 250),
        "HARD": (0, 51, 102),
        "EXPERT": (54, 69, 79)
    }
    running_gorgo = True
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    open_gorgo_window()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin2()

        background_color(gorgo_window, (135, 206, 235), (139, 69, 19))
        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(GORGO_COLORS.keys())[color_index % len(GORGO_COLORS)]
            color = GORGO_COLORS[color_level]
            pygame.draw.rect(gorgo_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        introduction_gorgo.roundrectdraw(gorgo_window)
        introduction_word2 = "As you've entered Stairs of Acropolis, for each game turn, you have to answer 25 questions correctly to achieve the highest goal:\
              BECOME THE MASTERMIND OF KNOWLEDGE."
        if progress < 1.0:
            introduction_gorgo.rw += 2
            progress += 0.01
            introduction_gorgo.update_color(progress)
        if index < len(str(introduction_word2)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(introduction_word2)[index]
                index += 1
                start_time = time.time()
        introduction_gorgo.roundrectfill(gorgo_window, typed_effect_char, 'Century Gothic', 30, (255, 255, 240), False)

        pygame.draw.rect(gorgo_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        gorgo_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(gorgo_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        gorgo_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))
        pygame.display.flip()

        clock.tick(60)
    pygame.quit()

def open_gorgo_window_twin2():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_gorgo = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    gorgo_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    stair_height = height//25
    typed_effect_char = ''
    typing_speed = 50
    clock = pygame.time.Clock()
    index = 0
    start_time = time.time()
    GORGO_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (0, 201, 87),
        "INTERMEDIATE": (135, 206, 250),
        "HARD": (0, 51, 102),
        "EXPERT": (54, 69, 79)
    }
    running_gorgo = True
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin3()

        background_color(gorgo_window, (135, 206, 235), (139, 69, 19))
        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(GORGO_COLORS.keys())[color_index % len(GORGO_COLORS)]
            color = GORGO_COLORS[color_level]
            pygame.draw.rect(gorgo_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        introduction_gorgo.roundrectdraw(gorgo_window)
        introduction_word4 = "As for Gorgo Version, the question you're going to meet is all multiple-choices questions with four options from A to D.\n You have to choose one of them to answer the question given.\n If your answer is correct, the option bar'll turn blue and you get points, otherwise it'll turn red and you'll be disadvantageous."
        if progress < 1.0:
            introduction_gorgo.rw += 2
            progress += 0.01
            introduction_gorgo.update_color(progress)
        if index < len(str(introduction_word4)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(introduction_word4)[index]
                index += 1
                start_time = time.time()
        introduction_gorgo.roundrectfill(gorgo_window, typed_effect_char, 'Century Gothic', 30, (255, 255, 240), False)

        pygame.draw.rect(gorgo_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        gorgo_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(gorgo_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        gorgo_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

def open_gorgo_window_twin3():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_gorgo = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    gorgo_window = pygame.display.set_mode((width, height))
    typed_effect_char = ''
    typing_speed = 50
    clock = pygame.time.Clock()
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    stair_height = height//25
    GORGO_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (0, 201, 87),
        "INTERMEDIATE": (135, 206, 250),
        "HARD": (0, 51, 102),
        "EXPERT": (54, 69, 79)
    }
    running_gorgo = True
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin2()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin4()

        background_color(gorgo_window, (135, 206, 235), (139, 69, 19))
        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(GORGO_COLORS.keys())[color_index % len(GORGO_COLORS)]
            color = GORGO_COLORS[color_level]
            pygame.draw.rect(gorgo_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        introduction_gorgo.roundrectdraw(gorgo_window)
        introduction_word6 = "25 questions are divided by five levels with difficulty gradually increasing.\n There are also nine specialties from Mathematics to Sports and for each question you're about to enter, you can choose one of them.\n After choosing, each speacialty'll show the remaining questions so you have to be cautious about your decision."
        if progress < 1.0:
            introduction_gorgo.rw += 2
            progress += 0.01
            introduction_gorgo.update_color(progress)
        if index < len(str(introduction_word6)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(introduction_word6)[index]
                index += 1
                start_time = time.time()
        introduction_gorgo.roundrectfill(gorgo_window, typed_effect_char, 'Century Gothic', 30, (255, 255, 240), False)

        pygame.draw.rect(gorgo_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        gorgo_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(gorgo_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        gorgo_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))
        
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

def open_gorgo_window_twin4():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_gorgo = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    divide_half_img = pygame.transform.scale(pygame.image.load('50:50.png'), (100, 100))
    hint_img = pygame.transform.scale(pygame.image.load('Light-bulb.png'), (100, 100))
    gif_symbol_img = pygame.transform.scale(pygame.image.load('gif.png'), (100, 100))
    gorgo_window = pygame.display.set_mode((width, height))
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    stair_height = height//25
    GORGO_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (0, 201, 87),
        "INTERMEDIATE": (135, 206, 250),
        "HARD": (0, 51, 102),
        "EXPERT": (54, 69, 79)
    }
    running_gorgo = True
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin2()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin5()

        background_color(gorgo_window, (135, 206, 235), (139, 69, 19))
        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(GORGO_COLORS.keys())[color_index % len(GORGO_COLORS)]
            color = GORGO_COLORS[color_level]
            pygame.draw.rect(gorgo_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        gorgo_window.blit(divide_half_img, (50, 400, divide_half_img.get_rect().width, divide_half_img.get_rect().height))
        gorgo_window.blit(hint_img, (150, 400, hint_img.get_rect().width, hint_img.get_rect().height))
        gorgo_window.blit(gif_symbol_img, (250, 400, gif_symbol_img.get_rect().width, gif_symbol_img.get_rect().height))

        introduction_gorgo.roundrectdraw(gorgo_window)
        introduction_word8 = "In Gorgo Version, in case you are in trouble with difficult questions, you can use one of the three lifelines:\
              50/50 DIVISION: To omit two wrong answers\
                GIVING HINT: To give a good hint for finding correct answer\
                GIVING GIFS: To give a cinemagraph for finding correct answer"
        if progress < 1.0:
            introduction_gorgo.rw += 2
            progress += 0.01
            introduction_gorgo.update_color(progress)
        if index < len(introduction_word8):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += (introduction_word8)[index]
                index += 1
                start_time = time.time()
        introduction_gorgo.roundrectfill(gorgo_window, typed_effect_char, 'Century Gothic', 30, (255, 255, 240), False)

        pygame.draw.rect(gorgo_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        gorgo_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(gorgo_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        gorgo_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

def open_gorgo_window_twin5():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    question_number_written = RoundRectTextbox(690, 40, 160, 75, (255, 165, 0), (248, 222, 126))
    introduction_gorgo = RoundRectTextbox(300, 150, 150, 250, (128, 128, 128), (255, 255, 255))
    gorgo_window = pygame.display.set_mode((width, height))
    surface_img = pygame.image.load('beautiful_mountain.jpeg')
    mathematics_img = pygame.transform.scale(pygame.image.load('mathematics.png'), (100, 100))
    physics_img = pygame.transform.scale(pygame.image.load('physics.png'), (100, 100))
    chemistry_img = pygame.transform.scale(pygame.image.load('chemistry.png'), (100, 100))
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    photo_surface = pygame.Surface((width, height))
    photo_surface.blit(surface_img, (0, 0))
    photo_surface.set_colorkey((255, 255, 255))
    photo_surface.set_alpha(128)
    gorgo_window.blit(photo_surface, (0, 0))
    pygame.display.flip()
    running_gorgo = True
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin2()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_window_twin5()
                if mathematics_img.get_rect(topleft=(300, 400)).collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_mathematics()
                elif physics_img.get_rect(topleft=(400, 400)).collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_physics()
                elif chemistry_img.get_rect(topleft=(500, 400)).collidepoint(pygame.mouse.get_pos()):
                    open_gorgo_chemistry()

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

        question_number_written.roundrectdraw(gorgo_window)
        question_number_written.roundrectfill(gorgo_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
    
        introduction_gorgo.roundrectdraw(gorgo_window)
        introduction_word8 = "HERE WE GO, FOR FIVE FIRST QUESTIONS IN BEGINNER LEVEL! PLEASE CHOOSE ONE OF THE SPECIALTIES BELOW."
        if progress < 1.0:
            introduction_gorgo.rw += 2
            progress += 0.01
            introduction_gorgo.update_color(progress)
        if index < len(introduction_word8):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += (introduction_word8)[index]
                index += 1
                start_time = time.time()
        introduction_gorgo.roundrectfill(gorgo_window, typed_effect_char, 'Century Gothic', 30, (255, 255, 240), False)

        gorgo_window.blit(mathematics_img, (300, 400, mathematics_img.get_rect().width, mathematics_img.get_rect().height))
        gorgo_window.blit(physics_img, (400, 400, physics_img.get_rect().width, physics_img.get_rect().height))
        gorgo_window.blit(chemistry_img, (500, 400, chemistry_img.get_rect().width, chemistry_img.get_rect().height))

        pygame.draw.rect(gorgo_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        gorgo_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(gorgo_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        gorgo_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

def open_gorgo_mathematics():
    """
    This is the docstring of function open_gorgo_mathematics(), which show Mathematics' side of Gorgo Version.
    """
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    question_number_written = RoundRectTextbox(690, 40, 160, 75, (255, 165, 0), (248, 222, 126))
    math_question = RoundRectTextbox(100, 350, 500, 100, (0, 117, 94), (41, 171, 135))
    option_A = RoundRectTextbox(100, 500, 150, 75, (0, 117, 94), (41, 171, 135))
    option_B = RoundRectTextbox(300, 500, 150, 75, (0, 117, 94), (41, 171, 135))
    option_C = RoundRectTextbox(100, 600, 150, 75, (0, 117, 94), (41, 171, 135))
    option_D = RoundRectTextbox(300, 600, 150, 75, (0, 117, 94), (41, 171, 135))
    gorgo_window = pygame.display.set_mode((width, height))
    surface_img = pygame.image.load('beautiful_mountain.jpeg')
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    photo_surface = pygame.Surface((width, height))
    photo_surface.blit(surface_img, (0, 0))
    photo_surface.set_colorkey((255, 255, 255))
    photo_surface.set_alpha(128)
    gorgo_window.blit(photo_surface, (0, 0))
    pygame.display.flip()
    running_gorgo = True
    option_boxes = [option_A, option_B, option_C, option_D]
    option_texts = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_gorgo = False
    gorgo_question_data = pop_questions_gorgo('Mathematics')
    if gorgo_question_data:
        question, optionA, optionB, optionC, optionD, correct_answer = gorgo_question_data
        math_question.roundrectdraw(gorgo_window)
        if progress < 1.0:
            math_question.rw += 2
            progress += 0.01
            math_question.update_color(progress)
        if index < len(str(question)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(question)[index]
                index += 1
                start_time = time.time()
        math_question.roundrectfill(gorgo_window, question, rrfont_name='Arial', rrfontsize=18, rrfontcolor=(255, 255, 255))
        pygame.time.wait(500)
        option_A.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_A.rw += 2
            progress += 0.01
            option_A.update_color(progress)
        if index < len(str(optionA)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionA)[index]
                index += 1
                start_time = time.time()
        option_A.roundrectfill(gorgo_window, optionA, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))
        pygame.time.wait(500)
        option_B.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_B.rw += 2
            progress += 0.01
            option_B.update_color(progress)
        if index < len(str(optionB)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionB)[index]
                index += 1
                start_time = time.time()
        option_B.roundrectfill(gorgo_window, optionB, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))
        pygame.time.wait(500)
        option_C.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_C.rw += 2
            progress += 0.01
            option_C.update_color(progress)
        if index < len(str(optionC)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionC)[index]
                index += 1
                start_time = time.time()
        option_C.roundrectfill(gorgo_window, optionC, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))
        pygame.time.wait(500)
        option_D.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_D.rw += 2
            progress += 0.01
            option_D.update_color(progress)
        if index < len(str(optionD)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionD)[index]
                index += 1
                start_time = time.time()
        option_D.roundrectfill(gorgo_window, optionD, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))

    username_written.roundrectdraw(gorgo_window)
    username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

    points_written.roundrectdraw(gorgo_window)
    points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

    question_number_written.roundrectdraw(gorgo_window)
    question_number_written.roundrectfill(gorgo_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
    pygame.display.flip()
    option_texts = [optionA, optionB, optionC, optionD]
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_gorgo = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option_box, option_text in zip(option_boxes, option_texts):
                    if option_box.roundrect.collidepoint(pygame.mouse.get_pos()):
                        if option_text == correct_answer:
                            pygame.time.wait(3000)
                            option_box.start_color = (0, 0, 255)
                        else:
                            pygame.time.wait(3000)
                            option_box.start_color = (255, 0, 0)
                        option_box.roundrectdraw(gorgo_window)
                        option_box.roundrectfill(gorgo_window, option_text, rrfont_name='Arial', rrfontsize=12)

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

        question_number_written.roundrectdraw(gorgo_window)
        question_number_written.roundrectfill(gorgo_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
        pygame.display.flip()

def open_gorgo_physics():
    """
    This is the docstring of function open_gorgo_physics(), which show Physics' side of Gorgo Version.
    """
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    question_number_written = RoundRectTextbox(690, 40, 160, 75, (255, 165, 0), (248, 222, 126))
    physics_question = RoundRectTextbox(100, 350, 500, 100, (0, 117, 94), (41, 171, 135))
    option_A = RoundRectTextbox(100, 500, 150, 75, (0, 117, 94), (41, 171, 135))
    option_B = RoundRectTextbox(300, 500, 150, 75, (0, 117, 94), (41, 171, 135))
    option_C = RoundRectTextbox(100, 600, 150, 75, (0, 117, 94), (41, 171, 135))
    option_D = RoundRectTextbox(300, 600, 150, 75, (0, 117, 94), (41, 171, 135))
    gorgo_window = pygame.display.set_mode((width, height))
    surface_img = pygame.image.load('beautiful_mountain.jpeg')
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    photo_surface = pygame.Surface((width, height))
    photo_surface.blit(surface_img, (0, 0))
    photo_surface.set_colorkey((255, 255, 255))
    photo_surface.set_alpha(128)
    gorgo_window.blit(photo_surface, (0, 0))
    pygame.display.flip()
    option_boxes = [option_A, option_B, option_C, option_D]
    option_texts = []
    running_gorgo = True
    gorgo_question_data = pop_questions_gorgo('Physics')
    if gorgo_question_data:
        question, optionA, optionB, optionC, optionD, correct_answer = gorgo_question_data
        physics_question.roundrectdraw(gorgo_window)
        if progress < 1.0:
            physics_question.rw += 2
            progress += 0.01
            physics_question.update_color(progress)
        if index < len(str(question)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(question)[index]
                index += 1
                start_time = time.time()
        physics_question.roundrectfill(gorgo_window, question, rrfont_name='Arial', rrfontsize=12)
        pygame.time.wait(500)
        option_A.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_A.rw += 2
            progress += 0.01
            option_A.update_color(progress)
        if index < len(str(optionA)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionA)[index]
                index += 1
                start_time = time.time()
        option_A.roundrectfill(gorgo_window, optionA, rrfont_name='Arial', rrfontsize=12)
        pygame.time.wait(500)
        option_B.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_B.rw += 2
            progress += 0.01
            option_B.update_color(progress)
        if index < len(str(optionB)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionB)[index]
                index += 1
                start_time = time.time()
        option_B.roundrectfill(gorgo_window, optionB, rrfont_name='Arial', rrfontsize=12)
        pygame.time.wait(500)
        option_C.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_C.rw += 2
            progress += 0.01
            option_C.update_color(progress)
        if index < len(str(optionC)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionC)[index]
                index += 1
                start_time = time.time()
        option_C.roundrectfill(gorgo_window, optionC, rrfont_name='Arial', rrfontsize=12)
        pygame.time.wait(500)
        option_D.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_D.rw += 2
            progress += 0.01
            option_D.update_color(progress)
        if index < len(str(optionD)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionD)[index]
                index += 1
                start_time = time.time()
        option_D.roundrectfill(gorgo_window, optionD, rrfont_name='Arial', rrfontsize=12)

    username_written.roundrectdraw(gorgo_window)
    username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

    points_written.roundrectdraw(gorgo_window)
    points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

    question_number_written.roundrectdraw(gorgo_window)
    question_number_written.roundrectfill(gorgo_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
    pygame.display.flip()
    option_texts = [optionA, optionB, optionC, optionD]
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_gorgo = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option_box, option_text in zip(option_boxes, option_texts):
                    if option_box.roundrect.collidepoint(pygame.mouse.get_pos()):
                        if option_text == correct_answer:
                            pygame.time.wait(3000)
                            option_box.start_color = (0, 0, 255)
                        else:
                            pygame.time.wait(3000)
                            option_box.start_color = (255, 0, 0)
                        option_box.roundrectdraw(gorgo_window)
                        option_box.roundrectfill(gorgo_window, option_text, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

        question_number_written.roundrectdraw(gorgo_window)
        question_number_written.roundrectfill(gorgo_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
        pygame.display.flip()

def open_gorgo_chemistry():
    """
    This is the docstring of function open_gorgo_chemistry(), which show Chemistry's side of Gorgo Version.
    """
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    question_number_written = RoundRectTextbox(690, 40, 160, 75, (255, 165, 0), (248, 222, 126))
    chemistry_question = RoundRectTextbox(100, 350, 500, 100, (0, 117, 94), (41, 171, 135))
    option_A = RoundRectTextbox(100, 500, 150, 75, (0, 117, 94), (41, 171, 135))
    option_B = RoundRectTextbox(300, 500, 150, 75, (0, 117, 94), (41, 171, 135))
    option_C = RoundRectTextbox(100, 600, 150, 75, (0, 117, 94), (41, 171, 135))
    option_D = RoundRectTextbox(300, 600, 150, 75, (0, 117, 94), (41, 171, 135))
    gorgo_window = pygame.display.set_mode((width, height))
    surface_img = pygame.image.load('beautiful_mountain.jpeg')
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    photo_surface = pygame.Surface((width, height))
    photo_surface.blit(surface_img, (0, 0))
    photo_surface.set_colorkey((255, 255, 255))
    photo_surface.set_alpha(128)
    gorgo_window.blit(photo_surface, (0, 0))
    pygame.display.flip()
    option_boxes = [option_A, option_B, option_C, option_D]
    option_texts = []
    running_gorgo = True
    gorgo_question_data = pop_questions_gorgo('Chemistry')
    if gorgo_question_data:
        question, optionA, optionB, optionC, optionD, correct_answer = gorgo_question_data
        chemistry_question.roundrectdraw(gorgo_window)
        if progress < 1.0:
            chemistry_question.rw += 2
            progress += 0.01
            chemistry_question.update_color(progress)
        if index < len(str(question)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(question)[index]
                index += 1
                start_time = time.time()
        chemistry_question.roundrectfill(gorgo_window, question, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))
        pygame.time.wait(500)
        option_A.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_A.rw += 2
            progress += 0.01
            option_A.update_color(progress)
        if index < len(str(optionA)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionA)[index]
                index += 1
                start_time = time.time()
        option_A.roundrectfill(gorgo_window, optionA, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))
        pygame.time.wait(500)
        option_B.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_B.rw += 2
            progress += 0.01
            option_B.update_color(progress)
        if index < len(str(optionB)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionB)[index]
                index += 1
                start_time = time.time()
        option_B.roundrectfill(gorgo_window, optionB, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))
        pygame.time.wait(500)
        option_C.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_C.rw += 2
            progress += 0.01
            option_C.update_color(progress)
        if index < len(str(optionC)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionC)[index]
                index += 1
                start_time = time.time()
        option_C.roundrectfill(gorgo_window, optionC, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))
        pygame.time.wait(500)
        option_D.roundrectdraw(gorgo_window)
        if progress < 1.0:
            option_D.rw += 2
            progress += 0.01
            option_D.update_color(progress)
        if index < len(str(optionD)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(optionD)[index]
                index += 1
                start_time = time.time()
        option_D.roundrectfill(gorgo_window, optionD, rrfont_name='Arial', rrfontsize=12, rrfontcolor=(255, 255, 255))
    
    username_written.roundrectdraw(gorgo_window)
    username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

    points_written.roundrectdraw(gorgo_window)
    points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

    question_number_written.roundrectdraw(gorgo_window)
    question_number_written.roundrectfill(gorgo_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
    pygame.display.flip()
    option_texts = [optionA, optionB, optionC, optionD]
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_gorgo = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option_box, option_text in zip(option_boxes, option_texts):
                    if option_box.roundrect.collidepoint(pygame.mouse.get_pos()):
                        if option_text == correct_answer:
                            pygame.time.wait(3000)
                            option_box.start_color = (0, 0, 255)
                        else:
                            pygame.time.wait(3000)
                            option_box.start_color = (255, 0, 0)
                        option_box.roundrectdraw(gorgo_window)
                        option_box.roundrectfill(gorgo_window, option_text, rrfont_name='Arial', rrfontsize=12)

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

        question_number_written.roundrectdraw(gorgo_window)
        question_number_written.roundrectfill(gorgo_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
        pygame.display.flip()

def open_sparta_window():
    """
    This is the docstring of function open_gorgo_window(), which shows how Stairs of Acropolis in Sparta Version works.
    """
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_sparta = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    sparta_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - New Game - Sparta')
    stair_height = height//25
    SPARTA_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (255, 255, 0),
        "INTERMEDIATE": (255, 165, 0),
        "HARD": (220, 20, 60),
        "EXPERT": (54, 69, 79)
    }
    running_sparta = True
    i = 0
    while running_sparta and i < 25:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_sparta = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    open_new_game_window()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin()

        background_color(sparta_window, (135, 206, 235), (139, 69, 19))

        width_in_process = (width/25)*(25 - i)

        start_stair_x = i*(width/25)
        start_stair_y = height - (i*stair_height)

        color_index = i // 5
        color_level = list(SPARTA_COLORS.keys())[color_index % len(SPARTA_COLORS)]
        color = SPARTA_COLORS[color_level]
        pygame.draw.rect(sparta_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(sparta_window)
        username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))
        if progress < 1.0:
            username_written.rw += 2
            username_written.rx -= 1
            username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))
            progress += 0.01
            username_written.update_color(progress)

        points_written.roundrectdraw(sparta_window)
        points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))
        if progress < 1.0:
            points_written.rw += 2
            points_written.rx -= 1
            points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))
            progress += 0.01
            points_written.update_color(progress)

        pygame.draw.rect(sparta_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        sparta_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))
        pygame.display.flip()

        pygame.draw.rect(sparta_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        sparta_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))
        pygame.display.flip()

        pygame.display.flip()
        i += 1
        pygame.time.wait(100)

    while running_sparta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    open_new_game_window()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin()

        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(SPARTA_COLORS.keys())[color_index % len(SPARTA_COLORS)]
            color = SPARTA_COLORS[color_level]
            pygame.draw.rect(sparta_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        introduction_sparta.roundrectdraw(sparta_window)
        introduction_word1 = ('Hello,', pop_username(), '! Welcome to the version of Stairs of Acropolis where you can challenge your own bravery and confidence, the Sparta Version!')
        introduction_sparta.roundrectfill(sparta_window, ''.join(str(item) for item in introduction_word1), 'Century Gothic', 30, (255, 255, 240), False)
        if progress < 1.0:
            introduction_sparta.rw += 2
            introduction_sparta.roundrectfill(sparta_window, ''.join(str(item) for item in introduction_word1), 'Century Gothic', 30, (255, 255, 240), False)
            progress += 0.01
            introduction_sparta.update_color(progress)

        pygame.draw.rect(sparta_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        sparta_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(sparta_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        sparta_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))
        pygame.display.flip()

def open_sparta_window_twin_docstring():
    """
    This is the docstring of function open_sparta_window_twin_docstring(), which represents all twins of open_sparta_window() to show how the host communicates with a player via Sparta Version.
    """
    pass
def open_sparta_window_twin():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_sparta = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    sparta_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - New Game - Sparta')
    stair_height = height//25
    SPARTA_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (255, 255, 0),
        "INTERMEDIATE": (255, 165, 0),
        "HARD": (220, 20, 60),
        "EXPERT": (54, 69, 79)
    }
    typed_effect_char = ''
    typing_speed = 50
    clock = pygame.time.Clock()
    index = 0
    start_time = time.time()
    running_sparta = True
    while running_sparta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    open_sparta_window()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin2()

        background_color(sparta_window, (135, 206, 235), (139, 69, 19))
        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(SPARTA_COLORS.keys())[color_index % len(SPARTA_COLORS)]
            color = SPARTA_COLORS[color_level]
            pygame.draw.rect(sparta_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(sparta_window)
        username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(sparta_window)
        points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        introduction_sparta.roundrectdraw(sparta_window)
        introduction_word3 = "As you've entered Stairs of Acropolis, for each game turn, you have to answer 25 questions correctly to achieve the highest goal:\n BECOME THE MASTERMIND OF KNOWLEDGE."
        if progress < 1.0:
            introduction_sparta.rw += 2
            progress += 0.01
            introduction_sparta.update_color(progress)
        if index < len(str(introduction_word3)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(introduction_word3)[index]
                index += 1
                start_time = time.time()
        introduction_sparta.roundrectfill(sparta_window, typed_effect_char.replace('(', '').replace(',', '').replace(')', ''), 'Century Gothic', 30, (255, 255, 240), False)

        pygame.draw.rect(sparta_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        sparta_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(sparta_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        sparta_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))
        pygame.display.flip()
    pygame.quit()

def open_sparta_window_twin2():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_sparta = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    sparta_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - New Game - Sparta')
    stair_height = height//25
    SPARTA_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (255, 255, 0),
        "INTERMEDIATE": (255, 165, 0),
        "HARD": (220, 20, 60),
        "EXPERT": (54, 69, 79)
    }
    typed_effect_char = ''
    typing_speed = 50
    index = 0
    clock = pygame.time.Clock()
    start_time = time.time()
    running_sparta = True
    while running_sparta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin3()

        background_color(sparta_window, (135, 206, 235), (139, 69, 19))
        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(SPARTA_COLORS.keys())[color_index % len(SPARTA_COLORS)]
            color = SPARTA_COLORS[color_level]
            pygame.draw.rect(sparta_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(sparta_window)
        username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(sparta_window)
        points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        introduction_sparta.roundrectdraw(sparta_window)
        introduction_word5 = "As for Sparta Version, the question you're going to meet is all questions on which you have to write or speak your own answer. \n If your answer matches with the original answer, the answer bar'll turn yellow and you get points, \n otherwise it'll turn red and you'll be disadvantageous."
        if progress < 1.0:
            introduction_sparta.rw += 2
            progress += 0.01
            introduction_sparta.update_color(progress)
        if index < len(str(introduction_word5)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(introduction_word5)[index]
                index += 1
                start_time = time.time()
        introduction_sparta.roundrectfill(sparta_window, typed_effect_char.replace('(', '').replace(',', '').replace(')', ''), 'Century Gothic', 30, (255, 255, 240), False)

        pygame.draw.rect(sparta_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        sparta_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(sparta_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        sparta_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

def open_sparta_window_twin3():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_sparta = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    sparta_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Stairs of Acropolis - New Game - Sparta')
    stair_height = height//25
    SPARTA_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (255, 255, 0),
        "INTERMEDIATE": (255, 165, 0),
        "HARD": (220, 20, 60),
        "EXPERT": (54, 69, 79)
    }
    typed_effect_char = ''
    typing_speed = 50
    index = 0
    clock = pygame.time.Clock()
    start_time = time.time()
    running_sparta = True
    while running_sparta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin2()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin4()

        background_color(sparta_window, (135, 206, 235), (139, 69, 19))
        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(SPARTA_COLORS.keys())[color_index % len(SPARTA_COLORS)]
            color = SPARTA_COLORS[color_level]
            pygame.draw.rect(sparta_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(sparta_window)
        username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(sparta_window)
        points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        introduction_sparta.roundrectdraw(sparta_window)
        introduction_word7 = "25 questions are divided by five levels with difficulty gradually increasing.\n There are also nine specialties from Mathematics to Sports and for each question you're about to enter, you can choose one of them.\n After choosing, each speacialty'll show the remaining questions so you have to be cautious about your decision."
        if progress < 1.0:
            introduction_sparta.rw += 2
            progress += 0.01
            introduction_sparta.update_color(progress)
        if index < len(str(introduction_word7)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(introduction_word7)[index]
                index += 1
                start_time = time.time()
        introduction_sparta.roundrectfill(sparta_window, typed_effect_char.replace('(', '').replace(',', '').replace(')', ''), 'Century Gothic', 30, (255, 255, 240), False)

        pygame.draw.rect(sparta_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        sparta_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(sparta_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        sparta_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

def open_sparta_window_twin4():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    introduction_gorgo = RoundRectTextbox(50, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    img_provide_img = pygame.transform.scale(pygame.image.load('image-symbol.png'), (100, 100))
    hint_img = pygame.transform.scale(pygame.image.load('Light-bulb.png'), (100, 100))
    gif_symbol_img = pygame.transform.scale(pygame.image.load('gif.png'), (100, 100))
    gorgo_window = pygame.display.set_mode((width, height))
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    stair_height = height//25
    SPARTA_COLORS = {
        "BEGINNER": (255, 255, 240),
        "EASY": (255, 255, 0),
        "INTERMEDIATE": (255, 165, 0),
        "HARD": (220, 20, 60),
        "EXPERT": (54, 69, 79)
    }
    running_gorgo = True
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin3()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin5()

        background_color(gorgo_window, (135, 206, 235), (139, 69, 19))
        for i in range(25):
            width_in_process = (width//25)*(25 - i)
            start_stair_x = i*(width//25)
            start_stair_y = height - (i*stair_height)
            color_index = i // 5
            color_level = list(SPARTA_COLORS.keys())[color_index % len(SPARTA_COLORS)]
            color = SPARTA_COLORS[color_level]
            pygame.draw.rect(gorgo_window, color, (start_stair_x, start_stair_y, width_in_process, stair_height))

        username_written.roundrectdraw(gorgo_window)
        username_written.roundrectfill(gorgo_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(gorgo_window)
        points_written.roundrectfill(gorgo_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        gorgo_window.blit(img_provide_img, (50, 400, img_provide_img.get_rect().width, img_provide_img.get_rect().height))
        gorgo_window.blit(hint_img, (150, 400, hint_img.get_rect().width, hint_img.get_rect().height))
        gorgo_window.blit(gif_symbol_img, (250, 400, gif_symbol_img.get_rect().width, gif_symbol_img.get_rect().height))

        introduction_gorgo.roundrectdraw(gorgo_window)
        introduction_word9 = "In Gorgo Version, in case you are in trouble with difficult questions, you can use one of the three lifelines:\
              GIVING IMAGE: To give an image for finding correct answer\
                GIVING HINT: To give a good hint for finding correct answer\
                GIVING GIFS: To give a cinemagraph for finding correct answer"
        if progress < 1.0:
            introduction_gorgo.rw += 2
            progress += 0.01
            introduction_gorgo.update_color(progress)
        if index < len(introduction_word9):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += (introduction_word9)[index]
                index += 1
                start_time = time.time()
        introduction_gorgo.roundrectfill(gorgo_window, typed_effect_char, 'Century Gothic', 30, (255, 255, 240), False)

        pygame.draw.rect(gorgo_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        gorgo_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(gorgo_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        gorgo_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))
        
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

def open_sparta_window_twin5():
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    question_number_written = RoundRectTextbox(690, 40, 160, 75, (255, 165, 0), (248, 222, 126))
    introduction_gorgo = RoundRectTextbox(300, 150, 100, 250, (128, 128, 128), (255, 255, 255))
    sparta_window = pygame.display.set_mode((width, height))
    mathematics_img = pygame.transform.scale(pygame.image.load('mathematics.png'), (100, 100))
    physics_img = pygame.transform.scale(pygame.image.load('physics.png'), (100, 100))
    chemistry_img = pygame.transform.scale(pygame.image.load('chemistry.png'), (100, 100))
    volcano_img = pygame.image.load('volcano.jpeg')
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Gorgo')
    photo_surface = pygame.Surface((width, height))
    photo_surface.blit(volcano_img, (0, 0))
    photo_surface.set_colorkey((255, 255, 255))
    photo_surface.set_alpha(128)
    sparta_window.blit(photo_surface, (0, 0))
    pygame.display.flip()
    running_gorgo = True
    while running_gorgo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin3()
                elif continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                    open_sparta_window_twin5()
                elif mathematics_img.get_rect(topleft=(300, 400)).collidepoint(pygame.mouse.get_pos()):
                    open_sparta_mathematics()
                elif physics_img.get_rect(topleft=(400, 400)).collidepoint(pygame.mouse.get_pos()):
                    open_sparta_physics()
                elif chemistry_img.get_rect(topleft=(500, 400)).collidepoint(pygame.mouse.get_pos()):
                    open_sparta_chemistry()

        username_written.roundrectdraw(sparta_window)
        username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(sparta_window)
        points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))

        question_number_written.roundrectdraw(sparta_window)
        question_number_written.roundrectfill(sparta_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))

        sparta_window.blit(mathematics_img, (300, 400, mathematics_img.get_rect().width, mathematics_img.get_rect().height))
        sparta_window.blit(physics_img, (400, 400, physics_img.get_rect().width, physics_img.get_rect().height))
        sparta_window.blit(chemistry_img, (500, 400, chemistry_img.get_rect().width, chemistry_img.get_rect().height))

        introduction_gorgo.roundrectdraw(sparta_window)
        introduction_word9 = "HERE WE GO, FOR FIVE FIRST QUESTIONS IN BEGINNER LEVEL! PLEASE CHOOSE ONE OF THE SPECIALTIES BELOW."
        if progress < 1.0:
            introduction_gorgo.rw += 2
            progress += 0.01
            introduction_gorgo.update_color(progress)
        if index < len(introduction_word9):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += (introduction_word9)[index]
                index += 1
                start_time = time.time()
        introduction_gorgo.roundrectfill(sparta_window, typed_effect_char, 'Century Gothic', 30, (255, 0, 0), False)

        pygame.draw.rect(sparta_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        sparta_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))

        pygame.draw.rect(sparta_window, (34, 139, 34), continue_button_rect)
        continue_text = pygame.font.SysFont('Arial', 18).render('CONTINUE', True, (255, 255, 255))
        sparta_window.blit(continue_text, continue_text.get_rect(center=continue_button_rect.center))

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

def open_sparta_mathematics():
    """
    This is the docstring of function open_sparta_mathematics(), which show Mathematics' side of Sparta Version.
    """
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    question_number_written = RoundRectTextbox(690, 40, 160, 75, (255, 165, 0), (248, 222, 126))
    math_question = RoundRectTextbox(100, 350, 500, 100, (0, 117, 94), (41, 171, 135))
    answer_bar = RoundRectTextbox(100, 500, 500, 100, (0, 117, 94), (41, 171, 135))
    sparta_window = pygame.display.set_mode((width, height))
    surface_img = pygame.image.load('volcano.jpeg')
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Sparta')
    photo_surface = pygame.Surface((width, height))
    photo_surface.blit(surface_img, (0, 0))
    photo_surface.set_colorkey((255, 255, 255))
    photo_surface.set_alpha(128)
    sparta_window.blit(photo_surface, (0, 0))
    pygame.display.flip()
    running_sparta = True
    option_texts = []
    typed_answer = ''
    sparta_question_data = pop_questions_sparta('Mathematics')
    if sparta_question_data:
        question, correct_answer = sparta_question_data
        math_question.roundrectdraw(sparta_window)
        if progress < 1.0:
            math_question.rw += 2
            progress += 0.01
            math_question.update_color(progress)
        if index < len(str(question)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(question)[index]
                index += 1
                start_time = time.time()
        math_question.roundrectfill(sparta_window, question, rrfont_name='Arial', rrfontsize=12)
        pygame.time.wait(500)
        answer_bar.roundrectdraw(sparta_window)
        answer_bar.roundrectfill(sparta_window, typed_answer, 'Arial', 12, (255, 255, 255))

    username_written.roundrectdraw(sparta_window)
    username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

    points_written.roundrectdraw(sparta_window)
    points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

    question_number_written.roundrectdraw(sparta_window)
    question_number_written.roundrectfill(sparta_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
    pygame.display.flip()
    while running_sparta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_sparta = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if answer_bar.roundrect.collidepoint(pygame.mouse.get_pos()):
                    typing = True
                else:
                    if typing:
                        if typed_answer.lower() == correct_answer.lower():
                            pygame.time.wait(3000)
                            answer_bar.start_color = (0, 255, 0)
                        else:
                            pygame.time.wait(3000)
                            answer_bar.start_color = (255, 165, 0)
                        typing = False
                answer_bar.roundrectdraw(sparta_window)
                answer_bar.roundrectfill(sparta_window, typed_answer, 24, (0, 0, 0))
            elif event.type == pygame.KEYDOWN:
                if typing:
                    if event.key == pygame.K_RETURN:
                        if typed_answer.lower() == correct_answer.lower():
                            pygame.time.wait(3000)
                            answer_bar.start_color = (0, 255, 0)
                        else:
                            pygame.time.wait(3000)
                            answer_bar.start_color = (255, 165, 0)
                        typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        typed_answer = typed_answer[:-1]
                    else:
                        typed_answer += event.unicode

        username_written.roundrectdraw(sparta_window)
        username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(sparta_window)
        points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

        question_number_written.roundrectdraw(sparta_window)
        question_number_written.roundrectfill(sparta_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
        pygame.display.flip()

def open_sparta_physics():
    """
    This is the docstring of function open_sparta_physics(), which show Physics' side of Sparta Version.
    """
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    question_number_written = RoundRectTextbox(690, 40, 160, 75, (255, 165, 0), (248, 222, 126))
    physics_question = RoundRectTextbox(100, 350, 500, 100, (0, 117, 94), (41, 171, 135))
    answer_bar = RoundRectTextbox(100, 500, 500, 100, (0, 117, 94), (41, 171, 135))
    sparta_window = pygame.display.set_mode((width, height))
    surface_img = pygame.image.load('beautiful_mountain.jpeg')
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Sparta')
    photo_surface = pygame.Surface((width, height))
    photo_surface.blit(surface_img, (0, 0))
    photo_surface.set_colorkey((255, 255, 255))
    photo_surface.set_alpha(128)
    sparta_window.blit(photo_surface, (0, 0))
    pygame.display.flip()
    running_sparta = True
    sparta_question_data = pop_questions_sparta('Physics')
    if sparta_question_data:
        question, correct_answer = sparta_question_data
        physics_question.roundrectdraw(sparta_window)
        if progress < 1.0:
            physics_question.rw += 2
            progress += 0.01
            physics_question.update_color(progress)
        if index < len(str(question)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(question)[index]
                index += 1
                start_time = time.time()
        physics_question.roundrectfill(sparta_window, question, rrfont_name='Arial', rrfontsize=24)
        pygame.time.wait(500)
        answer_bar.roundrectdraw(sparta_window)
        answer_bar.roundrectfill(sparta_window, typed_answer, 'Arial', 24, (255, 255, 255))

    username_written.roundrectdraw(sparta_window)
    username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

    points_written.roundrectdraw(sparta_window)
    points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

    question_number_written.roundrectdraw(sparta_window)
    question_number_written.roundrectfill(sparta_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
    pygame.display.flip()
    while running_sparta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_sparta = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if answer_bar.roundrect.collidepoint(pygame.mouse.get_pos()):
                    typing = True
                else:
                    if typing:
                        if typed_answer.lower() == correct_answer.lower():
                            answer_bar.start_color = (0, 255, 0)
                        else:
                            answer_bar.start_color = (255, 165, 0)
                        typing = False
                answer_bar.roundrectdraw(sparta_window)
                answer_bar.roundrectfill(sparta_window, typed_answer, 24, (0, 0, 0))
            elif event.type == pygame.KEYDOWN:
                if typing:
                    if event.key == pygame.K_RETURN:
                        if typed_answer.lower() == correct_answer.lower():
                            pygame.time.wait(3000)
                            answer_bar.start_color = (0, 255, 0)
                        else:
                            pygame.time.wait(3000)
                            answer_bar.start_color = (255, 165, 0)
                        typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        typed_answer = typed_answer[:-1]
                    else:
                        typed_answer += event.unicode

        username_written.roundrectdraw(sparta_window)
        username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(sparta_window)
        points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

        question_number_written.roundrectdraw(sparta_window)
        question_number_written.roundrectfill(sparta_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
        pygame.display.flip()

def open_sparta_chemistry():
    """
    This is the docstring of function open_sparta_chemistry(), which show Chemistry's side of Sparta Version.
    """
    progress = 0.0
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    question_number_written = RoundRectTextbox(690, 40, 160, 75, (255, 165, 0), (248, 222, 126))
    chemistry_question = RoundRectTextbox(100, 350, 500, 100, (0, 117, 94), (41, 171, 135))
    answer_bar = RoundRectTextbox(100, 500, 500, 100, (0, 117, 94), (41, 171, 135))
    sparta_window = pygame.display.set_mode((width, height))
    surface_img = pygame.image.load('beautiful_mountain.jpeg')
    typed_effect_char = ''
    clock = pygame.time.Clock()
    typing_speed = 50
    index = 0
    start_time = time.time()
    pygame.display.set_caption('Stairs of Acropolis - New Game - Sparta')
    photo_surface = pygame.Surface((width, height))
    photo_surface.blit(surface_img, (0, 0))
    photo_surface.set_colorkey((255, 255, 255))
    photo_surface.set_alpha(128)
    sparta_window.blit(photo_surface, (0, 0))
    pygame.display.flip()
    running_sparta = True
    sparta_question_data = pop_questions_sparta('Chemistry')
    if sparta_question_data:
        question, correct_answer = sparta_question_data
        chemistry_question.roundrectdraw(sparta_window)
        if progress < 1.0:
            chemistry_question.rw += 2
            progress += 0.01
            chemistry_question.update_color(progress)
        if index < len(str(question)):
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / typing_speed:
                typed_effect_char += str(question)[index]
                index += 1
                start_time = time.time()
        chemistry_question.roundrectfill(sparta_window, question, rrfont_name='Arial', rrfontsize=24)
        pygame.time.wait(500)
        answer_bar.roundrectdraw(sparta_window)
        answer_bar.roundrectfill(sparta_window, typed_answer, 'Arial', 24, (255, 255, 255))

    username_written.roundrectdraw(sparta_window)
    username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

    points_written.roundrectdraw(sparta_window)
    points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

    question_number_written.roundrectdraw(sparta_window)
    question_number_written.roundrectfill(sparta_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
    pygame.display.flip()
    while running_sparta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_sparta = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if answer_bar.roundrect.collidepoint(mouse_x, mouse_y):
                    typing = True
                else:
                    if typing:
                        if typed_answer.lower() == correct_answer.lower():
                            pygame.time.wait(3000)
                            answer_bar.start_color = (0, 255, 0)
                        else:
                            pygame.time.wait(3000)
                            answer_bar.start_color = (255, 165, 0)
                        typing = False
                answer_bar.roundrectdraw(sparta_window)
                answer_bar.roundrectfill(sparta_window, typed_answer, 24, (0, 0, 0))
            elif event.type == pygame.KEYDOWN:
                if typing:
                    if event.key == pygame.K_RETURN:
                        if typed_answer.lower() == correct_answer.lower():
                            answer_bar.start_color = (0, 255, 0)
                        else:
                            answer_bar.start_color = (255, 165, 0)
                        typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        typed_answer = typed_answer[:-1]
                    else:
                        typed_answer += event.unicode

        username_written.roundrectdraw(sparta_window)
        username_written.roundrectfill(sparta_window, pop_username(), 'Arial', 18, (255, 255, 255))

        points_written.roundrectdraw(sparta_window)
        points_written.roundrectfill(sparta_window, pop_points(), 'Times New Roman', 30, (255, 255, 255))

        question_number_written.roundrectdraw(sparta_window)
        question_number_written.roundrectfill(sparta_window, pop_question_number(), 'Tahoma', 30, (0, 0, 0))
        pygame.display.flip()

def open_new_game_window():
    """
    This is the docstring of function open_new_game_window(), which shows the window where a player starts the game and chooses Gorgo or Sparta.
    """
    username_written = RoundRectTextbox(50, 40, 160, 75, (15, 82, 186), (0, 30, 120))
    points_written = RoundRectTextbox((width - 160)//2, 40, 160, 75, (80, 200, 120), (10, 105, 33))
    choice_requirement = RoundRectTextbox((width - 380)//2, 150, 380, 75, (128, 128, 128), (224, 224, 224))
    new_game_window = pygame.display.set_mode((width, height))
    progress = 0.0
    pygame.display.set_caption('Stairs of Acropolis - New Game')
    gorgo_img = pygame.transform.scale(pygame.image.load('gorgo_queen.jpeg'), (250, 250))
    gorgo_rect = gorgo_img.get_rect(topleft=(180, 250))
    sparta_img = pygame.transform.scale(pygame.image.load('sparta_warrior.jpeg'), (250, 250))
    sparta_rect = sparta_img.get_rect(topleft=(500, 250))
    running_new_game_window = True
    while running_new_game_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_new_game_window = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    main_window()
                elif gorgo_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    open_gorgo_window()
                elif sparta_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(1000)
                    open_sparta_window()

        background_color(new_game_window, (135, 206, 235), (139, 69, 19))

        username_written.roundrectdraw(new_game_window)
        username_written.roundrectfill(new_game_window, pop_username(), 'Arial', 18, (255, 255, 255))
        if progress < 1.0:
            username_written.rw += 2
            username_written.rx -= 1
            username_written.roundrectfill(new_game_window, pop_username(), 'Arial', 18, (255, 255, 255))
            progress += 0.01
            username_written.update_color(progress)

        points_written.roundrectdraw(new_game_window)
        points_written.roundrectfill(new_game_window, pop_points(), 'Times New Roman', 20, (255, 255, 255))
        if progress < 1.0:
            points_written.rw += 2
            points_written.rx -= 1
            points_written.roundrectfill(new_game_window, pop_points(), 'Times New Roman', 18, (255, 255, 255))
            progress += 0.01
            points_written.update_color(progress)

        choice_requirement.roundrectdraw(new_game_window)
        choice_requirement.roundrectfill(new_game_window, 'CHOOSE A VERSION TO START THE GAME', 'Papyrus', 25, (0, 0, 0))
        if progress < 1.0:
            choice_requirement.rw += 2
            choice_requirement.rx -= 1
            choice_requirement.roundrectfill(new_game_window, 'CHOOSE A VERSION TO START THE GAME', 'Papyrus', 25, (0, 0, 0))
            progress += 0.01
            choice_requirement.update_color(progress)

        new_game_window.blit(gorgo_img, (180, 250))
        new_game_window.blit(sparta_img, (500, 250))

        gorgo_title = pygame.font.SysFont('Tahoma', 28).render('GORGO', True, (253, 218, 13), (0, 0, 0))
        new_game_window.blit(gorgo_title, (260, 490))

        sparta_title = pygame.font.SysFont('Tahoma', 28).render('SPARTA', True, (253, 218, 13), (0, 0, 0))
        new_game_window.blit(sparta_title, (580, 490))

        pygame.draw.rect(new_game_window, (34, 139, 34), return_button_rect)
        return_text = pygame.font.SysFont('Arial', 18).render('RETURN', True, (255, 255, 255))
        new_game_window.blit(return_text, return_text.get_rect(center=return_button_rect.center))
        pygame.display.flip()
    pygame.quit()

running = True
continue_button_rect = pygame.Rect((width - 100)//2 + 80, 600, 100, 50)
return_button_rect = pygame.Rect((width - 100)//2 - 80, 600, 100, 50)

darken_color = (0, 0, 0, 128)

def main_window():
    """
    This is the docstring of main_window(), which shows the window where a player enters the game and where everything happens.
    """
    running_main_window = True
    main_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Stairs of Acropolis")
    acropolis_temple = pygame.image.load('acropolis.png')
    frame = pygame.image.load('Greek_Style_Border_Frame.png')
    athena = pygame.image.load('athena_goddess.png')
    pygame.display.set_icon(acropolis_temple)
    acropolis_temple_new_w = 300
    acropolis_temple_new_h = 200
    athena_new_w = 500
    athena_new_h = 600
    new_acropolis_temple = pygame.transform.scale(acropolis_temple, (acropolis_temple_new_w, acropolis_temple_new_h))
    new_greek_frame = pygame.transform.scale(frame, (width, height))
    new_athena = pygame.transform.scale(athena, (athena_new_w, athena_new_h))
    title_font = pygame.font.SysFont("Times New Roman", 52, bold=True)
    shadow_title = title_font.render("STAIRS OF ACROPOLIS", False, (255, 255, 240))
    set_font_title = title_font.render("STAIRS OF ACROPOLIS", True, (0, 0, 0))
    stairs_num = 12
    first_stair_width = acropolis_temple_new_w
    first_stair_height = height // stairs_num
    first_stair_x = width//2 - first_stair_width//2
    first_stair_y = height//2 - 1.2*acropolis_temple_new_h + acropolis_temple_new_h
    stairs_bottom_color = (180, 180, 180)
    stairs_top_color = (255, 255, 240)
    base_color = [(
        int(stairs_bottom_color[0] + (stairs_top_color[0] - stairs_bottom_color[0]) * i / (stairs_num - 1)),
        int(stairs_bottom_color[1] + (stairs_top_color[1] - stairs_bottom_color[1]) * i / (stairs_num - 1)),
        int(stairs_bottom_color[2] + (stairs_top_color[2] - stairs_bottom_color[2]) * i / (stairs_num - 1))
    ) for i in range(stairs_num)]
    background_color(main_window, (135, 206, 235), (139, 69, 19))

    textbox_rect = pygame.Rect(100, 700, 180, 130)
    textbox_rect2 = pygame.Rect(350, 700, 180, 130)
    textbox_rect3 = pygame.Rect(600, 700, 180, 130)
    textbox_color = (255, 10, 10)

    while running_main_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_main_window = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if textbox_rect2.collidepoint(mouse_pos):
                    pygame.time.wait(1000)
                    open_new_window()
                elif textbox_rect.collidepoint(mouse_pos):
                    pygame.time.wait(1000)
                    darken_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                    darken_surface.fill(darken_color)
                    window.blit(darken_surface, (0, 0))

                    open_new_game_window()

        main_window.blit(shadow_title, (width//2 - set_font_title.get_width()//2 - 3, set_font_title.get_height()//2 + 3))
        main_window.blit(set_font_title, (width//2 - set_font_title.get_width()//2, set_font_title.get_height()//2 + 3))
        main_window.blit(new_acropolis_temple, (width//2 - acropolis_temple_new_w//2, height//2 - 1.2*acropolis_temple_new_h))
        main_window.blit(new_athena, (width//4 - 1.2*athena_new_w//2, 3*height//2 - 1.5*athena_new_h))
        main_window.blit(pygame.transform.flip(new_athena, True, False), (width//4 - 1.2*athena_new_w//2 + 1.2*width//2, 3*height//2 - 1.5*athena_new_h))
        main_window.blit(new_greek_frame, (0, 0))

        for i in range(stairs_num):
           symmetric_stairs_x = width//2 + (width//2 - first_stair_x - first_stair_width)
           pygame.draw.rect(main_window, base_color[i], pygame.Rect(first_stair_x, first_stair_y, first_stair_width, first_stair_height))
           pygame.draw.rect(main_window, base_color[i], pygame.Rect(symmetric_stairs_x, first_stair_y, first_stair_width, first_stair_height))
           first_stair_width += 12
           first_stair_y += first_stair_height // 2

        pop_up_animation(textbox_rect, y_to_popup, popup_speed)
        pop_up_animation(textbox_rect2, y_to_popup, popup_speed)
        pop_up_animation(textbox_rect3, y_to_popup, popup_speed)

        pygame.draw.rect(main_window, textbox_color, textbox_rect)
        pygame.draw.rect(main_window, (0, 48, 144), textbox_rect, 5)

        pygame.draw.rect(main_window, textbox_color, textbox_rect2)
        pygame.draw.rect(main_window, (0, 48, 144), textbox_rect2, 5)

        pygame.draw.rect(main_window, textbox_color, textbox_rect3)
        pygame.draw.rect(main_window, (0, 48, 144), textbox_rect3, 5)

        #Fill in the textbox
        textbox_font = pygame.font.SysFont('Arial', 23, bold=True)
        text_surface = textbox_font.render("NEW GAME", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=textbox_rect.center)
        main_window.blit(text_surface, text_rect)

        textbox2_font = pygame.font.SysFont('Arial', 23, bold=True)
        text_surface2 = textbox2_font.render("NEW PLAYER", True, (255, 255, 255))
        text_rect2 = text_surface2.get_rect(center=textbox_rect2.center)
        main_window.blit(text_surface2, text_rect2)

        textbox3_font = pygame.font.SysFont('Arial', 23, bold=True)
        text_surface3 = textbox3_font.render("RESUME GAME", True, (128, 128, 128))
        text_rect3 = text_surface3.get_rect(center=textbox_rect3.center)
        main_window.blit(text_surface3, text_rect3)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main_window()
    print(sign_up_player_data.__doc__)
    print(check_username_exists.__doc__)
    print(pop_username.__doc__)
    print(pop_points.__doc__)
    print(pop_question_number.__doc__)
    print(pop_questions_gorgo.__doc__)
    print(pop_questions_sparta.__doc__)
    print(background_color.__doc__)
    print(open_save_window.__doc__)
    print(open_gorgo_window.__doc__)
    print(open_gorgo_window_twin_docstring.__doc__)
    print(open_sparta_window.__doc__)
    print(open_sparta_window_twin_docstring.__doc__)
    print(open_gorgo_mathematics.__doc__)
    print(open_gorgo_physics.__doc__)
    print(open_gorgo_chemistry.__doc__)
    print(open_sparta_mathematics.__doc__)
    print(open_sparta_physics.__doc__)
    print(open_sparta_chemistry.__doc__)
    print(open_new_game_window.__doc__)
    print(open_new_window.__doc__)
    print(RoundRectTextbox.__doc__)
    print(main_window.__doc__)
