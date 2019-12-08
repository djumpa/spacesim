cmake_minimum_required(VERSION 3.10)

# set the project name
project(spacesim)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# add the executable
add_executable(fc fc/fc.c)
add_executable(sim simulation/sim.c)