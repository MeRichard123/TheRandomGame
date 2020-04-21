"""
NOTE TO USER --> The code here isn't very neat; I will take some time later to refactor it :D
But feel free to attempt to understand this mess of objects and functions.

BRIEF: Development of a text-based adventure game that eplores different parts of the world

NOTE: Initially I made an API call see other file (april_challenge,py), but the data wasn't quiet as I needed it.
"""

# Module imports;
import pygame
import random
import sys
import time


# Create Pygame objects
pygame.init()  # pylint: disable=no-member


# GLOBAL VARIABLES
gray = (51, 51, 51)
white = (255, 255, 255)
darkWhite = (255, 222, 173)

FPS = 15
X = 800
Y = 600

# Pygame Globals
gameExit = False
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 50)
fontInst = pygame.font.SysFont("Arial", 20)
fontLarge = pygame.font.SysFont("Arial", 100)

# Disctionary for places as the API didn't quite give me what I needed
places = {
    "Europe": ["Paris", "Rome", "Venice", "London", "Barcelona", "Berlin", "Budapest"],
    "Africa": ["Cairo", "Marrakesh", "Cape Town", "Luxor", "Fes", "Maasai Mara", "Fuerteventura"],
    "Asia": ["Bangkok", "Kyoto", "Singapore", "Tokyo", "Cambodia", "Beijing", "Dubai"],
    "Oceania": ["Sydney", "Melbourne", "Cairns", "Queenstown", "Perth", "Blue Mountains", "Fiji"],
    "South America": ["Machu Picchu", "Peru", "Cusco", "Lima", "Bueno Aires", "Rio de Janeiro", "Santiago"],
    "North America": ["Grand Canyon", "New York", "Las Vegas", "Los Angeles", "Cuba", "Vancouver", "Yellowstone"],
    "Anarctica": ["King George Island", "Deception Island", "Elephant Island", "Livingston", "General Bernardo's Base", "Eklund islands"],
}

# OBJECTS


class Place:
    # As unnecessary as this object is. It will help me later on
    def __init__(self):
        self.continent = random.choice(list(places.keys()))
        self.PlaceArray = places.get(self.continent)
        self.place = random.choice(self.PlaceArray)

# Create a Function so make an object instance


def getRandomPlace():
    return Place()


# This is equal to the random places
GetPlace = getRandomPlace()

# The Player Object


class Player:
    def __init__(self, name):
        self.name = name
        self.health = random.randrange(0, 20)
        self.points = 0
        self.inventory = []

    def death(self):
        # Method for when the player dies
        if "Honey Comb" in self.inventory:
            println("Opps! Looks like you died, however...")
            println(
                "Looks like you have a Honey comb, would you like to use it ot regain health?")
            option = input(">>>")
            if option == "yes" or option == "y":
                self.addHealth(random.randrange(1, 5))
        else:
            DeathScreen(self.points)
            println("You finished with a score of "+str(self.points))
            println("Here is what you finished with: "+str(self.inventory))
            pygame.quit()  # pylint: disable=no-member
            quit()

    def getHealth(self):
        # Output the payers current health
        if self.health == 0:
            println("You Start with 0 lives.")
            self.death()
        elif self.health <= 0:
            println("You have lost your lives")
            self.death()
        else:
            if self.health == 1:
                println("You have "+str(self.health)+" life")
            else:
                println("You have "+str(self.health)+" lives")

    def addHealth(self, damage):
        # Increase the health of the player
        # Damage the player if the value is negative
        self.health = self.health + damage

    def purchase(self, item, price=None):
        """Buy an item when offered from a merchant

        Arguments:
            item {[string]} -- Item to Buy.

        Keyword Arguments:
            price {[Real]} -- [Price for which to buy for. Random if none] (default: {None})
        """
        if self.points > 2:
            price = random.randrange(2, self.points)
            makePurchase = input("Would you like to buy a " +
                                 item+" for "+str(price)+" points? >>")
            print(" ")
            if makePurchase == "yes" or makePurchase == "y":
                if self.points >= price:
                    self.points -= price
                    self.inventory.append(item)
                    println("You Brought a "+item)
                    viewInventory(self)

                else:
                    println("You don't have enough points")
                    println("You are missing ", price-self.points, " points")
            else:
                println("Cancelling Transaction")

        else:
            println("You are too poor to buy anything, sorry")

    def earnPoints(self, amount):
        # Method for gaining points
        self.points += amount


class IncorrectCharacterTypeError(ValueError):
    # Defining a custom error message incase I mess up on the type specific method calls.
    pass


class Enemy():
    # The Enemy Object
    def __init__(self, type):
        self.type = type
        self.health = 10
        self.damageDealt = random.randrange(0, 15)
        self.fail = True

    def gamble(self):
        # Method for the gamble game
        enemy = "Dare Devil: "
        if self.type == "gambler":
            println(
                enemy+" I will roll a 6-sided dice. If you can guess the number you are free, if not you must pay with your life")
            println("Rolling...")
            diceNumber = random.randrange(1, 6)
            guess = input("Take a guess? >>>")
            if int(guess) == diceNumber:
                println("Congratulations Peasant, you may continue")
                println("You have been awarded 80 points!!!")
                self.fail = False
            else:
                println(
                    enemy+" You have failed, mortal. HaHaHa. My number was "+str(diceNumber))
                self.fail = True
        else:
            raise IncorrectCharacterTypeError(
                self.type + " has no attribute "+self.gamble.__name__)


# FUNCTIONS


wizard = "Wizard: "  # For the wizard so I dont have to type it out :D


def println(*args):
    # REDEFINING THE PRINT FUNCTION!! makes the code shorter
    print(*args)
    print(" ")
    time.sleep(2.8)


def viewInventory(object):
    # Shows the player thier inventory
    view = input("Would you like to view your Inventory?")
    if view == "yes" or view == "y":
        println("Your Inventory:")
        println(object.inventory)
    else:
        return


def pathway(newPlayer):
    # Final Stage Rock paper scissors game
    println(wizard+" Congratulations mighty warrior, It's a miracle you have got through alive.")
    println(wizard+" Here is your final Challenge before you can get to the hotel")
    # Make a new enemy
    thief = Enemy("thief")
    println(wizard+" Walk down the super secure totally safe path to the hotel!")
    println("Walking...")
    println("Oh no a ", thief.type, " has appeared")
    println("Would you like to pay the Thief to leave you or continue his challenge")
    option = input("Pay up or Play?").upper()
    if option == "PAY" or option == "PAY UP":
        println("Thief: I would like your points to let you free")
        newPlayer.purchase("Wimp Ticket")
        if "Wimp Ticket" in newPlayer.inventory:
            println("Thief: You may continue you wimp!!")
            victoryScreen(newPlayer.points)
        else:
            println("WHAT!! how dare you. Get out of here")
            newPlayer.death()
    elif option == "PLAY":
        println("Thief: We shall play Rock Paper Scissors and if you loose I Attack")
        choices = ["Rock", "Paper", "Scissors"]
        gameDraw = True
        while gameDraw:
            # Options for Rock Paper Scissors. and loop for reset
            ThiefChoice = random.choice(choices).upper()
            user = input("Please Choose from: "+str(choices)).upper()
            # Draw
            if user == ThiefChoice:
                println("Draw")
                continue
            # Rock
            elif user == "ROCK" and ThiefChoice == "SCISSORS":
                println("Thief: Ahh you won")
                newPlayer.earnPoints(70)
                println("You have been awarded 70 points")
                victoryScreen(newPlayer.points)
                gameDraw = False

            elif user == "ROCK" and ThiefChoice == "PAPER":
                println("Thief: You loose I attack")
                newPlayer.death()
                newPlayer.getHealth()
                gameDraw = False

            # paper
            elif user == "PAPER" and ThiefChoice == "ROCK":
                println("Thief: Ahh you won")
                newPlayer.earnPoints(70)
                println("You have been awarded 70 points")
                victoryScreen(newPlayer.points)
                gameDraw = False

            elif user == "PAPER" and ThiefChoice == "SCISSORS":
                println("Thief: You loose I attack")
                newPlayer.death()
                gameDraw = False
            # Scissors
            elif user == "SCISSORS" and ThiefChoice == "PAPER":
                println("Thief: Ahh you won")
                newPlayer.earnPoints(70)
                println("You have been awarded 70 points")
                victoryScreen(newPlayer.points)
                gameDraw = False

            elif user == "SCISSORS" and ThiefChoice == "ROCK":
                println("Thief: You loose I attack")
                newPlayer.death()
                newPlayer.getHealth()
                gameDraw = False
    else:
        # Get rid of the player if they think they can get around the game :P
        println("Thief: Don't mess with me fool")
        newPlayer.death()


def bridge(newPlayer):
    # Level 2. Games
    println("You have Encountered a pathway. Choose a direction.")
    println("Think carefully about the possible dangers")
    print(u'\u2022'+"Left - A flowery meadow")
    print(u'\u2022'+"Middle - A River")
    print(u'\u2022'+"Right - A Mountain path")
    direction = input(">>>").upper()
    if direction == "LEFT":
        # Speed typing game
        println("You encountered a BEE!!")
        println(
            "In order to defend yourself type: 'Block the Bee' before the timer runs out.")
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        t = time.time()
        defence = input("GO!!!  >>>")
        t2 = time.time()
        timedelta = t2 - t
        if defence == "Block the Bee":
            if int(round(timedelta, 1)) <= 2.5:
                println("Well done you killed the Bee")
                println("You have been awarded 10 points and a honeycomb.")
                newPlayer.inventory.append("Honey Comb")
                println("The honey Comb can be used to heal you when in need")
                newPlayer.earnPoints(10)
                println("You now have "+str(newPlayer.points)+" points")
                viewInventory(newPlayer)
            else:
                println("You ran out of time")
                beeDamage = random.randrange(1, 5)
                println("You were stung by the bee. Taking " +
                        str(beeDamage)+" points of damage")
                newPlayer.addHealth(-beeDamage)
                newPlayer.getHealth()
        else:
            println("Sorry you mistyped the phrase")
            beeDamage = random.randrange(1, 5)
            println("You were stung by the bee. Taking " +
                    str(beeDamage)+" points of damage")
            newPlayer.getHealth()

    elif direction == "RIGHT":
        # Guessing game
        dareDevil = Enemy("gambler")
        enemy = "Dare Devil: "
        println("You encontered a "+dareDevil.type+"!")
        println(
            enemy+"Hello Trespasser, If you want to cross you must gamble your way through")
        dareDevil.gamble()
        if dareDevil.fail == False:
            newPlayer.earnPoints(80)
            println("You have obtained a medal")
            newPlayer.inventory.append("medal")
            viewInventory(newPlayer)
        else:
            newPlayer.death()

    elif direction == "MIDDLE":
        # Luck game
        println("Welcome to the River")
        println("You must purchase a boat to cross")
        newPlayer.purchase("Boat")
        if "Boat" in newPlayer.inventory:
            println(
                "Please be aware that you have a 10"+'% ' + "chance of being eaten by a crocodile")
            chance = random.randrange(1, 10)
            if chance == 5:
                println("Oh no a Crocodile has attacked")
                newPlayer.death()
            else:
                println("You crossed the river Safetly")
                println("Your reward is 50 points")
                newPlayer.earnPoints(50)
                println("You earned a Crocodile badge")
                newPlayer.inventory.append("Crocodile Badge")
                viewInventory(newPlayer)
        else:
            println("Guess you have to swim then. The probability increases to 50%")
            chance = random.randrange(1, 2)
            if chance == 2:
                println("Oh no a Crocodile has attacked")
                newPlayer.death()
            else:
                println("You crossed the river Safetly")
                println("Your reward is 50 points")
                newPlayer.earnPoints(50)
                println("You earned a Crocodile badge")
                newPlayer.inventory.append("Crocodile Badge")
                viewInventory(newPlayer)

    else:
        println("You can't get away that easily")
        println("BANG!!")
        newPlayer.death()


def mainloop(player, locationCont, LocationPlace):
    """Stage One Journey 

    Arguments:
        player {Object} -- Pass the Player to use it's attribute
        locationCont {String} -- Randomly generated Location from dict
        LocationPlace {String} -- Random place from the Dictionary
    """
    newPlayer = Player(player)
    newPlayer.getHealth()
    time.sleep(2.5)
    println("You are Being transported to " +
            LocationPlace+","+locationCont+"...\n\n")
    println("Welcome to ", LocationPlace)
    flightDamage = random.randrange(0, newPlayer.health)
    newPlayer.addHealth(-flightDamage)
    println("Unfortunately the cabin pressure decreased in flight.")
    println("You took ", flightDamage, " points of damage")
    newPlayer.getHealth()
    println(wizard+" Hello again, I would like to congratulate you on safe arrival")
    reward = random.randrange(0, 80)
    newPlayer.earnPoints(reward)
    println(wizard+" I give you "+str(reward)+" points as a reward")
    println("A Merchant has appeared")
    newPlayer.purchase("Postcard")
    bridge(newPlayer)
    pathway(newPlayer)


def startGame():
    """Starts the main game and resets the screen
    """
    gameExit = True  # pylint: disable=unused-variable
    pygame.display.quit()  # pylint: disable=no-member
    game()
    sys.exit()


def quitGame():
    pygame.quit()  # pylint: disable=no-member
    sys.exit()


def game():
    """
    Start of the game Allows the screen to start the game
    """
    println(wizard+"Hello Fellow Traveller")
    println(wizard+"I Notice you come from afar, What is your name? Tell me you must")
    name = input(">>>")
    print(" ")
    time.sleep(5)
    println(wizard+"Ahhh, Hello There "+name+" A great Mission for you I have")
    println(wizard+"You ave' worked very hard my dear " +
            name+" Go on a holiday you must")
    start = input("Are you Ready to Begin??")
    print(" ")
    if start == "yes" or start == "y" or start == "yeah":
        println(wizard+"Welcome to the adventure "+name+"!")
        println(wizard+"Your random place to visit today is...")
        PlayerPlace = GetPlace.place
        PlayerContinent = GetPlace.continent
        println(PlayerPlace+" in "+PlayerContinent)
        println(
            wizard+"Good Luck! I shall be waiting for you with a reward IF you survive")
        mainloop(name, PlayerContinent, PlayerPlace)
    else:
        println(wizard+"You dared to waste the time of the great one!!!")
        println(wizard+"OUT!!!!")
        sys.exit()


def button(x, y, width, height, inactive, active, action=None):
    """Generate a pygame button. The cur is the position of the button and 
    then the boundary is check to see if the user is hovering

    Arguments:
        x {[int]} -- [x position]
        y {[int]} -- [y position]
        width {[int]} -- [Width of the button]
        height {[int]} -- [Height of the buttom]
        inactive {[tuple]} -- [Colour of inactive]
        active {[tuple]} -- [Colour of active button fro hover states]

    Keyword Arguments:
        action {[sting]} -- [Run a command when click the button] (default: {None})
    """
    cur = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, inactive, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "startGame":
                startGame()
            elif action == "quitGame":
                quitGame()
    else:
        pygame.draw.rect(gameDisplay, active, (x, y, width, height))


def LoadScreen():
    # Create a Screen on load
    global gameDisplay
    gameDisplay = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("The Random Game")

    pygame.display.update()
    # Text
    Instructions = "Welcome to the text-based game, where absolutely everything that happends is randomised."
    InstructionsTwo = "Yes including the damage you deal and the health you have."
    InstructionsThree = "Try to collect all the items."
    # Render Fonts
    text = font.render("The Random Game", True, white)
    inst = fontInst.render(Instructions, True, white)
    instTwo = fontInst.render(InstructionsTwo, False, white)
    InstThree = fontInst.render(InstructionsThree, False, white)
    # Generate a rectangle around the text to center it on coordinates
    textRect = text.get_rect()
    textRect.center = (X//2, Y//2.5)
    InstRect = inst.get_rect()
    InstRect.center = (X//2, Y//2)
    InstRectTwo = instTwo.get_rect()
    InstRectTwo.center = (X//2, Y//2+50)
    InstRectThree = InstThree.get_rect()
    InstRectThree.center = (X//2, Y//2+100)

    global gameExit
    # Event listeners
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                gameExit = True

        # Place Objects onto the screen
        gameDisplay.fill(gray)
        gameDisplay.blit(text, textRect)
        gameDisplay.blit(inst, InstRect)
        gameDisplay.blit(instTwo, InstRectTwo)
        gameDisplay.blit(InstThree, InstRectThree)

        # Make a button and rerender the screen
        button(350, Y//1.5+50, 100, 50, darkWhite, white, action="startGame")
        btn_text = fontInst.render("Start", True, gray)
        btnRect = btn_text.get_rect()
        btnRect.center = (X//2, Y//1.5+75)
        gameDisplay.blit(btn_text, btnRect)
        pygame.display.update()

        # Tick Speed
        clock.tick(FPS)


def DeathScreen(score):
    # Render Death screen
    global gameDisplay

    gameDisplay = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("The Random Game | You have Died")

    pygame.display.update()
    mainText = "You have Died"
    score = "Score: " + str(score)
    title = font.render(mainText, True, white)
    titleRect = title.get_rect()
    titleRect.center = (X//2, Y//2.5)
    ScoreText = font.render(score, True, white)
    ScoreRect = ScoreText.get_rect()
    ScoreRect.center = (X // 2, Y//1.5 - 60)

    deathExit = False
    while not deathExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                deathExit = True

        gameDisplay.fill(gray)
        gameDisplay.blit(title, titleRect)
        gameDisplay.blit(ScoreText, ScoreRect)

        button(350, Y//1.5, 100, 50, darkWhite, white, action="startGame")
        btn_text = fontInst.render("Retry", True, gray)
        btnRect = btn_text.get_rect()
        btnRect.center = (X//2, Y//1.5+25)
        gameDisplay.blit(btn_text, btnRect)

        pygame.display.update()
        clock.tick(FPS)


def victoryScreen(score):
    # Render The final screen
    global gameDisplay

    gameDisplay = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("The Random Game")

    pygame.display.update()
    mainText = "Congratulations"
    score = "Score: "+str(score)
    message = "You have just completed the very randomised game which I doubted was possible."
    #extra = "You either had imense luck! or you took the easy route?"
    title = fontLarge.render(mainText, True, white)
    titleRect = title.get_rect()
    titleRect.center = (X//2, Y//2.5 - 180)
    ScoreText = font.render(score, True, white)
    ScoreRect = ScoreText.get_rect()
    ScoreRect.center = (X // 2, Y//1.5 - 60)
    messageText = fontInst.render(message, True, white)
    #extraText = fontInst.render(extra, True, white)
    messageRect = messageText.get_rect()
    #extraRect = extraText.get_rect()
    messageRect.center = (X // 2, Y//1.5 - 150)
    # extraRect.center = (X // 2, Y//1.5 - 200)

    deathExit = False
    while not deathExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                deathExit = True

        gameDisplay.fill(gray)
        gameDisplay.blit(title, titleRect)
        gameDisplay.blit(ScoreText, ScoreRect)
        gameDisplay.blit(messageText, messageRect)
        #gameDisplay.blit(extraText, extraRect)

        button(X//2 - 150, Y//1.5, 100, 50,
               darkWhite, white, action="startGame")
        btn_text = fontInst.render("Play Again", True, gray)
        btnRect = btn_text.get_rect()
        btnRect.center = (X//2 - 100, Y//1.5 + 25)
        gameDisplay.blit(btn_text, btnRect)

        button(X//2 + 50, Y//1.5, 100, 50, darkWhite, white, action="quitGame")
        btn_textTwo = fontInst.render("Exit", True, gray)
        btnRectTwo = btn_textTwo.get_rect()
        btnRectTwo.center = (X//2 + 100, Y//1.5 + 25)
        gameDisplay.blit(btn_textTwo, btnRectTwo)

        pygame.display.update()
        clock.tick(FPS)


LoadScreen()
pygame.quit()  # pylint: disable=no-member
