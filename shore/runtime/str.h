#ifndef _SHORE_STRING_H
#define _SHORE_STRING_H

#include <string>

#include "shore.h"

namespace shore {
    class builtin__str : public Object {
        public:
            std::string value;
            
            static builtin__str* new_instance(std::string value_);
            
            builtin__str(std::string value_);
            
            builtin__str* __add__(shore::builtin__str* other);
            builtin__str* __mul__(shore::builtin__int* other);
    };
}
#endif
