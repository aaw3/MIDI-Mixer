import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MixerBoard(Gtk.Window):
    def __init__(self):
        super().__init__(title="Mixer Board Layout")
        self.set_default_size(1200, 600)

        # Store selected values for knobs, faders, and buttons
        self.selected_values = {}

        # Main vertical layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)

        # Create a grid for the mixer layout (knobs, faders, and buttons)
        top_grid = Gtk.Grid()
        top_grid.set_row_spacing(10)
        top_grid.set_column_spacing(10)
        top_grid.set_halign(Gtk.Align.FILL)  # Expand horizontally
        top_grid.set_valign(Gtk.Align.FILL)  # Expand vertically
        top_grid.set_hexpand(True)
        top_grid.set_vexpand(True)
        main_box.pack_start(top_grid, True, True, 0)

        # Create faders with buttons and dropdowns
        for i in range(8):
            # Endless scroll knob above each fader
            knob_label = Gtk.Label(label=f"knob_{i}")
            knob_label.set_halign(Gtk.Align.CENTER)
            top_grid.attach(knob_label, i, 0, 1, 1)

            knob_dropdown = self.create_multi_dropdown(f"knob_{i}")
            knob_dropdown.set_halign(Gtk.Align.FILL)
            knob_dropdown.set_hexpand(True)
            knob_dropdown.set_vexpand(True)  # Allow vertical expansion
            top_grid.attach(knob_dropdown, i, 1, 1, 1)

            # Fader
            fader_label = Gtk.Label(label=f"fader_{i}")
            fader_label.set_halign(Gtk.Align.CENTER)
            top_grid.attach(fader_label, i, 2, 1, 1)

            fader_dropdown = self.create_multi_dropdown(f"fader_{i}")
            fader_dropdown.set_halign(Gtk.Align.FILL)
            fader_dropdown.set_hexpand(True)
            fader_dropdown.set_vexpand(True)  # Allow vertical expansion
            top_grid.attach(fader_dropdown, i, 3, 1, 1)


            fader_buttons_label = Gtk.Label(label=f"buttons_{i}")
            fader_buttons_label.set_halign(Gtk.Align.CENTER)
            top_grid.attach(fader_buttons_label, i, 4, 1, 1)

            # Buttons to the right of the fader with dropdowns
            for j in range(4):
                dropdown = self.create_multi_dropdown(f"button_{i}_{j}")
                dropdown.set_halign(Gtk.Align.FILL)
                dropdown.set_hexpand(True)
                dropdown.set_vexpand(True)  # Allow vertical expansion
                top_grid.attach(dropdown, i, 8 + j, 1, 1)

        # Create a grid for the bottom buttons and dropdowns
        bottom_grid = Gtk.Grid()
        bottom_grid.set_row_spacing(5)
        bottom_grid.set_column_spacing(15)
        bottom_grid.set_halign(Gtk.Align.FILL)  # Expand horizontally
        bottom_grid.set_valign(Gtk.Align.FILL)  # Expand vertically
        bottom_grid.set_hexpand(True)
        bottom_grid.set_vexpand(False)  # Less vertical expansion than the top grid
        main_box.pack_start(bottom_grid, False, False, 0)

        control_buttons = [
            "Play", "Pause", "Rec", "Rewind", "Fastforward",
            "Chan Left", "Chan Right", "Up", "Down", "Left", "Right",
        ]

        for i, control in enumerate(control_buttons):
            # Add the label
            label = Gtk.Label(label=control)
            label.set_halign(Gtk.Align.CENTER)
            label.set_vexpand(False)  # Prevent vertical expansion
            bottom_grid.attach(label, i, 0, 1, 1)

            # Add the dropdown (or button in this case)
            dropdown = self.create_multi_dropdown(f"control_{i}")
            dropdown.set_halign(Gtk.Align.FILL)
            dropdown.set_hexpand(True)
            dropdown.set_vexpand(False)  # Prevent full vertical expansion
            dropdown.set_size_request(100, 40)  # Minimum height
            bottom_grid.attach(dropdown, i, 1, 1, 1)

    def create_multi_dropdown(self, identifier):
        """Create a button that mimics the dropdown behavior."""
        button = Gtk.Button(label="Select...")
        button.connect("clicked", self.show_menu, identifier)

        # Set alignment to match the dropdown behavior
        button.set_halign(Gtk.Align.FILL)
        button.set_hexpand(True)
        button.set_vexpand(False)  # Match dropdown behavior
        button.set_size_request(100, 40)  # Minimum height (same as dropdown)

        return button

    def show_menu(self, button, identifier):
        """Show a multi-level menu when the button is clicked."""
        # Create the main menu
        menu = Gtk.Menu()

        # Example categories and options
        categories = {
            "Category 1": ["Option 1.1", "Option 1.2", "Option 1.3"],
            "Category 2": ["Option 2.1", "Option 2.2"],
            "Category 3": ["Option 3.1", "Option 3.2", "Option 3.3"],
        }

        for category, options in categories.items():
            # Create a menu item for each category
            category_item = Gtk.MenuItem(label=category)
            menu.append(category_item)

            # Create a submenu for the category
            submenu = Gtk.Menu()
            for option in options:
                option_item = Gtk.MenuItem(label=option)
                option_item.connect("activate", self.on_option_selected, button, identifier)
                submenu.append(option_item)

            # Attach the submenu to the category item
            category_item.set_submenu(submenu)

        # Show all menu items
        menu.show_all()

        # Popup the menu
        menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

    def on_option_selected(self, menu_item, button, identifier):
        """Handle the selection of an option."""
        selected_value = menu_item.get_label()
        self.selected_values[identifier] = selected_value
        button.set_label(selected_value)  # Update button label
        print(f"Selected for {identifier}: {selected_value}")


# Run the application
if __name__ == "__main__":
    app = MixerBoard()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
