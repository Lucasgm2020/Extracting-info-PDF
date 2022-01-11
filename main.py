from tkinter import *
import PyPDF2
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfile

page_contents = []
all_images = []
img_idx = [0]
displayed_img = []

#Detect Images inside the PDF document
#Thank you sylvain of Stackoverflow
#https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
def extract_images(page):
    images = []
    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                mode = ""
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "CMYK"
                img = Image.frombytes(mode, size, data)
                images.append(img)
    return images

        
def resize_image(img):

    width,height = int(img.size[0]),int(img.size[1])

    if width > height:
        height = int(300 * (height / width))
        width = 300
    elif height > width:
        width = int(250 * (width / height))
        height = 250
    else:
        width, height = 250, 250

    img = img.resize((width,height))
    return img

def display_images(img):
    img = resize_image(img)
    image = ImageTk.PhotoImage(img)
   

    global label_img
    label_img.configure(image=None)
    label_img.configure(image=image)    
        

    return image
    
    
def open_pdf():
    text_button.set("Loading...")
    file = askopenfile(parent=root,title="Choose a file",filetype=[("PDF Files (.pdf)","*.pdf")],mode="rb")
    if file:
        global all_images,page_contents,img_idx,displayed_img
        
        if len(all_images)>0:
            page_contents = []
            all_images = []
            img_idx = [0]
            displayed_img = []
     
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        content_page = page.extractText()
        
        #Global variable
        page_contents.append(content_page)

        images = extract_images(page)

        #Saving the images         
        for i in images:
            all_images.append(i)
        text_label.set(f"Image 1 of {len(all_images)}") if len(all_images)> 0 else text_label.set(f"No hay imagenes")
        img = images[img_idx[-1]] #img_idx[-1] extrae el ultimo elemento de la lista
        
        
        displayed_img.append(display_images(img))
        
        text_pdf = Text(root,width=30,height=10,padx=10, pady=10)
        text_pdf.tag_configure("center", justify="center")
        text_pdf.tag_add("center", 1.0, "end")
        text_pdf.grid(row=4,column=0,padx=25,pady=25,sticky=SW)
        text_pdf.insert(1.0,content_page)
        text_button.set("Browse")

def right_arrow(all_images):
    
    if img_idx[-1] < len(all_images) - 1:
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        displayed_img.append(display_images(new_img))
        text_label.set(f"Image {img_idx[-1] + 1} of {len(all_images)} ")

        
def left_arrow(all_images):
    if img_idx[-1] > 0:
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        displayed_img.append(display_images(new_img))
        text_label.set(f"Image {img_idx[-1] + 1} of {len(all_images)} ")


def copy_text(content):
    root.clipboard_clear()
    root.clipboard_append(content[-1])

def saving_images(images):
    counter = 1
    for i in images:
        if i.mode != "RGB":
            i = i.convert("RGB")
        i.save("img " + str(counter) + ".png",format="png")
        counter+=1

def save_image(img):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("img 1" + ".png",format="png")    

root = Tk()

root.geometry("+%d+%d" % (350,10))

#Top Frame 
header = Frame(root, width=800, height=175, bg="white")
header.grid(row=0,rowspan=2,columnspan=3)

#Save frame

save_frame = Frame(root,width=800,height=50,bg="#c8c8c8")
save_frame.grid(row=3,rowspan=1,columnspan=3)

#Arrow frame
arrow_frame = Frame(root,width=800,height=50)
arrow_frame.grid(row=2,rowspan=1,columnspan=3)

#Bottom Frame
frm_text_images = Frame(root,width=800,height=250,bg="#20bebe")
frm_text_images.grid(row=4,rowspan=2,columnspan=3)

#Logo
logo = Image.open("logo.png")
logo = logo.resize((int(logo.size[0]/1.5),int(logo.size[1]/1.5)))
logo = ImageTk.PhotoImage(logo)

label_logo = Label(image=logo,bg="white")
label_logo.image = logo
label_logo.grid(row=0,column=0,rowspan=2,sticky = NW, padx=20, pady=40)

""" SEE THIS SPACE"""

################################

# space = Frame(header,width=400)
# space.grid(row=0,column=1)

################################




#Label and button
label_select = Label(root,text="Select a PDF File",font=("Raleway",10),bg="white")
label_select.grid(column=2,row=0,sticky=SE,padx=75,pady=5)

text_button = StringVar()
btn_select = Button(root,textvariable=text_button,font=("Raleway",12),width=15,height=1,bg="#20bebe", fg="white",command=open_pdf)
text_button.set("Browse")
btn_select.grid(row=1,column=2,sticky=NE,padx=60)   


#Label and arrows for visualizing images
text_label = StringVar()
label_img = Label(root,textvariable=text_label,height=1,width=10,font=("arial",9))
text_label.set("Sin imagenes")
label_img.grid(row=2,column=1,ipadx=10)

arr_l = Image.open("arrow_l.png")
arr_l = ImageTk.PhotoImage(arr_l)
arrow_left_btn = Button(root,image = arr_l,width=29,command=lambda: left_arrow(all_images),height=20)
arrow_left_btn.grid(row=2,column=0,sticky=E,padx=10)

arr_r = Image.open("arrow_r.png")
arr_r = ImageTk.PhotoImage(arr_r)
arrow_right_btn = Button(root,image = arr_r,command=lambda: right_arrow(all_images),width=29,height=20)
arrow_right_btn.grid(row=2,column=2,sticky=W,padx=10)


#Buttons for saving and copying
copy_text_btn = Button(root,text="Copy text",font=("shanti",10),height=1,width=15,command = lambda: copy_text(page_contents))
save_all_btn = Button(root,text="Save all images",font=("shanti",10),height=1,width=15,command = lambda: saving_images(all_images))
save_btn = Button(root,text="Save image",font=("shanti",10),height=1,width=15,command = lambda: save_image(all_images[img_idx[-1]]))

copy_text_btn.grid(row=3,column=0)
save_all_btn.grid(row=3,column=1)
save_btn.grid(row=3,column=2)

#Label for displaying images
label_img = Label(root,image=None,bg="#20bebe")
label_img.image = None
label_img.grid(row=4,column=2,rowspan=2)
root.mainloop()