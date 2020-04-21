"""
NOTE TO USER --> The code here isn't very neat; I will take some time later to refactor it :D
But feel free to attempt to understand this mess of objects and functions.

BRIEF: Development of a text-based adventure game that eplores different parts of the world

NOTE: Initially I made an API call see below, but the data wasn't quiet as I needed it.
"""

import random
import sys
import time


"""
MY FAILED ATTEMPT WITH AN API! WOOO

    import requests
    import pprint

    ACCOUNT_ID = "0GFG1HX"     API Creds No Longer Valid
    API_TOKEN = "cb2hgwo687kvcvyf2w3778ixuxr"
    CITY = "Rome"

    res = requests.get(
        f"https://www.triposo.com/api/20200405/location.json?id={CITY}&account={ACCOUNT_ID}&token={API_TOKEN}")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(res.json().get('results'))"""

places = {
    "Europe": ["Paris", "Rome", "Venice", "London", "Barcelona", "Berlin", "Budapest"],
    "Africa": ["Cairo", "Marrakesh", "Cape Town", "Luxor", "Fes", "Maasai Mara", "Fuerteventura"],
    "Asia": ["Bangkok", "Kyoto", "Singapore", "Tokyo", "Cambodia", "Beijing", "Dubai"],
    "Oceania": ["Sydney", "Melbourne", "Cairns", "Queenstown", "Perth", "Blue Mountains", "Fiji"],
    "South America": ["Machu Picchu", "Peru", "Cusco", "Lima", "Bueno Aires", "Rio de Janeiro", "Santiago"],
    "North America": ["Grand Canyon", "New York", "Las Vegas", "Los Angeles", "Cuba", "Vancouver", "Yellowstone"],
    "Anarctica": ["King George Island", "Deception Island", "Elephant Island", "Livingston", "General Bernardo's Base", "Eklund islands"],
}


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


class Player:
    def __init__(self, name):
        self.name = name
        self.health = random.randrange(0, 20)
        self.points = 0
        self.inventory = []

    def death(self):
        if "Honey Comb" in self.inventory:
            println("Opps! Looks like you died, however...")
            println(
                "Looks like you have a Honey comb, would you like to use it ot regain health?")
            option = input(">>>")
            if option == "yes" or option == "y":
                self.addHealth(random.randrange(1, 5))
        else:
            println("You have died")
            println("You finished with a score of "+str(self.points))
            println("Here is what you finished with: "+str(self.inventory))
            sys.exit()

    def getHealth(self):
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
        self.health = self.health + damage

    def purchase(self, item, price=None):
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
        self.points += amount


# Defining a custom error message incase I mess up on the type specific method calls.


class IncorrectCharacterTypeError(ValueError):
    pass

# The Enemy Object


class Enemy():
    def __init__(self, type):
        self.type = type
        self.health = 10
        self.damageDealt = random.randrange(0, 15)
        self.fail = True

    def Attack(self, object):
        object.addHealth(-self.damageDealt)

    def gamble(self):
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


# Main Game Loop
wizard = "Wizard: "

# REDEFINING THE PRINT FUNCTION!! makes the code shorter


def println(*args):
    print(*args)
    print(" ")
    time.sleep(2.8)


def viewInventory(object):
    view = input("Would you like to view your Inventory?")
    if view == "yes" or view == "y":
        println("Your Inventory:")
        println(object.inventory)
    else:
        return


def gameComplete(newPlayer):
    println("congratulations "+newPlayer.name)
    println("Welcome to the hotel")

# Stage 3


def pathway(newPlayer):
    println(wizard+" Congratulations mighty warrior, It's a miracle you have got through alive.")
    println(wizard+" Here is your final Challenge before you can get to the hotel")
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
            gameComplete(newPlayer)
        else:
            println("WHAT!! how dare you. Get out of here")
            newPlayer.death()
    elif option == "PLAY":
        println("Thief: We shall play Rock Paper Scissors and if you loose I Attack")
        choices = ["Rock", "Paper", "Scissors"]
        gameDraw = True
        while gameDraw:
            ThiefChoice = random.choice(choices).upper()
            user = input("Please Choose from: "+str(choices)).upper()
            # Draw
            if user == ThiefChoice:
                println("Draw")
                continue
            # Rock
            elif user == "ROCK" and ThiefChoice == "SCISSORS":
                println("Thief: Ahh you won")
                gameComplete(newPlayer)
                gameDraw = False

            elif user == "ROCK" and ThiefChoice == "PAPER":
                println("Thief: You loose I attack")
                thief.Attack(newPlayer)
                println("You have been attacked")
                newPlayer.getHealth()
                gameDraw = False

            # paper
            elif user == "PAPER" and ThiefChoice == "ROCK":
                println("Thief: Ahh you won")
                gameComplete(newPlayer)
                gameDraw = False

            elif user == "PAPER" and ThiefChoice == "SCISSORS":
                println("Thief: You loose I attack")
                thief.Attack(newPlayer)
                println("You have been attacked")
                newPlayer.getHealth()
                gameDraw = False
            # Scissors
            elif user == "SCISSORS" and ThiefChoice == "PAPER":
                println("Thief: Ahh you won")
                gameComplete(newPlayer)
                gameDraw = False

            elif user == "SCISSORS" and ThiefChoice == "ROCK":
                println("Thief: You loose I attack")
                thief.Attack(newPlayer)
                println("You have been attacked")
                newPlayer.getHealth()
                gameDraw = False
    else:
        println("Thief: Don't mess with me fool")
        newPlayer.death()


# Level 2


def bridge(newPlayer):
    println("You have Encountered a pathway. Choose a direction.")
    println("Think carefully about the possible dangers")
    print(u'\u2022'+"Left - A flowery meadow")
    print(u'\u2022'+"Middle - A River")
    print(u'\u2022'+"Right - A Mountain path")
    direction = input(">>>").upper()
    if direction == "LEFT":
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

# Level 1


def mainloop(player, locationCont, LocationPlace):
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


# Intro
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
    println(wizard+"Good Luck! I shall be waiting for you with a reward IF you survive")
    mainloop(name, PlayerContinent, PlayerPlace)
else:
    println(wizard+"You dared to waste the time of the great one!!!")
    println(wizard+"OUT!!!!")
    sys.exit()
