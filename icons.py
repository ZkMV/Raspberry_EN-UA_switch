#home/bin/icons.py

import os,cairo
def mk(text,out,sz):
    W=H=sz; r=round(sz*0.2)
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
    c.set_source_rgba(0,0,0,0); c.paint()
    c.set_source_rgba(0,0,0,0.9)
    c.move_to(r,0); c.arc(W-r,r,r,-1.57,0); c.arc(W-r,H-r,r,0,1.57)
    c.arc(r,H-r,r,1.57,3.14); c.arc(r,r,r,3.14,4.71); c.close_path(); c.fill()
    c.set_source_rgb(1,1,1); c.select_font_face("Sans",0,1); c.set_font_size(sz*0.55)
    xb,yb,w,h,xa,ya=c.text_extents(text); c.move_to((W-w)/2 - xb,(H-h)/2 - yb); c.show_text(text)
    s.write_to_png(out)
base=os.path.expanduser("~/.local/share/icons/hicolor")
for sz in (22,24):
    d=os.path.join(base,f"{sz}x{sz}","status")
    mk("EN",os.path.join(d,"en.png"),sz)
    mk("UA",os.path.join(d,"ua.png"),sz)
print("icons ready")
