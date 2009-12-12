#ifndef _SHORE_INT_H
#define _SHORE_INT_H

#include <cmath>

#include "shore.h"


namespace shore {
    class builtin__int : public shore::Object {
        public:
            // Some day this will be arbitrary percision, but not today.
            long long value;
            
            static shore::builtin__int* new_instance(long long value_);
            static shore::builtin__int* new_isntance(shore::builtin__str* value_);
            shore::builtint__int(long long value_);

            shore::builtin__bool* __eq__(builtin__int* other);
            shore::builtin__bool* __ne__(builtin__int* other);
            shore::builtin__bool* __lt__(builtin__int* other);
            shore::builtin__bool* __gt__(builtin__int* other);
            
            shore::builtin__int* __add__(builtin__int* other);
            shore::builtin__int* __sub__(builtin__int* other);
            shore::builtin__int* __mul__(builtin__int* other);
    };
}
#endif
