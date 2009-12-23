#ifndef _SHORE_LIST_H
#define _SHORE_LIST_H

#include <vector>

#include "shore.h"


namespace shore {
    template<typename T>
    class builtin__list : public shore::Object {
        public:
            std::vector<T> value;
        
            static builtin__list<T>* new_instance();
            
            GCSet __get_sub_objects();
                        
            builtin__bool* __bool__();
            T __getitem__(builtin__int* index);
            builtin__list<T>* __getitem__(builtin__slice* index);
            void __setitem__(builtin__int* index, T value);
            
            void append(T val);
            void insert(builtin__int* index, T value);
    };
    
    template<typename T>
    builtin__list<T>* builtin__list<T>::new_instance() {
        builtin__list<T>* val = new builtin__list<T>();
        shore::GC::register_object(val);
        return val;
    }
    
    template<typename T>
    GCSet builtin__list<T>::__get_sub_objects() {
        GCSet s;
        for (size_t i = 0; i < this->value.size(); i++) {
            s.insert(this->value[i]);
        }
        return s;
    }
    
    template<typename T>
    T builtin__list<T>::__getitem__(builtin__int* index) {
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
    
    template<typename T>
    builtin__list<T>* builtin__list<T>::__getitem__(builtin__slice* index) {
        // TODO: implement this.
        return NULL;
    }
    
    template<typename T>
    void builtin__list<T>::__setitem__(builtin__int* index, T value) {
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
    
    template<typename T>
    builtin__bool* builtin__list<T>::__bool__() {
        return builtin__bool::new_instance(this->value.size() != 0);
    }
    
    template<typename T>
    void builtin__list<T>::append(T val) {
        this->value.push_back(val);
    }
    
    template<typename T>
    void builtin__list<T>::insert(builtin__int* index, T val) {
        std::vector<T>::iterator itr = this->value.begin();
        for (long long i = 0LL; i < index->value; i++) {
            itr++;
        }
        this->value.insert(itr, val);
    }
}
#endif
