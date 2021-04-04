import sys

import cv2
import numpy as np
from datetime import datetime
from PIL import Image
import pytesseract
import settings
import models



def readPlayerCards(filename: str) -> list:
    cards = []

    cards_diff = 59
    card1 = [420, 436, 430, 452]
    card2 = [420 + cards_diff, 435 + cards_diff, 430, 451]
    image = cv2.imread(filename)
    #image = cv2.imread("232036_664814.png")

    card1 = image[card1[2]:card1[3], card1[0]:card1[1]]
    card2 = image[card2[2]:card2[3], card2[0]:card2[1]]

    # if card not on table yet
    if emptyCard(card2):
        pass
    else:
        #modificar
        symbol = image[420 + 20:435 + 20,
                 430 + 9:451 - 1]
        symbol_pil = Image.fromarray(symbol, 'RGB')

        symbol2 = image[420 + 35:435 + 36,
                  430 + 9 + 42:451 - 1 + 45]
        symbol_pil2 = Image.fromarray(symbol2, 'RGB')
        cards.append(cardInfo(card1,symbol_pil))
        cards.append(cardInfo(card2,symbol_pil2))

    return cards

def readTableCards(filename: str) -> list:
    cards = []

    # y position for cards on table don't change orginial
    #cards_y1, cards_y2 = 174, 190 orginial
    cards_y1, cards_y2 = 230, 260


    # x changes by 39 px right
    #cards_diff = 39 original
    cards_diff = 59
    
    # hardcoded card 1 x position
    #table_cards = [226, 237] original
    table_cards = [200, 227]


    # hardcoded floop, turn and river positions
    for i in range(1,7):
        table_cards.append(table_cards[0] + cards_diff * i)
        table_cards.append(table_cards[1] + cards_diff * i)

    image = cv2.imread(filename)
    #image = cv2.imread("232036_664814.png")

    for i in range(0, 14, 2):
        # that can be improved, card "10" has other coords
        if i == 6:
            card = image[cards_y1 + 7:cards_y2,
                   table_cards[i] + 7:table_cards[i + 1]]
            symbol = image[cards_y1 + 30:cards_y2 + 20,
                     table_cards[i] + 9:table_cards[i + 1] - 3]
            if not emptyCard(card):
                symbol_pil = Image.fromarray(symbol, 'RGB')
                cards.append(cardInfo(card, symbol_pil))
        elif i == 4:
            card = image[cards_y1 + 7:cards_y2,
                   table_cards[i] + 2:table_cards[i + 1] - 4]
            symbol = image[cards_y1 + 30:cards_y2 + 20,
                     table_cards[i] + 3:table_cards[i + 1] - 7]
            if not emptyCard(card):
                symbol_pil = Image.fromarray(symbol, 'RGB')
                cards.append(cardInfo(card, symbol_pil))
        elif i == 8:
            card = image[cards_y1 + 7:cards_y2,
                   table_cards[i] + 13:table_cards[i + 1] + 4]
            symbol = image[cards_y1 + 30:cards_y2 + 20,
                     table_cards[i] + 14:table_cards[i + 1] + 2]
            if not emptyCard(card):
                symbol_pil = Image.fromarray(symbol, 'RGB')
                cards.append(cardInfo(card, symbol_pil))
        elif i == 10:
            card = image[cards_y1 + 7:cards_y2,
                   table_cards[i] + 17:table_cards[i + 1] + 7]
            symbol = image[cards_y1 + 30:cards_y2 + 20,
                     table_cards[i] + 17:table_cards[i + 1] + 7]
            if not emptyCard(card):
                symbol_pil = Image.fromarray(symbol, 'RGB')
                cards.append(cardInfo(card, symbol_pil))
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




def grabScreen() -> list:
    """
    Takes screenshots and returns list of models.Screenshot objects

    Credits to hazzey from stackoverflow 
    I've just edited his function to search for windows by partial name, screenshot all of them and grab table name
    
    https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
    """
    screenshots = []
    if sys.platform == "darwin":
        from AppKit import NSWorkspace
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )

    if sys.platform == "darwin":
        curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        curr_pid = NSWorkspace.sharedWorkspace().activeApplication()[
            'NSApplicationProcessIdentifier']
        curr_app_name = curr_app.localizedName()
        options = kCGWindowListOptionOnScreenOnly
        windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
        for window in windowList:
            pid = window['kCGWindowOwnerPID']
            windowNumber = window['kCGWindowNumber']
            ownerName = window['kCGWindowOwnerName']
            geometry = window['kCGWindowBounds']
            windowTitle = window.get('kCGWindowName', u'Unknown')
            if  'al118345' in str(
                    windowTitle.encode('ascii', 'ignore')):
                #print("%s - %s (PID: %d, WID: %d): %s" % (
                #ownerName, windowTitle.encode('ascii', 'ignore'), pid,
                #windowNumber, geometry))
                import pyautogui

                screenshot = pyautogui.screenshot()
                from screeninfo import get_monitors


                screenshot = screenshot.resize((1440, 900))

                crop_rectangle = (
                    geometry['X'], geometry['Y'],
                    geometry['X'] + geometry['Width'],
                    geometry['Y'] + geometry['Height'])
                cropped_im = screenshot.crop(crop_rectangle)
                #cropped_im.show()


                filename = datetime.now().strftime("%H%M%S_%f") + '.png'
                cropped_im.save(filename)


                # cropped_im.save(filename)
                tablename = 'partida' #nada importante
                screenshot = models.Screenshot(tablename, filename)
                screenshots.append(screenshot)

                #borrar
                filename = 'ruben/'+ datetime.now().strftime("%H%M%S_%f") +'ruben' + '.png'
                cropped_im.save(filename)

        return screenshots





def cardInfo(image,tipo) -> models.Card:
    """
    Calls __getCardValue and __getCardColor and returns Card object
    """
    card = models.Card(__getCardValue(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)),
        __getCardColor(tipo))

    return card

def __getCardValue(image) -> str:
    """
    Do not use, it's is being called by cardInfo()
    
    Takes an image and returns card as a string:
        -> 2
        -> ...
        -> A
        -> X - error

    Uses --pcm 7 and --pcm 9 if first one fails
    Tested on grayscale images, more tests are requied.
    """
    card = pytesseract.image_to_string(image, config=settings.config_single_line).replace("\f", "").replace("\n", "").replace("\r", "").replace(" ", "")
    try:
        if card in '23456789JQKA':
            return card[0]
        elif '10' in card:
            return card[:2]
    except:
        try:
            card = pytesseract.image_to_string(image, config=settings.config_single_word).replace("\f", "").replace("\n", "").replace("\r", "").replace(" ", "")
            if card in '23456789JQKA':
                return card[0]
            elif '10' in card:
                return card[:2]
        except:
            return "?"
    return "X"

def __getCardColor(image) -> models.Colors:
    """
    Do not use, it's is being called by cardInfo()

    Takes an image in BGR format an returns a string:
        -> Tile
        -> Heart 
        -> Clover
        -> Pike
        -> Error
    """

    max = -1
    estado = ''
    for i in ['diamantes.png','pika.png','trevol.png', 'corazon.png']:
        comparacion = comparar_imagenes(image, i)
        if comparacion > max:
            max =  comparacion
            estado = i

    if  estado == 'diamantes.png':
        return models.Colors.Tiles
    if estado == 'pika.png':
        return models.Colors.Pikes
    if  estado == 'trevol.png':
        return models.Colors.Clovers
    if  estado == 'corazon.png':
        return models.Colors.Hearts
    return models.Colors.Error

    '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
    if __checkBlue(image):
        return models.Colors.Tiles
    elif __checkRed(image):
        return models.Colors.Hearts
    elif __checkGreen(image):
        return models.Colors.Clovers #trevoles
    elif __checkBlack(image):
        return models.Colors.Pikes
    return models.Colors.Error
    '''

def __checkRed(img) -> bool:
    red_lower = np.array([136, 87, 111], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
    red_mask = cv2.inRange(img, red_lower, red_upper) 
    if len(np.argwhere(red_mask)) > 30:
        return True
        
def __checkGreen(img) -> bool:  
    green_lower = np.array([25, 52, 72], np.uint8) 
    green_upper = np.array([102, 255, 255], np.uint8) 
    green_mask = cv2.inRange(img, green_lower, green_upper) 
    if len(np.argwhere(green_mask)) > 30:
        return True

def __checkBlue(img) -> bool:
    blue_lower = np.array([94, 80, 2], np.uint8) 
    blue_upper = np.array([120, 255, 255], np.uint8) 
    blue_mask = cv2.inRange(img, blue_lower, blue_upper)
    if len(np.argwhere(blue_mask)) > 30:
        return True

#more tests to black mask are requied
def __checkBlack(img) -> bool:
    black_lower = np.array([0, 0, 0], np.uint8) 
    black_upper = np.array([50, 50, 50], np.uint8) 
    black_mask = cv2.inRange(img, black_lower, black_upper) 
    if len(np.argwhere(black_mask)) > 20:
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

    imagen2 = imagen2.resize(imagen1.size, Image.ANTIALIAS).convert('RGB')
    imagen1 = imagen1.resize(imagen1.size, Image.ANTIALIAS).convert('RGB')


    img2 = np.array(imagen2)
    img1 = np.array(imagen1)

    from skimage.metrics import structural_similarity as ssim
    s = ssim(img1, img2, multichannel=True)

    return s


