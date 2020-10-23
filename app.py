from sig import SIG
from threading import Thread
import cProfile


def th(offset=1024):
    while offset > 0:
        thread = Thread(
            target=SIG.generate_sig,
            name="SIGThread-{}".format(offset)
        )
        thread.start()
        offset -= 1


if __name__ == "__main__":
    i = 1024 ** 3
    while i > 0:
        cProfile.run("SIG.generate_sig()")
        i -= 1
