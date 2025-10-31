import pygame

class PygameKeyboardClient:

    def __init__(self, width=640, height=480, title='Keyboard Control'):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.pressed_keys = set()
        self.instructions = ['===== Keyboard Controls Instructions =====', 'support combination of multiple keys', 'example: press UP+RIGHT for diagonal move', '', '   Movement (world EE coords):', '     UP    - Move +X', '     DOWN  - Move -X', '     LEFT  - Move +Y', '     RIGHT - Move -Y', '     e     - Move +Z', '     d     - Move -Z', '', '   Rotation (local EE coords):', '     q     - Roll + ', '     w     - Roll - ', '     a     - Pitch + ', '     s     - Pitch - ', '     z     - Yaw + ', '     x     - Yaw - ', '', '   Gripper:', '     Space - Close(hold) / Open(release)', '', '     ESC   - Quit Simulation', '==========================================']

    def update(self) -> bool:
        """
        fresh pygame event, update pressed_keys.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)
        return True

    def is_pressed(self, key: int) -> bool:
        return key in self.pressed_keys or pygame.key.get_pressed()[key]

    def close(self):
        pygame.quit()

    def draw_instructions(self):
        font = pygame.font.Font(pygame.font.match_font('DejaVu Sans Mono'), 25)
        text_color = (255, 255, 255)
        bg_color = (0, 0, 0)
        self.screen.fill(bg_color)
        y_offset = 20
        for line in self.instructions:
            text_surface = font.render(line, True, text_color)
            self.screen.blit(text_surface, (20, y_offset))
            y_offset += 30
        pygame.display.flip()