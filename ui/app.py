import tkinter as tk
from tkinter import ttk

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
    pass
def create_bingo_cards_single_tab(tab1):
    pass
def create_bingo_cards_double_tab(tab2):
    pass
def create_tokens_tab(tab3):
    pass
def create_calling_cards_single_tab(tab4):
    pass
def create_calling_cards_multi_page_tab(tab5):
    pass

if __name__ == '__main__':
    main()
