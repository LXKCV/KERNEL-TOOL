#include "application_controller.h"
#include "ui/main_window.h"
#include "services/settings_service.h"
#include "services/history_service.h"
#include "services/notes_service.h"

namespace app {
ApplicationController::ApplicationController()
    : settings_(std::make_unique<services::SettingsService>()),
      history_(std::make_unique<services::HistoryService>()),
      notes_(std::make_unique<services::NotesService>()) {}

void ApplicationController::start() {
    settings_->load();
    history_->initialize();
    notes_->load();
    mainWindow_ = std::make_unique<ui::MainWindow>(*settings_, *history_, *notes_);
    mainWindow_->show();
}
}
