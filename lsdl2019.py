"""lsdl2019 -- Lion's Comprehensive PySDL2 wrapper (2019 version)

"""


import ctypes, shlex, pprint, os, time, math
import sdl2


kA = sdl2.SDLK_a;  kB = sdl2.SDLK_b;  kC = sdl2.SDLK_c
kD = sdl2.SDLK_d;  kE = sdl2.SDLK_e;  kF = sdl2.SDLK_f
kG = sdl2.SDLK_g;  kH = sdl2.SDLK_h;  kI = sdl2.SDLK_i
kJ = sdl2.SDLK_j;  kK = sdl2.SDLK_k;  kL = sdl2.SDLK_l
kM = sdl2.SDLK_m;  kN = sdl2.SDLK_n;  kO = sdl2.SDLK_o
kP = sdl2.SDLK_p;  kQ = sdl2.SDLK_q;  kR = sdl2.SDLK_r
kS = sdl2.SDLK_s;  kT = sdl2.SDLK_t;  kU = sdl2.SDLK_u
kV = sdl2.SDLK_v;  kW = sdl2.SDLK_w;  kX = sdl2.SDLK_x
kY = sdl2.SDLK_y;  kZ = sdl2.SDLK_z;  SPC = sdl2.SDLK_SPACE

k0 = sdl2.SDLK_0;  k1 = sdl2.SDLK_1;  k2 = sdl2.SDLK_2;
k3 = sdl2.SDLK_3;  k4 = sdl2.SDLK_4;  k5 = sdl2.SDLK_5;
k6 = sdl2.SDLK_6;  k7 = sdl2.SDLK_7;  k8 = sdl2.SDLK_8;
k9 = sdl2.SDLK_9

KP0 = sdl2.SDLK_KP_0; KP1 = sdl2.SDLK_KP_1; KP2 = sdl2.SDLK_KP_2
KP3 = sdl2.SDLK_KP_3; KP4 = sdl2.SDLK_KP_4; KP5 = sdl2.SDLK_KP_5
KP6 = sdl2.SDLK_KP_6; KP7 = sdl2.SDLK_KP_7; KP8 = sdl2.SDLK_KP_8
KP9 = sdl2.SDLK_KP_9

KPMINUS = sdl2.SDLK_KP_MINUS; KPPLUS = sdl2.SDLK_KP_PLUS
KPRET = sdl2.SDLK_KP_ENTER;   KPPERIOD = sdl2.SDLK_KP_PERIOD

F1 = sdl2.SDLK_F1;   F2 = sdl2.SDLK_F2;   F3 = sdl2.SDLK_F3
F4 = sdl2.SDLK_F4;   F5 = sdl2.SDLK_F5;   F6 = sdl2.SDLK_F6
F7 = sdl2.SDLK_F7;   F8 = sdl2.SDLK_F8;   F9 = sdl2.SDLK_F9
F10 = sdl2.SDLK_F10; F11 = sdl2.SDLK_F11; F12 = sdl2.SDLK_F12

RET = sdl2.SDLK_RETURN;       ESC = sdl2.SDLK_ESCAPE
RSHIFT = sdl2.SDLK_RSHIFT;    LSHIFT = sdl2.SDLK_LSHIFT
LCTRL = sdl2.SDLK_LCTRL;      RCTRL = sdl2.SDLK_RCTRL
LALT = sdl2.SDLK_LALT;        RALT = sdl2.SDLK_RALT

COMMA = sdl2.SDLK_COMMA;      PERIOD = sdl2.SDLK_PERIOD
LBRACKET = sdl2.SDLK_LEFTBRACKET
RBRACKET = sdl2.SDLK_RIGHTBRACKET
SLASH = sdl2.SDLK_SLASH;      BKSLASH = sdl2.SDLK_BACKSLASH
TICK = sdl2.SDLK_QUOTE;       BKTICK = sdl2.SDLK_BACKQUOTE
MINUS = sdl2.SDLK_MINUS;      EQUAL = sdl2.SDLK_EQUALS
BKSPACE = sdl2.SDLK_BACKSPACE; TAB = sdl2.SDLK_TAB
CAPS = sdl2.SDLK_CAPSLOCK;    NUMLOCK = sdl2.SDLK_NUMLOCKCLEAR
SEMICOLON = sdl2.SDLK_SEMICOLON
LWIN = sdl2.SDLK_LGUI;        RWIN = sdl2.SDLK_RGUI
MENU = sdl2.SDLK_APPLICATION

LEFT = sdl2.SDLK_LEFT;  RIGHT = sdl2.SDLK_RIGHT
UP = sdl2.SDLK_UP;      DOWN = sdl2.SDLK_DOWN


INS = sdl2.SDLK_INSERT;  DEL = sdl2.SDLK_DELETE
HOME = sdl2.SDLK_HOME;   END = sdl2.SDLK_END
PGUP = sdl2.SDLK_PAGEUP; PGDOWN = sdl2.SDLK_PAGEDOWN

PRINTSCREEN = sdl2.SDLK_PRINTSCREEN
SCROLLLOCK = sdl2.SDLK_SCROLLLOCK
BREAK = sdl2.SDLK_PAUSE


eQUIT = sdl2.SDL_QUIT
eKEYDOWN = sdl2.SDL_KEYDOWN
eKEYUP = sdl2.SDL_KEYUP
eMOUSEUP = sdl2.SDL_MOUSEBUTTONUP
eMOUSEDOWN = sdl2.SDL_MOUSEBUTTONDOWN
eMOTION = sdl2.SDL_MOUSEMOTION
eWHEEL = sdl2.SDL_MOUSEWHEEL
eWINDOW = sdl2.SDL_WINDOWEVENT
eTEXTINPUT = sdl2.SDL_TEXTINPUT

eJOYAXIS = sdl2.SDL_JOYAXISMOTION

weMOVED = sdl2.SDL_WINDOWEVENT_MOVED
weEXPOSED = sdl2.SDL_WINDOWEVENT_EXPOSED
weRESIZE = sdl2.SDL_WINDOWEVENT_RESIZED
weSHOWN = sdl2.SDL_WINDOWEVENT_SHOWN
weHIDDEN = sdl2.SDL_WINDOWEVENT_HIDDEN
weENTER = sdl2.SDL_WINDOWEVENT_ENTER
weLEAVE = sdl2.SDL_WINDOWEVENT_LEAVE
weFOCUSED = sdl2.SDL_WINDOWEVENT_FOCUS_GAINED
weBLURRED = sdl2.SDL_WINDOWEVENT_FOCUS_LOST

mLEFT = sdl2.SDL_BUTTON_LEFT
mMIDDLE = sdl2.SDL_BUTTON_MIDDLE
mRIGHT = sdl2.SDL_BUTTON_RIGHT


kmap = {BKTICK: "`~", k1: "1!", k2: "2@", k3: "3#", k4: "4$", k5: "5%",
        k6: "6^", k7: "7&", k8: "8*", k9: "9(", k0: "0)", MINUS: "-_",
        EQUAL: "=+", kQ: "qQ", kW: "wW", kE: "eE", kR: "rR", kT: "tT",
        kY: "yY", kU: "uU", kI: "iI", kO: "oO", kP: "pP", LBRACKET: "[{",
        RBRACKET: "]}", BKSLASH: "\\|", kA: "aA", kS: "sS", kD: "dD", kF: "fF",
        kG: "gG", kH: "hH", kJ: "jJ", kK: "kK", kL: "lL", SEMICOLON: ";:",
        TICK: "'"+'"', kZ: "zZ", kX: "xX", kC: "cC", kV: "vV", kB: "bB",
        kN: "nN", kM: "mM", COMMA: ",<", PERIOD: ".>", SLASH: "/?", SPC: "  "}


QUIT = "QUIT"
W = "W"; RR = "RR"; T_COLL = "T_COLL"  # window, renderer, collision texture
MX = "MX"; MY = "MY"  # mouse X & Y
K = "K"; CH = "CH"  # key/button, character
JOY1 = "JOY1"  # the joystick, if there is one

g = {QUIT: False,
     eKEYDOWN: None, eKEYUP: None,
     eMOUSEUP: None, eMOUSEDOWN: None, eMOTION: None,
     W: None, RR: None, T_COLL: None,
     MX: None, MY: None,
     K: None, CH: None,
     JOY1: None}

down = set()  # keys (& buttons) held down presently


def enc(s): return s.encode("ascii", "replace")

# ACCESSIBLE VIA interact()
def search(s, pfix="SDL"):  # search SDL2 for a given string
    L, s, pfix = [], s.lower(), pfix.lower()
    for x in dir(sdl2):
        x_orig, x = x, x.lower()
        if s in x and x.startswith(pfix): L.append(x_orig)
    return L

def codestr(k, prefix=""):  # ACCESSIBLE VIA interact()
    return [n for n in globals() if globals()[n] == k and n.startswith(prefix)]

def sdlcodestr(k, prefix = ""):  # ACCESSIBLE VIA interact()
    return [n for n in dir(sdl2) if getattr(sdl2, n) == k and n.startswith(prefix)]


def init():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO|sdl2.SDL_INIT_JOYSTICK)
    if sdl2.SDL_NumJoysticks() > 0:
        print("joysticks detected")
        sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)
        g[JOY1] = sdl2.SDL_JoystickOpen(0)

def quit(): sdl2.SDL_Quit(); g[QUIT] = True

def delay(ms): sdl2.SDL_Delay(ms)


WINPOS = "WINPOS"
WINFLAGS = "WINFLAGS"

posUNDEF = sdl2.SDL_WINDOWPOS_UNDEFINED
posCENTER = sdl2.SDL_WINDOWPOS_CENTERED
winFULLSCREEN = sdl2.SDL_WINDOW_FULLSCREEN
winDESKTOP = sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP
winOPENGL = sdl2.SDL_WINDOW_OPENGL
winSHOWN = sdl2.SDL_WINDOW_SHOWN
winHIDDEN = sdl2.SDL_WINDOW_HIDDEN

g[WINPOS] = (posUNDEF, posUNDEF)
g[WINFLAGS] = winSHOWN

# flags: "F" -- full screen;  "C" -- collisions texture, too;  "R" -- resizable (size=minsize)
#        "p" -- turn off mouse pointer
def window(ttl, w, h, flags=""):
    if "F" in flags:
        g[W] = sdl2.SDL_CreateWindow(enc(ttl), posUNDEF, posUNDEF, 0, 0, winDESKTOP)
    else:
        g[W] = sdl2.SDL_CreateWindow(enc(ttl), g[WINPOS][0], g[WINPOS][1], w, h, g[WINFLAGS])
        if "R" in flags:
            sdl2.SDL_SetWindowResizable(g[W], True)
            sdl2.SDL_SetWindowMinimumSize(g[W], w, h)
    g[RR] = sdl2.SDL_CreateRenderer(g[W], -1, sdl2.SDL_RENDERER_ACCELERATED)
    if "F" in flags:
        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"1")
        sdl2.SDL_RenderSetLogicalSize(g[RR], w, h)
    if "C" in flags:
        g[T_COLL] = texture(w,h)
    if "p" in flags: show_cursor(False)
    return g[W], g[RR]

def wdestroy():
    if g[T_COLL]: tdestroy(g[T_COLL])
    sdl2.SDL_DestroyWindow(g[W]); g[W] = g[RR] = None
    for x in list(font_textures): del font_textures[x]  # seems to be necessary for fonts to work again

def windowWH():
    w = ctypes.c_int(0); h = ctypes.c_int(0)
    sdl2.SDL_GetWindowSize(g[W], ctypes.byref(w), ctypes.byref(h))
    return w.value, h.value

def displayWH():
    dm = sdl2.SDL_DisplayMode()
    if sdl2.SDL_GetDesktopDisplayMode(0, ctypes.byref(dm)) == -1:
        print(sdl2.SDL_GetError().decode("ascii"))
        raise EnvironmentError()
    return dm.w, dm.h

def resize():  # resize g[T_COLL], if it exists
    ww, wh = windowWH()
    if g[T_COLL] is not None: tdestroy(g[T_COLL])
    g[T_COLL] = texture(ww, wh)


def event(): return sdl2.SDL_Event()

evt = event()

def kcode(): return evt.key.keysym.sym  # key symbol code for an eKEYDOWN or eKEYUP event
def wevent(): return evt.window.event  # window event code for an eWINDOW event; ex: weFOCUSED

def poll():
    result = sdl2.SDL_PollEvent(ctypes.byref(evt))
    if evt.type == eWINDOW:
        if wevent() == weRESIZE: resize()  # intercept RESIZE to resize T_COLL
    elif evt.type in [eMOUSEDOWN, eMOUSEUP]:
        g[MX] = evt.button.x; g[MY] = evt.button.y
        g[K] = evt.button.button
        if evt.type == eMOUSEDOWN: down.add(g[K])
        else: down.discard(g[K])
    elif evt.type in [eKEYDOWN, eKEYUP]:
        g[K] = kcode()
        g[CH] = kmap.get(g[K], [None,None])[1 if shiftkey() else 0]
        if evt.type == eKEYDOWN: down.add(g[K])
        else: down.discard(g[K])
    elif evt.type == eMOTION:
        g[MX] = evt.motion.x; g[MY] = evt.motion.y
    return result

# expand with: https://wiki.libsdl.org/SDL_Keymod
#   (LCTRL, RCTRL, LALT, RALT)
key_to_keymod = {RSHIFT: sdl2.KMOD_RSHIFT,
                 LSHIFT: sdl2.KMOD_LSHIFT,
                 LCTRL: sdl2.KMOD_LCTRL,
                 RCTRL: sdl2.KMOD_RCTRL,
                 LALT: sdl2.KMOD_LALT,
                 RALT: sdl2.KMOD_RALT}

def pressed(key): return sdl2.SDL_GetModState() & key_to_keymod.get(key, 0)


WHITE = 0;          PALE = 1;           RED = 2;            PINK = 3
ORANGE = 4;         BROWN = 5;          YELLOW = 6;         GREEN = 7
LIGHT_GREEN = 8;    BLUE = 9;           LIGHT_BLUE = 10;    PURPLE = 11
LIGHT_PURPLE = 12;  UGLY = 13;          BLACK = 14;         GRAY = 15

colorchars1 = {"W": WHITE, "R": RED, "O": ORANGE, "Y": YELLOW, "G": GREEN,
               "B": BLUE, "P": PURPLE, "X": BLACK, "w": PALE, "r": PINK,
               "o": BROWN, "g": LIGHT_GREEN, "b": LIGHT_BLUE, "p": LIGHT_PURPLE,
               "U": UGLY, "x": GRAY,
               # -- Alternative, uppercase codes, for lower-case colors
               "S": PINK,  # "Salmon"
               "T": BROWN,  # "Tan"
               "V": LIGHT_GREEN,  # "Veridity"
               "C": LIGHT_BLUE,  # "Cyan"
               "L": LIGHT_PURPLE,  # "Lavendar"
               "A": PALE,  # "Ash"
               "D": GRAY  # "Dark"
              }

colorvals = [(255, 255, 255), (226, 226, 226), (237, 28, 36),
             (255, 174, 201), (241, 171, 7), (125, 89, 4),
             (255, 242, 0), (34, 177, 76), (117, 255, 134),
             (0, 162, 232), (153, 217, 234), (131, 52, 174),
             (192, 140, 221), (231, 46, 235), (0, 0, 0), (92, 92, 92)]

themes = {"synthwave": [(255, 255, 255), (162, 250, 251), (161, 44, 59),
                        (225, 190, 236), (250, 159, 19), (205, 121, 73),
                        (209, 202, 73), (15, 143, 19), (45, 173, 51),
                        (21, 20, 133), (124, 152, 205), (64, 30, 110),
                        (181, 56, 180), (191, 29, 204), (23, 2, 49),
                        (72, 178, 209)]}

def theme(named): colorvals[:] = themes[named]


colornames = ["WHITE", "PALE", "RED", "PINK",
              "ORANGE", "BROWN", "YELLOW", "GREEN",
              "LIGHT_GREEN", "BLUE", "LIGHT_BLUE", "PURPLE",
              "LIGHT_PURPLE", "UGLY", "BLACK", "GRAY"]

colorchars = ["WWhite", "wAsh", "RRed", "rSalmon",
              "OOrange", "oTan", "YYellow", "GGreen",
              "gVeridity", "BBlue", "bCyan", "PPurple",
              "pLavendar", "UUgly", "XX(black)", "xDark"]

def color(c): rgb(*colorvals[c])
def colorch(ch):
    for (i, x) in enumerate(colorchars):
        if ch in x[:2]: return color(i)
def colori(i): rgb((i & 0xFF0000) >> 16, (i & 0x00FF00) >> 8, i & 0x0000FF)
def rgb(r,gg,b,a=255): sdl2.SDL_SetRenderDrawColor(g[RR], r,gg,b,a)
def getrgb():
    r,gg,b,a = [ctypes.c_ubyte(0), ctypes.c_ubyte(0), ctypes.c_ubyte(0),
                ctypes.c_ubyte(0)]
    sdl2.SDL_GetRenderDrawColor(g[RR], r, gg, b, a)
    return r.value, gg.value, b.value, a.value


bNONE = sdl2.SDL_BLENDMODE_NONE    # B:0 no blending    https://wiki.libsdl.org/SDL_BlendMode
bBLEND = sdl2.SDL_BLENDMODE_BLEND  # B:A alpha blending
bADD = sdl2.SDL_BLENDMODE_ADD      # B:+ additive blending
bMOD = sdl2.SDL_BLENDMODE_MOD      # B:M color modulate

BLEND = "BLEND"; g[BLEND] = bNONE

def blend(mode): sdl2.SDL_SetRenderDrawBlendMode(g[RR], mode); g[BLEND] = mode


def show_cursor(true_is_yes):
    sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE if true_is_yes else sdl2.SDL_DISABLE)


def point(x, y): sdl2.SDL_RenderDrawPoint(g[RR], x, y)

def line(x1, y1, x2, y2, form=""):
    if form == "": sdl2.SDL_RenderDrawLine(g[RR], x1,y1, x2,y2)
    elif form == "B": sdl2.SDL_RenderDrawRect(g[RR], rect(x1,y1, x2-x1,y2-y1))
    elif form == "BF": sdl2.SDL_RenderFillRect(g[RR], rect(x1,y1, x2-x1,y2-y1))
    elif form == "X": line(x1,y1, x2, y2); line(x2,y1,x1,y2)
    elif form == "+":
        xmid = (x1+x2)//2; ymid = (y1+y2)//2
        line(xmid, y1, xmid, y2); line(x1, ymid, x2, ymid)

def direct_line(x1, y1, x2, y2): sdl2.SDL_RenderDrawLine(g[RR], x1,y1, x2,y2)
def direct_box(x,y, w,h): sdl2.SDL_RenderDrawRect(g[RR], rect(x,y, w,h))
def direct_fillbox(x,y, w,h): sdl2.SDL_RenderFillRect(g[RR], rect(x,y, w,h))

def clear(): sdl2.SDL_RenderClear(g[RR])

def present(): sdl2.SDL_RenderPresent(g[RR])  # basically, a flip


def ticks(): return sdl2.SDL_GetTicks()


def rect(x=0,y=0,w=0,h=0): return sdl2.SDL_Rect(x,y,w,h)


def texture(w, h):
    return sdl2.SDL_CreateTexture(g[RR], sdl2.SDL_PIXELFORMAT_ARGB8888,
                                  sdl2.SDL_TEXTUREACCESS_TARGET,
                                  w, h)

def tdestroy(t): sdl2.SDL_DestroyTexture(t)

def copy(t, src=None, dest=None):
    return sdl2.SDL_RenderCopy(g[RR], t, src, dest)

def safecopy(t, src=None, dest=None):  # use when copying overlapping regions within same texture
    tmp = texture(src.w, src.h)
    target(tmp)
    copy(t, src, None)
    target(t)
    copy(tmp, None, dest)
    tdestroy(tmp)


def target(t=None): sdl2.SDL_SetRenderTarget(g[RR], t)


# ------------------[ Collision Texture ]---------------------------------------

coll = []  # collisions texture table (index = R*2^16 + G*2^8 + B)

def coll_clear():
    del coll[:]
    color(BLACK)
    target(g[T_COLL])
    clear()

def coll_register(arg):  # associates arg w/ a given entry; returns the entry index (supply it to colori)
    coll.append(arg)
    return len(coll)-1

def readi(x, y):  # appears to work..!  -- but there'd probably be problems if textures worked differently...
    target(g[T_COLL])
    pixeldata = ctypes.c_uint32(0)
    (w,h) = windowWH()
    sdl2.SDL_RenderReadPixels(g[RR], rect(x, y, 1, 1),
                              0, # use texture format's default texture,
                              ctypes.byref(pixeldata), w*4)
    return pixeldata.value


# ------------------[ Saving/Loading Bitmaps ]----------------------------------

def s2t(s): return sdl2.SDL_CreateTextureFromSurface(g[RR], s)

def sfree(s): sdl2.SDL_FreeSurface(s)

def jpgt(fname):  # JPG -> texture
    import sdl2.sdlimage
    s = sdl2.sdlimage.IMG_Load(enc(fname))
    t = s2t(s)
    sfree(s)
    return t

def bmpt(fname):  # BMP -> texture
    s = sdl2.SDL_LoadBMP(enc(fname))
    t = s2t(s)
    sfree(s)
    return t

def save_bmp(s, filename):
    s_w = s.contents.w
    s_h = s.contents.h
    s_format = s.contents.format
    s_format2 = s_format.contents.format
    
    s_Bpp = s_format.contents.BytesPerPixel
    s_bpp = s_format.contents.BitsPerPixel
    s_cliprect = s.contents.clip_rect
    s_Rmask = s_format.contents.Rmask
    s_Gmask = s_format.contents.Gmask
    s_Bmask = s_format.contents.Bmask
    s_Amask = s_format.contents.Amask
    
    # pixels
    p = ctypes.create_string_buffer(s_w * s_h * s_Bpp)
    
    r = rect(0, 0, s_w, s_h)
    
    sdl2.SDL_RenderReadPixels(g[RR], ctypes.byref(r), s_format2, p, s_w * s_Bpp)
    rgb = sdl2.SDL_CreateRGBSurfaceFrom(p, s_w, s_h, s_bpp, s_w * s_Bpp,
                                        s_Rmask, s_Gmask, s_Bmask, s_Amask)
    sdl2.SDL_SaveBMP(rgb, enc(filename))


# ------------------[ Fonts, Text ]---------------------------------------------

fontkeys = """
ABCDEFGHIJKLMNOPQRS
abcdefghijklmnopqrs
TUVWXYZ1234567890-=
tuvwxyz!@#$%^&*()_+
`~[{]}\\|;:'",<.>/? 
""".strip("\n")

FW = "FW"; FH = "FH"  # font width, height
FFP = "FFP"; FT = "FT"; FTI = "FTI"  # font path, font (???), font image

g[FW] = 8; g[FH] = 16; g[FFP] = None; g[FT] = None; g[FTI] = None

font_textures = {}
f8x8 = (8, 8, "fonts/F8x8.bmp")
f6x9 = (6, 9, "fonts/F6x9.bmp")
f8x16 = (8, 16, "fonts/f8x16.bmp")

def font(f=None):  # f = (fw, fh, fp)  i.e. f8x8, f6x9, or f8x16; sets FW, FH, FT
    if f is None: return (g[FW], g[FH], g[FFP])
    g[FW], g[FH], g[FFP] = f  # ffp: (f)ont-(f)ile(p)ath
    if f not in font_textures: font_textures[f] = bmpt(g[FFP])
    g[FT] = font_textures[f]

def press(s, x0, y, cursor_i=None, cursor_color=WHITE, scale=1):
    sdl2.SDL_SetTextureColorMod(g[FT], *getrgb())
    sdl2.SDL_SetTextureBlendMode(g[FT], g[BLEND])
    x = x0
    ch_i = 0
    w,h = g[FW]*scale, g[FH]*scale
    for ch in s:  # don't enumerate; want ch_i to work if s == ""
        if ch == "\n": x = x0; y += h; continue
        try: i = fontkeys.index(ch)
        except ValueError: i = fontkeys.index("!")
        fx, fy = (i%20)*g[FW], (i//20)*g[FH]
        copy(g[FT], rect(fx, fy, g[FW], g[FH]), rect(x, y, w, h))
        if ch_i == cursor_i:  # draw cursor
            color(cursor_color)
            line(x, y, x+w, y+h, "B")
        x += w
        ch_i += 1
    if ch_i == cursor_i:  # draw cursor
        color(cursor_color)
        line(x, y, x+w, y+h, "B")

def backtype(s, x0, y, dataobj=None):  # fill collision texture
    if dataobj is None: dataobj = s
    target(g[T_COLL])
    x = x0
    for (i, ch) in enumerate(s):
        if ch == "\n": x = x0; y += g[FH]; continue
        colori(coll_register((dataobj, i)))
        line(x, y, x+g[FW], y+g[FH], "BF")
        x += g[FW]


# ------------------[ Input State ]---------------------------------------------

def mouse_pos():
    # https://bitbucket.org/marcusva/py-sdl2/issue/10/mouse-module-issues
    x = ctypes.c_int(0)
    y = ctypes.c_int(0)
    buttons = sdl2.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
    return (x.value, y.value)

shiftkey = lambda: (LSHIFT in down) or (RSHIFT in down)
ctrlkey = lambda: (LCTRL in down) or (RCTRL in down)
altkey = lambda: (LALT in down) or (RALT in down)


# ------------------[ Rectangle Processing ]------------------------------------


def rectspec(cmds, S=None):
    if S is None: S = []
    x0,y0,x1,y1 = 0,0,0,0
    for cmd in cmds.split():
        CMD = cmd.upper()
        if CMD == "BREAK": breakpoint()
        elif CMD == ".": print(S.pop())
        elif CMD == ".S": print(S)
        elif CMD == ".R": print(f"({x0}, {y0}) - ({x1}, {y1})")
        elif CMD == "DUP": S.append(S[-1])
        elif CMD == "SWAP": S[-2], S[-1] = S[-1], S[-2]
        elif CMD == "MIN": S.append(min(S.pop(), S.pop()))
        elif CMD == "MAX": S.append(max(S.pop(), S.pop()))
        elif CMD == "SCREEN": x0,y0, x1,y1 = (0,0)+displayWH()
        elif CMD == "WINDOW": x0,y0, x1,y1 = (0,0)+windowWH()
        elif CMD == "FWH": x0,y0, x1,y1 = (0,0,g[FW],g[FH])
        elif CMD == "X0": S.append(x0)
        elif CMD == "Y0": S.append(y0)
        elif CMD == "X1": S.append(x1)
        elif CMD == "Y1": S.append(y1)
        elif CMD == "W": S.append(x1-x0)
        elif CMD == "H": S.append(y1-y0)
        elif CMD == "FW": S.append(g[FW])
        elif CMD == "FH": S.append(g[FH])
        elif CMD == "!X0": x0 = S.pop()
        elif CMD == "!Y0": y0 = S.pop()
        elif CMD == "!X1": x1 = S.pop()
        elif CMD == "!Y1": y1 = S.pop()
        elif CMD == "SLIDE-X": n = S.pop(); x0 += n; x1 += n
        elif CMD == "SLIDE-Y": n = S.pop(); y0 += n; y1 += n
        elif CMD == "SKIP-X": n = S.pop(); w = x1-x0; x0 = x1+n; x1 = x0+w
        elif CMD == "SKIP-Y": n = S.pop(); h = y1-y0; y0 = y1+n; y1 = y0+h
        elif CMD == "!W": c = (x0+x1)//2; d2 = S.pop()//2; x0 = c-d2; x1 = c+d2
        elif CMD == "!H": c = (y0+y1)//2; d2 = S.pop()//2; y0 = c-d2; y1 = c+d2
        elif CMD == "!W-LEFT": x1 = x0+S.pop()
        elif CMD == "!W-RIGHT": x0 = x1-S.pop()
        elif CMD == "!H-TOP": y1 = y0+S.pop()
        elif CMD == "!H-BOTTOM": y0 = y1-S.pop()
        elif CMD == "GROW": v=S.pop(); x0 -= v; x1 += v; y0 -= v; y1 += v
        elif CMD == "%": p=S.pop(); v=S.pop(); S.append((v*p)//100)
        elif CMD == "+": S.append(S.pop()+S.pop())
        elif CMD == "-": less=S.pop(); S.append(S.pop()-less)
        elif CMD == "*": S.append(S.pop()*S.pop())
        elif CMD == "/": div=S.pop(); S.append(S.pop()//div)
        elif CMD == "%": div=S.pop(); S.append(S.pop()%div)
        elif CMD == "/%": div=S.pop(); num=S.pop(); S.append(num//div); S.append(num%div)
        elif CMD == "INV": S.append(-S.pop())
        elif CMD == "T": S.append(time.time())
        elif CMD == "SIN": S.append(math.sin(S.pop()))
        elif CMD == "INT": S.append(int(S.pop()))
        elif CMD[0] == "'": S.append(cmd[1:])
        elif CMD == "LOAD": x0,y0,x1,y1 = g[S.pop()]  # deprecated
        elif CMD == "LOAD-XYXY": x0,y0,x1,y1 = g[S.pop()]
        elif CMD == "LOAD-XYWH": x0,y0,w,h = g[S.pop()]; x1 = x0+w; y1 = y0+h
        elif CMD == "LOAD-X0Y0": x0,y0 = g[S.pop()]
        elif CMD == "LOAD-X1Y1": x1,y1 = g[S.pop()]
        elif CMD == "LOAD-N": S.extend(g[S.pop()])
        elif CMD == "LOAD-1": S.append(g[S.pop()])
        elif CMD == "SAVE": g[S.pop()] = (x0,y0,x1,y1)  # deprecated
        elif CMD == "SAVE-XYXY": g[S.pop()] = (x0,y0,x1,y1)
        elif CMD == "SAVE-XYWH": g[S.pop()] = (x0,y0,x1-x0,y1-y0)
        elif CMD == "SAVE-NW": g[S.pop()] = (x0,y0)
        elif CMD == "SAVE-SE": g[S.pop()] = (x1,y1)
        elif CMD == "SAVE-NE": g[S.pop()] = (x1,y0)
        elif CMD == "SAVE-SW": g[S.pop()] = (x0,y1)
        elif CMD == "SAVE-1": varname = S.pop(); g[varname] = S.pop()
        elif CMD == "PUSH": S.append((x0,y0,x1,y1))
        elif CMD == "POP": (x0,y0,x1,y1) = s.pop()
        elif CMD == "PUSH-XYWH": S.append((x0,y0,x1-x0,y1-y0))
        elif CMD == "POP-XYWH": x0,y0,w,h = S.pop(); x1 = x0+w; y1 = y0+h
        elif CMD == "OVERSIZE": w,h = windowWH(); S.append(x0 < 0 or y0 < 0 or x1 >= w or y1 >= h)
        elif CMD == "?":
            print(".S .R -- print rectangle")
            print("DUP SWAP")
            print("SCREEN WINDOW FWH  -- set rectangle to given size")
            print("X0 Y0 X1 Y1 W H FW FH  -- put given dimension onto stack")
            print("!X0 !Y0 !X1 !Y1  -- set coordinate directly")
            print("!W !H  -- set width or height, preserving center")
            print("!W-LEFT !W-RIGHT !H-TOP !H-BOTTOM  -- set width or height, to a side")
            print("SLIDE-X SLIDE-Y") 
            print("SKIP-X SKIP-Y  -- like slide, but based on a gutter distance")
            print("GROW  -- grow outward by N")
            print("% + - * / % /% SIN INT -- std. mathematical ops; % is 100-based")
            print("T  -- append time (as a float)")
            print("'...  -- append a string")
            print("SAVE LOAD SAVE-XYWH LOAD-XYWH  -- save rectangle to named string in g")
            print("PUSH POP PUSH-XYWH POP-XYWH  -- save rectangle to stack")
            print("OVERSIZE  -- push True (rect over window size) or False (not so)")
        else:
            try: S.append(int(CMD))
            except ValueError: breakpoint()
    return S


# General Graphics, Expedited

def gfx(s, x=None, y=None, data=None):
    def getxy(s):  # read two integers (x,y) from substring
        nonlocal data
        if s == "DATA": vals = data.pop()
        else: vals = s.split(",")
        if len(vals) == 1: return g[s]  # was name of a g-var (ex: "PT")
        else: return [int(x) for x in vals]
    def getxyxy(s):  # read four integers (x,y,x,y) from substring
        nonlocal x,y, data
        if s == "DATA": vals = data.pop()
        else: vals = s.split(",")
        if len(vals) == 1: vals = g[s]  # was name of a g-var (ex: "BG")
        else: vals = [int(x) for x in vals]
        return [x,y]+vals if len(vals) == 2 else vals
    if x is None: x=g[MX]
    if y is None: y=g[MY]
    data = data or []
    for cmd in s.split():
        if cmd.startswith("C:"): colorch(cmd[2])
        elif cmd == "B:0": blend(bNONE)  # no blending
        elif cmd == "B:+": blend(bADD)  # additive blending
        elif cmd == "B:A": blend(bBLEND)  # alpha blending
        elif cmd == "B:M": blend(bMOD)  # color modulate
        elif cmd == "8x8": font(f8x8)
        elif cmd == "6x9": font(f6x9)
        elif cmd == "8x16": font(f8x16)
        elif cmd.startswith("+XY:"):
            dx,dy = getxy(cmd[4:])
            x += dx; y += dy
        elif cmd == "XY:M": x,y = g[MX] or 0, g[MY] or 0
        elif cmd.startswith("XY:"): x,y = getxy(cmd[3:])
        elif cmd in ["X", "+"]: line(x-5,y-5,x+5,y+5, cmd)
        elif cmd == "|": line(x,0,x,windowWH()[1])
        elif cmd == "-": line(0,y,windowWH()[0],y)
        elif cmd == "[]": line(x-5,y-5,x+5,y+5, "BF")
        elif cmd == "[f]":
            qx = (x//g[FW])*g[FW];  qy = (y//g[FH])*g[FH]
            line(qx, qy, qx+g[FW], qy+g[FH], "B")
        elif (cmd.startswith("L:") or cmd.startswith("B:")
              or cmd.startswith("X:") or cmd.startswith("+:")):
            (x,y,x2,y2) = getxyxy(cmd[2:])
            line(x,y,x2,y2, "" if cmd[0] == "L" else cmd[0]); x,y = x2,y2
        elif cmd.startswith("BF:"):
            (x,y,x2,y2) = getxyxy(cmd[3:])
            line(x,y,x2,y2, "BF"); x,y = x2,y2
        elif cmd == "CLS": color(BLACK); clear()
        elif cmd == ".": point(x,y)
        elif cmd == "X,Y": press(str("{},{}".format(x,y)), x, y); y += g[FH]
        elif cmd == "TICKS": press(str(ticks()), x, y); y += g[FH]
        elif cmd == "TIME": press(str(time.ctime()), x, y); y += g[FH]
        elif cmd.startswith("T:"): press(cmd[2:], x, y); y += g[FH]
        elif cmd == "T": press(str(data.pop()), x, y); y += g[FH]
        elif cmd == "P": present()
    return x,y


if __name__ == "__main__":
    while True:
        cmds = input("rectspec>  ")
        if cmds.strip() and cmds.upper().split()[0] in ["Q", "QUIT", "X", "EXIT"]: break
        pprint.pprint(rectspec(cmds))


# ------------------[ Interactive System ]--------------------------------------

def welcome():
    print("LSDL 2019 - Lion's Comprehensive SDL2 Wrapper v2019")
    print()

def cmdparts(prompt):
    result = input(prompt+": ").split(None, 1)
    if len(result) == 0: return "", "", []
    elif len(result) == 1: return result[0].upper(), "", []
    else: return result[0].upper(), result[1], shlex.split(result[1])

QUITINTERACT = "QUITINTERACT"

INTERACTMENU = """
  SDL2  - SDL2 information access menu
  COLORS  - print colors table

  OPS  - basic SDL2 operations

  EVENTS  - observing events

  RECT  - rectspec commands

  Q  - quit
  DBG  -- enter Python debugger
  ?  - print this menu

wishlist:
 * check status of RR, W, ...
 * informational access to systems
 * systems to help construct API use
"""

def sdl2interact():
    while not g[QUITINTERACT]:
        (cmd, addl, parts) = cmdparts("sdl2: S/C/SC (Q/?)  ")
        if cmd == "Q": return
        elif cmd == "?":
            print("S: search(s)  -- searches SDL2 module for an identifier with this string")
            print("C: codestr(k)  -- searches lsdl2019 for something with this value")
            print("SC: sdlcodestr(k)  -- searches SDL2 module for something with this value")
            print("Q: quit")
        elif cmd == "S":
            s = input("search(s, pfix='SDL')  - what string to search SDL2 module for?  ")
            for result in search(s):
                print(f"RESULT: {result}")
        elif cmd == "C":
            k = input("codestr(k)  - what key (int or str) to search for a label in lsdl2019.py that matches?  ")
            result = codestr(k)
            if result is None:
                try: result = codestr(int(k))
                except ValueError: pass
            if result is None: print("NOT FOUND")
            else: print(f"RESULT: {result}")
        elif cmd == "SC":
            k = input("sdlcodestr(k)  - what key (int or str) to search for a label in sdl2.py that matches?  ")
            L = sdlcodestr(k)
            if len(L) == 0:
                try: L = sdlcodestr(int(k))
                except ValueError: pass
            if len(L) == 0: print("NOT FOUND")
            else:
                for result in L: print(f"RESULT: {result}")
    print("SDL2 Information Interactive Menu")

def print_colors():
    print("   # identifier             R   G   B   ch alt-character/name")
    print(" --- --------------------  --- --- ---  -- ------------------")
    for (i, name) in enumerate(colornames):
        red, green, blue = colorvals[i]
        character = colorchars[i][0]
        alt = colorchars[i][1:]
        print(f"{i:>4d}  {name:<20} {red:>3d} {green:>3d} {blue:>3d}  {character:<1}  {alt}")

def getint(prompt): return int(input(prompt+":  "))
def getstr(prompt): return input(prompt+":  ")

def ops():
    while not g[QUITINTERACT]:
        (cmd, addl, parts) = cmdparts("ops: W/P/PUMP/!W/WH/DWH C?/C/CC L/B/BF/X B0/B1/B+/BM F/FX/T T0/TC/CPC M1/M0 (Q/?)  ")
        if cmd == "Q": return
        elif cmd == "?":
            print("W: 640x480 window  P: present  PUMP: pump events  !W: close window  WH: width/height DWH: (display)")
            print("C?: print_colors()  C: color(#)  CC: color(char)  CI: colori(#)")
            print("L: line  B: line(...B)  BF: line(...BF)  X: line(...X)  +: line(...+)")
            print("B0: blend(bNONE)  B1: blend(bBLEND)  B+: blend(bADD)  BM: blend(bMOD)")
            print("F: font select  FX: custom font selection  T: type text (via press function)")
            print("T0: Target: None (primary display  TC: Target:T_COLL (collisions texture)  CPC: (copy collisions texture)")
            print("M1: mouse cursor visible (show_cursor(True));  M0: mouse cursor invisible (show_cursor(False))")
            print("Q: quit")
        elif cmd == "W":
            window("ops window (640x480)", 640, 480, "CR")
            print('window("ops window (640x480)", 640, 480, "CR")')
            print("  flag C: collision texture")
            print("  flag R: resize-able")
        elif cmd == "!W": wdestroy(); print("wdestroy(g[W]) complete")
        elif cmd == "WH": print(f"windowWH(): {windowWH()}")
        elif cmd == "DWH": print(f"displayWH(): {displayWH()}")
        elif cmd == "C?": print_colors()
        elif cmd == "C": color(getint("Color#"))
        elif cmd == "CC": colorch(getstr("Color ch"))
        elif cmd == "CI": colori(getint("Color i#"))
        elif cmd == "T0": target(); print("targeting window's texture")
        elif cmd == "TC": target(g[T_COLL]);  print("targeting T_COLL -- collisions texture")
        elif cmd == "CPC": target(); copy(g[T_COLL]);  print("copied collisions texture to window's texture")
        elif cmd == "L": line(getint("x0"),getint("y0"),getint("x1"),getint("y1"))
        elif cmd == "B": line(getint("x0"),getint("y0"),getint("x1"),getint("y1"), "B")
        elif cmd == "BF": line(getint("x0"),getint("y0"),getint("x1"),getint("y1"), "BF")
        elif cmd == "X": line(getint("x0"),getint("y0"),getint("x1"),getint("y1"), "X")
        elif cmd == "+": line(getint("x0"),getint("y0"),getint("x1"),getint("y1"), "+")
        elif cmd == "B0": blend(bNONE); print("blend(bNONE)")
        elif cmd == "B1": blend(bBLEND); print("blend(bBLEND)")
        elif cmd == "B+": blend(bADD); print("blend(bADD)")
        elif cmd == "BM": blend(bMOD); print("blend(bMOD)")
        elif cmd == "P": present()
        elif cmd == "PUMP":
            while poll(): pass
        elif cmd == "F":
            print("0. f8x8 -- 2014 f8x8.bmp")
            print("1. f6x9 -- 2014 f6x9.bmp")
            print("2. f8x16 -- 2015 f8x16.bmp")
            font([f8x8, f6x9, f8x16][getint("font")])
            print("selected")
        elif cmd == "FX":
            g[FW] = getint("FW: font character width")
            g[FH] = getint("FH: font character height")
            g[FFP] = getstr("FFP: full font filepath (.BMP)")
            g[FT] = bmpt(g[FFP])
            print("font loaded")
        elif cmd == "T":
            print("text to write to display (via press('s',x,y) fn):")
            press(getstr("s"), getint("x"), getint("y"))
            print("written")
        elif cmd == "M1": show_cursor(True)
        elif cmd == "M0": show_cursor(False)

def events():
    if not g[W]: print("you need to create a window, first"); return
    while not g[QUITINTERACT]:
        (cmd, addl, parts) = cmdparts("events: MXY EVTS TRAP JOY (Q/?)")
        if cmd == "Q": return
        elif cmd == "?":
            print("MXY  -- observe mouse X&Y positions, & collision objects")
            print("EVTS  -- observe events")
            print("TRAP  -- trap a specific event")
        elif cmd == "MXY":
            print("press ESC to break")
            quit = False
            while not quit:
                if poll():
                    if evt.type == eKEYDOWN and kcode() == ESC: quit = True
                    elif evt.type == eMOTION:
                        print(f"evt.motion.x -> MX: {g[MX]}  evt.motion.y -> MY: {g[MY]}")
        elif cmd == "EVTS":
            print("press ESC to break")
            quit = False
            while not quit:
                if poll():
                    if evt.type == eKEYDOWN and kcode() == ESC: quit = True
                    print(f"evt.type: {evt.type} <{codestr(evt.type, 'e')} - {sdlcodestr(evt.type)}>")
                    if evt.type == eWINDOW:
                        print(f"  -- eWINDOW: <wevent(): {wevent()} -- {codestr(wevent(), 'we')}>")
        elif cmd == "TRAP":
            trap = globals().get(getstr("lsdl event code (ex: eKEYDOWN, ex: eWINDOW)"))
            if trap is None: print("unrecognized event; aborting"); continue
            if trap == eWINDOW:
                trap2 = globals().get(getstr("window event code (ex: weRESIZE)"))
                if trap2 is None: print("unrecognized window event; aborting"); continue
            print("press ESC to break")
            quit = False
            while not quit:
                if poll():
                    if evt.type == eKEYDOWN and kcode() == ESC: quit = True
                    if evt.type == trap:
                        if trap != eWINDOW or (trap == eWINDOW and trap2 == wevent()):
                            print("trap hit"); breakpoint()
        elif cmd == "JOY":
            print("press ESC to break")
            quit = False
            gfx("8x16 C:B")
            while not quit:
                if poll():
                    if evt.type == eKEYDOWN and kcode() == ESC: quit = True
                    elif evt.type == eJOYAXIS:
                        vals = {}
                        vals[evt.jaxis.axis] = evt.jaxis.value
                        clear();
                        for (axis, val) in vals.items():
                            press(str(val), 50, 50+(axis*20))
                        present()
                        # gfx("XY:DATA T P", data=[str(evt.jaxis.value), (50, 50+(evt.jaxis.axis*20))])
                        #print(f"evt.jaxis: .axis: {evt.jaxis.axis}; .value: {evt.jaxis.value}")

def live():
    welcome()
    g[QUITINTERACT] = False
    while not g[QUITINTERACT]:
        (cmd, addl, parts) = cmdparts("interact: SDL2 COLORS OPS EVENTS RECT (Q/DBG/?)  ")
        if cmd == "Q": g[QUITINTERACT] = True
        elif cmd == "SDL2": sdl2interact()
        elif cmd == "COLORS": print_colors()
        elif cmd == "OPS": ops()
        elif cmd == "EVENTS": events()
        elif cmd == "RECT": rectspec(getstr("rectspec (?=help)"))
        elif cmd == "?": print(INTERACTMENU)
        elif cmd == "DBG": breakpoint()  # keep this one last

