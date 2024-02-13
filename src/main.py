import pygame
import sys
import csv
from datetime import datetime

# Initialize Pygame and set up the screen
pygame.init()
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Colors and Fonts
background_color = (255, 255, 255)
button_color = (0, 0, 255)
text_color = (255, 255, 255)
font = pygame.font.Font(None, 36)

# Define buttons
start_button = pygame.Rect(screen_width / 2 - 50, screen_height - 100, 100, 50)
choice_rect_left = pygame.Rect(50, 50, 140, 100)
choice_rect_right = pygame.Rect(screen_width - 190, 50, 140, 100)

# Set number of trials
num_trials = 5
current_trial = 0

# CSV setup
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
csv_filename = f"mouse_tracking_data_v2_{timestamp}.csv"
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['trial', 'timestamp', 'mouse_x', 'mouse_y'])

# Record mouse position function
def record_mouse_position(trial_active):
    if trial_active:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        mouse_pos = pygame.mouse.get_pos()
        with open(csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_trial, timestamp, mouse_pos[0], mouse_pos[1]])

# Main function
def main():
    global current_trial
    running = True
    trial_active = False
    while running and current_trial < num_trials:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos) and not trial_active:
                    trial_active = True
                    pygame.time.set_timer(pygame.USEREVENT, 10)  # Set timer to record position every 10ms
                elif (choice_rect_left.collidepoint(mouse_pos) or choice_rect_right.collidepoint(mouse_pos)) and trial_active:
                    record_result('Left' if choice_rect_left.collidepoint(mouse_pos) else 'Right')
                    pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer
                    trial_active = False

        screen.fill(background_color)
        if not trial_active:
            # Draw and display start button
            pygame.draw.rect(screen, button_color, start_button)
            text = font.render('Start', True, text_color)
            screen.blit(text, (start_button.x + 20, start_button.y + 10))
        else:
            # Draw and display choice buttons
            pygame.draw.rect(screen, button_color, choice_rect_left)
            pygame.draw.rect(screen, button_color, choice_rect_right)

            # Calculate the center position for the text "A" within choice_rect_left
            text_left = font.render('A', True, text_color)
            text_left_rect = text_left.get_rect(center=choice_rect_left.center)

            # Calculate the center position for the text "B" within choice_rect_right
            text_right = font.render('B', True, text_color)
            text_right_rect = text_right.get_rect(center=choice_rect_right.center)

            screen.blit(text_left, text_left_rect)
            screen.blit(text_right, text_right_rect)

        pygame.display.flip()

        # Record mouse position if trial is active
        if trial_active:
            record_mouse_position(trial_active)

    pygame.quit()
    sys.exit()

# Function to record result
def record_result(choice):
    global current_trial
    current_trial += 1

if __name__ == '__main__':
    main()