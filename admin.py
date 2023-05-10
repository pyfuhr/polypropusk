from data.users import User
from data import db_session
import pygame, os
from sqlalchemy import delete, null

pygame.font.init()
fnt = pygame.font.SysFont(None, 20)
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption('admin panel, left-remove, right - turn on qr')

db_session.global_init("bases/pass.db")
db_sess = db_session.create_session()
users = db_sess.query(User).filter((User.rights == '')).all()
current_index = 0

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_RIGHT:
                users[current_index].rights = 'q'
                db_sess.commit()
                current_index += 1
            if ev.key == pygame.K_LEFT:
                db_sess.delete(users[current_index])
                db_sess.commit()
                current_index += 1
        if ev.type == pygame.QUIT:
            running = False
    if current_index == len(users):
        running = False
        break
    
    if os.path.isfile(f'static/images/{users[current_index].photoid}'):
        screen.blit(pygame.transform.scale(pygame.image.load(f'static/images/{users[current_index].photoid}'), (270, 350)), (5, 5))
    screen.blit(fnt.render(users[current_index].name_surname, False, (255, 255, 255)), (280, 5))
    screen.blit(fnt.render(users[current_index].group_facult, False, (255, 255, 255)), (280, 25))
    pygame.display.flip()
    screen.fill((0, 0, 0))


db_sess.close()
pygame.quit()