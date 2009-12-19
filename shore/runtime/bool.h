#ifndef _SHORE_BOOL_H
#define _SHORE_BOOL_H

#include "shore.h"


namespace shore {
    class builtin__bool : public shore::Object {
        public:
            bool value;
            
            static builtin__bool* new_instance(bool value_);
            
            builtin__bool(bool value_);
            
            builtin__bool* __bool__();
    };
}
#endif
