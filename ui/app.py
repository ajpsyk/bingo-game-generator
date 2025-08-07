import tkinter as tk
from tkinter import ttk
from config.layouts import PageLayout, BingoCardLayout, BingoCardMultiLayout, TokensLayout, CallingCardsSinglePageLayout, CallingCardsMultiPageLayout

def main():
    root = tk.Tk()
    
    root.title('Bingo Game Generator')
    root.geometry("1200x720")
    tabbed_window = ttk.Notebook(root)
    tabbed_window.pack(expand=True, fill='both')

    tab0 = ttk.Frame(tabbed_window)
    tab1 = ttk.Frame(tabbed_window)
    tab2 = ttk.Frame(tabbed_window)
    tab3 = ttk.Frame(tabbed_window)
    tab4 = ttk.Frame(tabbed_window)
    tab5 = ttk.Frame(tabbed_window)

    tabbed_window.add(tab0, text="Page Layout")
    tabbed_window.add(tab1, text='Bingo Cards (Single)')
    tabbed_window.add(tab2, text='Bingo Cards (Double)')
    tabbed_window.add(tab3, text='Tokens')
    tabbed_window.add(tab4, text='Calling Cards (Single)')
    tabbed_window.add(tab5, text='Calling Cards (Multi Page)')

    style = ttk.Style()
    style.theme_use('alt')

    style.configure('TNotebook.Tab', focuscolor='')
    style.map('TNotebook.Tab',
            focuscolor=[('focus', '')],
            bordercolor=[('focus', '')],
            highlightcolor=[('focus', '')],
            highlightthickness=[('focus', 0)])
    
    create_page_layout_tab(tab0)
    create_bingo_cards_single_tab(tab1)
    create_bingo_cards_double_tab(tab2)
    create_tokens_tab(tab3)
    create_calling_cards_single_tab(tab4)
    create_calling_cards_multi_page_tab(tab5)

    root.mainloop()


def create_page_layout_tab(tab):

    fields = [
        ("DPI:", PageLayout.DPI),
        ("Page Width (in):", PageLayout.WIDTH_INCHES),
        ("Page Height (in):", PageLayout.HEIGHT_INCHES),
        ("Top Margin (in):", PageLayout.MARGIN_TOP_INCHES),
        ("Right Margin (in):", PageLayout.MARGIN_RIGHT_INCHES),
        ("Bottom Margin (in):", PageLayout.MARGIN_BOTTOM_INCHES),
        ("Left Margin (in):", PageLayout.MARGIN_LEFT_INCHES),
        ("Font Path:", PageLayout.FONT_PATH),
        ("How To Path:", PageLayout.INSTRUCTIONS_PATH),
        ("Game Rules, Calling Cards, Tokens Path:", PageLayout.OUTPUT_PATH),
    ]

    entries = {}
    
    for i, (label_text, default_value) in enumerate(fields):
        label = tk.Label(tab, text=label_text)
        label.grid(row=i, column=0, sticky='e', padx=5, pady=2)
        
        entry = tk.Entry(tab, width=50)
        entry.grid(row=i, column=1, sticky='w', padx=5, pady=2)
        entry.insert(0, str(default_value))
        
        entries[label_text] = entry

def create_bingo_cards_single_tab(tab):
    fields = [
        ("Card Amount:", BingoCardLayout.CARD_AMOUNT),
        ("Number of PDFS:", BingoCardLayout.NUM_PDFS),
        ("Label Color (hex):", BingoCardLayout.LABEL_COLOR),
        ("Frame Enabled:", BingoCardLayout.FRAME_ENABLED),
        ("Frame Padding:", PageLayout.RIGHT_MARGIN_INCHES),
        ("Bottom Margin (in):", PageLayout.BOTTOM_MARGIN_INCHES),
        ("Left Margin (in):", PageLayout.LEFT_MARGIN_INCHES),
        ("Font Path:", PageLayout.FONT_PATH),
        ("How To Path:", PageLayout.HOW_TO_PATH),
        ("Game Rules, Calling Cards, Tokens Path:", PageLayout.OUTPUT_PATH),
    ]

    entries = {}
    
    for i, (label_text, default_value) in enumerate(fields):
        label = tk.Label(tab, text=label_text)
        label.grid(row=i, column=0, sticky='e', padx=5, pady=2)
        
        entry = tk.Entry(tab, width=50)
        entry.grid(row=i, column=1, sticky='w', padx=5, pady=2)
        entry.insert(0, str(default_value))
        
        entries[label_text] = entry

def create_bingo_cards_double_tab(tab):
    pass
def create_tokens_tab(tab):
    pass
def create_calling_cards_single_tab(tab):
    pass
def create_calling_cards_multi_page_tab(tab):
    pass

if __name__ == '__main__':
    main()
