_with_completion() {
    local options="$(with commands)"

    # If the user is providing the first positional argument
    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=($(compgen -W "${options}" "${COMP_WORDS[COMP_CWORD]}"))
    fi
}

complete -F _with_completion with