#ifndef _SHORE_GC_H
#define _SHORE_GC_H

#include "object.h"


namespace shore {
    class GC {
        public:
            static GCSet allocated_objects;
            
            static void register_object(shore::Object* obj);
            static void collect();
    };
}
#endif
