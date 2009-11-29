#ifndef _SHORE_INT_H
#define _SHORE_INT_H

#include "gc.h"


namespace shore {
    class builtin__int {
        public:
            // Some day this will be arbitrary percision, but not today.
            long long value;
            
            static builtin__int* new_instance(long long value_) {
                return shore::GC::register_object(new builtin__int(value_));
            }
            
            builtin__int(long long value_) {
                this->value = value_;
            }
            
            builtin__bool* __eq__(builtin__int* other) {
                return builtin__bool::new_instance(this->value == other->value));
            }
            
            builtin__int* __add__(builtin__int* other) {
                return builtin__int::new_instance(this->value + other->value);
            }
            
            builtin__int* __sub__(builtin__int* other) {
                return builtin__int::new_instance(this->value - other->value);
            }
    };
}
#endif
