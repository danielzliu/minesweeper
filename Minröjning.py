#P-uppgift: Minröjning (#168)
#Daniel Liu, CINEK, HT2017
#Version: 2017-11-27
#OBS! Tryck på den gröna/röda/stjärnade rutan för att börja om
#Det finns en fil med logik i mappen "Information om projektet"

import tkinter
import pygame
import random
import time
import sys

#--------------------MENY--------------------------------
class User:
#Klass för med användarinformation som är inställningar för spelet.
    def __init__(self, name, board_width, board_height, mine_quantity, clock_time):
    #IN: Allt som matas in från startmenyn.
        self.name = name                                                            #Spelarens namn.
        self.board_width = int(board_width)                                         #Antal rutor brett.
        self.board_height = int(board_height)                                       #Antal rutor högt.
        self.mine_quantity = int(mine_quantity)                                     #Antal minor.
        self.clock_time = int(clock_time)
        self.score = int(int(self.mine_quantity)**2 /((0.02 * self.clock_time) + 1))


#----------------------SPEL-----------------------------------
class Square:
#Klass för varje ruta i spelet.
    def __init__(self,xpos,ypos):
    #Skapar en ruta.
    #IN: Rutans koordinater som genererar från en for-loop.
        self.xpos = range(xpos, xpos+25)                                            #Rutans x-koordinater som är ett intervall av pixlar på fönstret.           
        self.ypos = range(ypos, ypos+25)                                            #Rutans y-koordinater som är ett intervall av pixlar på fönstret.
        self.is_flipped = False                                                     #Variabel som talar om om rutan är vänd.
        self.mine_exists = False                                                    #Variabel som talar om om det finns en mina gömd under rutan.
        self.nearby_mines = 0                                                       #Variabel som talar om hur många av de närliggande rutorna som har minor under sig.
        self.is_flagged = False                                                     #Variabel som talar om om rutan är flaggad.
        self.image = pygame.transform.scale(pygame.image.load('GFX\square.jpg'), (25, 25))
        

    def assign_mine(self):
        #Tilldelar en mina till en ruta.
        self.mine_exists = True                                                     #Talar om om det finns en mina under rutan.

    def flip_square(self, number_images, gameDisplay):
        #Vänder på en ovänd ruta.
        #IN: Lista med bilder. Spelfönstret.
        if self.mine_exists == True:
            self.image = pygame.transform.scale(pygame.image.load('GFX\mine_clicked.jpg'), (25,25))
        elif self.mine_exists == False:
            self.image = pygame.transform.scale(pygame.image.load(number_images[self.nearby_mines]), (25,25))
        gameDisplay.blit(self.image, (self.xpos[0], self.ypos[0]))
        self.is_flagged = False
        self.is_flipped = True

    def flag_square(self, gameDisplay):
        #Flaggar en ovänd ruta.
        #IN: Spelfönstret
        if self.is_flagged == False:
            self.image = pygame.transform.scale(pygame.image.load('GFX\\flagged.jpg'), (25,25))
            gameDisplay.blit(self.image, (self.xpos[0], self.ypos[0]))
            self.is_flagged = True
        elif self.is_flagged == True:
            self.image = pygame.transform.scale(pygame.image.load('GFX\square.jpg'), (25,25))
            gameDisplay.blit(self.image, (self.xpos[0], self.ypos[0]))
            self.is_flagged = False

class Restart_Button:
    #Klass för knappen som startar om spelet.
    def __init__(self, gameDisplay, display_width):
        #Skapar knapp.
        #IN: Spelfönstret. Skärmbredd(För att veta var knappen placeras.
        self.xpos = range(display_width - 100, display_width)                   #Knappens x-koordinater som är ett intervall av pixlar på fönstret.
        self.ypos = range(0, 50)                                                #Knappens x-koordinater som är ett intervall av pixlar på fönstret.
        self.image = pygame.transform.scale(pygame.image.load('GFX\green.jpg'), (100, 50))
        gameDisplay.blit(self.image, (self.xpos[0], self.ypos[0]))

    def change_colour(self,gameDisplay, win_or_lose):
        #Byter färg på knappen
        #IN: Spelfönstret. Variabel som talar om om spelaren har vunnit eller förlorat.
        if win_or_lose == 1:
            self.image = pygame.transform.scale(pygame.image.load('GFX\star.jpg'), (100, 50))
            
        if win_or_lose == -1:
            self.image = pygame.transform.scale(pygame.image.load('GFX\\red.jpg'), (100, 50))
        gameDisplay.blit(self.image, (self.xpos[0], self.ypos[0]))

    def click(self, user):
        #Startar om spelet när knappen klickas.
        #IN: Användarinställningar.
        game(user)

#-----------------------------MENY----------------------------
def open_menu():
    #Skapar ett fönster för menyn.
    #UT: Menyfönstret.
    menuDisplay = tkinter.Tk()
    menuDisplay.title('Minröjning')
    menuDisplay.resizable(width=False, height=False)
    return menuDisplay

def create_menu(menuDisplay):
    #Lägger till widgets på menyfönstret.
    #IN: Menyfönstret.
    label_name = tkinter.Label(menuDisplay, text ='Namn')
    label_board_width = tkinter.Label(menuDisplay, text ='Spelplanens bredd')
    label_board_height = tkinter.Label(menuDisplay, text ='Spelplanens höjd')
    label_mine_quantity = tkinter.Label(menuDisplay, text ='Antal minor')
    
    label_name.grid(row=0, column=0, sticky='e')
    label_board_width.grid(row=1, column=0, sticky='e')
    label_board_height.grid(row=2, column=0, sticky='e')
    label_mine_quantity.grid(row=3, column=0, sticky='e')

    entry_name = tkinter.Entry(menuDisplay, width=20)
    entry_board_width = tkinter.Entry(menuDisplay, width=2)
    entry_board_height = tkinter.Entry(menuDisplay, width=2)
    entry_mine_quantity = tkinter.Entry(menuDisplay, width=4)

    entry_name.grid(columnspan=3, row=0, column=1, sticky='w')
    entry_board_width.grid(row=1, column=1, sticky='w')
    entry_board_height.grid(row=2, column=1, sticky='w')
    entry_mine_quantity.grid(row=3, column=1, sticky='w')

    label_board_width_range = tkinter.Label(menuDisplay, text ='5 - 25')
    label_board_height_range = tkinter.Label(menuDisplay, text ='5 - 20')

    label_board_width_range.grid(row=1, column=2, sticky='w')
    label_board_height_range.grid(row=2, column=2, sticky='w')

    highscore_button = tkinter.Button(menuDisplay, text = 'Topplista', command=lambda: open_highscore())
    highscore_button.grid(columnspan=5, row=5)

    play_button = tkinter.Button(menuDisplay, text='Spela!', command=lambda: start_game(entry_name,entry_board_width,entry_board_height,entry_mine_quantity,menuDisplay))
    play_button.grid(columnspan=5, row=6)

    menuDisplay.grid_rowconfigure(4, minsize=22)
    menuDisplay.grid_columnconfigure(4, minsize=100)

    label_error_text = ''

def retrieve_input(entry_name,entry_board_width,entry_board_height,entry_mine_quantity):
    #Hämtar input från menyn.
    #IN: Det som användaren har fyllt i från menyn.
    #UT: Det som användaren har fyllt i från menyn i form av siffror eller text.
    name = entry_name.get()
    board_width = entry_board_width.get()
    board_height = entry_board_height.get()
    mine_quantity = entry_mine_quantity.get()
    return name,board_width,board_height,mine_quantity

def open_highscore():
    #Skapar ett nytt fönster för topplistan.
    highscoreDisplay = tkinter.Tk()
    highscoreDisplay.title('Minröjning topplista')
    highscoreDisplay.resizable(width=False, height=False)
    infile = open('Topplista.txt', 'r')
    current_highscores = infile.readlines()
    current_highscores2 = []
    for i in range(len(current_highscores)):
        current_highscores2.append(current_highscores[i].split())               #Lägger in nuvarande toppoäng i en lista.
    current_highscores = []

    label_texts = ['Placering' , 'Namn' , 'Bredd', 'Höjd', 'Antal Minor', 'Tid', 'Poäng']

    for i in range(len(label_texts)):
        temp_label = tkinter.Label(highscoreDisplay, text = label_texts[i])
        temp_label.grid(row = 0, column = i, sticky = 'w')
    
    for i in range(len(current_highscores2)):
        for k in range(len(current_highscores2[i])):
            label_highscore = tkinter.Label(highscoreDisplay, text = current_highscores2[i][k])
            label_highscore.grid(row = i + 1, column = k, sticky = 'w')

def start_game(entry_name,entry_board_width,entry_board_height,entry_mine_quantity,menuDisplay):
    #Startar spelet. Skapar ett User-objekt med användarinställningar.
    #IN: Användarinställningar. Menyfönstret.
    name,board_width,board_height,mine_quantity = retrieve_input(entry_name,entry_board_width,entry_board_height,entry_mine_quantity)
    
    game_ready = True
    if name == '' or name.isspace()== True:
        name = 'Namnlös'

    try:
        board_width = int(board_width)
        board_height = int(board_height)
        mine_quantity = int(mine_quantity)
        #Lite felhantering så att användaren inte kan ange vad som helt i textfälten.
        if board_width > 25 or board_width < 5 or board_height > 20 or board_height < 5: #Max och min antal rutor.
            cover_frame = tkinter.Frame(menuDisplay, width=300,height=22)       #Skapar en frame som täcker över den text som fanns innan, för att sedan lägga till en ny text.
            cover_frame.grid(columnspan=5,row=4, column=0)
            label_error_text = tkinter.Label(menuDisplay, text ='Du måste ange tal inom intervallen!')
            label_error_text.grid(columnspan=5,row=4, column=0)
            game_ready = False
        elif mine_quantity >= board_width*board_height:
            cover_frame = tkinter.Frame(menuDisplay, width=300,height=22) 
            cover_frame.grid(columnspan=5,row=4, column=0)
            label_error_text = tkinter.Label(menuDisplay, text ='Det måste finnas färre minor är antalet rutor!')
            label_error_text.grid(columnspan=5,row=4, column=0)
            game_ready = False
        elif mine_quantity <= 0:
            cover_frame = tkinter.Frame(menuDisplay, width=300,height=22) 
            cover_frame.grid(columnspan=5,row=4, column=0)
            label_error_text = tkinter.Label(menuDisplay, text ='Det måste finnas minor!')
            label_error_text.grid(columnspan=5,row=4, column=0)
            game_ready = False
        if game_ready == True:
            user = User(name, board_width, board_height, mine_quantity, 0)
            menuDisplay.destroy()
            game(user)
            

    except ValueError:
        cover_frame = tkinter.Frame(menuDisplay, width=300,height=22)
        cover_frame.grid(columnspan=5,row=4, column=0)
        label_error_text = tkinter.Label(menuDisplay, text ='Du kan bara skriva in heltal!')
        label_error_text.grid(columnspan=5,row=4, column=0)

#----------------------SPEL---------------------

def open_window(colour, gameDisplay):
    #Öppnar fönster för spelet
    pygame.init()
    pygame.display.set_caption('Minröjning')                                        #Namn på spel.
    gameDisplay.fill(colour)
    pygame.display.update()                                                         #Uppdaterar skärmen.

def create_board(user, gameDisplay):
    #Skapar en lista med Square-objekt och lägger ut dem på skärmen.
    #IN: Spelfönstret.
    #UT: Lista med Square-objekt.
    squares = []                                                                    #En lista med ett Square-objekt på varje plats.
    for y in range(user.board_height):
        for x in range(user.board_width):
            square = Square(x * 25, y *25)
            squares.append(square)
            gameDisplay.blit(square.image, (square.xpos[0], square.ypos[0]))
    pygame.display.update()
    return squares

def load_number_images():
    #Gör en lista med bilder på siffror som finns i mappen.
    #UT: Lista med bilder.
    number_images = []
    for i in range(0,9):
        number_images.append('GFX\\' + str(i) + '.jpg')
    return number_images

def randomize_mines(user, squares):
    #Slumpar ut minor.
    #IN: Användarinställningar. Lista med Square-objekt.
    squares_i = []                                                                  #En lista med alla index från listan squares.
    squares_w_mines = []
    for i in squares:
        squares_i.append(i)
        
    for i in range(0 , user.mine_quantity):                                         #Flyttar objekt från squares_i till squares_w_mines.
        random_int = random.randint(0 , len(squares_i) - 1)
        squares_w_mines.append(squares_i[random_int])
        del squares_i[random_int]

    for i in range(0, len(squares_w_mines)):                                        #Matchar objekten i squares_w_mines med de i listan squares.                          
        for k in range(0, len(squares)): 
            if  squares_w_mines[i].xpos[0] == squares[k].xpos[0] and squares_w_mines[i].ypos[0] == squares[k].ypos[0]:
                squares[k].assign_mine()

def calculate_nearby_squares(squares, user, i):
    #Räknar ut vilka rutor som ligger bredvid. i står för index i listan.
    #IN: Lista med rutor. Användarinformation. Rutan, som vilket funktionen avsers, index.
    #UT: Lista med närliggande rutor.
    if (i + 1) % user.board_width != 1 and (i + 1) % user.board_width != 0 and (i + 1) > user.board_width and (i + 1) <= len(squares) - user.board_width: #alla rutor förutom de på kanterna
            nearby_squares_list = [i-user.board_width-1, i-user.board_width , i-user.board_width+1 , i-1, i+1, i+user.board_width-1, i+user.board_width , i+user.board_width+1] #lista med alla rutor som ligger bredvid aktuell rutas index
    elif (i + 1) % user.board_width == 1 and (i + 1) > user.board_width and (i + 1) <= len(squares) - user.board_width:# alla rutor på vänster kant
        nearby_squares_list = [i-user.board_width , i-user.board_width+1 , i+1, i+user.board_width , i+user.board_width+1]
    elif (i + 1) % user.board_width == 0 and (i + 1) > user.board_width and (i + 1) <= len(squares) - user.board_width: #alla på höger
        nearby_squares_list = [i-user.board_width-1, i-user.board_width , i-1, i+user.board_width-1, i+user.board_width]     
    elif (i + 1) % user.board_width != 1 and (i + 1) % user.board_width != 0 and (i + 1) < user.board_width: #alla rutor på övre rad
        nearby_squares_list = [i+user.board_width-1, i+user.board_width , i+user.board_width+1 , i-1, i+1] 
    elif (i + 1) % user.board_width != 1 and (i + 1) % user.board_width != 0 and (i + 1) >= len(squares) - user.board_width: #alla rutor på undre rad
        nearby_squares_list = [i-user.board_width-1, i-user.board_width , i-user.board_width+1 , i-1, i+1] 
        #hörnen
    elif i + 1 == 1:
        nearby_squares_list = [i+1, i+user.board_width , i+user.board_width+1] 
    elif i + 1 == user.board_width:
        nearby_squares_list = [i-1, i+user.board_width , i+user.board_width-1]
    elif i + 1 == len(squares) - user.board_width + 1 :
        nearby_squares_list = [i+1, i-user.board_width , i-user.board_width+1] 
    elif i + 1 == len(squares):
        nearby_squares_list = [i-1, i-user.board_width , i-user.board_width-1]
    return nearby_squares_list

def calculate_nearby_mines(squares, user):
    #Beräknar antal närliggande minor för varje Square-objekt.
    #IN: Lista med rutor. Användarinställningar.
    for i in range(0, len(squares)):
        nearby_squares_list = calculate_nearby_squares(squares, user, i) 
        for k in nearby_squares_list:
                if squares[k].mine_exists:
                    squares[i].nearby_mines = squares[i].nearby_mines + 1

def flip_adjacent_squares(squares, i, queue, number_images, user, gameDisplay):
    #Vänder närliggande rutor.i står för index i lista.
    #IN: Lista med rutor. Index i listan squares vilket funktionen avser. Lista med bilder. Användarinställningar. Spelfönstret.
    queue = []
    nearby_squares_list = calculate_nearby_squares(squares, user, i)
    for k in nearby_squares_list:                                                   #Lägger till närliggande oöppnade rutor till en kö.
        if squares[k].is_flipped == False:
            queue.append(k)
    for j in queue:
        squares[j].flip_square(number_images, gameDisplay)
        if squares[j].nearby_mines == 0:
            flip_adjacent_squares(squares, j, queue, number_images, user, gameDisplay)

def show_mines(squares, gameDisplay):
    #Visar alla minor.
    #IN: Lista med rutor. Spelfönstret.
    for i in squares:
        if i.mine_exists == True and i.is_flipped == False and i.is_flagged == False:
            i.image = pygame.transform.scale(pygame.image.load('GFX\mine.jpg'), (25,25))
            gameDisplay.blit(i.image, (i.xpos[0], i.ypos[0]))
        elif i.mine_exists == True and i.is_flipped == False and i.is_flagged == True:
            i.image = pygame.transform.scale(pygame.image.load('GFX\mine_sweeped.jpg'), (25,25))
            gameDisplay.blit(i.image, (i.xpos[0], i.ypos[0]))

def hide_mines(squares, gameDisplay):
    #Gömmer alla minor.
    #IN: Lista med rutor. Spelfönstret.
    for i in squares:
        if i.mine_exists == True and i.is_flipped == False: 
            if i.is_flagged == False:                                               #Gör så att bilden blir till den var från början
                i.image = pygame.transform.scale(pygame.image.load('GFX\square.jpg'), (25,25)) 
            if i.is_flagged == True:
                i.image = pygame.transform.scale(pygame.image.load('GFX\\flagged.jpg'), (25,25))
            gameDisplay.blit(i.image, (i.xpos[0], i.ypos[0]))

def check_win_condition(gameDisplay, user, restart_button, win_or_lose, squares, clock_time):
    #Kollar om vinstkriterierna är uppfyllda. Fryser spelet om spelaren vinner eller förlorar.
    #IN: Spelfönstret. Användarinställningar. Omstartsknapp. Vinstvariabel. Lista med rutor. Speltiden.
   
    squares_left = user.board_width * user.board_height
    correctly_flagged = 0

    for i in squares:
        
        if i.is_flipped == True:                                                    #Räknar ut hur många rutor som är oöppnade.
            squares_left = squares_left -1
        if i.mine_exists == True and i.is_flagged == True:                          #Räknar ut hur många rutor som är korrekt flaggade.
            correctly_flagged = correctly_flagged + 1
        elif i.mine_exists == False and i.is_flagged == True:
            correctly_flagged = correctly_flagged - 1

        if i.mine_exists == True and i.is_flipped == True:                          #Spelaren förlorar om en ruta innehåller en mina och är vänt.
            win_or_lose = -1

    if win_or_lose == 0:
        if squares_left == user.mine_quantity or correctly_flagged == user.mine_quantity: #Kollar om antalet oöppnade rutor är samma som antalet minor.
            win_or_lose = 1
    if win_or_lose == 1 or win_or_lose == -1:
        restart_button.change_colour(gameDisplay,win_or_lose)
        show_mines(squares, gameDisplay)
        if win_or_lose == 1:
            add_highscore(user, clock_time)
        freeze_game(user, restart_button)

def count_time(gameDisplay, font, black, grey, display_width, display_height, starting_time):
    #Räknar ut speltiden.
    #IN: Spelfönstret. Typsnitt. Färger. Fönstrets storlek. Starttid för beräkning av speltid.
    #UT: Speltiden.
    pygame.draw.rect(gameDisplay, grey, [display_width - 100, display_height - 25, 120, 30])     
    current_time = time.time()
    clock_time = int(current_time - starting_time)
    if clock_time > 9999:
        clock_time = 9999
    clock_font = font.render(str(clock_time), True, (black))
    gameDisplay.blit(clock_font,(display_width - 75, display_height - 25))
    return clock_time
        

def freeze_game(user, restart_button):
    #Fryser spelskärmen.
    #IN: Användarinställningar. Omstartsknapp.
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                close_window()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx,my = pygame.mouse.get_pos()
                    if mx in restart_button.xpos and my in restart_button.ypos:     #Om muskoordinaterna är inom knappens koordinater.
                        restart_button.click(user)
        pygame.display.update()

def add_highscore(user, clock_time):
    #Lägger till poäng i topplistan.
    #IN: Användarinformation. Speltiden.
    user.clock_time = clock_time
    infile = open('Topplista.txt' , 'r')
    current_highscores = infile.readlines()
    current_highscores2 = []
    for i in range(len(current_highscores)):
        current_highscores2.append(current_highscores[i].split())                   #Lägger in nuvarande toppoäng i en lista.
    current_highscores = []
    for i in current_highscores2:                                                   #Skapar klasser och lägger till i listan.
        top_user = User(i[1], i[2], i[3], i[4], i[5])
        current_highscores.append(top_user)
    infile.close()
    outfile = open('Topplista.txt' , 'w')
    new_highscores = []
    for i in current_highscores:
        user.score = int(int(user.mine_quantity)**2 /((0.02 * user.clock_time) + 1))#Beräkna poäng.
        if user.score >= i.score:                                                   #Byter plats med en toppoäng.
            new_highscores.append(user.name + '\t' + str(user.board_width) + '\t' + str(user.board_height) + '\t' + str(user.mine_quantity) + '\t' + str(user.clock_time) + '\t' + str(user.score) + '\n')
            user = i
        elif user.score < i.score:
            new_highscores.append(i.name + '\t' + str(i.board_width) + '\t' + str(i.board_height) + '\t' + str(i.mine_quantity) + '\t' + str(i.clock_time) + '\t' + str(i.score) + '\n')
    new_highscores_str = ''                                                         #Omvandlar listans innehåll till ett str-objekt.
    for i in range(len(new_highscores)): 
        new_highscores_str = new_highscores_str + str(i+1) + '\t' + str(new_highscores[i])
    outfile.write(new_highscores_str)
    outfile.close()

    
        
def close_window():
    #Stänger fönstret.
    pygame.quit()
    sys.exit()

#------------------------------------------------
def menu():
    #Menyn körs.
    menuDisplay=open_menu()
    create_menu(menuDisplay)
    menuDisplay.mainloop()

def game(user):
    #Spelet körs.
    #IN: Användarinställningar.
    display_width = (user.board_width) * 25 + 100                                   #Fönstrets storlek.
    display_height = (user.board_height) * 25
            
    black = (0,0,0)                                                                 #Färger.
    grey = (230,230,230)
    
    gameDisplay = pygame.display.set_mode((display_width , display_height))         #Spelfönstret.
    
    win_or_lose = 0                                                                 #-1 = förlora, 0 = forsätta spela, 1 = vinna.
    
    open_window(grey, gameDisplay)
    font = pygame.font.Font('Fonts\impact.ttf', 24)                                 #Typsnitt.
    starting_time = time.time()
    
    squares = create_board(user, gameDisplay)
    number_images = load_number_images()
    randomize_mines(user , squares)
    calculate_nearby_mines(squares, user)
    showing_mines = False

    restart_button = Restart_Button(gameDisplay, display_width)

    cheat_text = pygame.font.Font('Fonts\impact.ttf', 10).render('Tryck "S" för att fuska', True, (black))
    gameDisplay.blit(cheat_text,(display_width - 94, 50))

    while True:
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            
            if event.type == pygame.QUIT:
                close_window()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #1 = vänsterclick
                    mx,my = pygame.mouse.get_pos()                                  #mx och my är musen x- och ypositioner.
                    for i in range(len(squares)):                                   #Kollar igenom om muspositionen är inom koordinatintervallet för en ruta.
                        if mx in squares[i].xpos and my in squares[i].ypos:
                            squares[i].flip_square(number_images, gameDisplay)

                            if squares[i].nearby_mines == 0  and squares[i].mine_exists == False:
                                queue = []
                                flip_adjacent_squares(squares, i, queue, number_images, user, gameDisplay)
                    if mx in restart_button.xpos and my in restart_button.ypos:     #Om spelaren trycker på omstartsknappen.
                        restart_button.click(user)
                        
                if event.button == 3: #3 = högerclick
                        mx,my = pygame.mouse.get_pos()                              #mx och my är musen x- och ypositioner
                        for i in squares:                                           #Kollar igenom om muspositionen är inom koordinatintervallet för en ruta.
                            if mx in i.xpos and my in i.ypos:
                                if i.is_flipped == False:
                                    i.flag_square(gameDisplay)
                                
            if event.type == pygame.KEYDOWN:
                if key[pygame.K_s]:
                    if showing_mines == False:
                        show_mines(squares, gameDisplay)
                        showing_mines = True
                    elif showing_mines == True:
                        hide_mines(squares, gameDisplay)
                        showing_mines = False

        
        clock_time = count_time(gameDisplay, font, black, grey, display_width, display_height, starting_time) 
        check_win_condition(gameDisplay, user, restart_button, win_or_lose, squares, clock_time)
        pygame.display.update()
                
def main():
    menu()
                
main()
