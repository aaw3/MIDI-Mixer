import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from config import Config


class MixerBoard(Gtk.Window):
    module_fn_name_to_function = {}
    component_to_module_name = {}

    @staticmethod
    def get_function_by_component_name(name):
        if name not in MixerBoard.component_to_module_name:
            return None
        module_name = MixerBoard.component_to_module_name[name]
        return MixerBoard.module_fn_name_to_function[module_name] if module_name in MixerBoard.module_fn_name_to_function else None

    @staticmethod
    def get_extra_args(name):
        return MixerBoard.extra_args[name] if name in MixerBoard.extra_args else None


    extra_args = {}
    def __init__(self, module_functions):
        super().__init__(title="Mixer Board Layout")
        self.set_default_size(1200, 600)
        self.config = Config()


        # Have to convert from form [{pluginname1: {knob: {}, fader: {}, button: {}}}, {pluginname2: {knob: {}, fader: {}, button: {}}}]
        self.knob_functions = module_functions["KnobFunction"] if "KnobFunction" in module_functions else {}
        self.fader_functions = module_functions["FaderFunction"] if "FaderFunction" in module_functions else {}
        self.button_functions = module_functions["ButtonFunction"] if "ButtonFunction" in module_functions else {}
        #self.function_by_name = {}
        
        # Store selected values for knobs, faders, and buttons
        #self.selected_values = {}

        # Main vertical layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        




        # Create the menu bar
        menubar = Gtk.MenuBar()

        # Create the File menu
        file_menu = Gtk.Menu()
        file_menu_item = Gtk.MenuItem(label="File")
        file_menu_item.set_submenu(file_menu)

        # Add Save and Quit items to the File menu
        save_item = Gtk.MenuItem(label="Save")
        save_item.connect("activate", self.on_save)
        file_menu.append(save_item)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.on_quit)
        file_menu.append(quit_item)

        # Add File menu to the menu bar
        menubar.append(file_menu_item)

        # Add the menu bar to the layout
        main_box.pack_start(menubar, False, False, 0)




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

            knob_dropdown = self.create_multi_dropdown(f"KNOB_{i}")
            knob_dropdown.set_halign(Gtk.Align.FILL)
            knob_dropdown.set_hexpand(True)
            knob_dropdown.set_vexpand(True)  # Allow vertical expansion
            top_grid.attach(knob_dropdown, i, 1, 1, 1)

            # Fader
            fader_label = Gtk.Label(label=f"fader_{i}")
            fader_label.set_halign(Gtk.Align.CENTER)
            top_grid.attach(fader_label, i, 2, 1, 1)

            fader_dropdown = self.create_multi_dropdown(f"FADER_{i}")
            fader_dropdown.set_halign(Gtk.Align.FILL)
            fader_dropdown.set_hexpand(True)
            fader_dropdown.set_vexpand(True)  # Allow vertical expansion
            top_grid.attach(fader_dropdown, i, 3, 1, 1)


            fader_buttons_label = Gtk.Label(label=f"buttons_{i}")
            fader_buttons_label.set_halign(Gtk.Align.CENTER)
            top_grid.attach(fader_buttons_label, i, 4, 1, 1)

            # Buttons to the right of the fader with dropdowns
            for j in range(4):
                dropdown = self.create_multi_dropdown(f"BUTTON_{i}_{j}")
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
            dropdown = self.create_multi_dropdown(f"CONTROL_{i}")
            dropdown.set_halign(Gtk.Align.FILL)
            dropdown.set_hexpand(True)
            dropdown.set_vexpand(False)  # Prevent full vertical expansion
            dropdown.set_size_request(20, 8)  # Minimum height
            bottom_grid.attach(dropdown, i, 1, 1, 1)

    def on_save(self, widget):
        print("Save menu item clicked!")
        # Add your save functionality here
        # Need to work on a new system of saving the data
        # Will implement a uuid system into controlfunction and a get_identiffiable_info methdo that returns plugin name, function name, uuid
        # There will be a component ID that maps an ID to a function and when saving the function it will take the ID from the component and get the function and store based on the get_identifiable_info
        data = {
            'module_fn_name_to_function': MixerBoard.module_fn_name_to_function,
            'component_to_module': MixerBoard.component_to_module_name,
            'extra_args': MixerBoard.extra_args,
        }
        self.config.save_raw(data, "page.yaml")

    def on_quit(self, widget):
        print("Quit menu item clicked!")
        Gtk.main_quit()
        self.destroy()

    def create_multi_dropdown(self, identifier):
        """Create a button that mimics the dropdown behavior."""
        button = Gtk.Button(label="Select...")
        button.connect("clicked", self.show_menu, identifier)

        # Set alignment to match the dropdown behavior
        button.set_halign(Gtk.Align.FILL)
        button.set_hexpand(True)
        button.set_vexpand(False)  # Match dropdown behavior
        button.set_size_request(20, 8)  # Minimum height (same as dropdown)
        label = button.get_child()
        if isinstance(label, Gtk.Label):
            # Set ellipsize mode
            label.set_ellipsize(Pango.EllipsizeMode.END)
        #css_provider = Gtk.CssProvider()
        #css_provider.load_from_data(b"""
        #    button {
        #        font-size: 12px; /* Adjust font size here */
        #    }
        #""")
        #button.get_style_context().add_provider(
        #    css_provider,
        #    Gtk.STYLE_PROVIDER_PRIORITY_USER,
        #)

        return button

    def show_menu(self, button, identifier):
        """Show a multi-level menu when the button is clicked."""
        # Create the main menu
        menu = Gtk.Menu()

        match identifier.split("_")[0]:
            case "KNOB":
                # Convert from 
                categories = self.knob_functions
            case "FADER":
                categories = self.fader_functions
            case "BUTTON" | "CONTROL":
                categories = self.button_functions
            case _:
                raise ValueError(f"Invalid identifier: {identifier}")

        categories["Clear"] = ["Clear"]

        # Example categories and options

        for category, options in categories.items():
            # Create a menu item for each category
            category_item = Gtk.MenuItem(label=category)
            menu.append(category_item)

            if category == "Clear":
                category_item.connect("activate", self.on_option_selected, button, identifier)
                continue

            # Create a submenu for the category
            submenu = Gtk.Menu()
            for option in options:
                name = str(option)
                if name not in MixerBoard.module_fn_name_to_function:
                    MixerBoard.module_fn_name_to_function[name] = option
                option_item = Gtk.MenuItem(label=name)
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
        if selected_value == "Clear":
            self.clear_function(button, identifier)
            selected_value = "Select..."
        else:
            args = []
            function = MixerBoard.module_fn_name_to_function[selected_value]
            extra_args = function.get_callback_extra_args()
            if extra_args:
                for arg in extra_args:
                    while True:
                        # Display a dialog to get the extra argument
                        dialog = InputDialog(
                        parent=self,
                        title=f"Enter {arg.get_name()}",
                        description=arg.get_description(),
                        default_value=arg.get_default(),
                        input_type=arg.get_type(),
                        # Call the get_options method if it exists
                        options=arg.get_options()() if arg.get_options() else None,
                        )
                        response = dialog.run()
    
                        if response == Gtk.ResponseType.OK:
                            value = arg.get_type()(dialog.get_input_value())
                            if arg.get_criteria_callback() and not arg.get_criteria_callback()(value):
                                print(f"Invalid value for {arg.get_name()}: {value}")
                                continue
                            args.append(arg.get_type()(dialog.get_input_value()))
                            dialog.destroy()
                            break
                            print(f"User entered: {value}")
                        else:
                            print("Dialog was cancelled.")
                            dialog.destroy()
                            continue
                        
                MixerBoard.extra_args[identifier] = tuple(args)
            
        MixerBoard.component_to_module_name[identifier] = selected_value
        #button.set_label(selected_value)  # Update button label
        print(f"Selected for {identifier}: {selected_value}")

        label = button.get_child()
        if isinstance(label, Gtk.Label):
            #label.set_ellipsize(Pango.EllipsizeMode.END)
            label.set_text(selected_value)
            label.set_size_request(20, 8)

    def clear_function(self, button, identifier):
        """Clear the selected function."""
        MixerBoard.component_to_module_name[identifier] = None
        label = button.get_child()
        if isinstance(label, Gtk.Label):
            label.set_text("Select...")

    def start(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

class InputDialog(Gtk.Dialog):
    def __init__(self, parent, title, description, default_value, input_type, options=None):
        """
        :param parent: The parent window.
        :param title: Title of the dialog.
        :param description: Description of the input field.
        :param default_value: Default value for the input field.
        :param input_type: The type of input field (int, float, str, list).
        :param options: Options for ComboBox, required if input_type is list.
        """
        super().__init__(title=title, transient_for=parent, flags=0)

        # Add buttons to the dialog
        self.add_button("OK", Gtk.ResponseType.OK)

        # Set up the dialog content area
        self.set_default_size(300, 150)
        content_area = self.get_content_area()

        # Add a description label
        label = Gtk.Label(label=description)
        label.set_line_wrap(True)
        content_area.pack_start(label, True, True, 10)

        if options is None:
            # Create an input field based on the input type
            if input_type == int:
                self.input_field = Gtk.SpinButton()
                self.input_field.set_adjustment(Gtk.Adjustment(default_value, -1e6, 1e6, 1, 10, 0))
            elif input_type == float:
                self.input_field = Gtk.SpinButton()
                self.input_field.set_adjustment(Gtk.Adjustment(default_value, -1e6, 1e6, 1, 10, 0))
                self.input_field.set_digits(4)
            elif input_type == str:
                self.input_field = Gtk.Entry()
                self.input_field.set_text(str(default_value))
            else:
                raise ValueError(f"Unsupported input type: {input_type}")
        else:
            self.input_field = Gtk.ComboBoxText()
            for option in options:
                self.input_field.append_text(option)
            self.input_field.set_active(0)  # Set default selection to the first option

        content_area.pack_start(self.input_field, False, False, 10)

        self.show_all()

    def get_input_value(self):
        """
        Get the value entered or selected by the user in the dialog.

        :return: The input value (string, number, or selected option).
        """
        if isinstance(self.input_field, Gtk.Entry):
            return self.input_field.get_text()
        elif isinstance(self.input_field, Gtk.SpinButton):
            return self.input_field.get_value()
        elif isinstance(self.input_field, Gtk.ComboBoxText):
            return self.input_field.get_active_text()
        return None
