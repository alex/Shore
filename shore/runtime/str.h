#ifndef _SHORE_STRING_H
#define _SHORE_STRING_H

#include <string>

#include "gc.h"
#include "int.h"


namespace shore {
    class builtin__str : public shore::Object {
        public:
            std::string value;
            
            static builtin__str* new_instance(std::string value_) {
                builtin__str* val = new builtin__str(value_);
                shore::GC::register_object(val);
                return val;
            }
            
            builtin__str(std::string value_) {
                this->value = value_;
            }
            
            builtin__str* __add__(shore::builtin__str* other) {
                return shore::builtin__str::new_instance(this->value + other->value);
            }
            
            builtin__str* __mul__(shore::builtin__int* other) {
                std::string s;
                s.reserve(this->value.size() * other->value);
                for (long long i = 0; i < other->value; i++) {
                    s.append(this->value);
                }
                return shore::builtin__str::new_instance(s);
            }
    };
}
#endif
