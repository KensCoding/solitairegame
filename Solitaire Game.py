#Solitaire Game in Python

import pygame
import random
import sys
import os

# --- Constants ---
WIDTH, HEIGHT = 900, 700
FPS = 60
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
CARD_WIDTH, CARD_HEIGHT = 80, 120
PILE_SPACING = 100
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']

# --- Card Class ---
class Card:
    def __init__(self, suit, rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.face_up = face_up

    def color(self):
        return (255, 0, 0) if self.suit in ['♥', '♦'] else (0, 0, 0)

    def draw(self, surface, pos):
        rect = pygame.Rect(pos[0], pos[1], CARD_WIDTH, CARD_HEIGHT)
        # Load card back image once and cache it
        if not hasattr(Card, "card_back"):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            Card.card_back = pygame.image.load(os.path.join(script_dir, "card_back.jpg"))
            Card.card_back = pygame.transform.scale(Card.card_back, (CARD_WIDTH, CARD_HEIGHT))
        # Draw card
        if self.face_up:
            pygame.draw.rect(surface, (255, 255, 255), rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 2)
            font = pygame.font.SysFont('arial', 24, bold=True)
            text = font.render(f"{self.rank}{self.suit}", True, self.color())
            surface.blit(text, (pos[0] + 10, pos[1] + 10))
        else:
            surface.blit(Card.card_back, rect.topleft)
            pygame.draw.rect(surface, (0, 0, 0), rect, 2)

# --- Deck Setup ---
def create_deck():
    deck = [Card(s, r) for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck

# --- Solitaire Setup ---
def deal_solitaire(deck):
    tableau = [[] for _ in range(7)]
    for i in range(7):
        for j in range(i + 1):
            card = deck.pop()
            card.face_up = (j == i)
            tableau[i].append(card)
    stock = deck
    waste = []
    foundations = [[] for _ in range(4)]
    return tableau, stock, waste, foundations

# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Solitaire")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 24)

    # Load background image (make sure the path is correct and the image exists)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    background_img = pygame.image.load(os.path.join(script_dir, "background.jpg"))
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    deck = create_deck()
    tableau, stock, waste, foundations = deal_solitaire(deck)
    dragging = None
    drag_offset = (0, 0)

    # Timer setup
    start_ticks = pygame.time.get_ticks()

    menu_open = False

    running = True
    while running:
        # Draw background image
        screen.blit(background_img, (0, 0))

        # Draw glass-like header bar
        header_height = 50
        header_surface = pygame.Surface((WIDTH, header_height), pygame.SRCALPHA)
        header_surface.fill((255, 255, 255, 90))  # White with alpha for glass effect
        pygame.draw.rect(header_surface, (200, 200, 200, 80), (0, 0, WIDTH, header_height), border_radius=18)
        screen.blit(header_surface, (0, 0))

        # Draw timer in the header
        elapsed_sec = (pygame.time.get_ticks() - start_ticks) // 1000
        minutes = elapsed_sec // 60
        seconds = elapsed_sec % 60
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (30, 30, 30))
        screen.blit(timer_text, (WIDTH - 180, 12))

        # Draw Foundations
        for i, pile in enumerate(foundations):
            x = 500 + i * (CARD_WIDTH + 20)
            y = 60
            pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)
            if pile:
                pile[-1].draw(screen, (x, y))

        # Draw Stock
        pygame.draw.rect(screen, WHITE, (30, 60, CARD_WIDTH, CARD_HEIGHT), 2)
        if stock:
            pygame.draw.rect(screen, (0, 0, 128), (30, 60, CARD_WIDTH, CARD_HEIGHT))
        # Draw Waste
        pygame.draw.rect(screen, WHITE, (130, 60, CARD_WIDTH, CARD_HEIGHT), 2)
        if waste:
            waste[-1].draw(screen, (130, 60))

        # Draw Tableau
        for i, pile in enumerate(tableau):
            x = 30 + i * (CARD_WIDTH + 20)
            y = 230
            for j, card in enumerate(pile):
                pos = (x, y + j * 30)
                if dragging and dragging['card'] == card:
                    continue
                card.draw(screen, pos)

        # Draw Dragging Card
        if dragging:
            mx, my = pygame.mouse.get_pos()
            for idx, card in enumerate(dragging['cards']):
                card.draw(screen, (mx + drag_offset[0], my + drag_offset[1] + idx * 30))

        # Draw three-dot menu button (bottom right)
        dot_radius = 6
        menu_btn_rect = pygame.Rect(WIDTH - 50, HEIGHT - 50, 40, 40)
        pygame.draw.circle(screen, (230, 230, 230), menu_btn_rect.center, 20)
        for i in range(3):
            pygame.draw.circle(screen, (80, 80, 80), (menu_btn_rect.centerx - 12 + i * 12, menu_btn_rect.centery), dot_radius)

        # Draw menu if open
        if menu_open:
            menu_width, menu_height = 260, 180
            menu_x, menu_y = WIDTH - menu_width - 30, HEIGHT - menu_height - 70
            menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
            menu_surface.fill((255, 255, 255, 230))
            pygame.draw.rect(menu_surface, (180, 180, 180, 80), (0, 0, menu_width, menu_height), border_radius=18)
            screen.blit(menu_surface, (menu_x, menu_y))
            # Menu options
            menu_font = pygame.font.SysFont('arial', 22, bold=True)
            avatar_text = menu_font.render("Choose Avatar (not implemented)", True, (30, 30, 30))
            name_text = menu_font.render("Set Player Name (not implemented)", True, (30, 30, 30))
            screen.blit(avatar_text, (menu_x + 20, menu_y + 40))
            screen.blit(name_text, (menu_x + 20, menu_y + 90))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not dragging:
                mx, my = event.pos
                # Check if menu button is clicked
                if menu_btn_rect.collidepoint(mx, my):
                    menu_open = not menu_open
                # Stock click
                elif pygame.Rect(30, 60, CARD_WIDTH, CARD_HEIGHT).collidepoint(mx, my):
                    if stock:
                        waste.append(stock.pop())
                        waste[-1].face_up = True
                    else:
                        stock = waste[::-1]
                        for c in stock:
                            c.face_up = False
                        waste = []
                # Waste click
                elif waste and pygame.Rect(130, 60, CARD_WIDTH, CARD_HEIGHT).collidepoint(mx, my):
                    if waste[-1].face_up:
                        dragging = {'card': waste[-1], 'cards': [waste[-1]], 'from': 'waste'}
                        drag_offset = (130 - mx, 60 - my)
                # Tableau click
                else:
                    for i, pile in enumerate(tableau):
                        x = 30 + i * (CARD_WIDTH + 20)
                        y = 230
                        for j in range(len(pile)):
                            card = pile[j]
                            rect = pygame.Rect(x, y + j * 30, CARD_WIDTH, CARD_HEIGHT)
                            if card.face_up and rect.collidepoint(mx, my):
                                dragging = {'card': card, 'cards': pile[j:], 'from': ('tableau', i, j)}
                                drag_offset = (rect.x - mx, rect.y - my)
                                break

            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                mx, my = event.pos
                dropped = False
                # Drop on foundations
                for i, pile in enumerate(foundations):
                    x = 500 + i * (CARD_WIDTH + 20)
                    y = 60
                    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                    if rect.collidepoint(mx, my):
                        card = dragging['cards'][0]
                        if (not pile and card.rank == 'A') or (pile and SUITS.index(card.suit) == SUITS.index(pile[-1].suit) and RANKS.index(card.rank) == RANKS.index(pile[-1].rank) + 1):
                            if dragging['from'] == 'waste':
                                waste.pop()
                            else:
                                tableau[dragging['from'][1]] = tableau[dragging['from'][1]][:dragging['from'][2]]
                                if tableau[dragging['from'][1]] and not tableau[dragging['from'][1]][-1].face_up:
                                    tableau[dragging['from'][1]][-1].face_up = True
                            pile.append(card)
                            dropped = True
                            break
                # Drop on tableau
                if not dropped:
                    for i, pile in enumerate(tableau):
                        x = 30 + i * (CARD_WIDTH + 20)
                        y = 230 + len(pile) * 30
                        rect = pygame.Rect(x, y - 30, CARD_WIDTH, CARD_HEIGHT + 30)
                        card = dragging['cards'][0]
                        if rect.collidepoint(mx, my):
                            if pile:
                                top = pile[-1]
                                if top.face_up and ((top.color() != card.color()) and (RANKS.index(top.rank) == RANKS.index(card.rank) + 1)):
                                    if dragging['from'] == 'waste':
                                        waste.pop()
                                    else:
                                        tableau[dragging['from'][1]] = tableau[dragging['from'][1]][:dragging['from'][2]]
                                        if tableau[dragging['from'][1]] and not tableau[dragging['from'][1]][-1].face_up:
                                            tableau[dragging['from'][1]][-1].face_up = True
                                    tableau[i].extend(dragging['cards'])
                                    dropped = True
                                    break
                            elif card.rank == 'K':
                                if dragging['from'] == 'waste':
                                    waste.pop()
                                else:
                                    tableau[dragging['from'][1]] = tableau[dragging['from'][1]][:dragging['from'][2]]
                                    if tableau[dragging['from'][1]] and not tableau[dragging['from'][1]][-1].face_up:
                                        tableau[dragging['from'][1]][-1].face_up = True
                                tableau[i].extend(dragging['cards'])
                                dropped = True
                                break
                if not dropped and dragging['from'] == 'waste':
                    pass  # Return to waste
                dragging = None

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

