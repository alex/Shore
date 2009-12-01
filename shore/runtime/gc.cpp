#include "gc.h"
#include "state.h"
#include "frame.h"


namespace shore {
    void shore::GC::register_object(shore::Object* obj) {
        shore::GC::allocated_objects.insert(obj);
    }
    
    void shore::GC::collect() {
        shore::GCSet reachable;
        std::vector<shore::GCSet> to_process;
        
        for (size_t i = 0; i < shore::State::frames.size(); i++) {
            to_process.push_back(shore::State::frames[i]->__get_sub_objects());
        }
        
        while (!to_process.empty()) {
            shore::GCSet reachable_objs = to_process.back();
            to_process.pop_back();
            for (shore::GCSet::iterator itr = reachable_objs.begin();
                itr != reachable_objs.end(); itr++) {
                if (!reachable.count(*itr)) {
                    reachable.insert(*itr);
                    if (*itr != NULL) {
                        to_process.push_back((*itr)->__get_sub_objects());
                    }
                }
            }
        }
        std::vector<shore::Object*> deleted;
        for (shore::GCSet::iterator itr = shore::GC::allocated_objects.begin();
            itr != shore::GC::allocated_objects.end(); itr++) {
            if (!reachable.count(*itr)) {
                delete *itr;
                deleted.push_back(*itr);
            }
        }
        for (size_t i = 0; i < deleted.size(); i++) {
            shore::GC::allocated_objects.erase(deleted[i]);
        }
    }
}
