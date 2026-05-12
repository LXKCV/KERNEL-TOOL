#include "main_window.h"
#include "services/settings_service.h"
#include "services/history_service.h"
#include "services/notes_service.h"
#include "core/expression_engine.h"
#include <QHBoxLayout>
#include <QListWidget>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QWidget>

namespace ui {
MainWindow::MainWindow(services::SettingsService& s, services::HistoryService& h, services::NotesService& n, QWidget* parent)
    : QMainWindow(parent), settings_(s), history_(h), notes_(n) {
    setWindowTitle("ProCalcX");
    resize(1200, 760);
    buildUi();
}

void MainWindow::buildUi() {
    auto* root = new QWidget(this);
    auto* row = new QHBoxLayout(root);
    auto* nav = new QListWidget(root);
    nav->addItems({"Basic", "Scientific", "Programmer", "Converter", "Notes", "History", "Graph", "Solver"});
    nav->setMaximumWidth(220);

    pages_ = new QStackedWidget(root);

    auto* basicPage = new QWidget;
    auto* basicLayout = new QVBoxLayout(basicPage);
    auto* input = new QLineEdit;
    auto* output = new QLabel("0");
    auto* evalBtn = new QPushButton("Evaluate");
    basicLayout->addWidget(input); basicLayout->addWidget(output); basicLayout->addWidget(evalBtn);
    pages_->addWidget(basicPage);

    for (int i=1;i<8;++i){ auto* p=new QWidget; auto* l=new QVBoxLayout(p); l->addWidget(new QLabel("Module scaffold ready")); pages_->addWidget(p);}    
    row->addWidget(nav);
    row->addWidget(pages_, 1);
    setCentralWidget(root);

    auto* engine = new core::ExpressionEngine();
    connect(evalBtn, &QPushButton::clicked, this, [=, this]() {
        auto r = engine->evaluate(input->text().toStdString(), settings_.degreesMode);
        if (r.ok) { output->setText(QString::number(r.value)); history_.add(input->text(), output->text()); }
        else output->setText(QString::fromStdString(r.error));
    });
    connect(nav, &QListWidget::currentRowChanged, pages_, &QStackedWidget::setCurrentIndex);
    nav->setCurrentRow(0);
}
}
