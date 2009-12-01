#ifndef _SHORE_BUILTIN_H
#define _SHORE_BUILTIN_H

#include <iostream>

#include "bool.h"
#include "int.h"

namespace shore {
    void builtin__print(shore::builtin__int* val) {
        std::iostream << val->value << std::endl;
    }
}

#endif
