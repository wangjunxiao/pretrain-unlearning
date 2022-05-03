# -*- encoding=utf-8 -*-
import os
import tkinter as tk

from PIL import Image
from PIL import ImageTk


left_mouse_down_x = 0
left_mouse_down_y = 0
left_mouse_up_x = 0
left_mouse_up_y = 0
sole_rectangle = None


def left_mouse_down(event):
    global left_mouse_down_x, left_mouse_down_y
    left_mouse_down_x = event.x
    left_mouse_down_y = event.y


def left_mouse_up(event):
    global left_mouse_up_x, left_mouse_up_y
    left_mouse_up_x = event.x
    left_mouse_up_y = event.y
    corp_img(img_path, './img/one_corp.png', left_mouse_down_x, left_mouse_down_y,
             left_mouse_up_x, left_mouse_up_y)


def moving_mouse(event):
    global sole_rectangle
    global left_mouse_down_x, left_mouse_down_y
    moving_mouse_x = event.x
    moving_mouse_y = event.y
    if sole_rectangle is not None:
        canvas.delete(sole_rectangle)  # delete previous rectangle
    sole_rectangle = canvas.create_rectangle(left_mouse_down_x, left_mouse_down_y, moving_mouse_x,
                                             moving_mouse_y, outline='red')


def right_mouse_down(event):
    pass

def right_mouse_up(event):
    pass


def corp_img(source_path, save_path, x_begin, y_begin, x_end, y_end):
    if x_begin < x_end:
        min_x = x_begin
        max_x = x_end
    else:
        min_x = x_end
        max_x = x_begin
    if y_begin < y_end:
        min_y = y_begin
        max_y = y_end
    else:
        min_y = y_end
        max_y = y_begin
    save_path = os.path.abspath(save_path)
    if os.path.isfile(source_path):
        corp_image = Image.open(source_path)
        region = corp_image.crop((min_x, min_y, max_x, max_y))
        region.save(save_path)
        
        if min_x < 0:   min_x = 0
        if min_x > 224: min_x = 223
        if min_y < 0  : min_y = 0
        if min_y > 224: min_y = 223
        if max_x < 0  : max_x = 0
        if max_x > 224: max_x = 223
        if max_y < 0  : max_y = 0
        if max_y > 224: max_y = 223
        
        min_id=int(min_x/16)+int(min_y/16)*14
        max_id=int(max_x/16)+int(max_y/16)*14
        
        x_ids = int(max_x/16) - int(min_x/16)
        y_ids = int(max_y/16) - int(min_y/16)
        
        mask_ids = []
        for y_id in range(y_ids+1):
            id_ = min_id
            for x_id in range(x_ids+1):
                mask_ids.append(id_)
                id_ += 1
            min_id += 14
            
        print('mask_ids', mask_ids)
            
        print('mask finished, masked image saved at:{}'.format(save_path))
    else:
        print('cannot find path:{}'.format(source_path))


if __name__ == '__main__':
    pass
    img_path = './img/ILSVRC2012_val_3.JPEG'
    image = Image.open(img_path)
    image = image.resize((224, 224))
    image.save('./img/resize.jpg')
    
    win = tk.Tk()
    win.title('Mask GUI')
    frame = tk.Frame()
    frame.pack()
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    img_path = './img/resize.jpg'
    image = Image.open(img_path)
    image_x, image_y = image.size
    
    if image_x > screenwidth or image_y > screenheight:
        print('The picture size is too big,max should in:{}x{}, your:{}x{}'.format(screenwidth,
                                                                                   screenheight,
                                                                                   image_x,
                                                                                   image_y))
    img = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(frame, width=image_x, height=image_y, bg='pink')
    i = canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.pack()
    canvas.bind('<Button-1>', left_mouse_down)  
    canvas.bind('<ButtonRelease-1>', left_mouse_up)  
    canvas.bind('<Button-3>', right_mouse_down)  
    canvas.bind('<ButtonRelease-3>', right_mouse_up) 
    canvas.bind('<B1-Motion>', moving_mouse) 
    win.mainloop()