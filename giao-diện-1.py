import tkinter as tk
from tkinter import filedialog, Button, Label, Canvas
from tkinter.ttk import *
from PIL import Image, ImageTk,ImageEnhance,ImageOps,ImageFilter
import string
import os
import random
import cv2
import numpy as np
class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.selection=[]
        for i in range(10):
            self.selection.append(tk.IntVar())
        self.root.title("Image Editor")
        self.cout=0
        self.cout1=0
        self.images = []
        self.outimg=[]
        self.index = 0
        self.image_files=[]
        self.number=tk.StringVar()
        self.output_folder=""
        # Nút mở thư mục và mở tập tin
        self.open_folder_btn = Button(root, text="Open folder", command=self.open_folder)
        self.open_folder_btn.grid(row=0, column=0, padx=10, pady=10)
        self.open_file_btn = Button(root, text="Open file", command=self.open_file)
        self.open_file_btn.grid(row=0, column=1, padx=10, pady=10)
        self.tree=Treeview(root)
        self.tree["columns"]=("filepath","size","type")
        self.tree.column("#0", width=100, minwidth=100, anchor=tk.W)
        self.tree.column("filepath", width=300, minwidth=200, anchor=tk.W)
        self.tree.column("size", width=100, minwidth=100, anchor=tk.W)
        self.tree.column("type", width=100, minwidth=100, anchor=tk.W)
        self.tree.heading("filepath",text="file path",anchor=tk.W)
        self.tree.heading("size",text="size",anchor=tk.W)
        self.tree.heading("type", text="type", anchor=tk.W)
        self.tree.place(x=20,y=100)
        self.delete_file= Button(text="delete",command=self.delete)
        self.delete_file.place(x=20,y=350)
        self.show=Button(text="show image",command=self.show_img)
        self.creat=Button(text="creat file",command=self.creat_img)
        self.showimgout=Button(text="show output file",command=self.show_out_img)
        self.showimgout.place(x=800,y=350)
        self.creat.place(x=700,y=350)
        self.show.place(x=100,y=350)
        self.tree1=Treeview(root)
        self.tree1["columns"]=("filepath","size","type")
        self.tree1.column("#0", width=100, minwidth=100, anchor=tk.W)
        self.tree1.column("filepath", width=300, minwidth=200, anchor=tk.W)
        self.tree1.column("size", width=100, minwidth=100, anchor=tk.W)
        self.tree1.column("type", width=100, minwidth=100, anchor=tk.W)
        self.tree1.heading("filepath",text="file path",anchor=tk.W)
        self.tree1.heading("size",text="size",anchor=tk.W)
        self.tree1.heading("type", text="type", anchor=tk.W)
        self.tree1.place(x=700,y=100)
        self.delete_file_all=Button(text="delete all",command=self.delete_all)
        self.delete_file_all.place(x=180,y=350)
        self.delete_out_file_button=Button(text="delete out file",command=self.delete_out_file)
        self.delete_out_file_button.place(x=900,y=350)
    def create_image(self):
        func=[self.add_gaussian_noise,self.convert_image,self.add_salt_and_pepper_noise,self.add_speckle_noise,self.adjust_contrast_and_show,self.random_routate,self.random_crop,self.blur_image,self.corlorize,self.flip]
        func1=[]
        for i in range(len(func)):
            if self.selection[i].get()==1:
                func1.append(func[int(i)])
        func1 = random.sample(func1, len(func1))
        print(self.tree.get_children())
        for i in self.tree.get_children(): 
        #    try: 
            with Image.open(self.image_files[int(i)]) as imgaa:
                for k in range(int(self.number.get())):
                    img=imgaa
                    for j in func1:
                        a=random.randint(0,1)
                        if a==1:
                            img=j(img)
                    output=self.output_folder+"/"+self.random_name()
                    img.save(output)
                    self.outimg.append(output)
                    self.tree1.insert(parent="",index="end",iid=self.cout1,values=(output,str(os.path.getsize(output)/1024),output.split(".")[1]))
                    self.cout1+=1
        #    except:
        #        pass
    def random_name(self):
        letters = string.ascii_letters + string.digits
        name = ''.join(random.choice(letters)   for i in range(10))
        return name +".png"
    def foler_output(self):
        self.output_folder = filedialog.askdirectory()
        self.my_list_box.insert(tk.END, self.output_folder)
    def open_folder(self):
        self.folder_path = filedialog.askdirectory()
        try:
            self.image_files =self.image_files+[(self.folder_path+"/"+f) for f in os.listdir(self.folder_path) if f.endswith(('.jpg', '.png'))]
        except:
            pass
        self.show_image()
    def adjust_contrast_and_show(self,img):
        enhancer = ImageEnhance.Contrast(img) 
        # Tạo một tương phản ngẫu nhiên trong khoảng từ 0.5 đến 2.0
        factor = random.uniform(0.5, 2.0) 
        new_img = enhancer.enhance(factor)
        return new_img
    def show_out_img(self):
       try: 
        selec=self.tree1.selection()[0]
        if selec:
            img=Image.open(self.outimg[int(selec)])
            img.show()
       except:
           pass
    def convert_image(self,input_img):
        input_img = input_img.convert('RGB')
        image_invert = ImageOps.invert(input_img)
        return image_invert
    def creat_img(self):
        win=tk.Toplevel()
        win.geometry("300x700")
        gaussian_noise=tk.Checkbutton(win,text="gaussian_noise",variable=self.selection[0]).place(x=0,y=20)
        self.scale = tk.Scale(win, from_=1, to=25, orient="horizontal")
        self.scale.place(x=150,y=0)
        conver_img=tk.Checkbutton(win,text="conver",variable=self.selection[1]).place(x=0,y=50)
        blur_img=tk.Checkbutton(win,text="blur",variable=self.selection[7]).place(x=0,y=85)
        self.scale2=tk.Scale(win,from_=1,to=5,orient="horizontal")
        self.scale2.place(x=150,y=55)
        salt_and_pepper_noise=tk.Checkbutton(win,text="salt_and_pepper_noise",variable=self.selection[2]).place(x=0,y=120)
        self.scale1 = tk.Scale(win, from_=1, to=100, orient="horizontal")
        self.scale1.place(x=150,y=100)
        speckle_noise=tk.Checkbutton(win,text="speckle_noise",variable=self.selection[3]).place(x=0,y=150)
        colorsize=tk.Checkbutton(win,text="colorsize",variable=self.selection[8]).place(x=0,y=175)
        contrast=tk.Checkbutton(win,text="contrast",variable=self.selection[4]).place(x=0,y=200)
        routate=tk.Checkbutton(win,text="routate",variable=self.selection[5]).place(x=0,y=250)
        flip=tk.Checkbutton(win,text="flip",variable=self.selection[9]).place(x=0,y=275)
        crop=tk.Checkbutton(win,text="crop",variable=self.selection[6]).place(x=0,y=300)
        label=tk.Label(win,text="number images").place(x=0,y=350)
        number_file=tk.Entry(win,textvariable=self.number).place(x=0,y=375)
        choose_fle= Button(win,text="choose output folder",command=self.foler_output).place(x=0,y=400)
        create= Button(win,text="create",command=self.create_image).place(x=0,y=475)
        file_path=tk.Label(win,text="File output").place(x=0,y=425)
        self.my_list_box = tk.Listbox(win, width=20,height=1,font=("Times New Roman",10))
        self.my_list_box.place(x=0,y=450)
        win.mainloop()
    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
        self.image_files.append(self.file_path)
        self.index+=1
        self.show_image1()
    def show_image(self):
        if self.image_files:
            for i in self.image_files:
                if i:
                    self.tree.insert(parent="",index="end",iid=self.cout,values=(i,str(os.path.getsize(i)/1024),i.split(".")[1]))
                    self.cout+=1
    def add_gaussian_noise(self,img, mean=0, std=25):
        img0121=cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
        noise = np.random.normal(mean, self.scale.get(), img0121.shape).astype(np.uint8)
        noisy_image = cv2.add(img0121, noise)
        img1=Image.fromarray(noisy_image)
        return img1
    def random_routate(self,img):
        angle=random.randint(10,180)
        return img.rotate(angle,expand=True)
    def show_img(self):
       try: 
        selec=self.tree.selection()[0]
        if selec:
            img=Image.open(self.image_files[int(selec)])
            img.show()
       except:
           pass
    def add_salt_and_pepper_noise(self,image, salt_prob=0.01, pepper_prob=0.01):
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        noisy_image = np.copy(image)
        total_pixels = image.size
        salt_pixels = int(total_pixels * salt_prob*self.scale1.get())
        pepper_pixels = int(total_pixels * pepper_prob**self.scale1.get())

        # Adding salt noise
        salt_coords = [np.random.randint(0, d, salt_pixels) for d in image.shape[:-1]]
        noisy_image[salt_coords[0], salt_coords[1], :] = 255

        # Adding pepper noise
        pepper_coords = [np.random.randint(0, d, pepper_pixels) for d in image.shape[:-1]]
        noisy_image[pepper_coords[0], pepper_coords[1], :] = 0
        img=Image.fromarray(noisy_image)
        return img
    def add_speckle_noise(self,image, std=0.1):
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        noise = np.random.normal(0, std, image.shape)
        noisy_image = image + image * noise
        noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
        img=Image.fromarray(noisy_image)
        return img
    def delete(self):
        selec=self.tree.selection()
        for i in selec:
            self.tree.delete(i)
    def delete_all(self):
        selec=self.tree.get_children()
        for i in selec:
            self.tree.delete(i)
        # self.index=0
        # self.image_files=[]
    def show_image1(self):
        if self.file_path:
                self.tree.insert(parent="",index="end",iid=self.cout,values=(self.file_path,os.path.getsize(self.file_path)/1024,self.file_path.split(".")[1]))
                self.cout+=1            
    def delete_out_file(self):
        selec=self.tree1.selection()
        for i in selec:
            if os.path.exists(self.outimg[int(i)]):
                os.remove(self.outimg[int(i)])
                self.tree1.delete(i)
    def random_crop(self,img):
        x,y=img.size
        x1=random.randint(0,int(x/2))
        y1=random.randint(0,int(y/2))
        return img.crop((x1,y1,x1+int(x/2),y1+int(y/2)))
    def corlorize(self,img):
        i=random.randint(1,3)
        if i==1:
            return ImageOps.colorize(image=img.convert('L'),black='green',white='red')
        elif i==2:
            return ImageOps.colorize(image=img.convert('L'),black='blue',white='red')
        else:
            return ImageOps.colorize(image=img.convert('L'),black='green',white='blue')
    def flip(self,img):
        i=random.randint(1,2)
        if i==1:
            return img.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            return img.transpose(Image.FLIP_TOP_BOTTOM)
    
    def blur_image(self,image):
        # Mở hình ảnh
        # Làm mờ hình ảnh
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=self.scale2.get()))
        # Kiểm tra nếu hình ảnh là chế độ RGBA và lưu dưới dạng .jpg thì chuyển nó thành RGB
        if blurred_image.mode == "RGBA":
            blurred_image = blurred_image.convert("RGB")
        # Lưu hình ảnh đã làm mờ
        return blurred_image
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
