import os
from subprocess import check_call as run
import requests
from lcd_i2c import tampil_teks

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

def try_update():
    try :
        tampil_teks(['CEK', 'UPDATE')
        r = requests.get('https://github.com/Nat4Lia/finger/releases/latest', timeout=5)
        new_version = r.url[len(r.url)-5:]
        if Version != new_version :
            tampil_teks(['UPDATE', 'KE VERSI', str(new_version)])
            run(command['removesrc'].format(src), shell=True)
            run(command['getzipfile'].format(src, new_version, dst), shell=True)
            if not os.path.isdir(dst):
                os.system(command['unzipfile'].format(src, new_version, dst))
                tampil_teks(['UPDATE', 'BERHASIL'])
            else :
                os.chdir(dst)
                os.system(command['rmallex'])
                os.system(command['unzipfile'].format(src, new_version, new_version, dst))
                os.system(command['removezip'].format(src, new_version))
                tampil_teks(['UPDATE', 'BERHASIL'])
        else :
            tampil_teks(['TIDAK ADA', 'UPDATE'])
    except Exception as e :
        print ('Update Error : {}').format(e)
        tampil_teks(['UPDATE', 'GAGAL'])