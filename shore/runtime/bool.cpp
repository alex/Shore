#include "bool.h"

namespace shore {
    builtin__bool* builtin__bool::new_instance(bool value_) {
        builtin__bool* val = new builtin__bool(value_);
        shore::GC::register_object(val);
        return val;
    }
    
    builtin__bool::builtin__bool(bool value_) {
        this->value = value_;
    }
    
    builtin__bool* builtin__bool::__bool__() {
        return builtin__bool::new_instance(this->value);
    }
}
