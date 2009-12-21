#ifndef _SHORE_BUILTIN_H
#define _SHORE_BUILTIN_H

#include <iostream>

#include "shore.h"
#include "list.h"


namespace shore {
    void builtin__print(shore::builtin__int* val) {
        std::cout << val->value << std::endl;
    }
    
    void builtin__print(shore::builtin__str* val) {
        std::cout << val->value << std::endl;
    }
    
    // TODO: a) this doesn't handle negatives steps, b) there is no reason this
    // shouldn't be written in shore
    builtin__list<builtin__int*>* builtin__range(builtin__int* start,
        builtin__int* stop, builtin__int* step) {
        builtin__list<builtin__int*>* result = builtin__list<builtin__int*>::new_instance();
        for (long long i = start->value; i < stop->value; i+=start->value) {
            result->append(builtin__int::new_instance(i));
        }
        return result;
    }

    builtin__list<builtin__int*>* builtin__range(builtin__int* start, builtin__int* stop) {
        return builtin__range(start, stop, builtin__int::new_instance(1LL));
    }
    
    builtin__list<builtin__int*>* builtin__range(builtin__int* stop) {
        return builtin__range(builtin__int::new_instance(0LL), stop);
    }
}

#endif
