#pragma once
#include <QString>
#include <vector>

namespace services {
struct HistoryEntry { QString expr; QString result; QString timestamp; };
class HistoryService {
public:
    void initialize();
    void add(const QString& expr, const QString& result);
    void clear();
    std::vector<HistoryEntry> list() const;
private:
    QString path_{"data/history.json"};
    std::vector<HistoryEntry> entries_;
    void persist() const;
};
}
