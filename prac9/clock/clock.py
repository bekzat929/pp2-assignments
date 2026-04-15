import pygame
import datetime


class MickeyClock:
    def __init__(self, screen, background_path, right_hand_path, left_hand_path):
        self.screen = screen
        self.background = pygame.image.load(background_path).convert_alpha()
        self.right_hand = pygame.image.load(right_hand_path).convert_alpha()
        self.left_hand = pygame.image.load(left_hand_path).convert_alpha()

        self.center = (self.background.get_width() // 2, self.background.get_height() // 2)

    def get_time_angles(self):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

    
        minute_angle = -(minutes * 6)
        second_angle = -(seconds * 6)

        return minute_angle, second_angle

    def draw_rotated_hand(self, hand_image, angle):
        rotated_image = pygame.transform.rotate(hand_image, angle)
        rect = rotated_image.get_rect(center=self.center)
        self.screen.blit(rotated_image, rect)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        minute_angle, second_angle = self.get_time_angles()

        
        self.draw_rotated_hand(self.right_hand, minute_angle)

        
        self.draw_rotated_hand(self.left_hand, second_angle)