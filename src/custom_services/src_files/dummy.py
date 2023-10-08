# Built-in packages
import time

# Third-party packages

# Local packages


if __name__ == '__main__':
    for i in range(10):
        print(f"Keep alive: {i}")
        with open("/var/log/hw.log","a") as f:
            f.write(f"Keep alive: {i}")
        time.sleep(1)