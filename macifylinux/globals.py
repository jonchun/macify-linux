from pathlib import Path

G = {"LOCAL_DIRS": []}
# ==================== Start LOCAL_DIRS ====================
G["SOURCES_DIR"] = Path("~/sources/").expanduser()
G["LOCAL_DIRS"].append(G["SOURCES_DIR"])

G["ICONS_DIR"] = Path("~/.local/share/icons/").expanduser()
G["LOCAL_DIRS"].append(G["ICONS_DIR"])

G["FONTS_DIR"] = Path("~/.local/share/fonts/").expanduser()
G["LOCAL_DIRS"].append(G["FONTS_DIR"])

G["AURORAE_DIR"] = Path("~/.local/share/aurorae/themes/").expanduser()
G["LOCAL_DIRS"].append(G["AURORAE_DIR"])

G["COLOR_SCHEMES_DIR"] = Path("~/.local/share/color-schemes/").expanduser()
G["LOCAL_DIRS"].append(G["COLOR_SCHEMES_DIR"])

G["PLASMA_DIR"] = Path("~/.local/share/plasma/desktoptheme/").expanduser()
G["LOCAL_DIRS"].append(G["PLASMA_DIR"])

G["LOOK_FEEL_DIR"] = Path("~/.local/share/plasma/look-and-feel/").expanduser()
G["LOCAL_DIRS"].append(G["LOOK_FEEL_DIR"])

G["LAYOUTS_DIR"] = Path("~/.local/share/plasma/layout-templates/").expanduser()
G["LOCAL_DIRS"].append(G["LAYOUTS_DIR"])

G["KVANTUM_DIR"] = Path("~/.config/Kvantum/").expanduser()
G["LOCAL_DIRS"].append(G["KVANTUM_DIR"])

G["WALLPAPERS_DIR"] = Path("~/.local/share/wallpapers/").expanduser()
G["LOCAL_DIRS"].append(G["WALLPAPERS_DIR"])

# ==================== End LOCAL_DIRS ====================

G["COMPONENTS_DIR"] = Path(__file__).parent / Path("components")

G["DEFAULT_WALLPAPER"] = "kym-ellis-RPT3AjdXlZc-unsplash.jpg"

G["SDDM_THEMES_DIR"] = "/usr/share/sddm/themes"

GLOBALS = G

if __name__ == "__main__":
    # if this globals script is called directly, it outputs bash
    output = []
    for key, val in GLOBALS.items():
        if not (isinstance(val, str) or isinstance(val, Path)):
            continue
        output.append('{}="{}"'.format(key, str(val)))

    print("; ".join(output))
