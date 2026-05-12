#pragma once
#include <QString>
#include <vector>

namespace services {
struct FormulaNote { QString title; QString category; QString body; };
class NotesService {
public:
    void load();
    void save() const;
    void add(const FormulaNote& note);
    std::vector<FormulaNote> all() const;
private:
    QString path_{"data/notes.json"};
    std::vector<FormulaNote> notes_;
};
}
