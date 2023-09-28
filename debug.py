import pygame

pygame.init()

def debug(label,info,x,y):
    font = pygame.font.Font(None,30)
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(label + ': ' + str(info),False,'white')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface,'Black',debug_rect)
    display_surface.blit(debug_surf,debug_rect)