#include "int.h"


namespace shore {
    builtin__int* builtin__int::new_instance(long long value_) {
        shore::builtin__int* val = new builtin__int(value_);
        shore::GC::register_object(val);
        return val;
    }

    builtin__int* builtin__int::new_instance(shore::builtin__str* value_) {
        long long v = 0;
        for (size_t i = 0; i < value_->value.size(); i++) {
            // TODO: Handle values that aren't integers properly
            v += (value_->value[i] - 48) * std::pow(10, value_->value.size()-i-1);
        }
        return builtin__int::new_instance(v);
    }

    builtin__int::builtin__int(long long value_) {
        this->value = value_;
    }
                
    builtin__bool* shore::builtin__int::__eq__(shore::builtin__int* other) {
        return builtin__bool::new_instance(this->value == other->value);
    }

    builtin__bool* shore::builtin__int::__ne__(shore::builtin__int* other) {
        return builtin__bool::new_instance(this->value != other->value);
    }

    builtin__bool* shore::builtin__int::__lt__(shore::builtin__int* other) {
        return builtin__bool::new_instance(this->value < other->value);
    }

    shore::builtin__bool* shore::builtin__int::__gt__(shore::builtin__int* other) {
        return builtin__bool::new_instance(this->value > other->value);
    }

    shore::builtin__int* shore::builtin__int::__add__(shore::builtin__int* other) {
        return shore::builtin__int::new_instance(this->value + other->value);
    }

    shore::builtin__int* shore::builtin__int::__sub__(shore::builtin__int* other) {
        return shore::builtin__int::new_instance(this->value - other->value);
    }

    shore::builtin__int* shore::builtin__int::__mul__(shore::builtin__int* other) {
        return shore::builtin__int::new_instance(this->value * other->value);
    }
}
