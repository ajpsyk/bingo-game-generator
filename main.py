from pages.calling_card_single import generate_calling_card_single
from pages.bingo_cards_big import generate_bingo_cards_big
from config import DEFAULT_IMAGE_FOLDER, DEFAULT_OUTPUT_PATH

if __name__ == "__main__":
    #generate_calling_card_single(DEFAULT_IMAGE_FOLDER, DEFAULT_OUTPUT_PATH)
    generate_bingo_cards_big(DEFAULT_IMAGE_FOLDER, DEFAULT_OUTPUT_PATH)
