import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Map dimensions
MAP_WIDTH = 6000
MAP_HEIGHT = 640

# Colors
WHITE = (255, 255, 255)

# Speed
FLYAH_SPEED = 5

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flyah")

# Load map image from folder
map_image_path = os.path.join("assets", "tilemap.png")  # Change "maps" to your folder path
map_image = pygame.image.load(map_image_path).convert()

# Character movement variables
move_x = 0
move_y = 0
gravity = 0.5
jump_speed = -10
is_jumping = False

# Character animation
animation_frames = []
current_frame_index = 0
animation_timer = 0
animation_delay = 100  # milliseconds delay between each frame
animation_path_left = "assets/red_hood/left"  # Path to your animation frames
animation_path_right = "assets/red_hood/right"  # Path to your animation frames

# Load animation frames
for i in range(1, 26):  # Assuming you have 25 frames
    frame_path_left = os.path.join(animation_path_left, f"red_hood{i}.png")
    frame_path_right = os.path.join(animation_path_right, f"red_hood{i}.png")
    frame_left = pygame.image.load(frame_path_left).convert_alpha()
    frame_right = pygame.image.load(frame_path_right).convert_alpha()
    # Resize frames to shorter height
    new_height = 70  # Adjust this value to your desired height
    frame_left = pygame.transform.scale(frame_left, (int(frame_left.get_width() * (new_height / frame_left.get_height())), new_height))
    frame_right = pygame.transform.scale(frame_right, (int(frame_right.get_width() * (new_height / frame_right.get_height())), new_height))
    animation_frames.append({
        'left': frame_left,
        'right': frame_right
    })

# Character starting position
character_rect = animation_frames[0]['left'].get_rect()
character_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Viewport position
viewport_x = 0
viewport_y = 0

# Last facing direction (initially left)
last_facing_direction = 'left'

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                move_y = jump_speed  # Start the jump
                is_jumping = True

    # Get user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_x = -FLYAH_SPEED
        animation_timer += pygame.time.get_ticks() - animation_timer
        if animation_timer >= animation_delay:
            animation_timer = 0
            current_frame_index = (current_frame_index + 1) % len(animation_frames)
        last_facing_direction = 'left'
    elif keys[pygame.K_RIGHT]:
        move_x = FLYAH_SPEED
        animation_timer += pygame.time.get_ticks() - animation_timer
        if animation_timer >= animation_delay:
            animation_timer = 0
            current_frame_index = (current_frame_index + 1) % len(animation_frames)
        last_facing_direction = 'right'
    else:
        move_x = 0
        current_frame_index = 0  # Reset animation to the first frame when no movement keys are pressed

    # Apply gravity
    move_y += gravity

    # Update character position
    character_rect.move_ip(move_x, move_y)

    # Adjust the viewport to keep the character centered until it reaches the screen edges
    viewport_x += move_x

    # Ensure the viewport stays within the map boundaries
    viewport_x = max(0, min(viewport_x, MAP_WIDTH - SCREEN_WIDTH))

    # Check if the character is colliding with the ground
    if character_rect.bottom >= MAP_HEIGHT:
        character_rect.bottom = MAP_HEIGHT
        move_y = 0  # Stop vertical movement when on the ground
        is_jumping = False  # Reset jump flag when on the ground

    # Draw
    screen.fill(WHITE)
    screen.blit(map_image, (-viewport_x, -viewport_y))  # Draw the map with the viewport adjustments
    if move_x < 0:
        screen.blit(animation_frames[current_frame_index]['left'], (character_rect.x - viewport_x, character_rect.y - viewport_y))
    elif move_x > 0:
        screen.blit(animation_frames[current_frame_index]['right'], (character_rect.x - viewport_x, character_rect.y - viewport_y))
    else:
        # If not moving, display the first frame facing the last direction
        if last_facing_direction == 'left':
            screen.blit(animation_frames[0]['left'], (character_rect.x - viewport_x, character_rect.y - viewport_y))
        else:
            screen.blit(animation_frames[0]['right'], (character_rect.x - viewport_x, character_rect.y - viewport_y))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
