from field import Field
import pygame
import random as ra
import math

class Board:
    def __init__(self, screen, mouse, game_size, bomb_count, number_photos):
        self.screen = screen
        self.mouse = mouse

        self.game_ended = False

        self.restart_game = False

        self.flag_clicked = True

        self.game_size = game_size
        field_count = game_size**2

        self.fields = []

        self.height = (self.screen.get_height()  - game_size - 1) / game_size
        self.width = (self.screen.get_width() - game_size - 1) / game_size

        next_x = 0
        next_y = 0

        for i in range(field_count):

            temp_x = next_x
            temp_y = next_y

            self.fields.append(Field(self.screen, number_photos, temp_x, temp_y, self.width, self.height))

            if ((i + 1) % game_size) == 0:
                next_x = 0
                next_y += (self.height + 1)
            else:
                next_x += (self.width + 1)
        
        bomb_indicies = []

        for i in range(bomb_count):

            temp = 0
            while True:
                temp = ra.randint(0, field_count - 1)

                if temp in bomb_indicies:
                    temp = ra.randint(0, field_count - 1)
                else:
                    break

            bomb_indicies.append(temp)
            self.fields[temp].bomb = True

        def increment_spaces_around(active_field):
            active_field += 1

            close_left = False
            close_top = False
            close_bottom = False
            close_right = False

            if active_field == 1 or ((active_field - 1) % self.game_size == 0):
                close_left = True
            
            if active_field % self.game_size == 0:
                close_right = True
            
            if active_field <= self.game_size - 1:
                close_top = True
            
            if active_field >= (self.game_size**2 - self.game_size + 1):
                close_bottom = True
            
            active_field -= 1
            # Finding relative fields
            nearby_fields = []
            for i in range(3):
                nearby_fields.append(active_field - self.game_size - 1 + i)
            
            nearby_fields.append(active_field - 1)
            nearby_fields.append(active_field + 1)
            
            for i in range(3):
                nearby_fields.append(active_field + self.game_size - 1 + i)
            
            if close_top:
                nearby_fields[0] = -31
                nearby_fields[1] = -31
                nearby_fields[2] = -31
            
            if close_bottom:
                nearby_fields[5] = -31
                nearby_fields[6] = -31
                nearby_fields[7] = -31

            if close_left:
                nearby_fields[0] = -31
                nearby_fields[3] = -31
                nearby_fields[5] = -31
            
            if close_right:
                nearby_fields[2] = -31
                nearby_fields[4] = -31
                nearby_fields[7] = -31
            
            for i in nearby_fields:
                if i == -31:
                    continue

                self.fields[i].increase_bombs_near()
        
        for i in bomb_indicies:
            increment_spaces_around(i)
        




    def draw(self):

        width_count = math.floor(self.mouse.get_pos()[0] / (self.width + 1))
        height_count = math.floor(self.mouse.get_pos()[1] / (self.height + 1))

        hovered_field = min(self.game_size**2 - 1, max(0, height_count * self.game_size + width_count))

        self.fields[hovered_field].hovering = True

        def show_spaces_around(active_field):
            active_field += 1

            close_left = False
            close_top = False
            close_bottom = False
            close_right = False

            if active_field == 1 or ((active_field - 1) % self.game_size == 0):
                close_left = True
            
            if active_field % self.game_size == 0:
                close_right = True
            
            if active_field <= self.game_size:
                close_top = True
            
            if active_field >= (self.game_size**2 - self.game_size):
                close_bottom = True
            
            active_field -= 1

            nearby_fields = []
            for i in range(3):
                nearby_fields.append(active_field - self.game_size - 1 + i)
            
            nearby_fields.append(active_field - 1)
            nearby_fields.append(active_field + 1)
            
            for i in range(3):
                nearby_fields.append(active_field + self.game_size - 1 + i)
            
            if close_top:
                nearby_fields[0] = -31
                nearby_fields[1] = -31
                nearby_fields[2] = -31
            
            if close_bottom:
                nearby_fields[5] = -31
                nearby_fields[6] = -31
                nearby_fields[7] = -31

            if close_left:
                nearby_fields[0] = -31
                nearby_fields[3] = -31
                nearby_fields[5] = -31
            
            if close_right:
                nearby_fields[2] = -31
                nearby_fields[4] = -31
                nearby_fields[7] = -31
            
            for i in nearby_fields:
                if i == -31:
                    continue
                
                if self.fields[i].clicked or self.fields[i].bomb:
                    continue

                if self.fields[i].bombs_near > 0:
                    self.fields[i].clicked = True
                    continue

                self.fields[i].clicked = True
                show_spaces_around(i)
        if not self.game_ended:
            if self.mouse.get_pressed(3)[0]:
                if not self.fields[hovered_field].clicked:
                    self.fields[hovered_field].clicked = True

                    if self.fields[hovered_field].bomb:
                        self.game_ended = True

                        self.restart_game = False
                        for i in self.fields:
                            if not (i.flag_active and i.bomb):
                                i.clicked = True


                    if self.fields[hovered_field].bomb == False and self.fields[hovered_field].bombs_near == 0:
                        show_spaces_around(hovered_field)
            
            if self.mouse.get_pressed(3)[2] and not self.flag_clicked:
                self.fields[hovered_field].flag_active = not self.fields[hovered_field].flag_active
                self.flag_clicked = True

            if not self.mouse.get_pressed(3)[2]:
                self.flag_clicked = False
        else:
            if self.mouse.get_pressed(3)[2]:
                self.restart_game = True

        for field in self.fields:
            field.draw()




