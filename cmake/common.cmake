
STRING(REPLACE "/scripts/buildsystems/vcpkg.cmake" "" VCPKG_DIR ${CMAKE_TOOLCHAIN_FILE})

STRING(CONCAT VCPKG_LIB_DIR_DEBUG "${VCPKG_DIR}/installed/${VCPKG_TARGET_TRIPLET}/debug/lib/")
STRING(CONCAT VCPKG_LIB_DIR_RELEASE "${VCPKG_DIR}/installed/${VCPKG_TARGET_TRIPLET}/lib")

if (${CMAKE_BUILD_TYPE} EQUAL "Debug")
	set(libmariadb "${VCPKG_LIB_DIR_DEBUG}libmariadb.lib")
elseif(${CMAKE_BUILD_TYPE} EQUAL "Release")
	set(libmariadb "${VCPKG_LIB_DIR_RELEASE}libmariadb.lib")
elseif(${CMAKE_BUILD_TYPE} EQUAL "RelwithDebInfo")
endif()