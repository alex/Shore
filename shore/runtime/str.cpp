#include <sstream>

#include "str.h"


namespace shore {
    builtin__str* builtin__str::new_instance(std::string value_) {
        builtin__str* val = new shore::builtin__str(value_);
        shore::GC::register_object(val);
        return val;
    }
    
    builtin__str* builtin__str::new_instance(builtin__int* value_) {
        std::stringstream ss;
        ss << value_->value;
        return builtin__str::new_instance(ss.str());
    }

    builtin__str::builtin__str(std::string value_) {
        this->value = value_;
    }

    shore::builtin__str* shore::builtin__str::__add__(shore::builtin__str* other) {
        return shore::builtin__str::new_instance(this->value + other->value);
    }

    shore::builtin__str* shore::builtin__str::__mul__(shore::builtin__int* other) {
        std::string s;
        s.reserve(this->value.size() * other->value);
        for (long long i = 0; i < other->value; i++) {
            s.append(this->value);
        }
        return shore::builtin__str::new_instance(s);
    }
}
