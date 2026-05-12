cmake_minimum_required(VERSION 3.21)
project(ProCalcX LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets Core Gui Sql Charts)
find_package(nlohmann_json REQUIRED)

file(GLOB_RECURSE SRC_FILES CONFIGURE_DEPENDS src/*.cpp)

add_executable(${PROJECT_NAME} ${SRC_FILES})

target_include_directories(${PROJECT_NAME} PRIVATE src)
target_link_libraries(${PROJECT_NAME} PRIVATE
  Qt6::Widgets Qt6::Core Qt6::Gui Qt6::Sql Qt6::Charts
  nlohmann_json::nlohmann_json
)

if(WIN32)
  target_compile_definitions(${PROJECT_NAME} PRIVATE NOMINMAX)
endif()
