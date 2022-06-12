
class dvault_update:
    update_cmds = [
            [ 'pip', 'uninstall', '-y', 'dvault' ],
            [ 'pip', 'install', 'git+ssh://git@github.com/AlwaysTraining/dvault.git' ] ]
    entry_point = update_cmds

