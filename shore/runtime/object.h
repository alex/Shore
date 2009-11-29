#ifndef _SHORE_OBJECT_H
#define _SHORE_OBJECT_H

#include "gc.h"


namespace shore {
    class Object;
    typedef std::set<shore::Object*> GCSet;

    class Object {
        public:
            virtual shore::GCSet __get_sub_objects() {
                return shore::GCSet();
            }
    };

}
#endif
