#ifndef _SHORE_STATE_H
#define _SHORE_STATE_H

#include <vector>

#include "gc.h"
#include "frame.h"


namespace shore {
    class State {
        public:
            std::vector<shore::Frame*> frames;
    };
}
#endif
