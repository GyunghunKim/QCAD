cmake_minimum_required(VERSION 3.0)

project(csim)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/Modules/Backend)
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_BUILD_TYPE Release)

# set(CMAKE_VERBOSE_MAKEFILE true)

add_compile_options(-Wall -std=c++14 -O3 -fPIC)

file(GLOB SOURCE_FILES "${CMAKE_SOURCE_DIR}/Modules/Backend/C/*.cpp")
add_library(csim SHARED ${SOURCE_FILES})
set_target_properties(csim PROPERTIES PREFIX "")
