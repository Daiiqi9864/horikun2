import pygame


class EventHandler:
    def __init__() -> None:
        EventHandler.events = pygame.event.get()

    def poll_events():
        EventHandler.events = pygame.event.get()

    def keydown(key):
        for event in EventHandler.events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
        return False
