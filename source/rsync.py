#!/bin/usr/env python
# -*- coding: utf-8 -*-
import paramiko
import subprocess
import os
from IO import get_file_data_as_list, get_dirs, extract_common_dir


def make_basedir(dir_dict, server, sync_dir, common_file):
    common_dir_lst = get_file_data_as_list(dir_dict['from'] + common_file)
    dir_lst = extract_common_dir(common_dir_lst)

    config_file = dir_dict['home'] + '/.ssh/config'
    ssh_config = paramiko.SSHConfig()
    ssh_config.parse(open(config_file, 'r'))
    lkup = ssh_config.lookup(server)
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect(
            hostname=lkup['hostname'], username=lkup['user'],
            key_filename=lkup['identityfile']
        )

        for dir_tmp in dir_lst:
            path = os.path.join(dir_dict['to'], dir_tmp)
            ssh.exec_command('mkdir -p ' + path)

        path = os.path.join(dir_dict['to'], sync_dir)
        ssh.exec_command('mkdir -p ' + path)

    return


def rsync(dir_dict, server, sync_dir, direct, common_file):

    # common dir
    dir_lst = get_file_data_as_list(dir_dict['from'] + common_file)
    dir_lst.append(sync_dir)
    for dir_tmp in dir_lst:
        from_dir = os.path.join(dir_dict['from'], dir_tmp) + '/'
        to_dir = os.path.join(dir_dict['to'], dir_tmp)

        if direct == 'to':
            cmd = 'rsync -av %s %s:%s'%(from_dir, server, to_dir)
        elif direct == 'from':
            cmd = 'rsync -av %s:%s %s'%(server, to_dir, from_dir)

        subprocess.run(cmd.split())

    return


def rsync_main(direct, server, sync_dir, server_home):

    dir_dict = get_dirs(server_home)
    common_file = '/common/sync/commondir.txt'

    if direct == 'to':
        make_basedir(dir_dict, server, sync_dir, common_file)

    rsync(dir_dict, server, sync_dir, direct, common_file)

    return


def main():
    return


if __name__ == "__main__":
    main()