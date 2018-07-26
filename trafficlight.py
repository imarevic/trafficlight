# === import modules === #
import pygame
import sys
import random
import time

# === global settings dict === #
settings = {"caption" : "Traffic Light App",
            "running" : True,
            "screen" : None,
            "bgColor" : (240, 240, 240),
            "blackColor" : (0, 0, 0),
            "greenColor" : (150, 150, 150),
            "redColor" : (150, 150, 150),
            "yellowColor" : (150, 150, 150),
            "buttonColor" : (160, 160, 160),
            "clock" : None,
            "screenSize" : (900, 700),
            "FPS" : 60,
            "font" : None,
            "goText" : "GO",
            "stopText" : "STOP",
            "quitText" : "QUIT",
            "goContent" : None,
            "stopContent" : None,
            "quitContent" : None,
            "mousePos" : None,
            "boxRect" : None,
            "goRect" : None,
            "stopRect" : None,
            "quitRect" : None,
            "goButtonRect" : None,
            "stopButtonRect" : None,
            "quitButtonRect" : None,
            "goButton" : None,
            "stopButton" : None,
            "quitButton" : None,
            "clicked" : None,
            "changed" : False,
            "radius" : None,
            "redPos" : None,
            "yellowPos" : None,
            "greenPos" : None,
            }


# ===  define procedure that runs the program === #
def run():
    """runs the application."""

    # initialize pygame and font
    init_pygame()

    while settings["running"]:

        # process events
        process_events()
        # draw background
        draw_background()
        # draw static traffic light
        draw_traffic_light()
        draw_change_light(1.0)
        # draw buttons
        draw_buttons()
        # update screen
        update()



# === define helper functions that are called inside run() === #
def init_pygame():
    """
    initializes pygame backends explicitly with
    predefined settings.
    """

    # initialize pygame modules
    pygame.init()

    # set screen settings
    settings["screen"] = pygame.display.set_mode(settings["screenSize"])
    pygame.display.set_caption(settings["caption"])
    pygame.mouse.set_visible(True) # enable mouse

    # create clock
    settings["clock"] = pygame.time.Clock()

    # get screen rect and set font
    settings["font"] = pygame.font.SysFont("Arial", 25)
    settings["screenRect"] = settings["screen"].get_rect()

def process_events():
    """processes events of the app."""

    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            settings['running'] = False
            pygame.quit()
            sys.exit(0)
        # mouse events
        elif event.type == pygame.MOUSEBUTTONUP:
            settings["mousePos"] = pygame.mouse.get_pos()
            set_light_color()

def draw_background():
    """draws background."""

    settings["screen"].fill(settings["bgColor"])

def render_buttons():
    """renders buttons as text boxes."""
    # create text objects
    settings["goContent"] = settings["font"].render(settings["goText"], True, settings["blackColor"])
    settings["stopContent"] = settings["font"].render(settings["stopText"], True, settings["blackColor"])
    settings["quitContent"] = settings["font"].render(settings["quitText"], True, settings["blackColor"])

    # get rects of text objects
    settings["goRect"] = settings["goContent"].get_rect()
    settings["stopRect"] = settings["stopContent"].get_rect()
    settings["quitRect"] = settings["quitContent"].get_rect()

    # position the rects
    settings["goRect"] = settings["goRect"].move(settings["screenRect"].width * 0.75 - settings["goRect"].width // 2,
                                                    settings["screenRect"].height * 0.25 - settings["goRect"].height // 2)
    settings["stopRect"] = settings["stopRect"].move(settings["screenRect"].width * 0.75 - settings["stopRect"].width // 2,
                                                    settings["screenRect"].height * 0.5 - settings["stopRect"].height // 2)
    settings["quitRect"] = settings["quitRect"].move(settings["screenRect"].width * 0.75 - settings["quitRect"].width // 2,
                                                    settings["screenRect"].height * 0.75 - settings["quitRect"].height // 2)

    # create button rects
    settings["goButtonRect"] = pygame.Rect((10, 10), (settings["goRect"].width * 1.3, settings["goRect"].height * 1.3))
    settings["stopButtonRect"] = pygame.Rect((10, 10), (settings["stopRect"].width * 1.3, settings["stopRect"].height * 1.3))
    settings["quitButtonRect"] = pygame.Rect((10, 10), (settings["quitRect"].width * 1.3, settings["quitRect"].height * 1.3))

    # posiiton button rects
    settings["goButtonRect"].center = settings["goRect"].center
    settings["stopButtonRect"].center = settings["stopRect"].center
    settings["quitButtonRect"].center = settings["quitRect"].center

def render_traffic_light():
    """
    renders rect that makes up traffic light
    and defines circle parameters that make up
    the lights.
    """
    # creata the box
    settings["boxRect"] = pygame.Rect((10, 10), (settings["screenRect"].width * 0.3, settings["screenRect"].height * 0.75))
    # position box
    settings["boxRect"].center = (settings["screenRect"].centerx // 2, settings["screenRect"].centery)

def define_circle_pos():
    """
    defines the circle positions and radius
    (positions of each light).
    """
    # define posions of circles (posions of lights)
    settings["redPos"] = (settings["boxRect"].centerx,
                          int(settings["boxRect"].centery - (settings["boxRect"].height - settings["boxRect"].height * 0.75)))
    settings["yellowPos"] = (settings["boxRect"].centerx,
                          int(settings["boxRect"].centery - (settings["boxRect"].height - settings["boxRect"].height * 1)))
    settings["greenPos"] = (settings["boxRect"].centerx,
                           int(settings["boxRect"].centery - (settings["boxRect"].height - settings["boxRect"].height * 1.25)))
    # define radius
    settings["radius"] = int(settings["boxRect"].width * 0.2)

def draw_buttons():
    """draws all buttons."""
    # render buttons
    render_buttons()
    # draw button shape to backbuffer
    pygame.draw.rect(settings["screen"], settings["blackColor"], settings["goButtonRect"], 2)
    pygame.draw.rect(settings["screen"], settings["blackColor"], settings["stopButtonRect"], 2)
    pygame.draw.rect(settings["screen"], settings["blackColor"], settings["quitButtonRect"], 2)

    # draw content to backbuffer
    settings["screen"].blit(settings["goContent"], settings["goRect"])
    settings["screen"].blit(settings["stopContent"], settings["stopRect"])
    settings["screen"].blit(settings["quitContent"], settings["quitRect"])

def draw_traffic_light():
    """draws the traffic light."""

    # render traffic light box and circle positions
    render_traffic_light()
    define_circle_pos()
    # draw shape of traffic light box to backbuffer
    pygame.draw.rect(settings["screen"], settings["blackColor"], settings["boxRect"], 4)

    #draw static light
    static_light()
    # draw circles
    draw_circles()

def draw_change_light(duration):
    """draws the traffic light."""

    # render traffic light box and circle positions
    render_traffic_light()
    define_circle_pos()
    # draw shape of traffic light box to backbuffer
    pygame.draw.rect(settings["screen"], settings["blackColor"], settings["boxRect"], 4)

    if settings["changed"] == True:
        startTime = pygame.time.get_ticks() / 1000
        while pygame.time.get_ticks() / 1000 - startTime < duration:
            #draw static light
            dynamic_light()
            # draw circles
            draw_circles()
            draw_buttons()
            update()

    settings["changed"] = False

def draw_circles():
    """draws all circles"""

    # draw circles
    # red circle
    pygame.draw.circle(settings["screen"], settings["redColor"], settings["redPos"], settings["radius"])
    # yellow circle
    pygame.draw.circle(settings["screen"], settings["yellowColor"], settings["yellowPos"], settings["radius"])
    # green circle
    pygame.draw.circle(settings["screen"], settings["greenColor"], settings["greenPos"], settings["radius"])

def static_light():
    """
    sets static circle lights
    (green and red)
    """
    # set color accordingly
    if settings["clicked"] == "go":

        settings["redColor"] = (150, 150, 150)
        settings["yellowColor"] = (150, 150, 150)
        settings["greenColor"] = (0, 255, 0)

    elif settings["clicked"] == "stop":
        settings["redColor"] = (255, 0, 0)
        settings["yellowColor"] = (150, 150, 150)
        settings["greenColor"] = (150, 150, 150)


def dynamic_light():
    """
    sets dynamic light
    (yellow)
    """

    settings["redColor"] = (150, 150, 150)
    settings["yellowColor"] = (255, 255, 0)
    settings["greenColor"] = (150, 150, 150)



def set_light_color():
    """controls color of traffic lights."""
    # set boolean values to true depending on which one was clicked
    goClicked = settings["goButtonRect"].collidepoint(settings["mousePos"])
    stopClicked = settings["stopButtonRect"].collidepoint(settings["mousePos"])
    quitClicked = settings["quitButtonRect"].collidepoint(settings["mousePos"])

    # change flags for change and permanent light process_events
    # depending on mouse event
    if goClicked == True:
        settings["changed"] = True
        settings["clicked"] = "go"
    elif stopClicked == True:
        settings["changed"] = True
        settings["clicked"] = "stop"
    elif quitClicked == True:
        settings["running"] = False


def update():
    """updates the screen with FPS."""

    settings["clock"].tick(settings["FPS"])
    pygame.display.flip()



# == start the program == #
if __name__ == '__main__':
    run()
