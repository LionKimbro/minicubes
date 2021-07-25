
import time, os, sys, ast, traceback, json, re, webbrowser, subprocess
import pyperclip
import lsdl2019 as lsdl

from lsdl2019 import MX, MY, eMOUSEDOWN, eMOUSEUP, eMOTION  # low risk over-ride name imports

# --[ program control ]-------------------------------------------------
TEARDOWNSAVE = True

# --[ g ]---------------------------------------------------------------
g = {}

# --[ S ]---------------------------------------------------------------
S = []

def push(x): S.append(x)
def pop(): return S.pop()

# --[ constants ]-------------------------------------------------------
MAPW, MAPH = 64, 64  # map width & height in # of squares
SQW, SQH = 16, 16  # square footprint width & height in pixels
CUBEW, CUBEH = 64+32, 32  # cube width & height in characters
CHW, CHH = 8, 16  # how many pixels wide and tall for a character?

TRAYLINE = 56  # vertical position: 0-55: above the tray; 56-63: tray
TOTAL_REGION = (0,0, MAPW, MAPH)
PAGE_REGION = (0,0, MAPW, TRAYLINE)
TRAY_REGION = (0,TRAYLINE, MAPW, MAPH)

# --[ paths ]-----------------------------------------------------------
def path(*pp): return os.path.abspath(os.path.join(*pp).format(**PP))

PP = {}

PP.update({"BASE": path("content")})
PP.update({"FILE": path("{BASE}/minicubes.json"),
           "TRAY": path("{BASE}/tray.json")})

# --[ pyperclip i/o ]---------------------------------------------------
def clipboard_out(lines): pyperclip.copy("\r\n".join(lines))
def clipboard_in(): return pyperclip.paste().split("\r\n")  # returns lines

# --[ file i/o ]--------------------------------------------------------
rutf8 = lambda p: open(p, "r", encoding="utf-8").read()
wutf8 = lambda p, dat: open(p, "w", encoding="utf-8").write(dat)

rjson = lambda p: json.loads(rutf8(p))
wjson = lambda p, dat: wutf8(p, json.dumps(dat))

# --[ cubes: general operations ]---------------------------------------
cubes = []  # global list of loaded cubes

X="X"; Y="Y"; COLOR="COLOR"; TEXT="TEXT"; DATA="DATA"; TAGS="TAGS"
INSIDE="INSIDE"  # tag: INSIDE -- inside the last in/out division
OUTSIDE="OUTSIDE"  # tag: OUTSIDE -- outside the last in/out division
SELECTED="SELECTED"  # tag: SELECTED -- this cube is selected
PROVISIONALLY_SELECTED="PROVISIONALLY_SELECTED"  # ...(user is establishing bounding box)...
IMPORTED="IMPORTED"  # tag: IMPORTED -- this cube was imported  -- BEFORE USE, CLEAR
CLONED="CLONED"  # tag: CLONED -- this cube was cloned  -- BEFORE USE, CLEAR
CREATED="CREATED"  # tag: CREATED -- this cube was created -- BEFORE USE, CLEAR
GENERATED="GENERATED"  # tag: GENERATED -- this cube was created by a script
GHOST="GHOST"  # tag: GHOST -- this cube is a ghost
NOOP="NOOP"  # tag: NOOP -- do not operate on this cube  -- !!CLEAR AFTER USE!!

SCOPE="SCOPE"  # cube-scoped data; product of DATA["PYTHON"]

def cubes_map(cubefn, tag=None, region=None, outside_region=None):
    L = []
    for cube in cubes:
        if tag and tag not in cube[TAGS]: continue
        if NOOP in cube[TAGS]: continue
        if region and not xy_inside_xyxy(cube[X], cube[Y], *region): continue
        if outside_region and xy_inside_xyxy(cube[X], cube[Y], *outside_region): continue
        L.append(cubefn(cube))
    return L

def rmcubes(tag=None, region=None):
    L = []
    for (i, cube) in enumerate(cubes):
        if tag and tag not in cube[TAGS]: continue
        if NOOP in cube[TAGS]: continue
        if region and not xy_inside_xyxy(cube[X], cube[Y], *region): continue
        L.append(i)
    for i in reversed(L):
        del cubes[i]


def inside_outside(x0, y0, x1, y1):  # HMM.. THIS MIGHT NOT ACTUALLY BE NECESSARY...
    for cube in cubes:
        if xy_inside_xyxy(cube[X], cube[Y], x0, y0, x1, y1):
            cubes[TAGS].discard(OUTSIDE)
            cubes[TAGS].add(INSIDE)
        else:
            cubes[TAGS].discard(INSIDE)
            cubes[TAGS].add(OUTSIDE)


def scrubbed_cube(cube):
    return {X: cube[X], Y: cube[Y], COLOR: cube[COLOR], CLINE: cube[CLINE],
            CX: cube[CX], TEXT: list(cube[TEXT])}

def import_cube(c):  # c -- abbreviated cube, not yet a cube
    cubes.append({X: c[X], Y: c[Y], COLOR: c[COLOR], CLINE: c[CLINE],
                  CX: c[CX], TEXT: list(c[TEXT]),
                  DATA: None, TAGS: {IMPORTED,}})
    return cubes[-1]

def clone_cube(cube):
    cubes.append({X: cube[X], Y: cube[Y], COLOR: cube[COLOR], CLINE: cube[CLINE],
                  CX: cube[CX], TEXT: list(cube[TEXT]),
                  DATA: None, TAGS: {CLONED,}})
    return cubes[-1]


def create_cube(x,y):
    cubes.append({X: x, Y: y, COLOR: colorcycle[0], CLINE: 0,
                  CX: 0, TEXT: [],
                  DATA: None, TAGS: {CREATED,}})
    return cubes[-1]


def clear_tag(tag):
    cubes_map(lambda cube: cube[TAGS].discard(tag))

def add_tag(to_add, tag=None, region=None):
    cubes_map(lambda cube: cube[TAGS].add(to_add), tag=tag, region=region)


# Temporary Function:  Diagnostic, reports cube tags
def report_tags():
    report = ""
    for cube in cubes:
        s = "".join([t[0] for t in cube[TAGS]]) if cube[TAGS] else "..;"
        s = f"{s:4}"[:4]
        report += s
    print(report)
    print()

# --[ disk operations ]-------------------------------------------------
def mkdir(p):
    try: os.mkdir(p)
    except OSError: pass  # folder already exists


def wcubes(p, all_cubes): wjson(p, {"CUBES": all_cubes})

def rcubes(p):
    try: return rjson(p)["CUBES"]
    except FileNotFoundError: return []


def save_top_cubes():  # save the page, to PP["FILE"];
    # (graph paper notes: Mini-Cubes Master Cubes List pg. 2)
    wcubes(PP["FILE"], cubes_map(scrubbed_cube, region=PAGE_REGION))

def save_tray():
    wcubes(PP["TRAY"], cubes_map(scrubbed_cube, region=TRAY_REGION))

def load_top_cubes():
    rmcubes(region=PAGE_REGION)
    clear_tag(IMPORTED)
    for pre_cube in rcubes(PP["FILE"]): import_cube(pre_cube)
    rmcubes(tag=IMPORTED, region=TRAY_REGION)

def load_tray():
    rmcubes(region=TRAY_REGION)
    clear_tag(IMPORTED)
    for pre_cube in rcubes(PP["TRAY"]): import_cube(pre_cube)
    rmcubes(tag=IMPORTED, region=PAGE_REGION)


def cubes_to_clipboard(tag=SELECTED):  # exports SELECTED cubes
    clipboard_out(json.dumps(cubes_map(scrubbed_cube, tag=tag),
                             indent=2).splitlines())

def clipboard_to_cubes():  # adds IMPORTED cubes from clipboard
    cc = json.loads("\n".join(clipboard_in()))
    for c in cc: import_cube(c)


def setup_data():
    mkdir(PP["BASE"])
    load_top_cubes()
    load_tray()

def save_data_for_teardown():
    save_top_cubes()
    save_tray()

def switch_file(filename_wo_ext):
    g[FOCUS] = None  # I'm not sure HOW this clears top-right window? but it seems to do so..!
    save_top_cubes()
    PP.update({"FILE": path("{BASE}/"+filename_wo_ext+".json")})
    load_top_cubes()

# --[ positions ]-------------------------------------------------------
X="X"; Y="Y"
def pos(): return (g[X], g[Y])
def setpos(x,y): g[X] = x; g[Y] = y
def slide(dx, dy): g[X] += dx; g[Y] += dy

positions = {}
def gotopos(name): g[X], g[Y] = positions[name]
def namepos(name, retto): positions[name] = pos(); gotopos(retto)
def gotomouse(): g[X], g[Y] = lsdl.g[MX], lsdl.g[MY]

X0="X0"; Y0="Y0"; X1="X1"; Y1="Y1"
def tl(): g[X0] = g[X]; g[Y0] = g[Y]
def br(): g[X1] = g[X]; g[Y1] = g[Y]

def xy_inside_xyxy(x,y, x0,y0,x1,y1):  # [x0-x1) and [y0-y1)
    return not x < x0 and not x >= x1 and not y < y0 and not y >= y1

def inside():
    return xy_inside_xyxy(g[X], g[Y], g[X0], g[Y0], g[X1], g[Y1])

#    . . . . . . . . . . . . . .A A* . . . . . . ..
#    .                          |                 .
#    .                          |
#    .                          |                 .
#    .                          |
#    .                          |                 .
#    .                          B-----------------C
#    .                          | B*              .
#    .                          |
#    .                          |                 .
#    .                          |
#    .                          |                 .
#    E--------------------------D-----------------F
#    E*                                           .
#    . . . . . . . . . . . . . . . . . . . . . .END

setpos(MAPW*SQW, 0); namepos("A", "A"); slide(1, 0); namepos("A*", "A")
slide(0, CUBEH*CHH); namepos("B", "B"); slide(1, 1); namepos("B*", "B")
slide(CUBEW*CHW, 0); namepos("C", "B")
slide(0, CUBEH*CHH+1); namepos("D", "D")
g[X] = 0; namepos("E", "E")
slide(0, 1); namepos("E*", "D")
slide(CUBEW*CHW, 0); namepos("F", "F")
slide(0, 1); slide(0, CHH*2); namepos("END", "END")

def pos_line(a, b):
    gotopos(a); tl(); gotopos(b); br()
    lsdl.line(g[X0], g[Y0], g[X1], g[Y1])

def draw_per_spec(spec):
    L = spec.split()
    while L:
        if L[0].startswith("C:"):  lsdl.gfx(L[0]); del L[0]  # color-shift command
        else: pos_line(L[0], L[1]); del L[:2]  # line


def draw_display_lines():
    draw_per_spec("C:x  A D  B C  E F")
    if g[FOCUS] == W1:
        draw_per_spec("C:Y  A B  B C")
    elif g[FOCUS] == W2:
        draw_per_spec("C:Y  B D  D F")
    elif g[FOCUS] == None:
        draw_per_spec("C:Y A D  D E")

setpos(0, TRAYLINE*SQH); namepos("TRAY-LEFT", "TRAY-LEFT")
slide(MAPW*SQW-1,0); namepos("TRAY-RIGHT", "TRAY-RIGHT")

def draw_tray_lines():
    draw_per_spec("C:x TRAY-LEFT TRAY-RIGHT")


# --[ cube positions ]--------------------------------------------------
# TODO: check if some of these are obsolete (and deleteable or replacable,)
#       now that I've changed the cubes system --2020-03-06
cube_positions = {}
COLLISION="COLLISION"
g[COLLISION] = False  # global variable: has a collision been identified this frame?
g[OUTSIDE] = False  # global variable: are any cubes outside the map, this frame?
g[GHOST] = False  # global variable: does any cube have the GHOST tag?

def update_cube_positions():
    cube_positions.clear()
    cubes_map(lambda cube: cube_positions.setdefault((cube[X], cube[Y]), []).append(cube))

def notice_states():
    g[COLLISION] = any(len(L) > 1 for L in cube_positions.values())
    g[OUTSIDE] = False
    def fn(cube): g[OUTSIDE] = True
    cubes_map(fn, outside_region=TOTAL_REGION)
    g[GHOST] = any(GHOST in cube[TAGS] for cube in cubes)


def cube_at(x, y):
    for cube in cubes:
        if cube[X] == x and cube[Y] == y: return cube
    return None

def spot_near(x,y):  # search around for an empty space nearby
    for (dx,dy) in [(0,0), (1,0), (0,1), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1), (2,0), (0,2), (0,-2), (-2,0)]:
        if not cube_at(x+dx,y+dy):
            return (x+dx,y+dy)
    return None

# --[ cube misc assist ]------------------------------------------------
# TODO: check if some of these are obsolete (and deleteable or replacable,)
#       now that I've changed the cubes system --2020-03-06
colorcycle = [lsdl.WHITE, lsdl.YELLOW, lsdl.GRAY, lsdl.BLUE, lsdl.RED, lsdl.GREEN]

def try_create_cube(x, y):
    if cube_at(x,y) is not None:
        return None
    return create_cube(x,y)

def del_cube(cube):
    try: cubes.remove(cube)
    except ValueError: pass

def data_check(cube):
    if cube[TEXT] and cube[TEXT][0] == "DATA":
        if cube[DATA] is None:
            cube[DATA] = binder_keep(cube[TEXT][1:])
            if "PYTHON" in cube[DATA]:
                cube[DATA][SCOPE] = {"cube": cube, "cubes": cubes}  # clear whatever was there before
                try: exec(cube[DATA]["PYTHON"], cube[DATA][SCOPE])
                except: pass
    else:
        cube[DATA] = None

# --[ selection ]-------------------------------------------------------
def draw_selection_box():
    if g[DRAGGING] and not g[M0CUBE] and mouse_in_map():
        lsdl.color(lsdl.WHITE)
        lsdl.line(g[M0X], g[M0Y], lsdl.g[MX], lsdl.g[MY], "B")

def update_dynamic_selection_cubes():
    clear_tag(PROVISIONALLY_SELECTED)
    add_tag(PROVISIONALLY_SELECTED, region=(g[M0SX], g[M0SY], g[MSX], g[MSY]))

def finish_dynamic_selection():
    if not lsdl.ctrlkey(): clear_tag(SELECTED)  # Ctrl = add to selected, otherwise replace
    add_tag(SELECTED, PROVISIONALLY_SELECTED)
    clear_tag(PROVISIONALLY_SELECTED)

def delete_selected_cubes():
    rmcubes(SELECTED)

# --[ ghost set (drag, cut, paste) ]------------------------------------
GHOST_UNDO="GHOST_UNDO"  # set True if you want an aborted ghost-drag to UNDO
g[GHOST_UNDO] = False

PREGHOST_POSITION = "PREGHOST_POSITION"  # temporary on cubes, for remembering where they were

def retain_preghost_position(cube):
    cube[PREGHOST_POSITION] = (cube[X], cube[Y])

def restore_preghost_position(cube):
    cube[X], cube[Y] = cube[PREGHOST_POSITION]


def ghosting_abort():
    if g[GHOST_UNDO]:
        cubes_map(restore_preghost_position, GHOST)
        clear_tag(GHOST)
    else: rmcubes(GHOST)

def ghosting_finish():
    if not g[GHOST]: return  # do nothing, because there's no ghost
    if ghosting_ok():
        clear_tag(SELECTED)
        add_tag(SELECTED, GHOST)
        clear_tag(GHOST)
    else: ghosting_abort()

def ghosting_copy(): cubes_to_clipboard()
def ghosting_cut(): ghosting_copy(); delete_selected_cubes()

def ghosting_paste():  # adding cubes, not yet selected, in ghost state
    ghosting_abort()  # SAME
    #-------------------
    clear_tag(IMPORTED)
    clipboard_to_cubes()
    clear_tag(SELECTED)  # SIMILAR - to duplicate
    add_tag(SELECTED, IMPORTED) # SIMILAR - to duplicate
    #-------------------
    add_tag(GHOST, IMPORTED)  # SIMILAR: Ghost (IMPORTED)
    cubes_map(retain_preghost_position, GHOST)  # SAME
    g[GHOST_UNDO] = False  # SIMILAR(True)

def ghosting_start_drag(prior_ghost=False):  # dragging SELECTED
    if not prior_ghost: ghosting_abort()  # SAME
    #-------------------
    #-------------------
    add_tag(GHOST, SELECTED)  # SIMILAR(SELECTED)
    cubes_map(retain_preghost_position, GHOST)  # SAME
    g[GHOST_UNDO] = True  # SIMILAR(False)

def ghosting_start_duplicate():
    ghosting_abort()  # SAME
    #-------------------    
    clear_tag(CLONED)  # clone the selected, ...
    cubes_map(clone_cube, SELECTED)
    add_tag(GHOST, CLONED)  # SIMILAR(CLONED)
    clear_tag(SELECTED)  # SIMILAR
    add_tag(SELECTED, GHOST)  # SIMILAR
    #-------------------
    cubes_map(retain_preghost_position, GHOST)  # SAME
    g[GHOST_UNDO] = False  # SIMILAR(False)  (they'll be deleted if they can't be positioned


def ghosting_drag():
    def bump(cube):
        pre_pos = cube[PREGHOST_POSITION]
        cube[X] = pre_pos[0]+g[MDSX]
        cube[Y] = pre_pos[1]+g[MDSY]
    cubes_map(bump, GHOST)

def ghosting_ok():
    return not (g[COLLISION] or g[OUTSIDE])

# --[ data check timer ]------------------------------------------------
DATATIMER="DATATIMER"
g.update({DATATIMER: None})

def reset_data_timer(): g[DATATIMER] = time.time()+1

def check_data_timer():
    if g[DATATIMER] and time.time() > g[DATATIMER]:
        cube = focused_cube()
        if cube: cube[DATA] = None; data_check(cube)
        g[DATATIMER] = None

# --[ gfx ]-------------------------------------------------------------
def setup_gfx():
    gotopos("END")
    lsdl.window("MINI-CUBES", g[X],g[Y], "pR")
    lsdl.font(lsdl.f8x16)
    g[MOUSESTATE] = 0; g[TTARGET] = None
    g[DRAGGING] = False
    lsdl.g[MX] = lsdl.g[MY] = 0  # because: update_mouse_coordinates() needs non-None

def lsdl_stuff():  # friendly package of stuff from lsdl scope
    return (lsdl.g, lsdl.evt, lsdl.K, lsdl.CH)  # gg, evt, K, CH = lsdl_stuff()

def mouse_in_map(): gotopos("D"); return lsdl.g[MX] < g[X] and lsdl.g[MY] < g[Y]
def mouse_in_win1(): gotopos("A*"); tl(); gotopos("C"); br(); gotomouse(); return inside()
def mouse_in_win2(): gotopos("B*"); tl(); gotopos("F"); br(); gotomouse(); return inside()

def draw_sel_square(x, y, color):  # x,y -- in logical coordinates
    x0,y0 = x*SQW, y*SQH
    x1,y1 = x0+SQW, y0+SQH
    lsdl.color(color)
    lsdl.line(x0+1,y0+1,x1-1,y1-1, "B")
    lsdl.line(x0+2,y0+2,x1-2,y1-2, "B")

def draw_mouse_cursor():
    if mouse_in_map():
        draw_sel_square(lsdl.g[MX] // SQW, lsdl.g[MY] // SQH,
                        lsdl.YELLOW if g[DRAGGING] else lsdl.GRAY)
    else:
        lsdl.gfx("B:0 C:W XY:M + +XY:16,8 6x9 T", data=[f"{g[MSX]},{g[MSY]}"])

# --[ mouse coordinates ]-----------------------------------------------
MSX="MSX"; MSY="MSY"  # square X&Y, that the mouse is over
MCUBE="MCUBE"  # cube dictionary for the cube the mouse is over, or None
M0X="M0X"; M0Y="M0Y"  # mouse-down X/Y position (absolute pixel coordinates)
M0SX="M0SX"; M0SY="M0SY"  # mouse-down square X&Y position (MSX,MSY when started)
M0CUBE="M0CUBE"  # cube dictionary that was clicked on
MDX="MDX"; MDY="MDY"  # mouse shift in X/Y position since the start
MDSX="MDSX"; MDSY="MDSY"  # mouse shift in squares X/Y position, since start
MW1X="MW1X"; MW1Y="MW1Y"  # window 1 character X, Y that mouse is over
MW2X="MW2X"; MW2Y="MW2Y"  # window 2 character X, Y that mouse is over

def setup_mouse_data():
    g.update({MSX: None, MSY: None, MCUBE: None,
              M0X: None, M0Y: None, M0CUBE: None,
              MDX: None, MDY: None,
              M0SX: None, M0SY: None,
              MW1X: None, MW1Y: None,
              MW2X: None, MW2Y: None})

def update_mouse_coordinates():  # illustrated in 2020 Sparkle Book, pg 14
    mx = lsdl.g[MX]; my = lsdl.g[MY]
    if mouse_in_map():
        g[MSX] = mx // SQW
        g[MSY] = my // SQH
        g[MCUBE] = cube_at(g[MSX], g[MSY])
    else:
        g[MCUBE] = None  # leave g[MSX] and g[MSY] as they were, so that calculations do not crash
    if g[M0X] is not None:
        g[MDX] = mx-g[M0X]; g[MDY] = my-g[M0Y]
        if g[MSX] is not None and g[MSY] is not None:
            g[MDSX] = g[MSX]-g[M0SX]; g[MDSY] = g[MSY]-g[M0SY];
    if mouse_in_win1():
        g[MW1X] = (mx-g[X0]) // CHW
        g[MW1Y] = (my-g[Y0]) // CHH
    else:
        g[MW1X] = g[MW1Y] = None
    if mouse_in_win2():
        g[MW2X] = (mx-g[X0]) // CHW
        g[MW2Y] = (my-g[Y0]) // CHH
    else:
        g[MW2X] = g[MW2Y] = None

def start_dragging_calc():
    g[DRAGGING] = True
    g[M0X] = lsdl.g[MX]; g[M0Y] = lsdl.g[MY]  # keep start pos
    g[M0SX] = g[MSX]; g[M0SY] = g[MSY]  # keep start square
    g[MDSX] = 0; g[MDSY] = 0  # presently, no delta in square position
    g[M0CUBE] = g[MCUBE]  # keep mouse-over cube

def end_dragging_calc():
    g[DRAGGING] = False
    g[M0X] = g[M0CUBE] = None  # 2020-03-09: TODO: I think I need to formalize how dragging state is identified, around M0X


# --[ click/drag recognizer ]-------------------------------------------
DRAGGING="DRAGGING"  # g-var
MOUSESTATE = "MOUSESTATE"; TTARGET = "TTARGET"  # state & time-target

def click():
    if mouse_in_map():
        ghosting_finish()
        if g[MCUBE] is None:
            cube = try_create_cube(g[MSX], g[MSY])
            clear_tag(SELECTED)
            cube[TAGS].add(SELECTED)
        else:
            if lsdl.ctrlkey() and g[MCUBE][DATA] and "CLICK" in g[MCUBE][DATA]:
                click_cube_cmds(g[MCUBE], g[MCUBE][DATA]["CLICK"])
            else:
                set_window_to_cube(W1, g[MCUBE])
                g[FOCUS] = W1
                clear_tag(SELECTED)
                g[MCUBE][TAGS].add(SELECTED)
    elif mouse_in_win1() and windows[W1][CUBE] is not None:
        # calculate position, and set cursor location (CX, CLINE) for window appropriately
        print("clicking into window to position cursor not written yet")
    elif mouse_in_win2() and windows[W2][CUBE] is not None:
        # calculate position, and set cursor location (CX, CLINE) for window appropriately
        print("clicking into window to position cursor not written yet")

def dclick():
    g["DBGMSG"] = f"double-clicked: {lsdl.g[MX]}, {lsdl.g[MY]}"  # use MX,MY
    if mouse_in_map():
        if g[MCUBE] is not None:
            if g[MCUBE][COLOR] in colorcycle:
                i = (colorcycle.index(g[MCUBE][COLOR])+1)%len(colorcycle)
            else:
                i = 0
            g[MCUBE][COLOR] = colorcycle[i]

def dragstart():
    ghosting_finish()
    start_dragging_calc()
    if g[M0CUBE]:  # clicked on a cube?
        if SELECTED not in g[M0CUBE][TAGS]:  # if it wasn't selected, MAKE IT the only selected cube
            clear_tag(SELECTED)
            g[M0CUBE][TAGS].add(SELECTED)
        if GHOST in g[M0CUBE][TAGS]: ghosting_start_drag(prior_ghost=True)
        elif lsdl.shiftkey(): ghosting_start_duplicate()  # clones, +CLONED,+SELECTED, retain start positions
        else: ghosting_start_drag(prior_ghost=False)

def drag():
    if g[M0CUBE]: ghosting_drag()
    else: update_dynamic_selection_cubes()

def dragend():
    if g[M0CUBE]: ghosting_finish()
    else: finish_dynamic_selection()
    end_dragging_calc()
    g[FOCUS] = None

def mouse_statemachine(): #  3(dclick) 2(click) 1(down) 4(drag)  0(neutral)
    (gg, evt, K, CH) = lsdl_stuff()
    st, tt = g[MOUSESTATE], g[TTARGET]; t = time.time(); e = evt.type; alarm = False
    if tt is not None and t>tt: alarm = True; tt = None
    if st == 0:  # neutral
        if e == eMOUSEDOWN: st = 1; tt = t+.3
    elif st == 1:  # down
        if e == eMOUSEUP: st = 2; tt = t+.3
        elif alarm: st = 4; dragstart()
        elif e == eMOTION: st = 4; dragstart(); drag()
    elif st == 2:  # click
        if alarm or e == eMOTION: st = 0; click()
        elif e == eMOUSEDOWN: st = 3; tt = t+.3
    elif st == 3:  # d-click
        if alarm or e == eMOTION: st = 0
        elif e == eMOUSEUP: st = 0; dclick()
    elif st == 4:  # drag
        if e == eMOTION: drag()
        elif e == eMOUSEUP: st = 0; dragend()
    g[MOUSESTATE], g[TTARGET] = st, tt

# --[ cube binder ]-----------------------------------------------------
def binder_keep(lines):
    binder = {}
    def check():
        if key and building:  # triggered after 1st non-.. line
            if key == "DRAW:": binder["DRAW"] = "\n".join(building)
            elif key == "OVER:": binder["OVER"] = "\n".join(building)
            elif key == "SELECTED:": binder["SELECTED"] = "\n".join(building)
            elif key == "CLICK:": binder["CLICK"] = "\n".join(building)
            elif key == "PY-EVAL:": binder["PY-EVAL"] = ast.literal_eval("\n".join(building))
            elif key == "PYTHON:": binder["PYTHON"] = "\n".join(building)
            elif key == "TEXT:":  binder["TEXT"] = "\n".join(building)
            else: pass  # binder[key[:-1]] = list(building)  -- presently, just discards
    key, building = None, []
    for ln in lines:
        if len(ln) == 0: continue
        if len(ln) == 1: continue  # this is an err, but don't make a fuss
        if ln.startswith("  ") or ln.startswith(".."):
            building.append(ln[2:])
        else:
            check()
            if len(ln) == 0: continue
            key = ln
            del building[:]
    check()
    return binder

# --[ lexer ]-[ adapted from SLEX (snippets) ]--------------------------
WORD = "WORD"
STR = "STR"  # "..."
NUM = "NUM"
CHAR = "CHAR"
WS = "WS"
BAD = "BAD"

PATTERNS = [
    (NUM, re.compile(r'''[-]?\d+''')),
    (WORD, re.compile(r"\w+")),
    (STR, re.compile(r'''("([^\\]|([\\].))+?")''')),
    (CHAR, re.compile(r"[,-;()]")),
    (WS, re.compile(r"\s+")),
    (BAD, re.compile(r"\S+"))]

def lex(s):
    i = 0; tokens = []
    while i < len(s):
        for (sym,R) in PATTERNS:
            mo = R.match(s, i)
            if mo is not None:
                if sym != WS:
                    x = mo.group(0)
                    if sym == NUM: x = int(x)
                    elif sym == STR: x = x[1:-1]
                    tokens.append((sym, x))
                i = mo.end()
                break
        else: breakpoint()  # should not be possible; "BAD" should catch everything else
    return tokens

def cmd_match(cmd, pattern):  # pattern: ["specific_word", TOKTYPE, TOKTYPE, ",", TOKTYPE, ...]
    if not len(cmd) == len(pattern): return False
    if not (cmd[0][0] == WORD and cmd[0][1] == pattern[0]): return False  # first pattern item is always a word
    for i in range(1, len(pattern)):
        checking = pattern[i]
        if len(checking) == 1:  # CHAR match expressed with single char
            if cmd[i][1] != checking: return False  # for CHAR, check token literal
        else:
            if cmd[i][0] != checking: return False  # otherwise, check token type
    return True

def split_L(L, sep_fn):  # snippet "LSPL" (List Split)
    if len(L) == 0: return []
    R = [[]]
    for x in L:
        if sep_fn(x): R.append([])
        else: R[-1].append(x)
    return R

# --[ cube CLICK execution ]----------------------------------------------------
def click_cube_cmds(cube, click_cmds):
    commands = split_L(lex(click_cmds), lambda x: x[0] == CHAR and x[1] == ";")
    for cmd in commands:
        print(cmd)
        if not cmd: continue  # empty command
        if cmd_match(cmd, ["WEB", STR]): webbrowser.open(cmd[1][1])
        elif cmd_match(cmd, ["EDIT", STR]): switch_file(cmd[1][1])
        elif cmd_match(cmd, ["FOLDER", STR]):
            p = os.path.expandvars(cmd[1][1]).replace("/", "\\")
            subprocess.Popen('explorer "{}"'.format(p))
        elif cmd_match(cmd, ["START", STR]): os.startfile(cmd[1][1])
        elif cmd_match(cmd, ["CALL", STR]):
            try: exec(cmd[1][1]+"()", cube[DATA][SCOPE])
            except: pass


# --[ cube DATA drawing ]-------------------------------------------------------
def expand_relative_text(cube, s):
    return s.replace("$TEXT", cube[DATA].get("TEXT", "(no TEXT block found)"))

def draw_relative_text(cube, dx, dy, s):
    lsdl.press(expand_relative_text(cube, s), SQW*(cube[X]+dx), SQH*(cube[Y]+dy))

def draw_relative_text_scaled(cube, dx, dy, s, scale):  # experimental; may become the signature for draw_relative_text
    lsdl.press(expand_relative_text(cube, s), SQW*(cube[X]+dx), SQH*(cube[Y]+dy), scale=scale)

def draw_relative_line(cube, dx, dy, dx2, dy2):
    x0 = SQW*(cube[X]+dx) + (SQW//2)
    y0 = SQH*(cube[Y]+dy) + (SQH//2)
    x1 = SQW*(cube[X]+dx2) + (SQW//2)
    y1 = SQH*(cube[Y]+dy2) + (SQH//2)
    lsdl.line(x0,y0,x1,y1)

def draw_cube_draw_cmds(cube, draw_cmds):
    lsdl.color(cube[COLOR])
    lsdl.gfx("B:0 8x16")
    commands = split_L(lex(draw_cmds), lambda x: x[0] == CHAR and x[1] == ";")
    for cmd in commands:
        if not cmd: continue  # empty command
        if cmd_match(cmd, ["TEXT", NUM, ",", NUM, STR]):
            draw_relative_text(cube, cmd[1][1], cmd[3][1], cmd[4][1])
        elif cmd_match(cmd, ["TEXTx2", NUM, ",", NUM, STR]):
            draw_relative_text_scaled(cube, cmd[1][1], cmd[3][1], cmd[4][1], 2)
        elif cmd_match(cmd, ["LINE", NUM, ",", NUM, "-", NUM, "," ,NUM]):
            draw_relative_line(cube, cmd[1][1], cmd[3][1], cmd[5][1], cmd[7][1])
        elif cmd_match(cmd, ["COLOR", NUM]):
            lsdl.color(cmd[1][1])
        elif cmd_match(cmd, ["COLOR", WORD]):
            lsdl.colorch(cmd[1][1])

# --[ cube drawing ]----------------------------------------------------
def draw_cube(cube):
    sx0, sy0 = SQW*cube[X], SQH*cube[Y]
    sx1, sy1 = sx0+SQW, sy0+SQH
    sx0, sy0, sx1, sy1 = (sx0+1, sy0+1, sx1-1, sy1-1)  # feather in
    lsdl.color(cube[COLOR] if GHOST not in cube[TAGS] else lsdl.RED)
    lsdl.line(sx0,sy0,sx1,sy1, "BF")
    data_check(cube)
    if cube[DATA] is not None:
        if "DRAW" in cube[DATA]:
            draw_cube_draw_cmds(cube, cube[DATA]["DRAW"])
        if "OVER" in cube[DATA]:
            if g[MSX] == cube[X] and g[MSY] == cube[Y]:
                draw_cube_draw_cmds(cube, cube[DATA]["OVER"])
        if "SELECTED" in cube[DATA]:
            if SELECTED in cube[TAGS] or PROVISIONALLY_SELECTED in cube[TAGS]:
                draw_cube_draw_cmds(cube, cube[DATA]["SELECTED"])
    if SELECTED in cube[TAGS] or PROVISIONALLY_SELECTED in cube[TAGS]:  # selection
        draw_sel_square(cube[X], cube[Y], lsdl.YELLOW)
    if (cube[X], cube[Y]) not in cube_positions:
        return
    if len(cube_positions[(cube[X], cube[Y])]) > 1:  # two-cubes in same spot
        lsdl.color(lsdl.YELLOW)
        lsdl.line(sx0-4,sy0-4,sx1+4,sy1+4, "X")
        lsdl.color(lsdl.BLUE)
        lsdl.line(sx0-4,sy0-4,sx1+4,sy1+4, "+")

def draw_cubes():
    for cube in cubes:
        draw_cube(cube)

# --[ windows - scheme documented in 2020 Sparkle p31 ]-----------------
WINDOW="WINDOW"; W1="W1"; W2="W2"; WP="WP"  # which window is selected?
CUBE="CUBE"  # cube referenced by window
TEX="TEX"  # texture for the window
CHARS="CHARS"  # the newly calculated display characters for the window
OCHARS="OCHARS"  # the immediately displayed texture
CMAP="CMAP"  # the character map [(text-ln#, cx across in line), ...]

windows = {}

def setup_windows():
    for w in W1, W2, WP:
        D = {CUBE: None,
             TEX: lsdl.texture(CUBEW*CHW, CUBEH*CHH),
             CHARS: " "*CUBEW*CUBEH,
             OCHARS: " "*CUBEW*CUBEH,
             CMAP: [(0,0)]*CUBEH}
        lsdl.target(D[TEX])
        lsdl.clear()
        windows[w] = D
    lsdl.target()
    g[WINDOW] = None

def commit_win():
    w = g[WINDOW]
    if w is None: return
    for k in windows[w]:
        windows[w][k] = g[k]

def open_win(k): commit_win(); g.update(windows[k]); g[WINDOW] = k

def update_texture():
    n = CUBEW*CUBEH
    if g[OCHARS] == g[CHARS]: return  # no changes, nothing to do
    lsdl.target(g[TEX])
    lsdl.gfx("C:W B:0 8x16")
    for i in range(n):
        if g[OCHARS][i] != g[CHARS][i]:
            lsdl.press(g[CHARS][i], (i % CUBEW)*CHW, (i // CUBEW)*CHH)
    g[OCHARS] = g[CHARS]

def update_preview():
    if (not g[DRAGGING] and g[MCUBE] is not None and  # prepare preview in Window 2
        windows[WP][CUBE] != g[MCUBE]):
        set_window_to_cube(WP, g[MCUBE])

def update_textures():
    for k in windows:
        open_win(k); update_texture()

local_rect = lsdl.rect()

def into_rect():
    local_rect.x = g[X0]; local_rect.y = g[Y0]
    local_rect.w = g[X1]-g[X0]; local_rect.h = g[Y1]-g[Y0]

def draw_texture(w, a, b):
    gotopos(a); tl(); gotopos(b); br()
    into_rect()
    lsdl.target(None)
    lsdl.copy(windows[w][TEX], None, local_rect)

def draw_textures():
    if g[FOCUS] is not None: draw_texture(W1, "A*", "C")
    if not g[DRAGGING] and g[MCUBE] is not None:
        draw_texture(WP, "B*", "F")  # show the preview pane
    else:
        draw_texture(W2, "B*", "F")  # otherwise, show texture 2

# --[ cube-window-typing interface ]------------------------------------
FOCUS="FOCUS"

g[FOCUS] = None  # window presently focused

def wrap(lines, w, h):
    L = []
    cmap = []
    i, cx = 0, 0
    for (i, ln) in enumerate(lines):
        if len(ln) == 0:
            L.append(" "*w)
            cmap.append((i, 0))
        else:
            cx = 0
            while len(ln) > w:
                L.append(ln[:w])
                ln = ln[w:]
                cmap.append((i, cx))
                cx += w
            if len(ln):
                L.append(ln+(" "*(w-len(ln))))
                cmap.append((i, cx))
    last = (i, cx)
    while len(L) < h:
        L.append(" "*w)
        cmap.append(last)
        i += 1
    return L, cmap

def wrap_render():  # load CHARS & CMAP for the current text
    lines, g[CMAP] = wrap(g[CUBE][TEXT], CUBEW, CUBEH)
    g[CHARS] = "".join(lines)

def set_window_to_cube(win, cube):
    open_win(win)
    g[CUBE] = cube
    wrap_render()
    commit_win()

def focused_cube():
    f = g[FOCUS]
    if f is None: return None
    w = windows[f]
    if w is None: return None
    return w[CUBE]

def cue_focused_cube():  # cue typing for the currently focused window
    global LINES
    cube = focused_cube()
    if cube is None:
        LINES = g[CX] = g[CLINE] = None
        return False
    else:
        LINES = g[CUBE][TEXT]  # note: g[CX] and g[CLINE] are already correct
        g[CX] = cube[CX]
        g[CLINE] = cube[CLINE]
        return True

def commit_focused_cube():
    cube = focused_cube()
    cube[CX] = g[CX]
    cube[CLINE] = g[CLINE]

# --[ typing ]--[ origin: 0052/singlepageb ]----------------------------
MARK="MARK"
CX="x"; CLINE="y"; CUT="cut"  # NOTE: actually lowercase..!
g.update({CX:0, CLINE:0, MARK:None, CUT: ""})

LINES=[]  # the lines buffer

seq = {"right1": "@veryend ? ret ; @lnend ? 0 x! y 1 + y! ret ; x 1 + x!",
       "left1": "@verystart ? ret ; @lnstart ? y 1 - y! y lnlen x! ret ; x 1 - x!",
       "up1": "y 1 - 0 max y! >ln:eoln", "down1": "y 1 + numlns min y! >ln:eoln",
       ">ln:eoln": "y lnlen x min x!", "home": "0 x!", "end": "y lnlen x!",
       "@verystart": "x 0 == ? y 0 == ret ; F", "@lnstart": "x 0 ==",
       "@veryend": "y numlns ==", "@lnend": "y lnlen x ==",
       "addstr": "@veryend ? append ret ; insert",
       "right_word": "right_ws right_!ws",
       "right_ws": "@veryend ? ret ; @lnend ? right1 :| ; wsch ? right1 :|",
       "right_!ws": "@veryend ? ret ; @lnend ? ret ; wsch ? ret ; right1 :|",
       "left_word": "left_ws left_!ws",
       "left_ws": "@verystart ? ret ; @lnstart ? left1 :| ; @lnend ? left1 :| ; wsch ? left1 :|",
       "left_!ws": "@verystart ? ret ; @lnstart ? ret ; @lnend ? ret ; wsch ? ret ; left1 :|",
       "delch": "@veryend ? ret ; @lnend not mark right1 delreg ? left1 ; ret",
       "bkspace": "@verystart ? ret ; left1 delch",
       "enter": "@veryend ? BLANK append down1 ret ; x x end x delinline x! openln down1 cut insert",
       "kill-line": "@veryend ? ret ; @lnend ? delch ret ; x x end x delinline x!",
       "kill-word": "@veryend ? ret ; @lnend ? delch ret ; x x right_word x delinline x!",
       "yank": "from-clipboard insert"}

lit = {"0": 0, "1": 1, "F": False, "T": True, "BLANK": ""}

def inorder(x0,y0,x1,y1):
    if y0<y1: return x0,y0, x1,y1
    elif y0>y1: return x1,y1, x0,y0
    elif x0<x1: return x0,y0, x1,y1
    else: return x1,y1, x0,y1

def delreg():
    x0,y0 = g[MARK]; x1,y1 = g[CX], g[CLINE]
    x0,y0,x1,y1 = inorder(x0,y0,x1,y1)
    if y0 == y1: push(x0); push(x1); do("delinline")
    else:
        push(x0); g[CLINE]=y0; do("y lnlen delinline")
        for g[CLINE] in range(y0+1, y1):
            do("0 y lnlen delinline")
        push(0); push(x1); do("delinline")
        g[CX]=x0; g[CLINE]=y0
        del LINES[y0+1:y1]
        if y1 < len(LINES):
            LINES[y0] += LINES[y1]
            del LINES[y0+1]

def export_lines(): clipboard_out(LINES)  # F5 key, presently (2020-02-23)
def import_lines():
    LINES[:] = clipboard_in()  # F6 key, presently (2020-02-23)
    wrap_render()

def do(s):
    i=0; cmds=s.split()
    skipping = False
    while i < len(cmds):
        cmd = cmds[i]; i += 1
        if skipping: skipping = cmd != ";"
        elif cmd == ";": pass
        elif cmd == ":|": i = 0
        elif cmd == "?": skipping = not pop()
        elif cmd == "ret": return
        elif cmd == "==": push(pop() == pop())
        elif cmd == "lnlen": j=pop(); push(len(LINES[j]) if j < len(LINES) else 0)
        elif cmd == "numlns": push(len(LINES))
        elif cmd == "openln": LINES.insert(g[CLINE]+1, "")  # GFX
        elif cmd == "append": LINES.append(pop())  # GFX
        elif cmd == "insert":
            # this is ugly; I need to do some fundamental research to be
            # rid of this ugliness
            insert_lines = pop().split("\n")
            if LINES:
                ln = LINES[g[CLINE]]
                before,after = ln[:g[CX]], ln[g[CX]:]
                insert_lines[0] = before+insert_lines[0]
                insert_lines[-1] = insert_lines[-1]+after
                LINES[g[CLINE]:g[CLINE]+1] = insert_lines
            else:
                LINES[:] = insert_lines
        elif cmd == "mark": g[MARK] = (g[CX], g[CLINE])
        elif cmd == "delreg": delreg()  # -> multiple delinline calls
        elif cmd == "delinline": ln = LINES[g[CLINE]]; b=pop(); a=pop(); g[CUT] = ln[a:b]; LINES[g[CLINE]] = ln[:a]+ln[b:]  # GFX
        elif cmd == "wsch": push(LINES[g[CLINE]][g[CX]] in " \t")
        elif cmd == "from-clipboard": push(pyperclip.paste().replace("\r\n", "\n"))
        elif cmd == "+": push(pop()+pop())
        elif cmd == "-": b=pop(); push(pop()-b)
        elif cmd == ">": b=pop(); push(pop()>b)
        elif cmd == "<": b=pop(); push(pop()<b)
        elif cmd == "max": push(max(pop(), pop()))
        elif cmd == "min": push(min(pop(), pop()))
        elif cmd == "not": push(not pop())
        elif cmd in lit: push(lit[cmd])
        elif cmd in seq: do(seq[cmd])
        elif cmd[-1] == "!" and cmd[:-1] in g: g[cmd[:-1]] = pop()
        elif cmd in g: push(g[cmd])
        else: print("cmd not found:", cmd)

from lsdl2019 import kA, kB, kC, kD, kE, kF, kG, kH, kI, kJ, kK, kL, kM, kN, kO, kP, kQ, kR, kS, kT, kU, kV, kW, kX, kY, kZ, HOME, END, UP, DOWN, RIGHT, LEFT, SPC, BKSPACE, DEL, RET

kbcodes = {kA:"A", kB: "B", kC: "C", kD: "D", kE: "E", kF: "F", kG: "G", kH: "H", kI: "I", kJ: "J", kK: "K", kL: "L", kM: "M", kN:"N", kO: "O", kP:"P", kQ: "Q", kR: "R", kS: "S", kT: "T", kU: "U", kV: "V", kW: "W", kX: "X", kY: "Y", kZ: "Z", HOME:"HOME", END:"END", UP:"UP", DOWN:"DOWN", RIGHT:"RIGHT", LEFT:"LEFT", SPC:"SPACE", BKSPACE:"BKSPACE", DEL:"DEL", RET: "ENTER"}

kbtests = [(("C-F", "RIGHT"), "right1"),  (("A-F", "C-RIGHT"), "right_word"),
           (("C-B", "LEFT"), "left1"),    (("A-B", "C-LEFT"), "left_word"),
           (("C-P", "UP"), "up1"),        (("C-N", "DOWN"), "down1"),
           (("C-E", "END"), "end"),       (("C-A", "HOME"), "home"),
           (("C-D", "DEL"), "delch"),     (("C-SPACE",), "mark"),
           (("C-K",), "kill-line"),       (("A-D",), "kill-word"),
           (("BKSPACE",), "bkspace"),     (("ENTER",), "enter"),
           (("C-Y",), "yank")]

# --[ text cursor drawing ]---------------------------------------------
def draw_text_cursor():  # TODO: This could PROBABLY be folded into the wrap-text functionality...  & thus simplified greatly...  (g[CSCRNX], g[CSCRNY]), then *CHW, *CHH, +CHW, +CHH, ...
    if g[FOCUS] is None: return
    open_win(g[FOCUS])
    if g[CUBE] is None: return
    cube = g[CUBE]
    gotopos({W1: "A*", W2: "B*"}[g[FOCUS]])
    for (cline, cx) in g[CMAP]:
        if cline == cube[CLINE] and cube[CX] < cx+CUBEW:
            slide((cube[CX]-cx)*CHW, 0)
            lsdl.target(None)
            lsdl.gfx("C:Y")
            lsdl.line(g[X], g[Y], g[X]+CHW, g[Y]+CHH, "B")
            return  # done
        else:
            slide(0, CHH)

# --[ major ]-----------------------------------------------------------
QUIT="QUIT"

def setup():
    setup_data()
    setup_gfx()
    setup_mouse_data()
    setup_windows()
    g[QUIT] = False

def teardown():
    if TEARDOWNSAVE: save_data_for_teardown()
    lsdl.quit()

def loop():
    (gg, evt, K, CH) = lsdl_stuff()
    while lsdl.poll():
        update_mouse_coordinates()
        if evt.type == lsdl.eKEYDOWN:
            handled = False
            c=("A-" if lsdl.altkey() else "")+("C-" if lsdl.ctrlkey() else "")+kbcodes.get(gg[K],"")
            if cue_focused_cube():
                for tests, s in kbtests:
                    if c in tests: do(s); handled = True; break
                else:
                    if gg[CH] is not None: push(gg[CH]); do("addstr right1"); handled = True
                if handled: wrap_render(); commit_focused_cube(); reset_data_timer()
            elif g[FOCUS] is None:
                if c == "BKSPACE": delete_selected_cubes()
            if not handled:
                if gg[K] == lsdl.ESC:
                    if g[FOCUS] is None: g[QUIT] = True
                    else: g[FOCUS] = None
                elif c == "C-C": ghosting_copy()
                elif c == "C-X": ghosting_cut()
                elif c == "C-V": ghosting_paste()
                elif gg[K] == lsdl.F1: report_tags()
                elif gg[K] == lsdl.F5: export_lines()
                elif gg[K] == lsdl.F6: import_lines()
                elif gg[K] == lsdl.F11: os.startfile(PP["BASE"])
                elif gg[K] == lsdl.F12: breakpoint()
                elif gg[K] == lsdl.DEL: delete_selected_cubes()
        if evt.type in [eMOUSEDOWN, eMOUSEUP, eMOTION]: mouse_statemachine()
    update_cube_positions()
    notice_states()
    evt.type = 0  # blank the event, before calling mouse_statemachine() for timing
    mouse_statemachine()
    check_data_timer()
    lsdl.target(); lsdl.color(lsdl.BLACK); lsdl.clear()
    lsdl.color(lsdl.LIGHT_BLUE)
    lsdl.font(lsdl.f8x16)
    gotopos("E*")
    lsdl.press(f"MX: {lsdl.g[MX]}   MY: {lsdl.g[MY]}", g[X],g[Y])
    lsdl.press(f"CX: {g[CX]} CLINE: {g[CLINE]}", g[X], g[Y]+CHH)
    draw_display_lines()
    draw_tray_lines()
    draw_cubes()
    update_preview()
    update_textures()
    draw_textures()
    draw_mouse_cursor()
    draw_selection_box()
    draw_text_cursor()
    lsdl.present()

def run():
    setup()
    try:
        while not g[QUIT]: loop()
    except:
        traceback.print_exc()
    teardown()
    print("teardown complete")
    if TEARDOWNSAVE: print("data saved")

# --[ final ]-----------------------------------------------------------
if __name__ == "__main__":
    run()

