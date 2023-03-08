import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

class TextBox:
    def __init__(self, x, y, width, height, font_size=20, title=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.font_size = font_size
        self.title = title
        self.text = ""
        self.active = False
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        title_surface = self.font.render(self.title, True, (0, 0, 0))
        screen.blit(title_surface, (self.rect.x, self.rect.y - self.font_size - 5))
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


text_box = TextBox(100, 100, 200, 50, font_size=30, title="Enter your name:")

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        mew = text_box.handle_event(event)
        if mew:
            print(mew)

    screen.fill((255, 255, 255))
    text_box.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
