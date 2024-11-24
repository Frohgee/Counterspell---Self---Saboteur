# #updates bullet positions
#     for bullet in bullets:
#         bullet.y -= bullet_speed
#         # Remove bullet if off-screen
#         if bullet.bottom < 0:
#             bullets.remove(bullet)
#         else:
#             screen.blit(bullet_image, bullet.topleft)  # Draw each bullet with the image

#custom event for shooting every 1 sec
# SHOOT_EVENT = pygame.USEREVENT + 1
# pygame.time.set_timer(SHOOT_EVENT, 1000) 

# CHANGE_SHAPE = pygame.USEREVENT +1
# pygame.time.set_timer(CHANGE_SHAPE, 1000)

# def changing_borders(name, color, center):
#     if name == "square":

    #draws bullets
    # for bullet in bullets:
    #     pygame.draw.rect(screen, (255, 255, 255), bullet)


    # if bullets.colliderect(border):
    #     if bullets.left <= border.left or bullets.right <= border.right:
    #         bullet.x *= -1
    #     if bullets.top <= border.top or bullets.bottom <= border.bottom:
    #         bullet.y *= -1



#if bullet[0].left <= current_rectangle.left:
        #     bullet[0].x = current_rectangle.left + 1
        #     bullet[1] -= bullet[1] * 2

        # if bullet[0].right >= current_rectangle.right:
        #     bullet[0].x = current_rectangle.right - bullet[0].width - 1  
        #     bullet[1] = -bullet[1]  

        # if bullet[0].top <= current_rectangle.top:
        #     bullet[0].y = current_rectangle.top + 1  
        #     bullet[2] = -bullet[2]  

        # if bullet[0].bottom >= current_rectangle.bottom:
        #     bullet[0].y = current_rectangle.bottom - bullet[0].height - 1  
        #     bullet[2] = -bullet[2] 