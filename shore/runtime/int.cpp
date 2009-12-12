#include "int.h"

static shore::builtin__int* shore::builtin__int::new_instance(long long value_) {
    shore::builtin__int* val = new shore::builtin__int(value_);
    shore::GC::register_object(val);
    return val;
}

static shore::builtin__int* shore::builtint__int::new_instance(shore::builtin__str* value_) {
    long long v = 0;
    for (size_t i = value_->value.size()-1; i >= 0; i--;) {
        // TODO: Handle values that aren't integers properly
        v += (value_->value[i] - 30) * std::pow(10, i);
    }
    return shore::builtin__int::new_instance(v);
}

shore::builtin__int(long long value_) {
    this->value = value_;
}
            
shore::builtin__bool* __eq__(shore::builtin__int* other) {
    return shore::builtin__bool::new_instance(this->value == other->value);
}

