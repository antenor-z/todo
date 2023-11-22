import subprocess, tempfile, os

def asm(assembly):
    tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    try:
        tmp.write(assembly)
        tmp.seek(0)
        ret = subprocess.run(["python3", "-m", "puc8.asm", tmp.name], capture_output=True, text=True)
        if ret.returncode == 0:
            return ret.stdout
        else:
            return ret.stderr
    finally:
        tmp.close()
        os.unlink(tmp.name)
    