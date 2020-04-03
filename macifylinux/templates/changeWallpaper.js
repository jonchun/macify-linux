/* global desktops */
const all_desktops = desktops();                                                                                                                       
for (let i=0; i < all_desktops.length; i++) {
    const current_desktop = all_desktops[i];
    current_desktop.wallpaperPlugin = "org.kde.image";
    current_desktop.currentConfigGroup = Array("Wallpaper",
                                "org.kde.image",
                                "General");
    current_desktop.writeConfig("Image", "file://$IMAGE_PATH");
}
