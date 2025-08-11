from config.layouts import (
    PageLayout,
    BingoCardLayout,
    BingoCardMultiLayout,
    TokensLayout,
    CallingCardsSinglePageLayout,
    CallingCardsMultiPageLayout
)
import json
import tkinter as tk
from tkinter import ttk, filedialog
from dataclasses import asdict, fields
from collections import defaultdict
from core.drawing import (
    generate_bingo_cards, generate_bingo_cards_multi, generate_tokens, generate_calling_cards_single, generate_calling_cards_multi
)
from core.utils import merge_howto_tokens_callingcards


LAYOUTS = {
    "Page Layout": PageLayout,
    "Bingo Card Layout": BingoCardLayout,
    "Bingo Card Mini Layout": BingoCardMultiLayout,
    "Tokens Layout": TokensLayout,
    "Calling Cards Single Page Layout": CallingCardsSinglePageLayout,
    "Calling Cards Multi Page Layout": CallingCardsMultiPageLayout
}

LAYOUT_INSTANCES = {name: cls() for name, cls in LAYOUTS.items()}

TABS = {
    "Assets & Page Layout": ["Page Layout"],
    "Bingo Cards": ["Bingo Card Layout", "Bingo Card Mini Layout"],
    "C.C.,Tokens,Rules": ["Calling Cards Single Page Layout", "Calling Cards Multi Page Layout"]
}


def main():
    load_app_settings()
    root = init_root_window()
    notebook = init_notebook(root)
    tab_elements, tab_frames = build_tabs(notebook, TABS, LAYOUT_INSTANCES)
    add_create_buttons_to_tabs(tab_frames, tab_elements, notebook)
    handle_exit(root, tab_elements)
    root.mainloop()

def load_app_settings(filepath="settings.json"):
    try:
        with open(filepath) as f:
            settings = json.load(f)
        for name, attributes in settings.items():
            layout = LAYOUTS.get(name)
            if layout:
                LAYOUT_INSTANCES[name] = dict_to_instance(layout, attributes)
    except FileNotFoundError:
        pass

def dict_to_instance(layout, attributes):
    field_names = {f.name for f in fields(layout)}
    filtered_data = {key: value for key, value in attributes.items() if key in field_names}
    return layout(**filtered_data)

def init_root_window():
    root = tk.Tk()
    root.title('Bingo Game Generator')
    root.geometry("1200x720")
    style = ttk.Style()
    style.theme_use('alt')
    return root

def init_notebook(root):
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
    return notebook

def build_tabs(notebook, tabs, layout_instances):
    tab_elements = {}
    tab_frames = {}
    for tab_name, layouts in tabs.items():
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tab_name)
        classes = [layout_instances[layout] for layout in layouts]
        sections = create_fields(tab, classes)
        tab_elements[tab_name] = sections
        tab_frames[tab_name] = tab
        position_elements(tab, sections)
    return tab_elements, tab_frames

def create_fields(tab, instances):
    groups = defaultdict(lambda: defaultdict(list))

    for instance in instances:
        for field in fields(instance):
            group = field.metadata.get("group", "")
            section = field.metadata.get("section", "")
            label_text = field.metadata.get("label", field.name)
            default_value = getattr(instance, field.name)
            input_type = field.metadata.get("input_type", "entry")
            field_name = field.name
            is_header = field.metadata.get("header", False)

            label = ttk.Label(tab, text=label_text, font=('Segoe UI', 10, 'bold') if is_header else None)
            widget = None if is_header else create_widget_for_field(tab, input_type, default_value, instance, field_name)

            if widget:
                widget.field_name = field_name
                widget.instance = instance

            groups[group][section].append((label, widget, is_header))

    return groups

def create_widget_for_field(tab, input_type, default_value, instance, field_name):
    if input_type == "entry":
        widget = ttk.Entry(tab, width=50)
        widget.insert(0, str(default_value))
        return widget

    elif input_type == "checkbox":
        var = tk.BooleanVar(value=default_value)
        widget = ttk.Checkbutton(tab, variable=var)
        widget.var = var
        return widget

    elif input_type == "file":
        frame = ttk.Frame(tab)
        entry = ttk.Entry(frame, width=40)
        entry.insert(0, str(default_value))
        entry.pack(side='left', fill='x', expand=True)

        def browse():
            path = filedialog.askopenfilename(title=f"Select {field_name}")
            if path:
                entry.delete(0, 'end')
                entry.insert(0, path)
                setattr(instance, field_name, path)

        ttk.Button(frame, text="Browse...", command=browse).pack(side='left', padx=(5, 0))
        widget = frame
        widget.entry = entry
        return widget

    elif input_type == "directory":
        frame = ttk.Frame(tab)
        entry = ttk.Entry(frame, width=40)
        entry.insert(0, str(default_value))
        entry.pack(side='left', fill='x', expand=True)

        def browse():
            path = filedialog.askdirectory(title=f"Select {field_name}")
            if path:
                entry.delete(0, 'end')
                entry.insert(0, path)
                setattr(instance, field_name, path)

        ttk.Button(frame, text="Browse...", command=browse).pack(side='left', padx=(5, 0))
        widget = frame
        widget.entry = entry
        return widget

def position_elements(tab, groups):
    col_idx = 0
    for group_name, sections in groups.items():
        if not group_name or group_name.lower() == "default":
            continue

        group_label = ttk.Label(tab, text=group_name, font=('Segoe UI', 12, 'bold'))
        group_label.grid(row=0, column=col_idx * 2, columnspan=2, pady=(10, 5), sticky='w', padx=(30, 5))

        row = 1
        previous_spacer_after = False

        for section_name, items in sections.items():
            if previous_spacer_after:
                row += 1
                previous_spacer_after = False

            if section_name:
                section_label = ttk.Label(tab, text=section_name, font=('Segoe UI', 10, 'bold'))
                section_label.grid(row=row, column=col_idx * 2, columnspan=2, sticky='w', padx=(20, 5), pady=(10, 5))
                row += 1

            for label, widget, is_header in items:
                if widget and hasattr(widget, 'instance') and hasattr(widget, 'field_name'):
                    instance = widget.instance
                    field_name = widget.field_name
                    f = next((f for f in fields(type(instance)) if f.name == field_name), None)
                    if f and f.metadata.get("hidden", False):
                        continue

                label.grid(row=row, column=col_idx * 2, sticky='e', padx=5, pady=2)
                if widget:
                    widget.grid(row=row, column=col_idx * 2 + 1, sticky='w', padx=5, pady=2)

                spacer_after = False
                if widget and hasattr(widget, 'instance') and hasattr(widget, 'field_name'):
                    instance = widget.instance
                    field_name = widget.field_name
                    f = next((f for f in fields(type(instance)) if f.name == field_name), None)
                    if f:
                        spacer_after = f.metadata.get("spacer_after", False)

                row += 1
                previous_spacer_after = spacer_after

            if items:
                last_label, last_widget, last_is_header = items[-1]
                spacer_after_last = False
                if last_widget and hasattr(last_widget, 'instance') and hasattr(last_widget, 'field_name'):
                    instance = last_widget.instance
                    field_name = last_widget.field_name
                    f = next((f for f in fields(type(instance)) if f.name == field_name), None)
                    if f:
                        spacer_after_last = f.metadata.get("spacer_after", False)
                if spacer_after_last:
                    row += 1
                    previous_spacer_after = False

        col_idx += 1


def add_create_buttons_to_tabs(tab_frames, tab_elements, notebook):
    for tab_name, tab in tab_frames.items():
        frame_buttons = ttk.Frame(tab)
        frame_buttons.grid(row=999, column=0, columnspan=2, pady=10)

        if tab_name == "C.C.,Tokens,Rules":
            btn = ttk.Button(frame_buttons, text="Create Combined PDFs",
                             command=lambda: (update_instances(tab_elements), generate_outputs("Calling Cards Single Page Layout")))
            btn.pack(side='left', padx=5)

        elif tab_name == "Bingo Cards":
            btn1 = ttk.Button(frame_buttons, text="Create One-Page Bingo Cards",
                              command=lambda: (update_instances(tab_elements), generate_outputs("Bingo Card Layout")))
            btn1.pack(side='left', padx=5)
            btn2 = ttk.Button(frame_buttons, text="Create Multi-Page Bingo Cards",
                              command=lambda: (update_instances(tab_elements), generate_outputs("Bingo Card Mini Layout")))
            btn2.pack(side='left', padx=5)

def save_button_handler(tab_elements, tabbed_window):
    update_instances(tab_elements)
    save_settings()
    active_tab_name = tabbed_window.tab(tabbed_window.select(), "text")

    tab_to_layouts = {
        "Assets & Page Layout": ["Page Layout"],
        "Bingo Cards": ["Bingo Card Layout", "Bingo Card Mini Layout"],
        "C.C.,Tokens,Rules": ["Calling Cards Single Page Layout", "Calling Cards Multi Page Layout"]
    }

    layouts = tab_to_layouts.get(active_tab_name, ["Page Layout"])
    for layout_key in layouts:
        generate_outputs(layout_key)

def handle_exit(root, tab_elements):
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, tab_elements))

def on_closing(root, tab_elements):
    update_instances(tab_elements)
    save_settings()
    root.destroy()

def update_instances(tab_elements):
    for tab_name, groups in tab_elements.items():
        for group_name, sections in groups.items():
            for section_name, items in sections.items():
                for entry in items:
                    if not isinstance(entry, tuple) or len(entry) != 3:
                        continue
                    label, widget, is_header = entry
                    if is_header or widget is None:
                        continue

                    cls = type(widget.instance)
                    field_name = widget.field_name
                    expected_type = cls.__annotations__.get(field_name, str)

                    if isinstance(widget, ttk.Entry):
                        raw_value = widget.get()
                        value = convert_type(raw_value, expected_type)

                    elif isinstance(widget, ttk.Checkbutton):
                        value = widget.var.get()

                    elif hasattr(widget, 'entry'):
                        raw_value = widget.entry.get()
                        value = convert_type(raw_value, expected_type)

                    else:
                        continue

                    setattr(widget.instance, field_name, value)

def convert_type(value, to_type):
    try:
        if to_type == bool:
            return str(value).lower() in ('true', '1', 'yes', 'on')
        elif to_type == int:
            return int(value) if value != '' else 0
        elif to_type == float:
            return float(value) if value != '' else 0.0
        return to_type(value)
    except Exception:
        return value

def save_settings(filepath="settings.json"):
    data = {name: asdict(inst) for name, inst in LAYOUT_INSTANCES.items()}
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def generate_outputs(active_tab_name):
    if active_tab_name == "Calling Cards Single Page Layout":
        page_layout = LAYOUT_INSTANCES["Page Layout"]
        tokens_layout = LAYOUT_INSTANCES["Tokens Layout"]
        single_layout = LAYOUT_INSTANCES["Calling Cards Single Page Layout"]
        multi_layout = LAYOUT_INSTANCES["Calling Cards Multi Page Layout"]

        print("Generating tokens and calling cards...")

        generate_tokens(page_layout, tokens_layout)
        generate_calling_cards_single(page_layout, single_layout)
        generate_calling_cards_multi(page_layout, multi_layout)
        merge_howto_tokens_callingcards(page_layout, single_layout, multi_layout, tokens_layout)    
    elif active_tab_name == "Bingo Card Layout":
        page_layout = LAYOUT_INSTANCES["Page Layout"]
        bingo_layout = LAYOUT_INSTANCES["Bingo Card Layout"]
        print("Generating Bingo Cards...")
        generate_bingo_cards(page_layout, bingo_layout)
    elif active_tab_name == "Bingo Card Mini Layout":
        page_layout = LAYOUT_INSTANCES["Page Layout"]
        mini_layout = LAYOUT_INSTANCES["Bingo Card Mini Layout"]
        print("Generating Mini Bingo Cards...")
        generate_bingo_cards_multi(page_layout, mini_layout)

if __name__ == '__main__':
    main()
