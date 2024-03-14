import pygame

from src.dialog import DialogBox
from player import Player
from src.map import MapManager

pygame.init()


class Game:
    def __init__(self):
        # display the window
        self.show_rules = True
        self.typewriter_timer = pygame.time.get_ticks()  # Timer for typewriter effect
        self.typewriter_delay = 50  # Delay between each letter (in milliseconds)
        self.typewriter_index = 0

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("PyGamon - Adventure")

        self.player = Player(dialog_player={"paul": {"A": ["Player : Do nothing"],
                                                     "B": ["Player : Remove the fake new"],
                                                     "C": ["Player : Remove and report the fake news"]},

                                            "boss": {"A": ["Player : Keep the post"],
                                                     "B": ["Player : Keep the post and report the fact that the ",
                                                           "person tried to hide the truth"],
                                                     "C": ["Player : Delete the “fake news"]},
                                            "axel": {"A": ["Player : Keep the post as nobody can know it"],
                                                     "B": ["Player : Remove the post"],
                                                     "C": ["Player : Delete the post and ",
                                                           "fire the employee for stupidity"]},
                                            "ephraim": {"A": ["Player : Post  the information immediately"],
                                                        "B": ["Player : Verify and post",
                                                              ],
                                                        "C": ["Player : Do nothing"]},
                                            "florian": {"A": ["Player :You keep his posts because it’s fun"],
                                                        "B": ["Player : You delete his posts and report them ",
                                                              "to prevent problems"],
                                                        "C": ["Player : You fire the employee, ",
                                                              "and delete and report all his posts"]},
                                            "asser": {"A": ["Player : You can take the decision to report the fact"],
                                                      "B": ["Player : You can take the decision to not report the fact"
                                                            ],
                                                      "C": ["Player : Publish to make fun of the creator"]},
                                            "donovan": {"A": ["Player : Publish the information"],
                                                        "B": ["Player : Publish the information"],
                                                        "C": ["Player : Do nothing"]},
                                            "chasseur": {"A": ["Player : Publish the exclusive news and ",
                                                               "be the first company to talk about the news "],
                                                         "B": ["Player : Try to verify the news first but ",
                                                               "you’re risking to lose the exclusivity"],
                                                         "C": ["Player : Do Nothing"]},
                                            "pilou": {"A": ["Player : Do nothing"],
                                                      "B": ["Player : Fire Both of them. "],
                                                      "C": ["Player : Establish clear and strict guidelines/protocols ",
                                                            "for handling dubious information ",
                                                            "that balance transparency ",
                                                            "with sensitivity to potential consequences"]},
                                            "pixou": {"A": ["Player : Take down the clickbaiting headlines"],
                                                      "B": ["Player : Leave the articles to gain more interactions "],
                                                      "C": ["Player : Train your algorithm to detect ",
                                                            "and delete those headlines"]},
                                            "jack": {"A": ["Player : Do a post about the scandals"],
                                                     "B": ["Player : Find some interesting good news ",
                                                           "about the player to post"],
                                                     "C": ["Player : Decline his request"]},
                                            "benedict": {"A": ["Player : Keep the poInform users.",
                                                               " Implement strict privacy measures such as ",
                                                               "anonymization and encryption to protect user data ",
                                                               "while utilizing the AI technology."],
                                                         "B": [
                                                             "Player : Use it without informing anyone to gain money "],
                                                         "C": ["Player : Explore alternative methods that ",
                                                               "do not compromise user privacy, ",
                                                               "even if it means sacrificing some efficiency ",
                                                               "in fake news detection. "]}},

                             max_user_growth=100, max_ad_revenue=100,
                             max_team_morale=100)

        self.map_manager = MapManager(self.screen, player=self.player)
        self.dialog_box = DialogBox()

        self.rules_text = """
                Welcome to PyGamon!\n
                * Use arrow keys to move your player around the map.\n
                * Interact with NPCs (represented as characters) by pressing the space key when near them.\n
                * Choose your response options (A, B, or C) using the corresponding keys (A, B, C).\n
                * Your choices will affect your game metrics (user growth, ad revenue, team morale).\n
                * Navigate through the map and fulfill challenges to progress.\n
                Have fun!
                """

        # Create a temporary surface for displaying the rules (optional, adjust dimensions)
        self.rules_surface = pygame.Surface((600, 400))
        self.rules_surface.fill((255, 255, 255))  # White background
        self.rules_display_timer = 3000  # Time to display rules (milliseconds)
        self.render_rules(screen=self.screen)

        self.show_score = False
        self.score_surface = pygame.Surface((600, 400))
        self.score_text = "Your Score: \n\n"
        self.score_font = pygame.font.Font("dialog/dialog_font.ttf", 16)

    def render_score(self, screen):
        score_box = pygame.Surface((700, 100))
        score_box.fill((255, 255, 255))  # White background
        score_box_rect = score_box.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        screen.blit(score_box, score_box_rect)

        score_lines = self.score_text.split("\n")  # Split the score text here
        y_offset = 20  # Initial y offset for first line
        for line in score_lines:
            text_surface = self.score_font.render(line, True, (0, 0, 0))  # Black color
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, score_box_rect.top + y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 30  # Adjust for next line

    def display_score(self):
        unvisited_npcs = [npc_name for npc_name in
                          ["axel", "ephraim", "asser", "pilou", "paul", "boss", "pixou", "jack", "chasseur", "florian",
                           "benedict", "donovan"]
                          if not self.player.has_talked_to_npc(npc_name)]

        if unvisited_npcs:
            self.score_text = f"You haven't talked to the following NPCs yet:\n"
            for npc_name in unvisited_npcs:
                self.score_text += f"- {npc_name}\n"
            self.score_text += "\n"

        total_score = self.player.current_user_growth + self.player.current_ad_revenue + self.player.current_team_morale

        self.score_text += f"Your Score: {total_score}\n\n"
        self.score_text += "Comments:\n"
        self.score_text += "Comment 1\n"
        self.score_text += "Comment 2\n"
        self.show_score = True

    def render_rules(self, screen):
        # Define the position and size of the white box
        box_width = 600
        box_height = 400
        box_x = (screen.get_width() - box_width) // 2
        box_y = (screen.get_height() - box_height) // 2

        # Render the white box onto the screen
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height))

        # Render the rules text with typewriter effect
        if pygame.time.get_ticks() - self.typewriter_timer > self.typewriter_delay:
            self.typewriter_timer = pygame.time.get_ticks()
            if self.typewriter_index < len(self.rules_text):
                self.typewriter_index += 1

        text_to_render = self.rules_text[:self.typewriter_index]

        # Render the rules text onto the white box
        font = pygame.font.Font("dialog/dialog_font.ttf", 12)  # Replace with your desired font
        text_lines = self.wrap_text(font, text_to_render, box_width - 20)  # Wrap text to fit within the box
        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(midtop=(box_x + box_width // 2, box_y + 30 + i * 20))
            screen.blit(text_surface, text_rect)

    def wrap_text(self, font, text, max_width):
        """Wrap text to fit within a maximum width."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = ''
        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            width, _ = font.size(test_line)
            if width <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word
        if current_line:
            wrapped_lines.append(current_line)
        return wrapped_lines

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_SPACE]:
            if self.show_rules:
                self.show_rules = False
            elif self.show_score:
                pygame.quit()
        elif pressed[pygame.K_0]:
            self.display_score()

    def update(self):
        self.map_manager.update()

    def run(self):

        clock = pygame.time.Clock()
        # Game loop
        running = True
        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.player.draw_metrics_bar(self.screen)
            self.dialog_box.render(self.screen)
            if self.show_rules:
                self.render_rules(screen=self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)
                        print("Succesfully choice from Game")
                        self.player.draw_metrics_bar(self.screen)
                        print("Succesfully drawed from Playe.draw_metrics")
                    elif event.key == pygame.K_a:
                        self.map_manager.check_npc_collisions(self.dialog_box, choice="A")
                        print("Succesfully choice from Game")
                        self.player.draw_metrics_bar(self.screen)
                        print("Succesfully drawed from Playe.draw_metrics")
                    elif event.key == pygame.K_b:
                        self.map_manager.check_npc_collisions(self.dialog_box, choice="B")
                        print("Succesfully choice from Game")
                        self.player.draw_metrics_bar(self.screen)
                        print("Succesfully drawed from Playe.draw_metrics")
                    elif event.key == pygame.K_c:
                        self.map_manager.check_npc_collisions(self.dialog_box, choice="C")
                        print("Succesfully choice from Game")
                        self.player.draw_metrics_bar(self.screen)
                        print("Succesfully drawed from Playe.draw_metrics")
                if self.show_score:
                    self.render_score(self.screen)

            clock.tick(60)

        pygame.quit()
