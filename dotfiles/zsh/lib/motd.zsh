motd(){
    if [[ -f /etc/motd ]]; then
        if [[ -f "${HOME}/.config/dotfiles/motd_check" ]]; then
            motd_updated=$(stat --format="%Y" /etc/motd)
            if [[ "${motd_updated}" > "$(cat "${HOME}/.config/dotfiles/motd_check")" ]]; then
                date +%s > "${HOME}/.config/dotfiles/motd_check"
                echo -e "MotD: $(stat --format="%y" /etc/motd)\n"
                cat /etc/motd
            fi
        else
            mkdir -p "${HOME}/.config/dotfiles"
            date +%s > "${HOME}/.config/dotfiles/motd_check"
            echo -e "MotD: $(stat --format="%y" /etc/motd)\n"
            cat /etc/motd
        fi
    fi
}
