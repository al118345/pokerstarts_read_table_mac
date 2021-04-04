import sys

from PIL import Image, ImageChops

if sys.platform == "darwin":
    from AppKit import NSWorkspace
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID
    )

if sys.platform == "darwin":
    curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    curr_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
    curr_app_name = curr_app.localizedName()
    options = kCGWindowListOptionOnScreenOnly
    windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for window in windowList:
        pid = window['kCGWindowOwnerPID']
        windowNumber = window['kCGWindowNumber']
        ownerName = window['kCGWindowOwnerName']
        geometry = window['kCGWindowBounds']
        windowTitle = window.get('kCGWindowName', u'Unknown')
        if curr_pid == pid and 'Poker' in str(windowTitle.encode('ascii','ignore')) :
            print("%s - %s (PID: %d, WID: %d): %s" % (ownerName, windowTitle.encode('ascii','ignore'), pid, windowNumber, geometry))
            import pyautogui

            screenshot = pyautogui.screenshot()
            from screeninfo import get_monitors

            for m in get_monitors():
                print(str(m))
            screenshot = screenshot.resize((1440, 900))


            crop_rectangle = (
            geometry['X'], geometry['Y'], geometry['X'] + geometry['Width'],
            geometry['Y'] + geometry['Height'])
            cropped_im = screenshot.crop(crop_rectangle)
            cropped_im.show()
            break;