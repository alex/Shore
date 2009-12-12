#include "str.h"

static shore::builtin__str* shore::builtin__str:new_instance(std::string value_) {
    builtin__str* val = new shore::builtin__str(value_);
    shore::GC::register_object(val);
    return val;
}

shore::builtin__str* shore::builtin__str::__mul__(shore::builtin__int* other) {
    std::string s;
    s.reserve(this->value.size() * other->value);
    for (long long i = 0; i < other->value; i++) {
        s.append(this->value);
    }
    return shore::builtin__str::new_instance(s);
}

