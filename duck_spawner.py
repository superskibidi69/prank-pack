import time, threading, random, sys, os, io
from AppKit import NSApplication, NSWindow, NSImageView, NSBackingStoreBuffered, NSRect, NSScreen, NSImage
from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
from PyObjCTools import AppHelper
from PIL import Image
from Foundation import NSData

# ---------- CONFIG ----------
duck_files = ["duck.webp", "duck1.webp"]  # duck images
window_size = 128
fps = 60
max_delta = 6

# ---------- HELPER FUNCTIONS ----------
def resource_path(relative_path):
    """Support PyInstaller single-file executable."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def resize_square_keep_aspect(im, size):
    im = im.convert("RGBA")
    w, h = im.size
    ratio = size / max(w, h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0,0,0,0))
    offset_x = (size - new_w) // 2
    offset_y = (size - new_h) // 2
    canvas.paste(im, (offset_x, offset_y))
    return canvas

def pil_to_nsimage(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    data = NSData.dataWithBytes_length_(buf.getvalue(), len(buf.getvalue()))
    return NSImage.alloc().initWithData_(data)

# ---------- LOAD IMAGES ----------
ns_images = []
for f in duck_files:
    path = resource_path(f)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{f} not found")
    im = resize_square_keep_aspect(Image.open(path), window_size)
    ns_images.append(pil_to_nsimage(im))

# ---------- SCREEN BOUNDS ----------
screens = NSScreen.screens()
screen_bounds = []
for s in screens:
    f = s.frame()
    screen_bounds.append({
        "x1": int(f.origin.x),
        "y1": int(f.origin.y),
        "x2": int(f.origin.x + f.size.width),
        "y2": int(f.origin.y + f.size.height)
    })

# ---------- INIT APP ----------
app = NSApplication.sharedApplication()
NSRunningApplication.currentApplication().activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

# ---------- CREATE DUCK WINDOWS ----------
duck_windows = []

for img in ns_images:
    screen = random.choice(screen_bounds)
    x = random.randint(screen["x1"], screen["x2"] - window_size)
    y = random.randint(screen["y1"], screen["y2"] - window_size)
    frame = NSRect((x, y), (window_size, window_size))

    win = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame, 0x10C0000, NSBackingStoreBuffered, False
    )
    win.setLevel_(3)
    win.setOpaque_(False)
    win.setBackgroundColor_(None)

    view = NSImageView.alloc().initWithFrame_(frame)
    view.setImage_(img)
    win.setContentView_(view)
    win.makeKeyAndOrderFront_(None)

    dx = random.choice([-1,1]) * random.randint(2, max_delta)
    dy = random.choice([-1,1]) * random.randint(2, max_delta)

    duck_windows.append({
        "window": win,
        "x": x,
        "y": y,
        "dx": dx,
        "dy": dy,
        "screen": screen
    })

# ---------- MOVE DUCKS ----------
def move_ducks():
    sleep_time = 1 / fps
    while True:
        for d in duck_windows:
            # vary speed slightly
            d["dx"] += random.choice([-1,0,1])
            d["dy"] += random.choice([-1,0,1])
            d["dx"] = max(-max_delta, min(max_delta, d["dx"]))
            d["dy"] = max(-max_delta, min(max_delta, d["dy"]))

            d["x"] += d["dx"]
            d["y"] += d["dy"]

            # bounce within current screen
            if d["x"] < d["screen"]["x1"] or d["x"] + window_size > d["screen"]["x2"]:
                d["dx"] = -d["dx"] + random.choice([-1,0,1])
            if d["y"] < d["screen"]["y1"] or d["y"] + window_size > d["screen"]["y2"]:
                d["dy"] = -d["dy"] + random.choice([-1,0,1])

            d["window"].setFrameOrigin_((d["x"], d["y"]))

        time.sleep(sleep_time)

threading.Thread(target=move_ducks, daemon=True).start()
AppHelper.runEventLoop()
