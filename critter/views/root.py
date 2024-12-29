from critter.core.application import View

from .load import LoadView
from .menu import MenuView

from critter.lib.splash import Splash, Action
from critter.lib.loading import SleepTask
from resources import load_png

from arcade import BasicSprite, draw_sprite, clock, get_default_texture


class RootView(View):

    def __init__(self):
        super().__init__()
        self.splashes = [
            Splash(
                'splash_dragon',
                3.0,
                True,
                alpha_action=Action.PULSE,
                scale_b=0.8,
                scale_v=0.2
            ),
            Splash(
                'splash_arcade',
                3.0,
                False,
                alpha_action=Action.PULSE,
                scale_b=0.8,
                scale_v=0.2
            )
        ]

        self.splash_idx = 0
        self.splash_tm = 0
        self.splash = None

        self.splash_sprite = BasicSprite(get_default_texture(), 1.0, self.center_x, self.center_y, visible=False)

    def on_key_release(self, _symbol, _modifiers):
        self.window.show_view(MenuView())

    def on_draw(self) -> None:
        self.clear()
        if self.splash is None:
            self.splash = self.splashes[self.splash_idx]
            self.splash_tm = self.window.time
            self.splash_idx += 1

            self.splash_sprite.texture = load_png(self.splash.icon)
            self.splash_sprite.visible = True
        
        if self.splash.duration < clock.GLOBAL_CLOCK.time_since(self.splash_tm):
            if self.splash_idx >= len(self.splashes):
                self.window.show_view(LoadView(SleepTask(lambda: self.window.show_view(MenuView()), 10.0)))
                return

            self.splash_tm += self.splash.duration
            self.splash = self.splashes[self.splash_idx]
            self.splash_idx += 1
            
            self.splash_sprite.texture = load_png(self.splash.icon)
        
        t = clock.GLOBAL_CLOCK.time_since(self.splash_tm)
        self.splash_sprite.scale = self.splash.scale(t)
        self.splash_sprite.alpha = self.splash.alpha(t)

        draw_sprite(self.splash_sprite, pixelated=self.splash.pixelated)