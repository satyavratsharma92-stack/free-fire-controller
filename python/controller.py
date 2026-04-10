# pip install pyserial keyboard pynput
# Run as ADMINISTRATOR
import serial
import time
import sys
import keyboard
import ctypes
from pynput.mouse import Button, Controller as MouseController

# ── Config ────────────────────────────────────────
COM_PORT        = 'COM3'
BAUD_RATE       = 9600
DEADZONE_LOW    = 400
DEADZONE_HIGH   = 624
AIM_SENSITIVITY = 20

# ── Low-level mouse MOVE only (for in-game camera) ─
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx",          ctypes.c_long),
        ("dy",          ctypes.c_long),
        ("mouseData",   ctypes.c_ulong),
        ("dwFlags",     ctypes.c_ulong),
        ("time",        ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [("type", ctypes.c_ulong), ("_input", _INPUT)]

def send_mouse_move(dx, dy):
    inp = INPUT()
    inp.type = 0
    inp.mi.dx = dx
    inp.mi.dy = dy
    inp.mi.mouseData = 0
    inp.mi.dwFlags = 0x0001  # MOUSEEVENTF_MOVE
    inp.mi.time = 0
    inp.mi.dwExtraInfo = None
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

# ── Mouse (pynput) for clicks only ────────────────
mc         = MouseController()
fire_held  = False
scope_held = False
w_held = a_held = s_held = d_held = False
space_held = False
g_held     = False
q_held     = False
r_held     = False

def delta(v):
    if DEADZONE_LOW < v < DEADZONE_HIGH:
        return 0
    n = (v - 512) / 512.0
    return int(n * abs(n) * AIM_SENSITIVITY)

# ── Connect ───────────────────────────────────────
print(f"Connecting to {COM_PORT}...")
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
time.sleep(2)
ser.flushInput()
print("Ready! Push RIGHT joystick for WASD, LEFT joystick for mouse.")
print("Ctrl+C to stop.\n")

# ── Main loop ─────────────────────────────────────
try:
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue
            p = line.split(',')
            if len(p) != 10:
                continue
            lx, ly, lsw, rx, ry, rsw, btn1, btn2, btn3, btn4 = [int(x) for x in p]
        except:
            continue

        # RIGHT joystick → WASD (W↔S swapped, A↔D swapped)
        if ry > DEADZONE_HIGH and not w_held:         # was ry < DEADZONE_LOW
            keyboard.press('w'); w_held = True
        elif ry <= DEADZONE_HIGH and w_held:
            keyboard.release('w'); w_held = False

        if ry < DEADZONE_LOW and not s_held:          # was ry > DEADZONE_HIGH
            keyboard.press('s'); s_held = True
        elif ry >= DEADZONE_LOW and s_held:
            keyboard.release('s'); s_held = False

        if rx > DEADZONE_HIGH and not a_held:         # was rx < DEADZONE_LOW
            keyboard.press('a'); a_held = True
        elif rx <= DEADZONE_HIGH and a_held:
            keyboard.release('a'); a_held = False

        if rx < DEADZONE_LOW and not d_held:          # was rx > DEADZONE_HIGH
            keyboard.press('d'); d_held = True
        elif rx >= DEADZONE_LOW and d_held:
            keyboard.release('d'); d_held = False

        # BTN1 → Spacebar
        if btn1 == 0 and not space_held:
            keyboard.press('space'); space_held = True
        elif btn1 == 1 and space_held:
            keyboard.release('space'); space_held = False

        # BTN2 → G key
        if btn2 == 0 and not g_held:
            keyboard.press('g'); g_held = True
        elif btn2 == 1 and g_held:
            keyboard.release('g'); g_held = False

        # BTN3 → Q key
        if btn3 == 0 and not q_held:
            keyboard.press('q'); q_held = True
        elif btn3 == 1 and q_held:
            keyboard.release('q'); q_held = False

        # BTN4 → R key
        if btn4 == 0 and not r_held:
            keyboard.press('r'); r_held = True
        elif btn4 == 1 and r_held:
            keyboard.release('r'); r_held = False

        # RIGHT click → Scope (pynput)
        if rsw == 0 and not scope_held:
            mc.press(Button.right); scope_held = True
        elif rsw == 1 and scope_held:
            mc.release(Button.right); scope_held = False

        # LEFT joystick → Camera/Head (inverted X and Y axes)
        mx, my = delta(lx), delta(ly)                 # horizontal normal, vertical inverted
        if mx or my:
            send_mouse_move(mx, my)

        # LEFT click → Fire (pynput)
        if lsw == 0 and not fire_held:
            mc.press(Button.left); fire_held = True
        elif lsw == 1 and fire_held:
            mc.release(Button.left); fire_held = False

except KeyboardInterrupt:
    if w_held:     keyboard.release('w')
    if a_held:     keyboard.release('a')
    if s_held:     keyboard.release('s')
    if d_held:     keyboard.release('d')
    if space_held: keyboard.release('space')
    if g_held:     keyboard.release('g')
    if q_held:     keyboard.release('q')
    if r_held:     keyboard.release('r')
    if fire_held:  mc.release(Button.left)
    if scope_held: mc.release(Button.right)
    ser.close()
    print("Stopped.")