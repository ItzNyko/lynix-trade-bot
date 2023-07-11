import ctypes
import time
import psutil
import utils
import sys
import os

# https://github.com/ittech25/Pydbg
BLACKLIST = [
    "filemon.exe",
    "regmon.exe",
    "dbgview.exe",
    "diskmon.exe",
    "windbg.exe",
    "ollydbg.exe",
    "procmon.exe",
    "immunitydebugger.exe",
    "wireshark.exe",
    "x32dbg.exe",
    "ida.exe",
    "x64dbg.exe",
    "ida64.exe",
    "httptoolkit.exe",
    "httpdebuggerui.exe",
    "wireshark.exe",
    "fiddler.exe",
    "vboxservice.exe",
    "df5serv.exe",
    "processhacker.exe",
    "vboxtray.exe",
    "vmtoolsd.exe",
    "vmwaretray.exe",
    "ida64.exe",
    "ollydbg.exe",
    "pestudio.exe",
    "vmwareuser",
    "vgauthservice.exe",
    "vmacthlp.exe",
    "x96dbg.exe",
    "vmsrvc.exe",
    "x32dbg.exe",
    "vmusrvc.exe",
    "prl_cc.exe",
    "prl_tools.exe",
    "qemu-ga.exe",
    "joeboxcontrol.exe",
    "ksdumperclient.exe",
    "ksdumper.exe",
    "joeboxserver.exe",
    "xenservice.exe",
]

# ANTI-DLL INJECTIONS POSSIBLY ADD


def check_for_dll_injection() -> None:
    """
    Checks whether a dll was injected into program
    """
    if len(psutil.Process().children(recursive=True)) > 0:
        utils.printf("DLL Injection detected. Please restart to continue!", 5)
        time.sleep(1)
        os._exit(-1)


def only_safe_processes() -> None:
    """
    Checks whether blacklisted processes are present while running
    """
    for p in psutil.process_iter():
        for i in BLACKLIST:
            if p.name().replace(" ", "").lower() == i:
                utils.printf(
                    i
                    + " has been detected running on your computer. Please restart to continue program!"
                )
                time.sleep(1)
                os._exit(-1)

    return True


def is_debugger_present() -> None:
    """
    Checks whether a debugger is present while program is running
    """
    if (
        ctypes.windll.kernel32.CheckRemoteDebuggerPresent(
            ctypes.windll.kernel32.GetCurrentProcess(), False
        )
        != 0
    ):
        utils.printf(
            "A has been detected running on your computer. Please restart to continue program!"
        )
        time.sleep(1)
        os._exit(-1)
    if ctypes.windll.kernel32.IsDebuggerPresent() != 0:
        utils.printf(
            "A has been detected running on your computer. Please restart to continue program!"
        )
        os._exit(-1)


def security_thread():
    while True:
        only_safe_processes()
        is_debugger_present()
        check_for_dll_injection()
        time.sleep(2)
