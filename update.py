import os
from subprocess import check_call as run
import requests
import time
import json
from lcd_ import teks

global Version, src, dst, command, r, new_version
Version = '3.4.0'
src = '/home/pi/finger'
dst = '/etc/finger'
command = {
    'remove': 'sudo rm -drf {}',
    'getzipfile': 'wget -P /home/pi/download '
    'https://github.com/Nat4Lia/finger/archive/v{}.zip',
    'unzipfile': 'sudo unzip -o /home/pi/download/v{} finger-{}/* -d /home/pi',
    'chdir': 'cd {}',
    'rmexcept': 'sudo find . ! -name "instansi_id.py" '
    '-type d,f -exec rm -rf {} +',
    'reboot': 'sudo reboot',
    'removezip': 'sudo rm -rf /home/pi/download/v{}.zip',
    'rename': 'sudo mv /home/pi/finger-{} /home/pi/finger',
    'copy': 'sudo cp -R /home/pi/finger /etc/'
}


def get_New_Version():
    try:
        r = requests.get('http://eabsen.kalselprov.go.id/api/version')
        if r.status_code == requests.codes.ok:
            return json.loads(r.content)['version']
        else:
            raise requests.exceptions.RequestException
    except requests.exceptions.RequestException:
        pass


def try_update():
    try:
        teks('CEK', 'UPDATE')
        new_version = get_New_Version()
        if new_version:
            if Version < new_version:
                teks('UPDATE', 'KE VERSI', str(new_version))
                run(command['remove'].format(src), shell=True)
                run(command['getzipfile'].format(new_version), shell=True)
                os.system(
                    command['unzipfile'].format(new_version, new_version)
                )
                os.system(command['rename'].format(new_version))
                if not os.path.isdir(dst):
                    teks('UPDATE...')
                    os.system(command['copy'])
                else:
                    teks('UPDATE...')
                    os.chdir(dst)
                    os.system(command['rmexcept'])
                    os.system(command['copy'])
                os.system(command['removezip'].format(new_version))
                teks('REBOOT...')
                os.system(command['reboot'])
            else:
                teks('TIDAK ADA', 'UPDATE')
                time.sleep(2)
        else:
            raise Exception
    except Exception as e:
        # teks('Update Error : {}').format(e)
        teks('UPDATE', 'GAGAL')
