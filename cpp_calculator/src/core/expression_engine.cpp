#include "expression_engine.h"
#include <cmath>
#include <stack>
#include <sstream>

namespace core {
EvalResult ExpressionEngine::evaluate(const std::string& expr, bool degreesMode) const {
    try {
        std::stringstream ss(expr);
        double lhs = 0.0, rhs = 0.0; char op = 0;
        ss >> lhs;
        while (ss >> op >> rhs) {
            switch(op) {
                case '+': lhs += rhs; break;
                case '-': lhs -= rhs; break;
                case '*': lhs *= rhs; break;
                case '/': if (rhs == 0) return {false,0,"Division by zero"}; lhs /= rhs; break;
                case '%': lhs = std::fmod(lhs, rhs); break;
                case '^': lhs = std::pow(lhs, rhs); break;
                default: return {false,0,"Unsupported token"};
            }
        }
        return {true,lhs,{}};
    } catch (...) { return {false, 0, "Parse error"}; }
}
}
