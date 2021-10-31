import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

# Define the width and height of the window, change the title.
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders by: MiguelFocus")

# Colors whe're gonna use
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create SOunds
BULLETS_HIT_SOUND = pygame.mixer.Sound('Porfolio Space INvaders/Assets/explosion.wav')
BULLETS_HIT_SOUND.set_volume(0.3)
BULLET_FIRE_SOUND = pygame.mixer.Sound('Porfolio Space INvaders/Assets/shoot.wav')
# Change Font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Game constants.
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 50
ALIEN_WIDTH, ALIEN_HEIGHT = 50, 25
BOUNCE = 0

# Pygame events
ALIEN_HIT = pygame.USEREVENT + 1

# Create Player Spaceship and reescale it.
PLAYER_SPACESHIP = pygame.image.load(os.path.join(os.path.expanduser('~'),
    'Desktop', 'Python Projects', 'Porfolio Space INvaders', 
    'Assets', 'player_spaceship.png'))
PLAYER_SPACESHIP = pygame.transform.scale(PLAYER_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
# Create Aliens and reescale them.
ALIEN_SPACESHIP = pygame.image.load(os.path.join(os.path.expanduser('~'),
    'Desktop', 'Python Projects', 'Porfolio Space INvaders', 
    'Assets', 'aliens.png'))
ALIEN_SPACESHIP = pygame.transform.scale(ALIEN_SPACESHIP, (ALIEN_WIDTH, ALIEN_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join(os.path.expanduser('~'),
    'Desktop', 'Python Projects', 'Porfolio Space INvaders', 
    'Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(player, aliens, bullets, alien_bullets, player_health):
    # Draws everithing on the window
    WIN.blit(SPACE, (0, 0))
    # Draws player health
    player_health_text = HEALTH_FONT.render(
        "Health: " + str(player_health), 1, WHITE)
    WIN.blit(player_health_text,
     (WIDTH - player_health_text.get_width() - 10, 10))
    # Draws player spaceship
    WIN.blit(PLAYER_SPACESHIP, (player.x, player.y))
    # Draws aliens
    for alien in aliens:
        WIN.blit(ALIEN_SPACESHIP, (alien.x, alien.y))
    # Draws bullets
    for bullet in bullets:
        pygame.draw.rect(WIN, WHITE, bullet)
    # Draws alien bullets
    for alien_bullet in alien_bullets:
        pygame.draw.rect(WIN, RED, alien_bullet)

    pygame.display.update()


def player_movement(keys_pressed, player):
        if keys_pressed[pygame.K_a] and player.x > 0: # LEFT
            player.x -= VEL
        if keys_pressed[pygame.K_d] and player.x < 726: # RIGHT
            player.x += VEL


def create_aliens():
    # Create Aliens
    aliens = []
    alien_space_x = 0
    alien_space_y = 0
    for n in range(0, 5):
        for n in range(0, 8):
            alien = pygame.Rect((150+alien_space_x), (60+alien_space_y),
            ALIEN_WIDTH, ALIEN_HEIGHT)
            alien_space_x += 60
            aliens.append(alien) 
        alien_space_x = 0 
        alien_space_y += 50    
    return aliens


def move_aliens(aliens):
    # Move and bounce the aliens
    global BOUNCE
    for alien in aliens:
        if alien.x > 0 and BOUNCE %2 == 0:
            alien.x -= 1
            if alien.x <= 0:
                BOUNCE += 1
        elif alien.x <= 750 and BOUNCE %2 != 0:
            alien.x += 1
            if alien.x >= 750:
                BOUNCE -= 1


def handle_player_bullets(player, player_bullets, aliens, alien_bullets):
    # Makes the bullets move and detect collision between bullets and aliens.
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        for alien in aliens:
            if alien.colliderect(bullet):
                aliens.remove(alien)
                player_bullets.remove(bullet)
                BULLETS_HIT_SOUND.play()
                
        if bullet.y < 0:
            print(bullet)
            player_bullets.remove(bullet)
            

    for alien_bullet in alien_bullets:
        alien_bullet.y += BULLET_VEL
        if player.colliderect(alien_bullet):
            pygame.event.post(pygame.event.Event(ALIEN_HIT))
            alien_bullets.remove(alien_bullet)


def handle_alien_bullets(aliens):
    # Creates bullet from a random alien
    random_alien = random.choice(aliens)
    bullet = pygame.Rect(random_alien.x +  random_alien.width//2 - 2,
            random_alien.y + random_alien.height, 5, 10)

    return bullet


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2,
                         HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():
    timer = 0
    player = pygame.Rect(365, 730, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    player_health = 5

    aliens = create_aliens()
    player_bullets = []
    alien_bullets = []

    clock = pygame.time.Clock()
    run = True
    # Start main loop of the aplication.
    while run:
        clock.tick(FPS)
        # Checks when the app is closed.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                # Create bullets if space is pressed
                if event.key == pygame.K_SPACE and len(player_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x +  player.width//2 - 2,
                        player.y - player.height, 5, 10)
                    player_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    

            if event.type == ALIEN_HIT:
                player_health -= 1
                BULLETS_HIT_SOUND.play()

        winner_text = ""
        if player_health <= 0:
            winner_text = "You lose"
            run = False
        
        if len(aliens) <= 0:
            winner_text = "You win"
            run = False

        if winner_text != "":
            draw_winner(winner_text)
            run = False

        # Make a timer , everytime the timer gets to 50, an alien shots a bullet
        timer += 1
        if timer == 50:
            alien_bullets.append(handle_alien_bullets(aliens))
            timer = 0

        keys_pressed = pygame.key.get_pressed()

        player_movement(keys_pressed, player)
        move_aliens(aliens)

        handle_player_bullets(player, player_bullets, aliens, alien_bullets)

        draw_window(player, aliens, player_bullets, alien_bullets, player_health)
    
    main()

if __name__ == "__main__":
    main()
