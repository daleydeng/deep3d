#ifndef SIGNAL_HH
#define SIGNAL_HH

#include <map>
#include <functional>

template <typename... Args>
struct Signal {
  Signal() : current_id_(0) {}
  Signal(Signal const& other) : current_id_(0) {}

  template <typename T>
  int connect_member(T *inst, void (T::*func)(Args...)) {
    return connect([=](Args... args) {
      (inst->*func)(args...);
    });
  }

  template <typename T>
  int connect_member(T *inst, void (T::*func)(Args...) const) {
    return connect([=](Args... args) {
      (inst->*func)(args...);
    });
  }

  int connect(std::function<void(Args...)> const& slot) const {
    slots_.insert(std::make_pair(++current_id_, slot));
    return current_id_;
  }

  void disconnect(int id) const {
    slots_.erase(id);
  }
  void disconnect_all() const {
    slots_.clear();
  }

  void operator()(Args... p) {
    for(auto it : slots_) {
      it.second(p...);
    }
  }

  Signal& operator = (Signal const& other) {
    disconnect_all();
    return *this;
  }

 private:
  mutable std::map<int, std::function<void(Args...)>> slots_;
  mutable int current_id_;
};

#endif
