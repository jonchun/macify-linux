# macify-linux
Automated setup scripts to transform Linux into macOS.

## Intro
This project was started because I grew obsessed with the idea of making the macOS-like experience available for free. I am personally sick of vendor-locking from Apple, so am excited about moving to Linux, and want to make this available to others as well who might not be willing to put in the time into customization, or find it hard to get started.

Please feel free to open issues with comments/suggestions.

## Goals
- Must be relatively easy for users new to Linux to start using. This is why an Ubuntu-based distro was chosen.
- Must be easy for developers used to macOS to start using in this setup. They should have their workflow impacted minimally in terms of the available hotkeys, software, etc.

** WARNING: ** This utility is currently pre-alpha. It is absolutely not ready for a full release. However, it

## Installation
First, you need to be on a fresh install of KDE Neon
```
wget https://raw.githubusercontent.com/Jonchun/macify-linux/master/install.sh
bash install.sh
```

## Screenshots
Script Finished Installing:
![macify-linux-1.png](https://raw.githubusercontent.com/Jonchun/macify-linux/master/images/macify-linux-1.png)

Global Menu:
![macify-linux-2.png](https://raw.githubusercontent.com/Jonchun/macify-linux/master/images/macify-linux-2.png)

Notification Center alternative:
![macify-linux-3.png](https://raw.githubusercontent.com/Jonchun/macify-linux/master/images/macify-linux-3.png)
![macify-linux-4.png](https://raw.githubusercontent.com/Jonchun/macify-linux/master/images/macify-linux-4.png)

Spotlight search alternative (Albert):
![macify-linux-5.png](https://raw.githubusercontent.com/Jonchun/macify-linux/master/images/macify-linux-5.png)

## Notes
This is definitely a "rough draft" of the script! PLEASE DO NOT USE IT IN ANYTHING OTHER THAN A VM!

## TODO
- Make the installer interactive so you can choose light/dark and more
- Work on customizing widgets so they don't look like they're about to pop out of their panels
- Test on hardware instead of only VMs