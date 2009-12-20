#include "slice.h"


namespace shore {
    builtin__slice* builtin__slice::new_instance(builtin__int* start_,
        builtin__int* stop_, builtin__int* step_) {
        shore::builtin__slice* val = new builtin__slice(start_, stop_, step_);
        shore::GC::register_object(val);
        return val;
    }
    
    builtin__slice::builtin__slice(builtin__int* start_, builtin__int* stop_,
        builtin__int* step_) {
        this->start = start_;
        this->stop = stop_;
        this->step = step_;
    }
}
