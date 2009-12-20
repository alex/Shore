#ifndef _SHORE_SLICE_H
#define _SHORE_SLICE_H

#include "shore.h"


// TODO: This whole class should be written in Shore.
namespace shore {
    class builtin__slice : public shore::Object {
        public:
            builtin__int* start;
            builtin__int* stop;
            builtin__int* step;
            
            static builtin__slice* new_instance(builtin__int* start_,
                builtin__int* stop_, builtin__int* step_);
            
            builtin__slice(builtin__int* start_, builtin__int* stop_,
                builtin__int* step_);
    };
}
#endif
