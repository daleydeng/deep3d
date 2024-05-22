lib=pbgraphmatching$(shell python3-config --extension-suffix)

PREFIX = $(shell python3-config --prefix)
CXXFLAGS += -O3 -Wall -shared -std=c++11 -fPIC $(shell python3-config --includes) -I$(PREFIX)/include/eigen3 -I$(PREFIX)/include

$(lib): pbgraphmatching.cc
	g++ $(CXXFLAGS) $^ -o $@
