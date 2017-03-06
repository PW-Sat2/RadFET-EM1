cmake_minimum_required(VERSION 3.1)
set(CMAKE_TOOLCHAIN_FILE "$ENV{HAL_PATH}/toolchain.cmake")

project(radfet)

add_subdirectory(bsp)
add_subdirectory($ENV{HAL_PATH} hal)


add_hal_executable(testapp
    main.cpp
)
