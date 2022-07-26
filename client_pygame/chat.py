import pygame
from utils import input_box_color, chat_color, user_rect_color_text, bot_rect_color_text, \
    text_color


# TODO: fix scroll - ideal like whatsapp chat
# TODO: spanish lng
# TODO: handle text longer then width


class Chat:
    def __init__(self, q, chat_width, chat_height, width_offset):
        self.q = q

        self.chat_height = chat_height
        self.chat_width = chat_width
        self.width_offset = width_offset

        # params
        self.chat_prompt = "Type a message"
        self.headline_text = 'CLG lab - Chat Bot 1.0'
        self.font_size = 15
        self.line_size = 32
        self.headline_size = 64
        self.scroll_adv = 25

        # colors
        self.input_box_color = input_box_color
        self.chat_color = chat_color

        self.scroll_y = 0
        self.chat_y = 0  # self.chat_height - 2 * self.line_size
        self.user_text = self.chat_prompt

        # Layout
        self.headline = pygame.surface.Surface((chat_width, self.headline_size))
        self.headline_rect = pygame.Rect(0, 0, chat_width, self.headline_size)

        self.chat_box = pygame.surface.Surface(
            (chat_width, chat_height - self.line_size - self.headline_size))
        self.chat_box.fill(self.chat_color)
        self.input_box = pygame.surface.Surface((chat_width, self.line_size))
        self.input_rect = pygame.Rect(0, 0, chat_width,
                                      self.line_size)  # relative to self input box

        self.chat_font = pygame.font.SysFont('segoeui', self.font_size)
        self.input_font = pygame.font.SysFont('segoeui', self.font_size)
        self.headline_font = pygame.font.SysFont('segoeui', self.font_size + 5)

    def add_text(self, text, speaker='user'):
        if speaker == 'user':
            self.q.put({'speaker': speaker, 'text': text})

        x_left = 1
        rect_color = user_rect_color_text
        text_width = self.chat_font.size(text)[0]

        if speaker != 'user':
            x_left = self.chat_width - text_width - 1
            rect_color = bot_rect_color_text

        text_rect = pygame.Rect(x_left, self.chat_y, text_width + 10, self.line_size - 5)
        pygame.draw.rect(self.chat_box, rect_color, text_rect, 0, 3)
        text_surface = self.chat_font.render(text, True, text_color)

        self.chat_box.blit(text_surface, (x_left, self.chat_y + 5))
        self.user_text = self.chat_prompt
        self.chat_y += self.line_size

    def on_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:
                self.scroll_y = min(self.scroll_y + self.scroll_adv, 0)
            if e.button == 5:  # scroll down
                self.scroll_y = self.scroll_y - self.scroll_adv

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                if self.user_text == self.chat_prompt:
                    return
                if len(self.user_text) == 1:
                    self.user_text = self.chat_prompt
                    return
                self.user_text = self.user_text[:-1]
            else:
                if e.unicode == '\r':
                    self.add_text(self.user_text)
                else:
                    if self.user_text == self.chat_prompt:
                        self.user_text = ''
                    self.user_text += e.unicode

    def on_frame(self, screen):
        screen.blit(self.headline, (self.width_offset, 0))
        screen.blit(self.chat_box, (self.width_offset, self.scroll_y + self.headline_size))
        screen.blit(self.input_box, (self.width_offset, self.chat_height - self.line_size))

        pygame.draw.rect(self.input_box, self.input_box_color, self.input_rect)
        input_text = self.input_font.render(self.user_text, True, text_color)
        self.input_box.blit(input_text, (self.input_rect.x + 5, self.input_rect.y + 5))

        pygame.draw.rect(self.headline, self.input_box_color, self.headline_rect)
        headline_font = self.headline_font.render(self.headline_text, True, text_color)
        text_width, text_height = self.headline_font.size(self.headline_text)
        self.headline.blit(headline_font, ((self.chat_width - text_width) / 2,
                                           (self.headline_size - text_height) / 2))
