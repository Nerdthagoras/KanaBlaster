import pygame

pygame.init()
font = pygame.font.Font(None,30)

def debug(label,info,x,y,color):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(label + ': ' + str(info),False,color)
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface,'Black',debug_rect)
    display_surface.blit(debug_surf,debug_rect)
