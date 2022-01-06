from ursina import *
import os


SCORE_FILE = "previous_score.txt"
if not os.path.isfile(SCORE_FILE):
    with open(SCORE_FILE, "w+") as f:
        f.write(str(0))


def read_previous_score():
    with open(SCORE_FILE, "r") as f:
        hs = f.read()
        global high_score_text
        high_score_text = Text(hs)
        high_score_text.enabled = True
        high_score_text.position = (0, .1)
        high_score_text.origin = (0, 0)


# Class of game menu
class MenuMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)

        # Create empty entities that will be parents of our menus content
        self.main_menu = Entity(parent=self, enabled=True)
        self.previous_score_menu = Entity(parent=self, enabled=False)
        self.help_menu = Entity(parent=self, enabled=False)

        # Add a background. You can change 'shore' to a different texture of you'd like.
        self.background = Sprite(
            '/assets/main_menu.png/', color=color.dark_gray, z=1)

        # [MAIN MENU] WINDOW START
        # Title of our menu
        Text("Virus Fighter", parent=self.main_menu, y=0.4, x=0, origin=(0, 0))

        def start_game_btn():
            self.main_menu.disable()
            self.background.disable()
            import app

        # Reference of our action function for quit button
        def quit_game():
            application.quit()

        # Reference of our action function for previous_score button
        def previous_score_menu_btn():
            read_previous_score()
            self.previous_score_menu.enable()
            self.main_menu.disable()

        # Reference of our action function for help button
        def help_menu_btn():
            self.help_menu.enable()
            self.main_menu.disable()

        # Button list
        ButtonList(button_dict={
            "Start": Func(start_game_btn),
            "Previous Score": Func(previous_score_menu_btn),
            "Help": Func(help_menu_btn),
            "Exit": Func(quit_game)
        }, y=0, parent=self.main_menu)
        # [MAIN MENU] WINDOW END

        # [SCORE MENU] WINDOW START
        # Title of our menu
        Text("Previous Score", parent=self.previous_score_menu,
             y=0.4, x=0, origin=(0, 0))

        # Reference of our action function for back button
        def previous_score_back_btn_action():
            high_score_text.enabled = False
            self.main_menu.enable()
            self.previous_score_menu.disable()

        # Button
        Button("Back", parent=self.previous_score_menu, y=-0.3, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=previous_score_back_btn_action)

        # [HIGH SCORES MENU] WINDOW END

        # [HELP MENU] WINDOW START
        # Title of our menu
        Text("HELP MENU", parent=self.help_menu, y=0.4, x=0, origin=(0, 0))

        # Reference of our action function for back button
        def help_back_btn_action():
            about.enabled = False
            controls.enabled = False
            self.main_menu.enable()
            self.help_menu.disable()

        about = Text('Hello there')
        about.enabled = False
        about.position = (0, .1)
        about.origin = (0, 0)

        def enable_about_info():
            controls.enabled = False
            about.enabled = True

        controls = Text("WASD to move.\nSpace to shoot.\nEasy peasy!")
        controls.enabled = False
        controls.position = (0, .1)
        controls.origin = (0, 0)

        def enable_controls_info():
            about.enabled = False
            controls.enabled = True

        # Button list
        ButtonList(button_dict={
            "About": Func(enable_about_info),
            "Controls": Func(enable_controls_info),
            "Back": Func(help_back_btn_action)
        }, y=0, parent=self.help_menu)
        # [HELP MENU] WINDOW END

        # Here we can change attributes of this class when call this class
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Input function that check if key pressed on keyboard
    def input(self, key):
        # And if you want use same keys on different windows
        # Like [Escape] or [Enter] or [Arrows]
        # Just write like that:

        # If our main menu enabled and we press [Escape]
        if self.main_menu.enabled:
            if key == "escape":
                # Close app
                application.quit()

        # If our previous_score menu enabled and we press [Escape]
        if self.previous_score_menu.enabled:
            if key == "escape":
                # Close previous_score window and show main menu
                self.main_menu.enable()
                self.previous_score_menu.disable()

        # If our help menu enabled and we press [Escape]
        if self.help_menu.enabled:
            if key == "escape":
                # Close help window and show main menu
                self.main_menu.enable()
                self.help_menu.disable()

    # Update function that check something every frame
    # You can use it similar to input with checking
    # what menu is currently enabled
    def update(self):
        pass


# Setup window title
window.title = "Virus Fighter"

# Init application
app = Ursina()

# Call our menu
main_menu = MenuMenu()

# Run application
app.run()
