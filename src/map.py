from dataclasses import dataclass

import pygame
import pyscroll
import pytmx

from src.player import NPC
from src.dialog import DialogBox


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]


class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()  # "house" : Map("house, "walls", "group")
        self.current_map = "world"
        self.screen = screen
        self.player = player
        self.dialog_count = 0

        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house", target_world="house",
                   teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2",
                   teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_dungeon", target_world="dungeon",
                   teleport_point="spawn_dungeon")
        ], npcs=[
            NPC("paul", nb_points=4, npc_texts=["A user sends an email to report that one of our publications ",
                                                "on a news is in fact a fake news AI-generated to damage severely ",
                                                "her reputation. We don't have enough information to know if this is ",
                                                "the truth or not but the person in question insists that it ",
                                                "should be deleted.", "What should we do ?"],
                dialog_consequence={
                    'A': [-15, -10, -10, ["Paul : The user killed himself, ",
                                          "we got sued,",
                                          "jost subscribers, ",
                                          "the media and population are complaining about our lack of action."]],
                    'B': [0, 0, 10, ["Paul : The user is happy that we removed the fake news, nobody knows about it"]],
                    'C': [-10, 10, 10, ["Paul : It cost a bit of money, ",
                                        "user is happy that we removed the fake news and ",
                                        "explained by media the misunderstanding, people liked your initiative"]]}),
            NPC("asser", nb_points=4, npc_texts=["A popular newspaper uses AI for its posts (image, text …) and ",
                                                 "has never mentioned it.", "Taking into account the reputation "
                                                                            "of that newspaper ,",
                                                 "should we report the use of ",
                                                 "generative AI for images ",
                                                 "for the posts of the newspaper ?"],
                dialog_consequence={
                    'A': [5, 10, 5, ["Asser : We gained popularity (and money) as the ",
                                     "other newspaper lost popularity and trust of his subscribers."]],
                    'B': [0, 0, -5, ["Asser : Nobody actually knows about it but it’ll be known for sure. ",
                                     "Employees are disappointed with your decisions."]],
                    'C': [0, 0, 0, ["Asser : Hum you're weird"]]}),
            NPC("ephraim", nb_points=2, npc_texts=[" A guy hears something on tiktok and wants us to publish it "
                                                   "without verifying it because the tiktok account is well known.",
                                                   "Should we decide to put the information in the newspaper without "
                                                   "verifying it because of the notoriety of the sourcer ?"],
                dialog_consequence={
                    'A': [10, -10, -10, ["Ephraim :  You decide to post it immediately without",
                                         "knowing if it’s true or false",
                                         "We lose our credibility and nobody will trust us post anymore"]],
                    'B': [5, 10, 8, ["Ephraim : We are becoming more credible because ",
                                     "our post will only provide the good information."]],
                    'C': [0, -5, 0, ["Ephraim : You decided to do anything. It is awful for",
                                     "us because we may lose part of our community"]]}),
            NPC("axel", nb_points=4, npc_texts=["A user sends an email to report that one of our publications ",
                                                "on a news is in fact a fake news AI-generated to damage severely",
                                                "her reputation. We don't have enough information to know if this is",
                                                "the truth or not but the person in question insists that it ",
                                                "should be deleted.", "You’re in a position where no one can have "
                                                                      "the possibility ",
                                                "to know that you published fake news. ",
                                                "Otherwise, you can keep the claimed glory ",
                                                "if you don’t delete the post. ",
                                                "What will you do ? "],
                dialog_consequence={
                    'A': [5, 0, -15, ["Axel : Nobody knows about that incident but employees ",
                                      "are really disappointed with your decision"
                                      ]],
                    'B': [0, 0, 5, ["Axel :Nobody knows about the incident but employees liked your decision",
                                    "our post will only provide the good information."]],
                    'C': [0, 0, -5, ["Axel : Nobody knows about the incident and the employee got fired. ",
                                     "Some employees think your decision is unfair"]]})

        ])
        self.register_map("house", portals=[
            Portal(from_world="house", origin_point="exit_house", target_world="world",
                   teleport_point="enter_house_exit")], npcs=[
            NPC("florian", nb_points=2, npc_texts=["An employee enjoys publishing fake news, arguing that the ",
                                                   "humor / sarcasm is easily perceptible", " How do you evaluate and ",
                                                   "react to the publication ",
                                                   "of these fake news ? "],
                dialog_consequence={
                    'A': [-15, 10, 5, ["Florian : People actually take his post seriously ",
                                       "(and don’t even find it funny). ",
                                       "We got sued for massive propagation of fake news"]],
                    'B': [-5, -5, 10, ["Florian : It cost a bit of money but people like the fact that ",
                                       "we clarified the post and apologized"]],
                    'C': [-5, -5, 5, ["Florian : It cost a bit of money but people like the fact that ",
                                      "we clarified the post and apologized. ",
                                      "Some Employees find your decision unfair (they must have liked his jokes)"]]
                }),
            NPC("donovan", nb_points=4, npc_texts=[" We receive an e-mail from a well-known creator who wants ",
                                                   "to denounce a children's series loved by everyone ",
                                                   "that has scenes deemed to be non-conforming. ",
                                                   " How will you react, when you received that information ?"],
                dialog_consequence={
                    'A': [5, 10, -5, ["Donovan :  The post about the creator went viral, ",
                                      "people really love this kind of post ",
                                      "but the creator is being harassed for it."]],
                    'B': [5, -10, -5, ["Donovan :  We earn a bit of money. The post went negatively viral. ",
                                       "People found our post totally nonsense and started unsubscribing as ",
                                       "“We started sharing anything”."]],
                    'C': [0, 0, 0, ["Donovan : Nobody knows about the demand …"]]})
        ])

        self.register_map("house2", portals=[
            Portal(from_world="house2", origin_point="exit_house", target_world="world", teleport_point="exit_house2")
        ], npcs=[
            NPC("chasseur", nb_points=2, npc_texts=["You got a call from a friend telling ",
                                                    "you shocking news that is not verified about ",
                                                    "a really well known person", "What would you do?"],
                dialog_consequence={
                    'A': [-20, -10, -10, ["Chasseur : We got sued by the celebrity and they are asking for whoever ",
                                          "published this news because it was a fake news. "
                                          "Try to verify the news first but you’re risking to lose the exclusivity"]],
                    'B': [5, 15, 10, ["Chasseur : Great work! We have built a great relationship with ",
                                      "the celebrity and we got some free marketing."]],
                    'C': [0, 0, 0, ["Chasseur : Comments"]]}),
            NPC("jack", nb_points=2, npc_texts=["You got a call from a player’s agent asking you to talk more about ",
                                                "his player in order to gain more fame and ",
                                                "to increase his transfer fees. ",
                                                "This player is in many scandals that are true.",
                                                "What would you do ?"],
                dialog_consequence={
                    'A': [-50, 15, 10, ["Jack : Great moral, but we got in some issues with the player and ",
                                        "his agent because we harmed the player’s career prospect "]],
                    'B': [15, -15, -15, ["Jack : Not a bad choice, "
                                         "Might prevent conflicts with the player and ",
                                         "their agent by fostering a positive image."]],
                    'C': [0, 5, 10, ["Jack : Great Work! Could prevent issues with the player ",
                                     "and their agent by avoiding harmful actions"]]})
        ])
        self.register_map("dungeon", portals=[
            Portal(from_world="dungeon", origin_point="exit_dungeon", target_world="world",
                   teleport_point="dungeon_exit_spawn")
        ], npcs=[
            NPC("boss", nb_points=2, npc_texts=["Boss : A celebrity or political personality sends an email to report ",
                                                "that one of our publications on a news is in fact a fake news ",
                                                "AI-generated to damage its reputation. We have enough information ",
                                                "to say that it’s true but the person in question insists that ",
                                                "we have to delete it.", "What should we do"],
                dialog_consequence={
                    "A": [-5, 5, 5, ["Boss : We got sued by the political personality and ",
                                     "lost a bit of money, ",
                                     "the post went viral and people are preasing us for defending the truth."]],
                    "B": [-10, 15, 10, ["Boss : We got sued by the politic personality and lost money for it ",
                                        "and the report, ",
                                        "the post went viral and people are preasing us for defending the truth."]],
                    "C": [0, -10, -10, ["Boss : People are disappointed with the fact that we listened to ",
                                        "political personalities under pressure and ",
                                        "start questioning if they can still trust the media"]]}),
            NPC("pilou", nb_points=4, npc_texts=["Two members of your team have divergent ethical opinions on how ",
                                                 "to handle dubious information. One proposes total transparency, ",
                                                 "while the other prioritizes discretion to avoid causing panic.",
                                                 " How would you resolve this conflict and maintain team cohesion?"],
                dialog_consequence={
                    'A': [0, 0, -5, ["Pilou : This option may lead to unresolved tension within the team, ",
                                     "potentially affecting morale and productivity."]],
                    'B': [-20, -20, -20, ["Pilou : Terminating both team members is an extreme and ",
                                          "disproportionate response to the conflict.",
                                          "It not only disrupts team dynamics ",
                                          "but also creates a culture of fear and mistrust. "]],
                    'C': [-5, 0, 5, ["Pilou : Clear guidelines provide structure for decision-making ",
                                     "and ensure consistency, ",
                                     "but may not fully resolve underlying ethical differences."]]}),
            NPC("pixou", nb_points=2, npc_texts=["As the CEO of a media company, ",
                                                 "you oversee the editorial process for selecting headlines ",
                                                 "for articles published on your platform. ",
                                                 "However, you've noticed a trend where sensational ",
                                                 "or clickbait headlines are being prioritized over accurate and ",
                                                 "balanced ones, ",
                                                 "potentially contributing to the spread of fake news and ",
                                                 "misinformation.", "What should we do ?"],
                dialog_consequence={
                    'A': [-5, -5, 5, ["Pixou :Good point of view, "
                                      "however, this might lead to a decrease in immediate traffic and revenue."]],
                    'B': [15, -10, -10, ["Pixou : Not the smartest choice because, ",
                                         "while it may yield temporary benefits, ",
                                         "it ultimately erodes trust and damages your brand reputation. "]],
                    'C': [-15, 15, 15, ["Pixou : This idea is good however it requires some investment."]]}),
            NPC("benedict", nb_points=2, npc_texts=["Your team has developed an AI technology that could ",
                                                    "significantly improve the speed of detecting fake news, ",
                                                    "but it requires collecting sensitive user data.",
                                                    "How would you address the ethical concerns ?"],
                dialog_consequence={
                    'A': [-15, 10, 10, ["benedict : This choice will help the company to ",
                                        "avoid relaying bad information"]],
                    'B': [10, -15, -15,
                          ["benedict :  It can make us lose a lot of money if users bring us to justice"]],
                    'C': [0, 0, 5, ["benedict :  Maybe not the smartest decision ",
                                    "from a business point of view, but great moral !"]]})
        ])

        self.teleport_player("Player")
        self.teleport_npcs()

    def check_npc_collisions(self, dialog_box, choice=None):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(npc_name=sprite.name,
                                   dialog_npc=sprite.dialog, dialog_player=self.player.dialog_player,
                                   dialog_consequence=sprite.dialog_consequence, player_answer=choice,
                                   player=self.player)
                self.player.interact_with_npc(npc_name=sprite.name)

    def check_collisions(self):
        # portals
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
        # collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # load the map  (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f"map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # define a list of all collision rect
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Draw layer map
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        # Retrieve all the NPCs and add them to group
        for npc in npcs:
            group.add(npc)

        # Map loading
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()


