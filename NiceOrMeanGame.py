##
##Python:     3.10
##
##Author:     Salvador Sanchez
##
##Purpose:    This is a game that I created while studying at the Tech Academy

def start(nice=0,mean=0,name=""):
    #get users name in describeGame()
    name = describeGame(name)
    nice,mean,name - niceMean(nice,mean,name)

def describeGame(name):
    """
        check if this is a new game or not.
        If it is new, get the users name.
        if it is not a new game, thank the play for
        playing again and continue with the game.
    """
    if name != "": #if we already have a name, we can skip inputting a new one.
        print('\nI knew you would want to play again, {}.'.format(name))
    else:
        stop = True
        while stop:
            if name == "":
                name = input('\nWhat\'s your name? \n>>> ').capitalize() # capitalizes the first letter
                if name != "":
                    print('\nWelcome, {}!'.format(name))
                    #explain how the game will work
                    print('\nIn this game, you will be greeted\nby several different people.\nYou can choose to be nice or mean')
                    print('but at the end of the game your fate \nwill be sealed, and we\'ll know \nwhat you\'re made of.')
                    stop = False
    return name

def niceMean(nice,mean,name):
    stop = True
    while stop:
        showScore(nice,mean,name)
        #the question is always the same, and the player enters y or n
        pick = input('\nA stranger approaches you for a \nchat. Will you be nice \nor mean? (N/M) \n>>>').lower()
        if pick == 'n':
            print('\nThe stranger skips away feeling good.')
            nice = (nice + 1)
            stop = False
        if pick == 'm':
            print('\nThe stranger glares at you \nmenacingly then storms off \nto post about you on their socials...')
            mean = (mean + 1)
            stop = False
    score(nice,mean,name) #pass the three vars to score()

def showScore(nice,mean,name):
    print('\n{}, your current total: \n({}, Nice) and ({}, Mean)'.format(name,nice,mean))

def score(nice,mean,name):
    if nice > 2:
        win(nice,mean,name) # call win() if condition is valid
    if mean > 2:
        lose(nice,mean,name) #call lose() if condition is valid
    else:
        niceMean(nice,mean,name) #if neither score > 2, keep playing
 
def win(nice,mean,name):
    print('\nNice job {}, you win! \nEveryone loves you and you\'ve \nmade lots of friends along the way!'.format(name))
    again(nice,mean,name) # will see if they want to play again

def lose(nice,mean,name):
    print('\nAhh, too bad, game over! \n{}, you live in a dirty beat-up \nvan by the river'.format(name))
    again(nice,mean,name) # will see if they want to play again
    
def again(nice,mean,name):
    # as the user if they want to play again, and either quit() or start()
    stop = True
    while stop:
        choice = input('\nDo you want to play again? (y/n):\n>>> ').lower()
        if choice == 'y':
            stop = False
            reset(nice,mean,name)
        if choice == 'n':
            print('\nCome back whenever you like. BYE!')
            stop = False
            quit()
        else: #in case they did not provide a valid entry
            print('\nEnter ( Y ) for \'YES\' or ( N ) for \'NO\':\n>>> ')


def reset(nice,mean,name):
    nice = 0
    mean = 0
    # We actually do not need the name variable since it will already hold the user's name
    start(nice,mean,name)


if __name__ == '__main__':
    start()
