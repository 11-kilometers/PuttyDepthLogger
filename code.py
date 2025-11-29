# code.py — Feather RP2040 Adalogger + LPS28
# - Logs to /sd/Logs/pressure_log_<NNNN>.csv
# - Creates a new file each boot by incrementing N
# - Flushes each write and fsyncs every SYNC_PERIOD_S seconds

import time, os, board
import adafruit_lps28

LOG_DIR = "/sd/Logs"
CSV_HEADER = "timestamp_s,pressure_hPa,temperature_C\n"
SAMPLE_PERIOD = 1.0          # seconds
SYNC_PERIOD_S = 5.0          # fsync cadence (1–10 s typical)

print("code.py: LPS28 → /sd/Logs logger")

# ----- Wait for /sd to be mounted (boot.py handles mount policy) -----
t0 = time.monotonic()
while "sd" not in os.listdir("/"):
    if time.monotonic() - t0 > 5.0:
        print("WARNING: /sd not found; logging disabled.")
        break
    time.sleep(0.05)

def ensure_dir(path):
    try:
        os.stat(path)
    except OSError:
        os.mkdir(path)
        print("Created directory", path)

def next_log_path(dirpath):
    """Finds next index and returns '/sd/Logs/pressure_log_<NNNN>.csv'."""
    try:
        names = os.listdir(dirpath)
    except Exception:
        names = []
    max_n = 0
    prefix = "pressure_log_"
    suffix = ".csv"
    for name in names:
        if name.startswith(prefix) and name.endswith(suffix):
            mid = name[len(prefix):-len(suffix)]
            try:
                n = int(mid)
                if n > max_n:
                    max_n = n
            except ValueError:
                pass
    next_n = max_n + 1
    return "{}/{}{:04d}{}".format(dirpath, prefix, next_n, suffix)

def ensure_csv(path):
    try:
        os.stat(path)
    except OSError:
        with open(path, "w") as f:
            f.write(CSV_HEADER)
        print("Created", path)

# ----- Sensor -----
i2c = board.I2C()
lps28 = adafruit_lps28.LPS28(i2c)  # default 0x5C
print("LPS28 ready")

log_path = None
if "sd" in os.listdir("/"):
    ensure_dir(LOG_DIR)
    log_path = next_log_path(LOG_DIR)
    ensure_csv(log_path)
    print("Logging to:", log_path)

last_sample = 0.0
last_sync = time.monotonic()

while True:
    now = time.monotonic()
    if now - last_sample >= SAMPLE_PERIOD:
        last_sample = now
        try:
            p = lps28.pressure        # hPa
            t = lps28.temperature     # °C

            if log_path and "sd" in os.listdir("/"):
                with open(log_path, "a") as f:
                    f.write(f"{int(time.time())},{p:.3f},{t:.2f}\n")
                    f.flush()  # push Python buffers

                # periodic filesystem-level sync (FAT + card)
                if now - last_sync >= SYNC_PERIOD_S:
                    last_sync = now
                    try:
                        os.sync()
                    except Exception as e:
                        print("sync skipped:", e)

            print(f"P={p:.3f} hPa, T={t:.2f} °C")
        except Exception as e:
            print("Sensor/SD error:", e)

    time.sleep(0.01)
