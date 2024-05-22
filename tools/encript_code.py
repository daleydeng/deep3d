#!/usr/bin/env python
import os
import shutil

rsync_clone_cmd_tpl = "rsync_clone.py {src} {rules} {dst} --t=0"
obfuscate_cmd_tpl = 'pyminifier {obfuscate} -o {0} {0}'
pyconcrete_cmd_tpl = "~/miniconda3/bin/pyconcrete-admin.py compile --source={} --pye {remove_py}"

def main(src, rules, dst, main_f='', remove_py=True, obfuscate=True):
    cmd = rsync_clone_cmd_tpl.format(src=src, rules=rules, dst=dst)
    print (cmd)
    os.system(cmd)

    for dirpath, dirnames, filenames in os.walk(dst):
        for d in dirnames:
            if d == '__pycache__':
                shutil.rmtree(dirpath+'/'+d, ignore_errors=True)

        for f in filenames:
            if f.endswith('.py'):
                cmd = obfuscate_cmd_tpl.format(dirpath+'/'+f, obfuscate=("-O" if obfuscate else ""))
                print (cmd)
                os.system(cmd)

    cmd = pyconcrete_cmd_tpl.format(dst, remove_py=('--remove-py --remove-pyc' if remove_py else ''))
    print (cmd)
    os.system(cmd)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
