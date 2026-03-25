cmake_minimum_required(VERSION 3.8)
project(hangman_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 🔥 필수
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rosidl_default_runtime REQUIRED)   # ⭐ 이거 추가

# 🔥 인터페이스 생성
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Progress.msg"
  "srv/CheckLetter.srv"
  "action/GameProgress.action"
  DEPENDENCIES builtin_interfaces
)

# 🔥 필수
ament_package()
