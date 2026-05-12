#include "settings_service.h"
#include <fstream>

namespace services {
void SettingsService::load() {
    std::ifstream in(path_.toStdString());
    if (!in) return;
    nlohmann::json j; in >> j;
    soundEnabled = j.value("soundEnabled", false);
    degreesMode = j.value("degreesMode", true);
    theme = QString::fromStdString(j.value("theme", "themes/dark.qss"));
}
void SettingsService::save() const {
    nlohmann::json j{{"soundEnabled", soundEnabled},{"degreesMode", degreesMode},{"theme", theme.toStdString()}};
    std::ofstream out(path_.toStdString());
    out << j.dump(2);
}
}
