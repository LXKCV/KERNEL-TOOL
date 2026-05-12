#pragma once
#include <QString>
#include <nlohmann/json.hpp>

namespace services {
class SettingsService {
public:
    void load();
    void save() const;
    bool soundEnabled{false};
    bool degreesMode{true};
    QString theme{"themes/dark.qss"};
private:
    QString path_{"data/settings.json"};
};
}
