#ifndef _SHORE_FRAME_H
#define _SHORE_FRAME_H

#include "gc.h"


namespace shore {
    class Frame {
        public:
            virtual shore::GCSet __get_sub_objects() = 0;
    };
}
#endif
