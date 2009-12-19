#ifndef _SHORE_INT_H
#define _SHORE_INT_H

#include <cmath>

#include "shore.h"


namespace shore {
    class builtin__int : public shore::Object {
        public:
            // Some day this will be arbitrary percision, but not today.
            long long value;
            
            static builtin__int* new_instance(long long value_);
            static builtin__int* new_instance(builtin__str* value_);
            builtin__int(long long value_);

            shore::builtin__bool* __eq__(shore::builtin__int* other);
            shore::builtin__bool* __ne__(shore::builtin__int* other);
            shore::builtin__bool* __lt__(shore::builtin__int* other);
            shore::builtin__bool* __gt__(shore::builtin__int* other);
            
            shore::builtin__int* __add__(shore::builtin__int* other);
            shore::builtin__int* __sub__(shore::builtin__int* other);
            shore::builtin__int* __mul__(shore::builtin__int* other);
    };
}
#endif
