#pragma once
#include <string>
#include <optional>

namespace core {
struct EvalResult { bool ok{}; double value{}; std::string error; };
class ExpressionEngine {
public:
    EvalResult evaluate(const std::string& expr, bool degreesMode = false) const;
};
}
