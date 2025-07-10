from config.layouts import PageLayout, BingoCardLayout, CallingCardsSinglePageLayout, CallingCardsMultiPageLayout, TokensLargeLayout, TokensSmallLayout
from core.drawing import generate_bingo_cards, generate_calling_cards_single, generate_calling_cards_multi, generate_tokens_large, generate_tokens_small

def main():
    page_layout = PageLayout()
    bingo_card_layout = BingoCardLayout()
    calling_card_single_layout = CallingCardsSinglePageLayout()
    calling_card_multi_layout =  CallingCardsMultiPageLayout()
    tokens_large_layout = TokensLargeLayout()
    tokens_small_layout = TokensSmallLayout()

    generate_bingo_cards(page_layout, bingo_card_layout)
    generate_calling_cards_single(page_layout, calling_card_single_layout)
    generate_calling_cards_multi(page_layout, calling_card_multi_layout)
    generate_tokens_large(page_layout, tokens_large_layout)
    generate_tokens_small(page_layout, tokens_small_layout)

if __name__ == "__main__":
    main()
