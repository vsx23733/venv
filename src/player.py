import pygame
from animation import AnimateSprite


class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey(0, 0)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.interacted_npcs = set()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def interact_with_npc(self, npc_name):
        self.interacted_npcs.add(npc_name)

    def has_talked_to_npc(self, npc_name):
        return npc_name in self.interacted_npcs

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self):
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self):
        self.change_animation("left")
        self.position[0] -= self.speed

    def move_up(self):
        self.change_animation("up")
        self.position[1] -= self.speed

    def move_down(self):
        self.change_animation("down")
        self.position[1] += self.speed

    def update(self) -> None:
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image


class Player(Entity):

    def __init__(self, dialog_player, max_user_growth, max_ad_revenue,
                 max_team_morale):
        super().__init__("robin", 0, 0)
        self.dialog_player = dialog_player
        self.max_user_growth = max_user_growth
        self.current_user_growth = max_user_growth
        self.max_ad_revenue = max_ad_revenue
        self.current_ad_revenue = max_ad_revenue
        self.max_team_morale = max_team_morale
        self.current_team_morale = max_team_morale

    def draw_metrics_bar(self, screen):
        # DEFINE BAR PROPERTIES

        # popularity
        user_growth_bar_width = 100
        user_growth_bar_height = 20
        user_growth_bar_x = 10
        user_growth_bar_y = 70

        # revenue
        ad_revenue_bar_width = 100
        ad_revenue_bar_height = 20
        ad_revenue_bar_x = 10
        ad_revenue_bar_y = 95

        # Team morale
        team_morale_bar_width = 100
        team_morale_bar_height = 20
        team_morale_bar_x = 10
        team_morale_bar_y = 120

        # Font
        font = pygame.font.Font("dialog/dialog_font.ttf", 12)

        # Text for each bar
        text_color = (3, 79, 255)

        # POPULARITY BAR
        user_growth_text_offset_x = 5
        user_growth_text_offset_y = 2.5

        # REVENUE BAR
        ad_revenue_text_offset_x = 5
        ad_revenue_text_offset_y = 2.5

        # TEAM MORALE BAR
        team_morale_text_offset_x = 5
        team_morale_text_offset_y = 2.5

        # CALCULATE RATIOS
        user_growth_ratio = self.current_user_growth / self.max_user_growth
        ad_revenue_ratio = self.current_ad_revenue / self.max_ad_revenue
        team_morale_ratio = self.current_team_morale / self.max_team_morale

        # DRAW BAR

        # POPULARITY BAR
        # Draw user growth bar background
        pygame.draw.rect(screen, (200, 0, 0), (user_growth_bar_x, user_growth_bar_y,
                                               user_growth_bar_width,
                                               user_growth_bar_height),
                         border_radius=10)

        # Draw user growth bar fill
        fill_width = int(user_growth_ratio * user_growth_bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (user_growth_bar_x, user_growth_bar_y, fill_width,
                                               user_growth_bar_height),
                         border_radius=10)

        # REVENUE BAR
        # Draw ad revenue bar background
        pygame.draw.rect(screen, (200, 0, 0), (ad_revenue_bar_x, ad_revenue_bar_y,
                                               ad_revenue_bar_width,
                                               ad_revenue_bar_height),
                         border_radius=10)

        # Draw ad revenue bar fill
        fill_width = int(ad_revenue_ratio * ad_revenue_bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (ad_revenue_bar_x, ad_revenue_bar_y, fill_width,
                                               ad_revenue_bar_height),
                         border_radius=10)

        # TEAM MORALE
        # Draw team morale bar background
        pygame.draw.rect(screen, (200, 0, 0), (team_morale_bar_x, team_morale_bar_y,
                                               team_morale_bar_width,
                                               team_morale_bar_height),
                         border_radius=10)

        # Draw team morale bar fill
        fill_width = int(team_morale_ratio * team_morale_bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (team_morale_bar_x, team_morale_bar_y, fill_width,
                                               team_morale_bar_height),
                         border_radius=10)

        # Text

        # USER GROWTH
        user_growth_text = "USER GROWTH"
        user_growth_text_surface = font.render(user_growth_text, True, text_color)

        user_growth_text_height = user_growth_text_surface.get_height()
        user_growth_text_width = user_growth_text_surface.get_width()

        user_growth_text_x = user_growth_bar_x + user_growth_bar_width + user_growth_text_offset_x
        user_growth_text_y = user_growth_bar_y + (user_growth_bar_height -
                                                          user_growth_text_height) // 2

        screen.blit(user_growth_text_surface, (user_growth_text_x, user_growth_text_y))

        # REVENUE
        ad_revenue_text = "AD REVENUE"
        ad_revenue_text_surface = font.render(user_growth_text, True, text_color)

        ad_revenue_text_height = ad_revenue_text_surface.get_height()
        ad_revenue_text_width = ad_revenue_text_surface.get_width()

        ad_revenue_text_x = ad_revenue_bar_x + ad_revenue_bar_width + ad_revenue_text_offset_x
        ad_revenue_text_y = ad_revenue_bar_y + (ad_revenue_bar_height -
                                                ad_revenue_text_height) // 2

        screen.blit(ad_revenue_text_surface, (ad_revenue_text_x, ad_revenue_text_y))

        # TEAM MORALE
        team_morale_text = "TEAM MORALE"
        team_morale_text_surface = font.render(team_morale_text, True, text_color)

        team_morale_text_height = team_morale_text_surface.get_height()
        team_morale_text_width = team_morale_text_surface.get_width()

        team_morale_text_x = team_morale_bar_x + team_morale_bar_width + team_morale_text_offset_x
        team_morale_text_y = team_morale_bar_y + (team_morale_bar_height -
                                                  team_morale_text_height) // 2

        screen.blit(team_morale_text_surface, (team_morale_text_x, team_morale_text_y))


class NPC(Entity):

    def __init__(self, name, nb_points, npc_texts, dialog_consequence):
        super().__init__(name, 0, 0)
        self.dialog = npc_texts
        self.nb_points = nb_points
        self.points = []
        self.name = name
        self.current_point = 0
        self.dialog_consequence = dialog_consequence

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 2:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 2:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 2:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 2:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
