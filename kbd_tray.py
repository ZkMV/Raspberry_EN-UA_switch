import glob, time, gi
gi.require_version("Gtk","3.0")
gi.require_version("AyatanaAppIndicator3","0.1")
from gi.repository import Gtk, GLib, AyatanaAppIndicator3 as AppIndicator

def find_scroll_led():
    paths = sorted(glob.glob("/sys/class/leds/*scrolllock*/brightness"))
    return paths[0] if paths else None

BR_PATH = find_scroll_led()

def led_on():
    try:
        with open(BR_PATH,"r") as f:
            return f.read().strip() == "1"
    except Exception:
        return False

class Tray:
    def __init__(self):
        self.ind = AppIndicator.Indicator.new("kbd-scroll", "en", AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        m=Gtk.Menu(); q=Gtk.MenuItem(label="Quit"); q.connect("activate", lambda *_: Gtk.main_quit()); m.append(q); m.show_all()
        self.ind.set_menu(m)
        self.cur=None
        GLib.timeout_add(200, self.tick)

    def tick(self):
        state = led_on()
        icon = "ua" if state else "en"
        if icon != self.cur:
            self.cur = icon
            self.ind.set_icon(icon)   # en/ua з теми hicolor
        return True

if __name__=="__main__":
    if not BR_PATH:
        # немає ScrollLock у системі
        print("No ScrollLock LED found at /sys/class/leds/*scrolllock*/brightness")
    else:
        Tray(); Gtk.main()