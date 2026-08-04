from core.kernel import Kernel


def bootstrap():
    print("=" * 50)
    print("        JARVIS AI OS Booting")
    print("=" * 50)

    kernel = Kernel()
    kernel.initialize()

    print("[Bootstrap] Kernel started successfully.")

    return kernel