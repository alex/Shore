#ifndef _SHORE_BOOL_H
#define _SHORE_BOOL_H

#include "gc.h"


namespace shore {
    class builtin__bool {
        public:
            bool value;
            
            static builtin__bool* new_instance(bool value_) {
                return shore::GC::register_object(new builtin__bool(value_));
            }
            
            builtin__bool(bool value_) {
                this->value = value_;
            }
            
            builtin__bool* __bool__() {
                return builtin__bool::new_instance(this->value);
            }
    };
}
#endif
