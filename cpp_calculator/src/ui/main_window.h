#pragma once
#include <QMainWindow>
#include <QStackedWidget>

namespace services { class SettingsService; class HistoryService; class NotesService; }
namespace core { class ExpressionEngine; }

namespace ui {
class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(services::SettingsService&, services::HistoryService&, services::NotesService&, QWidget* parent = nullptr);
private:
    services::SettingsService& settings_;
    services::HistoryService& history_;
    services::NotesService& notes_;
    QStackedWidget* pages_{};
    void buildUi();
};
}
