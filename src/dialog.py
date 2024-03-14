import pygame


class DialogBox:
    X_POSITION = 60
    Y_POSITION = 470

    def __init__(self):
        self.box = pygame.image.load("dialog/dialog_box.png")
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = []
        self.letter_index = 0
        self.text_index = 0
        self.conversation_index = 0
        self.font = pygame.font.Font("dialog/dialog_font.ttf", 12)
        self.reading = False
        self.conversation = True
        self.player_answer = None
        self.showing_options = False
        self.options = []

    def execute(self, npc_name, dialog_npc=[], dialog_player={}, dialog_consequence={},
                player_answer=None, player=None):

        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog_npc + [f"{key}: {value}" for key, value in dialog_player[npc_name].items()]
        if self.conversation:
            self.player_answer = player_answer
            if self.player_answer is not None:
                # if player has chosen an option, branch the conversation
                self.showing_options = False
                self.reading = True
                self.text_index = 0
                self.texts = dialog_player[npc_name][self.player_answer] + dialog_consequence[self.player_answer][3]

                # UPDATE METRICS

                impact_user_growth = dialog_consequence[self.player_answer][0]
                impact_ad_revenue = dialog_consequence[self.player_answer][1]
                impact_team_morale = dialog_consequence[self.player_answer][2]

                # Update in the player instance
                player.current_user_growth = max(min(player.current_user_growth + impact_user_growth, 100), 0)
                player.current_ad_revenue = max(min(player.current_ad_revenue + impact_ad_revenue, 100), 0)
                player.current_team_morale = max(min(player.current_team_morale + impact_team_morale, 100), 0)

                print("values updated in the player object from DialogBox")
                print("Success !! from DialogBox ")

    def render(self, screen):
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 30))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False  # close the dialog if all text were read
