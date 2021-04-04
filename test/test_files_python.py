import cv2
import numpy as np



def readPlayerCards(filename: str) -> list:
    cards = []

    cards_diff = 59
    card1 = [420, 435, 430, 451]
    card2 = [420+cards_diff, 435+cards_diff, 430, 451]


    image = cv2.imread("104314_321879ruben.png")

    card1 = image[card1[2]:card1[3], card1[0]:card1[1]]
    import matplotlib.pyplot as plt

    card2 = image[card2[2]:card2[3], card2[0]:card2[1]]
    from PIL import Image
    import numpy as np
    symbol = image[420 + 37:435 +36,
             430 + 9:451 -1]


    img = Image.fromarray(symbol, 'RGB')
    #img.save('my.png')
    img.show()
    # if card not on table yet

    return cards


def readTableCards(filename: str) -> list:
    cards = []

    # y position for cards on table don't change
    cards_y1, cards_y2 = 230, 260

    # x changes by 39 px right
    cards_diff = 59

    # hardcoded card 1 x position
    table_cards = [200, 227]
    #320,235,337,259

    # hardcoded floop, turn and river positions
    for i in range(1, 6):
        table_cards.append(table_cards[0] + cards_diff * i)
        table_cards.append(table_cards[1] + cards_diff * i)

    image = cv2.imread("093324_148552.png")

    for i in range(0, 12, 2):

        # that can be improved, card "10" has other coords
        if i == 6 or i == 4:
            card = image[cards_y1:cards_y2,
                   table_cards[i] - 2:table_cards[i + 1]]
            symbol = image[cards_y1 + 30:cards_y2 + 20,
                     table_cards[i] + 3:table_cards[i + 1] - 7]
            from PIL import Image
            if not emptyCard(card):
                print('entre1')

            img = Image.fromarray(symbol, 'RGB')
            img.save('trevol.png')
            break


            from PIL import Image
            img = Image.fromarray(card, 'RGB')
            if not emptyCard(card):
                print('entre1')
                # cards.append(cardInfo(card))
            #img.show()

        elif i == 8:
            card = image[cards_y1 +7:cards_y2 ,
                   table_cards[i] +10:table_cards[i + 1] ]
            from PIL import Image
            symbol = image[cards_y1+ 30:cards_y2+20,
                   table_cards[i] + 14:table_cards[i + 1]+2]

            img = Image.fromarray(symbol, 'RGB')



            img.save('pika.png')
            img.show()
            if not emptyCard(card):
                print('entre2')
                # cards.append(cardInfo(card))
        elif i == 10:
            card = image[cards_y1+7:cards_y2, table_cards[i]+17:table_cards[i + 1]+7]
            from PIL import Image
            img = Image.fromarray(card, 'RGB')
            #img.save('my2.png')
            #img.show()
            if not emptyCard(card):
                print('entre3')
                # cards.append(cardInfo(card))
        # if card not on table yet


    return cards


def emptyCard(img) -> bool:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        orange_lower = np.array([10, 100, 20], np.uint8)
        orange_upper = np.array([25, 255, 255], np.uint8)
        orange_mask = cv2.inRange(img, orange_lower, orange_upper)
        if len(np.argwhere(orange_mask)) > 100:
            return True

aux = readPlayerCards(' ')
print (aux)



def comparar_imagenes(img2, img1):

    picture1_norm = img2 / np.sqrt(np.sum(img2 ** 2))
    picture2_norm = img1 / np.sqrt(np.sum(img1 ** 2))
    return (np.sum(picture2_norm * picture1_norm))
