#include "history_service.h"
#include <nlohmann/json.hpp>
#include <fstream>
#include <QDateTime>

namespace services {
void HistoryService::initialize(){std::ifstream in(path_.toStdString()); if(!in) return; nlohmann::json j; in>>j; for(auto& e:j) entries_.push_back({QString::fromStdString(e["expr"]),QString::fromStdString(e["result"]),QString::fromStdString(e["timestamp"])});} 
void HistoryService::add(const QString& expr, const QString& result){entries_.push_back({expr,result,QDateTime::currentDateTime().toString(Qt::ISODate)});persist();}
void HistoryService::clear(){entries_.clear();persist();}
std::vector<HistoryEntry> HistoryService::list() const { return entries_; }
void HistoryService::persist() const { nlohmann::json j=nlohmann::json::array(); for (auto& e:entries_) j.push_back({{"expr",e.expr.toStdString()},{"result",e.result.toStdString()},{"timestamp",e.timestamp.toStdString()}}); std::ofstream out(path_.toStdString()); out<<j.dump(2);} 
}
