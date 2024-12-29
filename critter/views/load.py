from critter.core.application import View
from critter.core.context import context

from critter.lib.loading import Task

from arcade import Texture, SpriteSheet, BasicSprite, draw_sprite
from resources import load_png_sheet

class LoadView(View):
    throbber_sheet: SpriteSheet = None
    throbber_frames: tuple[Texture, ...] = ()

    def __init__(self, task: Task) -> None:
        super().__init__()
        self.task = task

        if LoadView.throbber_sheet is None:
            s = context.THROBBER_SIZE
            LoadView.throbber_sheet = sheet = load_png_sheet('throbber_sheet')
            LoadView.throbber_frames = tuple(sheet.get_texture(s * x, 0, s, s) for x in range(int(sheet.image.width / s)))

        self.start = self.window.time
        self.sprite = BasicSprite(LoadView.throbber_frames[0], 1.0, self.center_x, self.center_y)

    def on_show_view(self):
        self.task.begin()

    def on_draw(self) -> None:
        self.clear()

        t = 1000 * (self.window.time - self.start)
        if t <= context.THROBBER_FADE:
            a = t / context.THROBBER_FADE
        else:
            a = 1.0
        idx = int(t / context.THROBBER_SPEED) % len(LoadView.throbber_frames)
        self.sprite.texture = LoadView.throbber_frames[idx]
        self.sprite.alpha = int(255 * a)

        draw_sprite(self.sprite)
        
        if self.task.complete:
            self.task.finish()