import os
from subprocess import check_call as run
import requests, time
from lcd_ import teks

Version = '3.1.0'
src = '/home/pi/finger'
dst = '/etc/finger'
command = {
    'removesource'  : 'sudo rm -rf {}',
    'getzipfile'    : 'wget -P {} https://github.com/Nat4Lia/finger/archive/v{}.zip',
    'unzipfile'     : 'sudo unzip -o -j {}/v{} finger-{}/* -d {}',
    #'enextglob'     : 'shopt -s extglob',
    'chdir'         : 'cd {}',
    #'rmallex'       : 'sudo rm -rf -v !("instansi_id.py")',
    'rmexcept'      : 'sudo find . ! -name "instansi_id.py" -type f -exec rm -rf {} +',
    'reboot'        : 'sudo reboot',
    'removezip'     : 'sudo rm -rf {}/v{}.zip',
    'rmfolder'      : 'sudo rmdir {}'    
}
def try_update() :
    try :
        teks('CEK','UPDATE')
        r = requests.get('https://github.com/Nat4Lia/finger/releases/latest')
        new_version = r.url[len(r.url)-5:]
        print new_version
        if Version != new_version :
            teks('UPDATE', 'KE VERSI', str(new_version))
            run(command['removesource'].format(src), shell=True)
            run(command['getzipfile'].format(src, new_version, dst), shell=True)
            if not os.path.isdir(dst):
                teks('UPDATE...')
                os.system(command['unzipfile'].format(src, new_version, dst))
            else :
                teks('UPDATE...')
                os.chdir(dst)
                os.system(command['rmexcept'])
                os.system(command['unzipfile'].format(src, new_version, new_version, dst))
                os.system(command['removezip'].format(src, new_version))
                teks('REBOOT...')
                os.system(command['reboot'])
        else :
            teks('TIDAK ADA','UPDATE')
            time.sleep(2)
    except Exception as e :
        print ('Update Error : {}').format(e)
        teks('UPDATE', 'GAGAL')