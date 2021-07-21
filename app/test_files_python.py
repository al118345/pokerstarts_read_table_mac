import cv2
import numpy as np

from app import tools
from app.tools import cardInfo
from PIL import Image


def readPlayerCards(filename: str) -> list:
    cards = []

    cards_diff = 59
    card1 = [420, 436, 430, 452]
    card2 = [420 + cards_diff, 435 + cards_diff, 430, 451]
    image = cv2.imread(filename)
    image = cv2.imread("125326_308006ruben.png")

    card1 = image[card1[2]:card1[3], card1[0]:card1[1]]
    card2 = image[card2[2]:card2[3], card2[0]:card2[1]]

    # if card not on table yet
    if emptyCard(card2):
        pass
    else:
        # modificar
        symbol = image[420 +20:435 +20,
                 430 + 9:451 - 1]
        symbol_pil = Image.fromarray(card1, 'RGB')
        symbol_pil.show()

        symbol_pil = Image.fromarray(symbol, 'RGB')
        symbol_pil.show()

        symbol2 = image[420 + 35:435 + 36,
                  430 + 9 + 42:451 - 1 + 45]
        symbol_pil2 = Image.fromarray(symbol2, 'RGB')
        cards.append(cardInfo(card1, symbol_pil))
        cards.append(cardInfo(card2, symbol_pil2))

    return cards


def readTableCards(filename: str) -> list:

    cards = []
    # y position for cards on table don't change
    cards_y1, cards_y2 = 230, 260
    # x changes by 39 px right
    cards_diff = 59
    # hardcoded card 1 x position
    table_cards = [200, 227]

    # hardcoded floop, turn and river positions
    for i in range(1, 7):
        table_cards.append(table_cards[0] + cards_diff * i)
        table_cards.append(table_cards[1] + cards_diff * i)

    image = cv2.imread("104451_019554ruben.png")

    for i in range(0, 14, 2):

        # that can be improved, card "10" has other coords
        if i == 6:
            card = image[cards_y1+7:cards_y2,
                   table_cards[i]+7:table_cards[i + 1]]
            symbol = image[cards_y1 + 30:cards_y2 + 20,
                     table_cards[i] + 9:table_cards[i + 1] - 3]
            if not emptyCard(card):
                print('entre1')
                symbol_pil = Image.fromarray(symbol, 'RGB')
                cards.append(cardInfo(card,symbol_pil))

        elif i == 4:
            card = image[cards_y1 + 7:cards_y2,
                   table_cards[i] + 2:table_cards[i + 1]-4]
            symbol = image[cards_y1 + 30:cards_y2+20,
                   table_cards[i] + 3:table_cards[i + 1] -7]
            if not emptyCard(card):
                symbol_pil = Image.fromarray(symbol, 'RGB')
                symbol_pil.show()
                cards.append(cardInfo(card,symbol_pil))
        elif i == 8:
            card = image[cards_y1 +7:cards_y2 ,
                   table_cards[i] +13:table_cards[i + 1] +4]
            symbol =  image[cards_y1 + 30:cards_y2+20,
                   table_cards[i] + 14:table_cards[i + 1]+2]
            if not emptyCard(card):
                symbol_pil = Image.fromarray(symbol, 'RGB')
                symbol_pil.show()

                symbol_pil = Image.fromarray(symbol, 'RGB')
                cards.append(cardInfo(card,symbol_pil))

        elif i == 10:
            card = image[cards_y1+7:cards_y2, table_cards[i]+17:table_cards[i + 1]+7]
            symbol = image[cards_y1 + 30:cards_y2 + 20,
                     table_cards[i] + 17:table_cards[i + 1] + 7]
            if not emptyCard(card):
                symbol_pil = Image.fromarray(symbol, 'RGB')
                cards.append(cardInfo(card,symbol_pil))
        elif i == 12:
            card = image[cards_y1 + 7:cards_y2,
                   table_cards[i] + 22:table_cards[i + 1] + 12]
            symbol = image[cards_y1 + 30:cards_y2 + 20,
                     table_cards[i] + 22:table_cards[i + 1] + 12]
            if not emptyCard(card):
                symbol_pil = Image.fromarray(symbol, 'RGB')
                cards.append(cardInfo(card, symbol_pil))

    return cards


def emptyCard(img) -> bool:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        orange_lower = np.array([10, 100, 20], np.uint8)
        orange_upper = np.array([25, 255, 255], np.uint8)
        orange_mask = cv2.inRange(img, orange_lower, orange_upper)
        if len(np.argwhere(orange_mask)) > 100:
            return True

def comparar_imagenes(img2, img1):
    if isinstance(img1, str):
        imagen1 = Image.open(img1)
    else:
        imagen1=img1
    if isinstance(img2, str):
        imagen2 = Image.open(img2)
    else:
        imagen2=img2


    imagen2 = imagen2.resize((160,60), Image.ANTIALIAS).convert('RGB')
    imagen1 = imagen1.resize((160,60), Image.ANTIALIAS).convert('RGB')
    img2 = np.array(imagen2)
    img1 = np.array(imagen1)
    from skimage.metrics import structural_similarity as ssim
    s = ssim(img1, img2, multichannel=True)
    return s



def number_player(img):


    player1 = [80,335,96,341]
    player2 = [107,126,125,135]
    player3 = [437,65,461,71]
    player4 = [768,129,787,136]
    player5 = [858,334,882,340]

    image = cv2.imread(img)
    image = cv2.imread("125326_308006ruben.png")
    #image = cv2.imread("124535_473536ruben.png")


    '''
    card1 = image[player1[1]:player1[3], player1[0]:player1[2]]
    symbol_pil = Image.fromarray(card1, 'RGB')
    #symbol_pil.save("/Users/rubenperezibanez/PycharmProjects/Pokerstars-Api/app/imagenes/jugadores/player1.jpeg")

    card1 = image[player2[1]:player2[3], player2[0]:player2[2]]
    symbol_pil = Image.fromarray(card1, 'RGB')
    #symbol_pil.save("/Users/rubenperezibanez/PycharmProjects/Pokerstars-Api/app/imagenes/jugadores/player2.jpeg")

    card1 = image[player3[1]:player3[3], player3[0]:player3[2]]
    symbol_pil = Image.fromarray(card1, 'RGB')
    #symbol_pil.save("/Users/rubenperezibanez/PycharmProjects/Pokerstars-Api/app/imagenes/jugadores/player3.jpeg")

    card1 = image[player4[1]:player4[3], player4[0]:player4[2]]
    symbol_pil = Image.fromarray(card1, 'RGB')
    #symbol_pil.save( "/Users/rubenperezibanez/PycharmProjects/Pokerstars-Api/app/imagenes/jugadores/player4.jpeg")

    card1 = image[player5[1]:player5[3], player5[0]:player5[2]]
    symbol_pil = Image.fromarray(card1, 'RGB')
    #symbol_pil.save("/Users/rubenperezibanez/PycharmProjects/Pokerstars-Api/app/imagenes/jugadores/player5.jpeg")
    '''

    ruta = "/Users/rubenperezibanez/PycharmProjects/Pokerstars-Api/app/imagenes/jugadores/"
    ficheros = ["player1.jpeg","player2.jpeg","player3.jpeg","player4.jpeg","player5.jpeg"]
    players = [player1,player2,player3,player4,player5]
    cont = 0
    resultado = 0
    for i in ficheros:

        card1 = image[players[cont][1]:players[cont][3], players[cont][0]:players[cont][2]]
        symbol_pil = Image.fromarray(card1, 'RGB')
        comparacion = comparar_imagenes( symbol_pil, ruta +i)
        cont = cont +1
        if comparacion> 0.9:
            resultado = resultado +1

    return resultado


aux = number_player(' ')
print (aux)