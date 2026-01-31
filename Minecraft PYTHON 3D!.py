import tkinter as tk
from tkinter import messagebox
import math

# --- STARTUP GUI MESSAGE ---
# This runs BEFORE the main game window opens
root_startup = tk.Tk()
root_startup.withdraw() # Hide the tiny empty window
messagebox.showinfo("Controls Help", 
    "Welcome to Minecraft PYTHON 3D!\n\n" +
    "MOVEMENT:\n" +
    " - W/A/S/D or Arrow Keys to Move\n" +
    " - SPACE to Jump\n\n" +
    "BUILDING:\n" +
    " - B: Stone (Gray)\n" +
    " - N: Wood (Brown)\n" +
    " - M: Leaves (Green)\n" +
    " - V: Mine (Destroy)\n\n" +
    "Press OK to Start the World!")
root_startup.destroy()

# --- MAIN GAME SETTINGS ---
WIDTH, HEIGHT = 500, 400
TILE_SIZE = 50
GAME_MAP = [[1 if (x==0 or x==9 or y==0 or y==9) else 0 for x in range(10)] for y in range(10)]
px, py, pa = 200, 200, 0 
jump_y, is_jumping = 0, False
current_block = "Stone"

def draw_3d():
    canvas.delete("all")
    # SKY & GROUND
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT/2 + jump_y, fill="#87ceeb", outline="")
    canvas.create_rectangle(0, HEIGHT/2 + jump_y, WIDTH, HEIGHT, fill="#2ecc71", outline="")
    
    for r in range(50):
        ra = pa - (30 * math.pi/180) + (r * 1.2 * math.pi/180)
        dist = 0
        hit_type = 0
        while dist < 500:
            dist += 5
            x, y = px + math.cos(ra)*dist, py + math.sin(ra)*dist
            mx, my = int(x/TILE_SIZE), int(y/TILE_SIZE)
            if 0 <= mx < 10 and 0 <= my < 10 and GAME_MAP[my][mx] > 0:
                hit_type = GAME_MAP[my][mx]
                break
        
        line_h = (TILE_SIZE * HEIGHT) / (dist * math.cos(ra - pa) + 0.001)
        if hit_type > 0:
            if hit_type == 1: base_c = (150, 150, 150) # Stone
            elif hit_type == 2: base_c = (100, 65, 30)  # Wood
            else: base_c = (34, 139, 34)               # Leaves
            
            sh = max(0.2, 1 - (dist / 500))
            color = '#%02x%02x%02x' % (int(base_c[0]*sh), int(base_c[1]*sh), int(base_c[2]*sh))
            sy, ey = (HEIGHT/2 - line_h/2) + jump_y, (HEIGHT/2 + line_h/2) + jump_y
            canvas.create_line(r*(WIDTH/50), sy, r*(WIDTH/50), ey, fill=color, width=WIDTH/50+1)
            canvas.create_line(r*(WIDTH/50), sy, r*(WIDTH/50), sy+2, fill="black", width=WIDTH/50+1)

    # --- THE HUD ---
    canvas.create_line(WIDTH/2-8, HEIGHT/2, WIDTH/2+8, HEIGHT/2, fill="white", width=2)
    canvas.create_line(WIDTH/2, HEIGHT/2-8, WIDTH/2, HEIGHT/2+8, fill="white", width=2)
    canvas.create_rectangle(WIDTH/2-100, HEIGHT-50, WIDTH/2+100, HEIGHT-10, fill="#333", outline="white")
    canvas.create_text(WIDTH/2, HEIGHT-30, text=f"BLOCK: {current_block}", fill="white", font=("Arial", 12, "bold"))

def official_jump(vel):
    global jump_y, is_jumping
    jump_y += vel
    vel -= 6 
    if jump_y <= 0:
        jump_y = 0; is_jumping = False
    else:
        root.after(15, lambda: official_jump(vel))
    draw_3d()

def actions(event):
    global px, py, pa, is_jumping, current_block
    key = event.keysym.lower()
    if key == 'space' and not is_jumping:
        is_jumping = True; official_jump(30); return

    if key in ['left', 'right', 'up', 'w', 'down', 's', 'a', 'd']:
        if key == 'left' or key == 'a': pa -= 0.15
        elif key == 'right' or key == 'd': pa += 0.15
        else:
            mult = 15 if key in ['up', 'w'] else -15
            nx, ny = px + math.cos(pa)*mult, py + math.sin(pa)*mult
            if 0 <= int(ny/TILE_SIZE) < 10 and 0 <= int(nx/TILE_SIZE) < 10:
                if GAME_MAP[int(ny/TILE_SIZE)][int(nx/TILE_SIZE)] == 0:
                    px, py = nx, ny

    tx, ty = int((px + math.cos(pa)*75)/TILE_SIZE), int((py + math.sin(pa)*75)/TILE_SIZE)
    if 0 <= tx < 10 and 0 <= ty < 10:
        if key == 'b': GAME_MAP[ty][tx] = 1; current_block = "Stone"
        if key == 'n': GAME_MAP[ty][tx] = 2; current_block = "Wood"
        if key == 'm': GAME_MAP[ty][tx] = 3; current_block = "Leaves"
        if key == 'v': GAME_MAP[ty][tx] = 0 
    draw_3d()

root = tk.Tk()
root.title("Minecraft PYTHON 3D!")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
canvas.pack()
draw_3d()
root.bind("<KeyPress>", actions)
root.mainloop()
