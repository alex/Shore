#include "gc.h"
#include "state.h"

namespace shore {
    shore::Object* shore::GC::register_object(shore::Object* obj) {
        this->allocated_objects.insert(obj);
        return obj;
    }
    
    void shore::GC::collect() {
        shore::GCSet reachable;
        std::vector<shore::GCSet> to_process;
        
        for (int i = 0; i < shore::State.frames.size(); i++) {
            to_process.push_back(shore::State.frames[i]->__get_sub_objects());
        }
        
        while (!to_process.empty()) {
            shore::GCSet reachable_objs = to_process.back();
            to_process.pop_back();
            for (shore::GCSet::iterator itr = reachable_objs.begin();
                itr != reachable_objs.end(); itr++) {
                if (!reachable.count(*itr)) {
                    reachable.insert(*itr);
                    to_process.push_back((*itr)->__get_sub_objects());
                }
            }
        }
        
        for (shore::GCSet::iterator itr = this->allocated_objects.begin();
            itr != this->allocated_objects.end(); itr++) {
            if (!reachable.count(*itr)) {
                delete *itr;
                this->allocated_objects.erase(itr);
            }
        }
    }
}
