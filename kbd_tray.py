import glob
import gi

# Ensure specific versions of Gtk and AppIndicator are used
gi.require_version("Gtk", "3.0")
gi.require_version("AyatanaAppIndicator3", "0.1")

from gi.repository import Gtk, GLib, AyatanaAppIndicator3 as AppIndicator

class Tray:
    def __init__(self):
        # Initialize indicator with default icon "en"
        self.ind = AppIndicator.Indicator.new(
            "kbd-scroll", 
            "en", 
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        # Create the menu
        menu = Gtk.Menu()
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", lambda *_: Gtk.main_quit())
        menu.append(quit_item)
        menu.show_all()
        self.ind.set_menu(menu)

        # Track current state to avoid unnecessary updates
        self.cur = "en"

        # Check status every 200 ms
        GLib.timeout_add(200, self.tick)

    def tick(self):
        """
        Check the Scroll Lock LED status dynamically.
        Logic:
        - If the LED file is found: read status and update icon (en/ua).
        - If the LED file is NOT found (keyboard sleep/disconnected): DO NOTHING. Keep the last known icon.
        """
        # Search for the LED path every tick because BT keyboards change input IDs or disappear
        paths = glob.glob("/sys/class/leds/*scrolllock*/brightness")

        # Case 1: Keyboard is asleep or disconnected
        if not paths:
            # Do nothing, keep the current icon state
            return True

        # Case 2: Keyboard is active
        try:
            # Use the first found path
            path = paths[0]
            with open(path, "r") as f:
                content = f.read().strip()
                # Assuming '1' means ON (UA) and '0' means OFF (EN)
                is_ua = (content == "1")

            new_icon = "ua" if is_ua else "en"

            # Update the tray icon only if the state has changed
            if new_icon != self.cur:
                self.cur = new_icon
                self.ind.set_icon(new_icon)

        except Exception:
            # Handle cases where the file disappears during read (race condition)
            # Do nothing, try again next tick
            pass

        return True

if __name__ == "__main__":
    # Start the tray icon unconditionally
    # It will wait for the keyboard to appear
    Tray()
    Gtk.main()
