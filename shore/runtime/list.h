#ifndef _SHORE_LIST_H
#define _SHORE_LIST_H

#include <vector>

#include "gc.h"
#include "object.h"


namespace shore {
    template<typename T>
    class builtin__list : public shore::Object {
        public:
            std::vector<T> value;
        
            static builtin__list<T>* new_instance() {
                builtin__list<T>* val = new builtin__list<T>();
                shore::GC::register_object(val);
                return val;
            }
            
            builtin__list<T>() {
            }
            
            T __getitem__(shore::builtin__int* index) {
                long long idx = index->value;
                if (idx < 0) {
                    idx += this->value.size();
                }
                if (idx > this->value.size() || idx < 0) {
                    // TODO: This probably just leads to a segfault, figure out
                    // exceptions.
                    return NULL;
                }
                return this->value[idx];
            }
            
            void __setitem__(shore::builtin__int* index, T value) {
                long long idx = index->value;
                if (idx < 0) {
                    idx += this->value.size();
                }
                if (idx < this->value.size() || idx < 0) {
                    // TODO: This doesn't even raise or anything, it just fails
                    // silently, so many reasons that's a bad idea.
                    return;
                }
                this->value[idx] = value;
            }
            
            shore::builtin__bool* __bool__() {
                return shore::builtin__bool::new_instance(this->value.size() == 0);
            }
    };
}
#endif
