project(eternity_dbserver)
file(GLOB_RECURSE source_SRC "*.h" "*.cpp")
message("source_SRC ${source_SRC}")
add_executable(${PROJECT_NAME}
${source_SRC}
)

target_link_libraries(${PROJECT_NAME} 
PUBLIC
${GRPC_SERVER}
${MYSQL_MODULE_ORM}
)

set(output_dir ${VS_WORKING_DIRECTORY})
set(output_dir_debug ${output_dir}/debug)
set(output_dir_release ${output_dir}/release)
set(debug_lib_dir ${output_dir}/debug)
set(release_lib_dir ${output_dir}/release)
set_target_properties( ${PROJECT_NAME} 
    PROPERTIES 
      MAP_IMPORTED_CONFIG_RELWITHDEBINFO RELEASE
      MAP_IMPORTED_CONFIG_MINSIZEREL RELEASE

      VS_DEBUGGER_WORKING_DIRECTORY "${output_dir}"

      RUNTIME_OUTPUT_DIRECTORY_RELEASE "${output_dir_release}"
      PDB_OUTPUT_DIRECTORY_RELEASE "${output_dir_release}"
      LIBRARY_OUTPUT_DIRECTORY_RELEASE "${release_lib_dir}"
      ARCHIVE_OUTPUT_DIRECTORY_RELEASE "${output_dir_release}"

      RUNTIME_OUTPUT_DIRECTORY_DEBUG "${output_dir_debug}"
      PDB_OUTPUT_DIRECTORY_DEBUG "${output_dir_debug}"
      LIBRARY_OUTPUT_DIRECTORY_DEBUG "${debug_lib_dir}"
      ARCHIVE_OUTPUT_DIRECTORY_DEBUG "${debug_lib_dir}"


      RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO "${output_dir_release}"
      PDB_OUTPUT_DIRECTORY_RELWITHDEBINFO "${output_dir_release}"
      LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO "${release_lib_dir}"
      ARCHIVE_OUTPUT_DIRECTORY_RELWITHDEBINFO "${output_dir_release}"

      RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL	"${output_dir_release}"
      PDB_OUTPUT_DIRECTORY_MINSIZEREL "${output_dir_release}"
      LIBRARY_OUTPUT_DIRECTORY_MINSIZEREL "${release_lib_dir}"
      ARCHIVE_OUTPUT_DIRECTORY_MINSIZEREL "${output_dir_release}"
    )