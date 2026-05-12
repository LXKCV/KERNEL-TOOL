#pragma once
#include <memory>

namespace ui { class MainWindow; }
namespace services { class SettingsService; class HistoryService; class NotesService; }

namespace app {
class ApplicationController {
public:
    ApplicationController();
    void start();
private:
    std::unique_ptr<ui::MainWindow> mainWindow_;
    std::unique_ptr<services::SettingsService> settings_;
    std::unique_ptr<services::HistoryService> history_;
    std::unique_ptr<services::NotesService> notes_;
};
}
