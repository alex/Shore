#ifndef _SHORE_GC_H
#define _SHORE_GC_H

#include <set>

#include "object.h"


namespace shore {
    typedef std::set<shore::Object*> GCSet;

    class GC {
        public:
            GCSet allocated_objects;
            
            shore::Object* register_object(shore::Object* obj);
            void collect();
    };
}
#endif
