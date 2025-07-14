from config.layouts import PageLayout, BingoCardLayout, BingoCardMultiLayout, CallingCardsSinglePageLayout, CallingCardsMultiPageLayout, TokensLayout
from core.drawing import generate_bingo_cards, generate_bingo_cards_multi, generate_calling_cards_single, generate_calling_cards_multi, generate_tokens

def main():
    page_layout = PageLayout()
    #bingo_card_layout = BingoCardLayout()
    #bingo_card_multi_layout = BingoCardMultiLayout()
    #calling_card_single_layout = CallingCardsSinglePageLayout()
    calling_card_multi_layout =  CallingCardsMultiPageLayout()
    #tokens_layout = TokensLayout()

    #generate_bingo_cards(page_layout, bingo_card_layout)
    #generate_bingo_cards_multi(page_layout, bingo_card_multi_layout)
    #generate_calling_cards_single(page_layout, calling_card_single_layout)
    generate_calling_cards_multi(page_layout, calling_card_multi_layout)
    #generate_tokens(page_layout, tokens_layout)

if __name__ == "__main__":
    main()
