function areArraysEqualSets(a1, a2) {
// https://stackoverflow.com/a/55614659
  let superSet = {};
  for (let i = 0; i < a1.length; i++) {
    const e = a1[i] + typeof a1[i];
    superSet[e] = 1;
  }

  for (let i = 0; i < a2.length; i++) {
    const e = a2[i] + typeof a2[i];
    if (!superSet[e]) {
      return false;
    }
    superSet[e] = 2;
  }

  for (let e in superSet) {
    if (superSet[e] === 1) {
      return false;
    }
  }

  return true;
}

function isPanelDefault(panel) {
    const widgets = panel.widgets();
    const widgetArray = [];
    const defaultArray = [
        "org.kde.plasma.kickoff",
        "org.kde.plasma.pager",
        "org.kde.plasma.taskmanager",
        "org.kde.plasma.systemtray",
        "org.kde.plasma.digitalclock",
        "org.kde.plasma.showdesktop"
    ];

    for (var widgetIndex = 0; widgetIndex < widgets.length; widgetIndex++) {
        var w = widgets[widgetIndex];
        widgetArray.push(w.type)
    }

    if (areArraysEqualSets(defaultArray, widgetArray)) {
        return true;
    } else {
        return false;
    }
}

// Delete all existing desktop panels
function removeDefaultPanels() {
    const allPanels = panels();

    for (let panelIndex = 0; panelIndex < allPanels.length; panelIndex++) {
        const p = allPanels[panelIndex];
        if (p.type === "org.kde.panel" && isPanelDefault(p)) {
            p.remove();
        }
    }
}

removeDefaultPanels();