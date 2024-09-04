import random
import sys
import pygame, choice

class Player(pygame.sprite.Sprite): #Player hérite de Sprite
    def __init__(self):
        super().__init__() #on inisialise la class Sprit dans la class Player
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]  # la liste des frames
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: #à partir de 300, on garde le joueur à ce niveau artificiellement
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300: #si le joueur n'est pas par terre
            self.image = self.player_jump #affiche le entrain de sauter
        else: #si le joueur est par terre
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)] #affiche les images dans la liste de player_walk l'un après l'autre

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type): #le type peut être "fly" ou "snail"
        super().__init__()

        if type == "fly":
            fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210

        else: #si type == "snail"
            snail_frame_1 = pygame.image.load("graphics/snail/snail1.png")
            snail_frame_2 = pygame.image.load("graphics/snail/snail2.png")
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: #si l'obstacle va trop à gauche
            self.kill() #on kill() l'objet obstacle


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list: #si la liste n'est pas vide
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            #vérifier la hauteur du rect et dessiner le bon png (le bon surf)
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)



        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] #la liste est replacé par une deuxième liste contenant que les obstacles ayant un x > -100
        return obstacle_list
    else:
        return []

def collisions(player, obstacles): #obstacles est la liste des obstacles
    if obstacles: #si la liste n'est pas vide
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):return False
    return True

def player_animation():
    #walking animation if player_rect.bottom == 300:
    global player_surf, player_index

    if player_rect.bottom < 300:
        #jump animation
        player_surf = player_jump #quand le joueuer saute il n'y a qu'une seul surface à montrer
    else:
        #walk animation
        player_index += 0.1 #on va lentement augmenter l'index pour passer à la deuxième image à un moment donné
        if player_index >= len(player_walk): #si on déspasse la longeur de la liste, on remet l'index à 0
            player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

#Groupes
player = pygame.sprite.GroupSingle() #on crée un groupe pour player et on l'appelle "player"
player.add(Player()) #on rajoute à ce groupe une instance de la class player
#ducoup on a un group "player" qui contient un "sprit" et le sprit contient les attributs de la class Player

obstacle_groupe = pygame.sprite.Group()


sky_surface = pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

# score_surf = test_font.render("My game", False, (64, 64, 64)).convert_alpha()
# score_rect = score_surf.get_rect(center = (400, 50))

#obstacles
#snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png")
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png")
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

#fly
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2] #la liste des frames
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#Intro screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha() #on importe l'image du joueur pour la page d'acceuil
player_stand = pygame.transform.rotozoom(player_stand,0,2) # surface, l'anle de rotation, coefficient d'aggrandissement
player_stand_rect = player_stand.get_rect(center = (400, 200)) # on crée le rect du surf et on le place au centre du screen

game_name = test_font.render("pixel runner", False, (111, 196, 169)) #le titre du jeu pour la page d'acceuil
game_name_rect = game_name.get_rect(center = (400, 80)) #rect du titre du jeu crée à partir de la surface

game_message = test_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 340))

#Timer:
obstacle_timer = pygame.USEREVENT + 1 #on crée un userevent comme pour le snake
pygame.time.set_timer(obstacle_timer, 1500) #on génère des snail tout les 1500ms

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 200)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 50)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                        player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else: #si game_active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # et qu'on appuye sur space:
                game_active = True #game active devient True
                 #on on passe le snale tout à drote pour pas avoir le bug avec l'écran qui reste jaune
                start_time = int(pygame.time.get_ticks()/1000) #

        if game_active:
            if event.type == obstacle_timer:
                obstacle_groupe.add(Obstacle(choice(['fly', 'snail'])))
                # if random.randint(0, 2): #generer snail ou fly aléatoirement
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright=(random.randint(900, 1100), 300))) #snail
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright=(random.randint(900, 1100), 210))) #fly

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]



    if game_active:
        screen.blit(ground_surface, (0, 300))
        screen.blit(sky_surface, (0, 0))
        # pygame.draw.rect(screen, pygame.Color("#c0e8ec"), score_rect)
        # pygame.draw.rect(screen, pygame.Color("#c0e8ec"), score_rect, border_radius=10)
        # screen.blit(score_surf, score_rect)
        display_score()
        score = display_score()#ce que la fonction display_score() return

        # snail_rect.x -= 6  l'ancien methode pour faire  bouger les snails
        # if snail_rect.right < 0: snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)
        player.draw(screen) #on dessine le group "player" contenant le sprit player
        obstacle_groupe.draw(screen)
        obstacle_groupe.update()
        player.update()


        #obstacle_movement
        obstacle_movement(obstacle_rect_list)


        #collision
        game_active = collisions(player_rect, obstacle_rect_list)


    else: #si game_active == False / si on est dans la page d'acceuil
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect) #on rajoute le player_stand_surf au screen grace à son rect
        obstacle_rect_list.clear() #supprime le contenu de cette liste
        player_rect.midbottom = (80, -100)

        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message, game_message_rect) #affiche le message "tap to run"
        else:screen.blit(score_message, score_message_rect) #si le score >0 , affiche le score

    pygame.display.update()
    clock.tick(60)




# on a refait le jeux avec object oriented
# on doit maintenant gerer les collisions





