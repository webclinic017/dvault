
class dvault_update:
    uninstall_cmd = [ 'pip', 'uninstall', '-y', 'dvault' ],
    install_cmd = [ 'pip', 'install', 'git+ssh://git@github.com/AlwaysTraining/dvault.git' ]
    reinstall_cmds = [ uninstall_cmd, install_cmd ]
    entry_point = reinstall_cmds

