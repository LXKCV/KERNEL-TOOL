#include "notes_service.h"
#include <nlohmann/json.hpp>
#include <fstream>

namespace services {
void NotesService::load(){std::ifstream in(path_.toStdString()); if(!in) return; nlohmann::json j; in>>j; for(auto& n:j) notes_.push_back({QString::fromStdString(n["title"]),QString::fromStdString(n["category"]),QString::fromStdString(n["body"])});} 
void NotesService::save() const { nlohmann::json j=nlohmann::json::array(); for(auto& n:notes_) j.push_back({{"title",n.title.toStdString()},{"category",n.category.toStdString()},{"body",n.body.toStdString()}}); std::ofstream out(path_.toStdString()); out<<j.dump(2);} 
void NotesService::add(const FormulaNote& note){notes_.push_back(note); save();}
std::vector<FormulaNote> NotesService::all() const { return notes_; }
}
