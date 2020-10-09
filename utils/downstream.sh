#!/bin/bash -eu

# Script to dual-home the upstream and downstream Collection in a single repo
#
#   This script will build or test a downstream collection, removing any
#   upstream components that will not ship in the downstream release
#
#   NOTES:
#       - All functions are prefixed with f_ so it's obvious where they come
#         from when in use throughout the script

DOWNSTREAM_VERSION="1.1.1"
KEEP_DOWNSTREAM_TMPDIR="${KEEP_DOWNSTREAM_TMPDIR:-''}"


f_log_info()
{
    printf "%s:LOG:INFO: %s\n" "${0}" "${1}\n"
}

f_prep()
{
    f_log_info "${FUNCNAME[0]}"
    # Array of excluded files from downstream build (relative path)
    _file_exclude=(
    )

    # Files to copy downstream (relative repo root dir path)
    _file_manifest=(
        CHANGELOG.rst
        galaxy.yml
        LICENSE
        README.md
        Makefile
        setup.cfg
        .yamllint
    )

    # Directories to recursively copy downstream (relative repo root dir path)
    _dir_manifest=(
        changelogs
        meta
        plugins
        tests
        molecule
    )

    # Temp build dir
    _tmp_dir=$(mktemp -d)
    _build_dir="${_tmp_dir}/ansible_collections/kubernetes/core"
    mkdir -p "${_build_dir}"
}

f_show_help()
{
    printf "Usage: downstream.sh [OPTION]\n"
    printf "\t-s\t\tCreate a temporary downstream release and perform sanity tests.\n"
    printf "\t-i\t\tCreate a temporary downstream release and perform integration tests.\n"
    printf "\t-m\t\tCreate a temporary downstream release and perform molecule tests.\n"
    printf "\t-b\t\tCreate a downstream release and stage for release.\n"
    printf "\t-r\t\tCreate a downstream release and publish release.\n"
}

f_text_sub()
{
    # Switch FQCN and dependent components
    sed -i.bak "s/community-kubernetes/kubernetes-core/" "${_build_dir}/Makefile"
    sed -i.bak "s/community\/kubernetes/kubernetes\/core/" "${_build_dir}/Makefile"
    sed -i.bak "s/^VERSION\:/VERSION: ${DOWNSTREAM_VERSION}/" "${_build_dir}/Makefile"
    sed -i.bak "s/community.kubernetes/kubernetes.core/" "${_build_dir}/galaxy.yml"
    sed -i.bak "s/name\:.*$/name: core/" "${_build_dir}/galaxy.yml"
    sed -i.bak "s/namespace\:.*$/namespace: kubernetes/" "${_build_dir}/galaxy.yml"
    sed -i.bak "s/^version\:.*$/version: ${DOWNSTREAM_VERSION}/" "${_build_dir}/galaxy.yml"
    find "${_build_dir}" -type f -exec sed -i.bak "s/community\.kubernetes/kubernetes\.core/g" {} \;
    sed -i.bak "s/a\.k\.a\. \`kubernetes\.core\`/formerly known as \`community\.kubernetes\`/" "${_build_dir}/README.md";
    find "${_build_dir}" -type f -name "*.bak" -delete
}

f_cleanup()
{
    f_log_info "${FUNCNAME[0]}"
    if [[ -n ${KEEP_DOWNSTREAM_TMPDIR} ]]; then
        if [[ -d ${_build_dir} ]]; then
            rm -fr "${_build_dir}"
        fi
    fi
}

# Exit and handle cleanup processes if needed
f_exit()
{
    f_cleanup
    exit "$0"
}

f_create_collection_dir_structure()
{
    f_log_info "${FUNCNAME[0]}"
    # Create the Collection
    for f_name in "${_file_manifest[@]}";
    do
        cp "./${f_name}" "${_build_dir}/${f_name}"
    done
    for d_name in "${_dir_manifest[@]}";
    do
        cp -r "./${d_name}" "${_build_dir}/${d_name}"
    done
    if [ -n "${_file_exclude:-}" ]; then
        for exclude_file in "${_file_exclude[@]}";
        do
            if [[ -f "${_build_dir}/${exclude_file}" ]]; then
                rm -f "${_build_dir}/${exclude_file}"
            fi
        done
    fi
}

f_copy_collection_to_working_dir()
{
    f_log_info "${FUNCNAME[0]}"
    # Copy the Collection build result into original working dir
    cp "${_build_dir}"/*.tar.gz ./
}

f_common_steps()
{
    f_log_info "${FUNCNAME[0]}"
    f_prep
    f_create_collection_dir_structure
    f_text_sub
}

# Run the test sanity scanerio
f_test_sanity_option()
{
    f_log_info "${FUNCNAME[0]}"
    f_common_steps
    pushd "${_build_dir}" || return
        f_log_info "SANITY TEST PWD: ${PWD}"
        make test-sanity
    popd || return
    f_cleanup
}

# Run the test integration
f_test_integration_option()
{
    f_log_info "${FUNCNAME[0]}"
    f_common_steps
    pushd "${_build_dir}" || return
        f_log_info "INTEGRATION TEST WD: ${PWD}"
        make test-integration
    popd || return
    f_cleanup
}

# Run the molecule tests
f_test_molecule_option()
{
    f_log_info "${FUNCNAME[0]}"
    f_common_steps
    pushd "${_build_dir}" || return
        f_log_info "MOLECULE TEST WD: ${PWD}"
        make test-molecule
    popd || return
    f_cleanup
}

# Run the release scanerio
f_release_option()
{
    f_log_info "${FUNCNAME[0]}"
    f_common_steps
    pushd "${_build_dir}" || return
        f_log_info "RELEASE WD: ${PWD}"
        make release
    popd || return
    f_cleanup
}

# Run the build scanerio
f_build_option()
{
    f_log_info "${FUNCNAME[0]}"
    f_common_steps
    pushd "${_build_dir}" || return
        f_log_info "BUILD WD: ${PWD}"
        make build
    popd || return
    f_copy_collection_to_working_dir
    f_cleanup
}

# If no options are passed, display usage and exit
if [[ "${#}" -eq "0" ]]; then
    f_show_help
    f_exit 0
fi

# Handle options
while getopts ":simrb" option
do
  case $option in
    s)
        f_test_sanity_option
        ;;
    i)
        f_test_integration_option
        ;;
    m)
        f_test_molecule_option
        ;;
    r)
        f_release_option
        ;;
    b)
        f_build_option
        ;;
    *)
        printf "ERROR: Unimplemented option chosen.\n"
        f_show_help
        f_exit 1
        ;;   # Default.
  esac
done

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
