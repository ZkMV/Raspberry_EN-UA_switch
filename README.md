# Write a downloadable README.md file to /mnt/data
readme = r"""# EN/UA Tray Indicator (Wayland/Wayfire, Raspberry Pi OS)

Невеликий трей‑індикатор **EN/UA** для Raspberry Pi OS (Bookworm, Wayfire/wf-panel-pi).
Показує **EN** або **UA** залежно від стану **Scroll Lock**.  
Ідея: у системних налаштуваннях прив’язуємо індикатор розкладки до Scroll Lock, а скрипт читає його стан із `/sys/class/leds/*scrolllock*/brightness`.

> Працює без fcitx/ibus. Потрібна наявність ScrollLock LED у ядрі для вашої клавіатури.

---

## Вимоги

- Raspberry Pi OS **Bookworm** (Wayland / **Wayfire**, панель **wf-panel-pi** із System Tray).
- Пакети:
  ```bash
  sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
       gir1.2-ayatanaappindicator3-0.1 libgtk-3-bin
Структура репозиторію
Always show details

Copy code
.
├── README.md
├── kbd_tray.py
└── icons/
    ├── 22x22/
    │   ├── en.png
    │   └── ua.png
    └── 24x24/
        ├── en.png
        └── ua.png
```
kbd_tray.py — Python‑скрипт трея (Ayatana AppIndicator).

icons/.../en.png, icons/.../ua.png — іконки з прапорами для 22×22 та 24×24.

Інсталяція
Скопіювати скрипт у домашній bin

bash
Always show details

Copy code
mkdir -p ~/bin
cp kbd_tray.py ~/bin/
chmod +x ~/bin/kbd_tray.py
Встановити іконки у тему hicolor (локально для користувача)

bash
Always show details

Copy code
mkdir -p ~/.local/share/icons/hicolor/22x22/status
mkdir -p ~/.local/share/icons/hicolor/24x24/status
cp icons/22x22/en.png ~/.local/share/icons/hicolor/22x22/status/en.png
cp icons/22x22/ua.png ~/.local/share/icons/hicolor/22x22/status/ua.png
cp icons/24x24/en.png ~/.local/share/icons/hicolor/24x24/status/en.png
cp icons/24x24/ua.png ~/.local/share/icons/hicolor/24x24/status/ua.png

# один раз підкласти index.theme (якщо ще нема) та оновити кеш іконок
cp /usr/share/icons/hicolor/index.theme ~/.local/share/icons/hicolor/ 2>/dev/null || true
gtk-update-icon-cache -f ~/.local/share/icons/hicolor
Прив’язати розкладку до Scroll Lock (разово)

Відкрий: Preferences → Mouse and Keyboard Settings → Keyboard → Set Layout…

Поле Indicator = Scroll Lock.
(Toggle Key лишається будь‑який твій, напр. Ctrl+Shift.)

Перевірити, що ядро бачить Scroll Lock

bash
Always show details

Copy code
cat /sys/class/leds/*scrolllock*/brightness
# Натисни хоткей перемикання — значення має змінюватись між 0 ↔ 1.
Запустити індикатор

bash
Always show details

Copy code
python3 ~/bin/kbd_tray.py &
Автозапуск після входу

bash
Always show details

Copy code
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/kbd_tray.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Keyboard Tray
Exec=/usr/bin/env python3 /home/$USER/bin/kbd_tray.py
EOF
Готово: при перемиканні розкладки іконка в треї міняється EN ⇄ UA.

Використання
Скрипт не змінює розкладок — лише читає стан Scroll Lock і ставить іконку en/ua.

Іконки підхоплюються з локальної теми: ~/.local/share/icons/hicolor/**/status/en.png|ua.png.

Діагностика
Трей показує стандартну «клавіатуру»
Онови кеш і вийди/зайди в сесію:

bash
Always show details

Copy code
gtk-update-icon-cache -f ~/.local/share/icons/hicolor
Іконка не змінюється
Переконайся, що Scroll Lock тикається разом із розкладкою:

bash
Always show details

Copy code
cat /sys/class/leds/*scrolllock*/brightness
Якщо файлу немає — ця клавіатура/драйвер не експонує ScrollLock у /sys.

Видалення
bash
Always show details

Copy code
pkill -f kbd_tray.py 2>/dev/null
rm -f ~/.config/autostart/kbd_tray.desktop ~/bin/kbd_tray.py
rm -f ~/.local/share/icons/hicolor/22x22/status/en.png ~/.local/share/icons/hicolor/22x22/status/ua.png
rm -f ~/.local/share/icons/hicolor/24x24/status/en.png ~/.local/share/icons/hicolor/24x24/status/ua.png
gtk-update-icon-cache -f ~/.local/share/icons/hicolor
Примітки
Проєкт для Wayland/Wayfire. На X11 стандартні індикатори розкладки працюють інакше.

Якщо клавіатура не має ScrollLock LED у /sys, потрібен інший транспорт (IME з API або плагін панелі).
"""

with open("/mnt/data/README.md", "w", encoding="utf-8") as f:
f.write(readme)

"/mnt/data/README.md"


----------
# EN/UA Tray Indicator for Raspberry Pi OS (Labwc & Wayfire)

Невеликий трей-індикатор **EN/UA** для Raspberry Pi OS (Bookworm).  
Працює як на **Labwc** (новий стандарт), так і на **Wayfire**.

Показує **EN** або **UA** залежно від стану **Scroll Lock** LED.  
Скрипт динамічно відстежує підключення клавіатури: якщо це Bluetooth-клавіатура, яка "засинає", індикатор коректно очікує її пробудження, не вилітаючи з помилкою.

---

## History / Історія змін

### v02 (Current)

- **Labwc Support:** Перевірено та адаптовано для роботи в середовищі Labwc (RPi OS за замовчуванням).
- **Dynamic Hotplug:** Скрипт більше не падає, якщо клавіатура відсутня при запуску або йде в сон (Bluetooth).
- **Improved Autostart:** Додано затримку (`sleep`) при запуску, щоб іконка гарантовано з'являлася в треї після завантаження графіки.

### v01

- Початкова версія для Wayfire.
- Базова підтримка Scroll Lock LED.

---

## Вимоги

- Raspberry Pi OS **Bookworm** (Labwc або Wayfire).
- Системний трей (wf-panel-pi).
- Пакети Python:

```bash
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
     gir1.2-ayatanaappindicator3-0.1 libgtk-3-bin
```
