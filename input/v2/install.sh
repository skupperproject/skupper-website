#!/bin/sh
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

troubleshooting_url="https://skupper.io/install/troubleshooting.html"

# Make the local keyword work with ksh93 and POSIX-style functions
case "${KSH_VERSION:-}" in
    *" 93"*) alias local="typeset -x" ;;
    *) ;;
esac

# Make zsh emulate the Bourne shell
if [ -n "${ZSH_VERSION:-}" ]
then
    emulate sh
fi

# This is required to preserve the Windows drive letter in the
# path to HOME
case "$(uname)" in
    CYGWIN*) HOME="$(cygpath --mixed --windows "${HOME}")" ;;
    *) ;;
esac

assert() {
    local location="$0:"

    # shellcheck disable=SC2128 # We want only the first element of the array
    if [ -n "${BASH_LINENO:-}" ]
    then
        location="$0:${BASH_LINENO}:"
    fi

    if ! "$@" > /dev/null 2>&1
    then
        printf "%s %s assert %s\n" "$(red "ASSERTION FAILED:")" "$(yellow "${location}")" "$*" >&2
        exit 1
    fi
}

random_number() {
    printf "%s%s" "$(date +%s)" "$$"
}

print() {
    if [ "$#" = 0 ]
    then
        printf "\n" >&5
        printf -- "--\n"
        return
    fi

    printf "   %s\n" "$1" >&5
    printf -- "-- %s\n" "$1"
}

print_result() {
    printf "   %s\n\n" "$(green "$1")" >&5
    log "Result: $(green "$1")"
}

print_section() {
    printf "== %s ==\n\n" "$(bold "$1")" >&5
    printf "== %s\n" "$1"
}

run() {
    printf -- "-- Running '%s'\n" "$*" >&2
    "$@"
}

log() {
    printf -- "-- %s\n" "$1"
}

fail() {
    printf "   %s %s\n\n" "$(red "ERROR:")" "$1" >&5
    log "$(red "ERROR:") $1"

    if [ -n "${2:-}" ] && [ -n "${troubleshooting_url:-}" ]
    then
        printf "   See ${troubleshooting_url}%s\n\n" "$2" >&5
        log "See ${troubleshooting_url}$2"
    fi

    suppress_trouble_report=1

    exit 1
}

green() {
    printf "[0;32m%s[0m" "$1"
}

yellow() {
    printf "[0;33m%s[0m" "$1"
}

red() {
    printf "[1;31m%s[0m" "$1"
}

bold() {
    printf "[1m%s[0m" "$1"
}

init_logging() {
    local log_file="$1"
    local verbose="$2"

    # shellcheck disable=SC2064 # We want to expand these now, not later
    trap "handle_exit '${log_file}' '${verbose}'" EXIT

    if [ -e "${log_file}" ]
    then
        mv "${log_file}" "${log_file}.$(date +%Y-%m-%d).$(random_number)"
    fi

    # Use file descriptor 5 for the default display output
    exec 5>&1

    # Use file descriptor 6 for logging and command output
    exec 6>&2

    # Save stdout and stderr before redirection
    exec 7>&1
    exec 8>&2

    # If verbose, suppress the default display output and log
    # everything to the console. Otherwise, capture logging and
    # command output to the log file.
    if [ -n "${verbose}" ]
    then
        exec 5> /dev/null
    else
        exec 6> "${log_file}"
    fi
}

handle_exit() {
    # This must go first
    local exit_code=$?

    local log_file="$1"
    local verbose="$2"

    # Restore stdout and stderr
    exec 1>&7
    exec 2>&8

    # shellcheck disable=SC2181 # This is intentionally indirect
    if [ "${exit_code}" != 0 ] && [ -z "${suppress_trouble_report:-}" ]
    then
        if [ -n "${verbose}" ]
        then
            printf "%s Something went wrong.\n\n" "$(red "TROUBLE!")"
        else
            printf "   %s Something went wrong.\n\n" "$(red "TROUBLE!")"
            printf "== Log ==\n\n"

            sed -e "s/^/  /" < "${log_file}" || :

            printf "\n"
        fi
    fi
}

enable_debug_mode() {
    # Print the input commands and their expanded form to the console
    set -vx

    if [ -n "${BASH:-}" ]
    then
        # Bash offers more details
        export PS4='[0;33m${BASH_SOURCE}:${LINENO}:[0m ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
    fi
}

enable_strict_mode() {
    # No clobber, exit on error, and fail on unbound variables
    set -Ceu

    if [ -n "${BASH:-}" ]
    then
        # Inherit traps, fail fast in pipes, enable POSIX mode, and
        # disable brace expansion
        #
        # shellcheck disable=SC3040,SC3041 # We know this is Bash in this case
        set -E -o pipefail -o posix +o braceexpand

        assert test -n "${POSIXLY_CORRECT}"
    fi
}

program_is_available() {
    local program="${1}"

    assert test -n "${program}"

    command -v "${program}"
}

check_required_programs() {
    log "Checking for required programs"

    local programs="$*"
    local program=
    local unavailable_programs=

    for program in ${programs}
    do
        log "Checking program '${program}'"

        if ! command -v "${program}"
        then
            unavailable_programs="${unavailable_programs}${program}, "
        fi
    done

    if [ -n "${unavailable_programs}" ]
    then
        fail "Some required programs are not available: ${unavailable_programs%??}" \
             "#some-required-programs-are-not-available"
    fi
}

check_required_network_resources() {
    log "Checking for required network resources"

    local urls="$*"
    local url=
    local unavailable_urls=

    assert program_is_available curl

    for url in ${urls}
    do
        log "Checking URL '${url}'"

        if ! curl -sf --show-error --head "${url}"
        then
            unavailable_urls="${unavailable_urls}${url}, "
        fi
    done

    if [ -n "${unavailable_urls}" ]
    then
        fail "Some required network resources are not available: ${unavailable_urls%??}" \
             "#some-required-network-resources-are-not-available"
    fi
}

check_writable_directories() {
    log "Checking for permission to write to the install directories"

    local dirs="$*"
    local dir=
    local base_dir=
    local unwritable_dirs=

    for dir in ${dirs}
    do
        log "Checking directory '${dir}'"

        base_dir="${dir}"

        while [ ! -e "${base_dir}" ]
        do
            base_dir="$(dirname "${base_dir}")"
        done

        if [ -w "${base_dir}" ]
        then
            printf "Directory '%s' is writable\n" "${base_dir}"
        else
            printf "Directory '%s' is not writeable\n" "${base_dir}"
            unwritable_dirs="${unwritable_dirs}${base_dir}, "
        fi
    done

    if [ -n "${unwritable_dirs}" ]
    then
        fail "Some install directories are not writable: ${unwritable_dirs%??}" \
             "#some-install-directories-are-not-writable"
    fi
}

ask_to_proceed() {
    while true
    do
        printf "   Do you want to proceed? (yes or no): " >&5
        printf -- "-- Do you want to proceed? (yes or no): "
        read -r response

        case "${response}" in
            yes) break ;;
            no)  exit  ;;
            *) ;;
        esac
    done
}

extract_archive() {
    local archive_file="$1"
    local output_dir="$2"

    assert test -f "${archive_file}"
    assert test -d "${output_dir}"
    assert program_is_available gzip
    assert program_is_available tar

    gzip -dc "${archive_file}" | (cd "${output_dir}" && tar xf -)
}

# func <version> <output-dir> -> release_version=<version>, release_file=<file>
fetch_skupper_release() {
    local version="$1"
    local output_dir="$2"

    assert test -d "${output_dir}"
    assert program_is_available awk
    assert program_is_available curl
    assert program_is_available uname

    log "Determining your OS an architecture"

    case $(uname -s) in
        # CYGWIN*) local operating_system=windows ;;
        Darwin)  local operating_system=mac     ;;
        Linux)   local operating_system=linux   ;;
        *)       fail "Unknown operating system: $(uname -s)" ;;
    esac

    case $(uname -m) in
        aarch64) local architecture=arm64 ;;
        arm64)   local architecture=arm64 ;;
        armv7l)  local architecture=arm32 ;;
        i386)    local architecture=i386  ;;
        i686)    local architecture=i386  ;;
        x86_64)  local architecture=amd64 ;;
        *)       fail "Unknown architecture: $(uname -m)" ;;
    esac

    log "Operating system: ${operating_system}"
    log "Architecture: ${architecture}"

    local release_version_file="${output_dir}/release-version.txt"

    case "${version}" in
        latest)
            log "Looking up the latest release version"

            run curl -sf "https://skupper.io/v2/data/install.json" \
                | awk 'match($0, /"version": "[0-9]+\.[0-9]+\.[0-9]+"/) { print substr($0, RSTART+12, RLENGTH-13) }' \
                      >| "${release_version_file}"
            ;;
        main)
            echo "main-release" >| "${release_version_file}"
            ;;
        *)
            echo "${version}" >| "${release_version_file}"
            ;;
    esac

    release_version="$(cat "${release_version_file}")"

    log "Release version: ${release_version}"
    log "Release version file: ${release_version_file}"

    local release_file_name="skupper-cli-${release_version}-${operating_system}-${architecture}.tgz"
    # release_file is "returned"
    release_file="${output_dir}/${release_file_name}"

    assert test -n "${release_file}"
    assert test -n "${release_file_name}"
    assert test -n "${release_version}"

    if [ ! -e "${release_file}" ] || [ "${release_version}" = "main-release" ]
    then
        log "Downloading the ${release_version} release"

        local release_url="https://github.com/skupperproject/skupper/releases/download/${release_version}/${release_file_name}"

        if ! run curl -sfL --show-error -o "${release_file}" "${release_url}"
        then
            fail "No release found at ${release_url}"
        fi
    else
        log "Using the cached release archive"
    fi

    log "Archive file: ${release_file}"

    # release_version is "returned"
    release_version="$(cat "${release_version_file}")"

    assert test -n "${release_version}"
    assert test -f "${release_file}"
}

usage() {
    local error="${1:-}"

    if [ -n "${error}" ]
    then
        printf "%b %s\n\n" "$(red "ERROR:")" "${*}"
    fi

    cat <<EOF
Usage: install.sh [OPTION...]

Install the Skupper command-line tool

Options:
  -h, --help          Print this help text and exit
  --version VERSION   Select the version (default "latest")
  --scheme SCHEME     Select an installation scheme (default "home")
  --interactive       Operate in interactive mode
  --verbose           Print detailed logging to the console

Versions:
  latest              The latest release
  main                The latest CI/CD release from main
  X.Y.Z               A specific version

Schemes:
  home                Install to ~/.local/bin
  opt                 Install to /opt/skupper/bin
EOF

    if [ -n "${error}" ]
    then
        exit 1
    fi

    exit 0
}

require_option_arg() {
    local opt="$1"
    local optarg="$2"

    if [ -z "${optarg}" ]
    then
        usage "Option ${opt} is missing a required argument"
    fi

    case "${optarg}" in
        -*) usage "Option ${opt} is missing a required argument" ;;
        *) : ;;
    esac
}

main() {
    enable_strict_mode

    if [ -n "${DEBUG:-}" ]
    then
        enable_debug_mode
    fi

    local version=latest
    local scheme=home
    local interactive=
    local verbose=

    while [ $# -gt 0 ]
    do
        case "$1" in
            -h|--help) usage ;;
            --version)
                require_option_arg "$1" "${2:-}"
                version="$2"
                shift
                ;;
            --scheme)
                require_option_arg "$1" "${2:-}"
                scheme="$2"
                shift
                ;;
            --interactive) interactive=1 ;;
            --verbose) verbose=1 ;;
            *) usage "Unknown option: ${1}" ;;
        esac

        shift
    done

    case "${scheme}" in
        home) local skupper_bin_dir="${TEST_INSTALL_PREFIX:-}${HOME}/.local/bin" ;;
        opt)  local skupper_bin_dir="${TEST_INSTALL_PREFIX:-}/opt/skupper/bin" ;;
        *)    usage "Unknown installation scheme: ${scheme}" ;;
    esac

    local work_dir="${TEST_INSTALL_PREFIX:-}${HOME}/.cache/skupper-install-script"
    local log_file="${work_dir}/install.log"
    local backup_dir="${work_dir}/backup"

    mkdir -p "${work_dir}"
    cd "${work_dir}"

    init_logging "${log_file}" "${verbose}"

    {
        if [ -n "${interactive}" ]
        then
            print_section "Preparing to install"

            print "This script will install the Skupper command to:"
            print
            print "    ${skupper_bin_dir}/skupper"
            print
            print "It will save a backup of any existing installation to:"
            print
            print "    ${backup_dir}"
            print
            print "Run \"install.sh -h\" to see the installation options."
            print

            ask_to_proceed

            print
        fi

        print_section "Checking prerequisites"

        check_writable_directories "${skupper_bin_dir}"
        check_required_programs awk curl gzip tar
        check_required_network_resources "https://github.com/" "https://skupper.io/"

        print_result "OK"

        print_section "Downloading the release"

        fetch_skupper_release "${version}" "${work_dir}"

        print_result "OK"

        if [ -e "${skupper_bin_dir}/skupper" ]
        then
            print_section "Saving the existing installation to a backup"

            if [ -e "${backup_dir}" ]
            then
                mv "${backup_dir}" "${backup_dir}.$(date +%Y-%m-%d).$(random_number)"
            fi

            run mkdir -p "${backup_dir}"
            run mv "${skupper_bin_dir}/skupper" "${backup_dir}"

            print_result "OK"
        fi

        print_section "Installing the Skupper command"

        log "Extracting the command from the release archive"

        extract_archive "${release_file}" "${work_dir}"

        assert test -x skupper

        log "Moving the command to its install location"

        run mkdir -p "${skupper_bin_dir}"
        run mv skupper "${skupper_bin_dir}"

        print_result "OK"

        print_section "Testing the installation"

        log "Testing the Skupper command"

        run "${skupper_bin_dir}/skupper" --help > /dev/null

        print_result "OK"

        print_section "Summary"

        print_result "SUCCESS"

        print "The Skupper command is now installed."
        print
        print "    Version:  ${release_version}"
        print "    Path:     ${skupper_bin_dir}/skupper"
        print

        if [ "$(command -v skupper)" != "${skupper_bin_dir}/skupper" ]
        then
            print "$(yellow "NOTE:") The Skupper command is not on your path.  To add it, use:"
            print

            if [ "${scheme}" = "home" ]
            then
                print "    export PATH=\"\$HOME/.local/bin:\$PATH\""
            else
                print "    export PATH=\"${skupper_bin_dir}:\$PATH\""
            fi

            print
        fi

        print "If you are trying Skupper for the first time, see the getting started guide:"
        print
        print "    https://skupper.io/start/"
        print
        print "To uninstall Skupper, use:"
        print
        print "    curl https://skupper.io/uninstall.sh | sh"
        print
    } >&6 2>&6
}

main "$@"
