class Settings:
    def __init__(self):

        # Screen Settings
        self.screen_width=1000
        self.screen_height=600
        self.bg_color=(230,230,230)

        # Ship Settings
        self.ship_speed=1.5 
        self.ship_limit=3


        # Bullet settings
        self.bullet_speed=2.5
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullets_allowed=7

        # Aliens
        self.alien_speed=1.0
        self.fleet_drop_speed=10
        self.fleet_direction=1

        # Initialize the game's static settings
        # How quickly the game speeds up
        self.speedup_scale=1.2

        self.score_scale=1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        self.ship_speed=4.0
        self.bullet_speed=5.0
        self.alien_speed=1.0

        self.fleet_direction=1

        # Score setting
        self.alien_point=10


    def increase_speed(self):
        # Increase speed settings
        self.ship_speed*=1.1
        self.bullet_speed*=1.1
        self.alien_speed *= self.speedup_scale

        self.alien_point=int(self.alien_point*self.score_scale)

        print(self.alien_point)