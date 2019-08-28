import os
from subprocess import check_call as run
import requests

Version = '4.0'
src = '/home/pi/finger'
dst = '/etc/finger'
command = {
    'removesource'  : 'sudo rm -rf {}',
    'getzipfile'    : 'wget -P {} https://github.com/Nat4Lia/finger/archive/v{}.zip',
    'unzipfile'     : 'sudo unzip -o -j {}/v{} finger-{}/* -d {}',
    'enextglob'     : 'shopt -s extglob',
    'chdir'         : 'cd {}',
    'rmallex'       : 'sudo rm -rf -v !("instansi_id.py")',
    'rmexcept'      : 'sudo find . ! -name "instansi_id.py" -type f -exec rm -f {} +',
    'reboot'        : 'sudo reboot',
    'removezip'     : 'sudo rm -rf {}/v{}.zip'    
}

r = requests.get('https://github.com/Nat4Lia/finger/releases/latest')
new_version = r.url[len(r.url)-5:]
if version != new_version :
    run(command['removesrc'].format(src), shell=True)
    run(command['getzipfile'].format(src, new_version, dst), shell=True)
    if not os.path.isdir(dst):
        os.system(command['unzipfile'].format(src, new_version, dst))
    else :
        os.chdir(dst)
        os.system(command['enextglob'])
        os.system(command['rmallex'])
        os.system(command['unzipfile'].format(src, new_version, new_version, dst))
        os.system(command['removezip'].format(src, new_version))