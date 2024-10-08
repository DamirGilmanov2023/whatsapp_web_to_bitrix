from tkinter import *
from PIL import ImageTk, Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from datetime import datetime
import base64
from tkinter import messagebox
from tkinter import scrolledtext

def tksleep(self, time: float) -> None:
    self.after(int(time * 1000), self.quit)
    self.mainloop()
Misc.tksleep = tksleep

def log_message(message):
    log_area.insert(END, message + '\n')
    log_area.see(END)
    with open("./logs/logs.txt", 'a') as file:
        file.write(message + '\n')

driver=None
driver_bitrix = None
last_message = ""
last_id = ""
buffer = []
to_work = False
flag_work = False
login=""
password=""

def open_driver():
    global driver
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--headless=old")
    options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    #time.sleep(10)
    window.tksleep(5)

def bool_log():
    if len(driver.find_elements(by=By.CLASS_NAME,value="_akaz"))>0:
        return False
    else:
        return True

def get_mess():
    global last_message,last_id,buffer
    #Получение всех видимых контактов
    visible_contacts = driver.find_elements(by=By.CLASS_NAME, value="x1g42fcv")
    #ahlk это контакты, от которых есть свежее сообщение
    ahlk=[]
    vis_con=[]
    names=[]
    for vis in visible_contacts:
        perems=vis.find_elements(by=By.CLASS_NAME,value="_ahlk")
        for p in perems:
            pers=p.find_elements(by=By.CLASS_NAME,value="x1rg5ohu")
            if len(pers)>0:
                per=pers[0]
                ahlk.append(per)
                vis_con.append(vis)
                names.append(vis.find_element(by=By.CLASS_NAME,value="_aou8"))
    for i in range(len(ahlk)):
        #j это количество сообщений
        j=int(ahlk[i].text)
        #Клик по контакту
        ActionChains(driver).click(vis_con[i]).perform()
        #Котейнер сообщений в переписке
        container_mess=driver.find_element(by=By.CLASS_NAME,value="x3psx0u")
        messages_in=container_mess.find_elements(by=By.CLASS_NAME,value="message-in")
        messages=[]
        for mes in messages_in:
            try:
                elem=mes.find_element(by=By.CLASS_NAME, value="_akbu")
                messages.append(elem)
            except:
                pass
                
        messages=messages[-j:]
        flag_nal=False
        for k in range(len(buffer)):
            if buffer[k]["name"]==names[i].text:
                flag_nal=True
                for mess in messages:
                    buffer[k]["mess"]+=mess.text+' / '
                log_message(f"< -- {datetime.now()} --> // Новое сообщение от {buffer[k]['name']} //")
                log_message(f"< -- {datetime.now()} --> // Буфер сообщений {buffer[k]['mess']} //")
                buffer[k]["time"]=int(spin.get())
                last_message=messages[-1].text
                last_id=names[i].text
                break
        if flag_nal==False:
            slovar={}
            slovar["name"]=names[i].text
            slovar["mess"]=""
            for mess in messages:
                slovar["mess"]+=mess.text+' / '
            slovar["time"]=int(spin.get())
            log_message(f"< -- {datetime.now()} --> // Сообщение от {slovar['name']} //")
            log_message(f"< -- {datetime.now()} --> // Сообщение {slovar['mess']} //")
            last_message=messages[-1].text
            last_id=names[i].text
            buffer.append(slovar)

def last_mess():
    global last_message,last_id
    if last_message!="":
        new_str=""
        container_mess=driver.find_element(by=By.CLASS_NAME,value="x3psx0u")
        messages_in=container_mess.find_elements(by=By.CLASS_NAME,value="message-in")
        messages=[]
        for mes in messages_in:
            try:
                elem=mes.find_element(by=By.CLASS_NAME, value="_akbu")
                messages.append(elem)
            except:
                pass
        if messages[-1].text!=last_message:
            for l in range(len(messages)-1,0,-1):
                if messages[l].text!=last_message:
                    new_str=messages[l].text+" / "+new_str
                else:
                    break
            find=False
            log_message(f"< -- {datetime.now()} --> // Свежее сообщение от {last_id} //")
            log_message(f"< -- {datetime.now()} --> // Сообщение {new_str} //")
            for k in range(len(buffer)):
                if buffer[k]["name"]==last_id:
                    buffer[k]["mess"]+=new_str+' / '
                    buffer[k]["time"]=int(spin.get())
                    find=True
                    break
            if find==False:
                slovar={}
                slovar["name"]=last_id
                slovar["mess"]=new_str
                slovar["time"]=int(spin.get())
                buffer.append(slovar)
            last_message=messages[-1].text

def time_monitor():
    #print(buffer)
    del_index=[]
    for i in range(len(buffer)):
        buffer[i]["time"]-=5
        if buffer[i]["time"]<=0:
            del_index.append(i)
            create_lid(buffer[i]["name"],buffer[i]["mess"])
            log_message(f"< -- {datetime.now()} --> // Создание лида от {buffer[i]['name']} //")
            log_message(f"< -- {datetime.now()} --> // Сообщение {buffer[i]['mess']} //")
    del_index.sort()
    i=len(del_index)-1
    while(i>=0):
        buffer.pop(del_index[i])
        i-=1

def open_driver_bitrix():
    global driver_bitrix
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver_bitrix = webdriver.Chrome(options=options)
    driver_bitrix.get(
        "https://auth2.bitrix24.net/oauth/authorize/?user_lang=ru&client_id=b24.66ed13e55a2793.42237403&redirect_uri=https%3A%2F%2Fekopromkz.bitrix24.kz%2Fauth%2F%3Fauth_service_id%3DBitrix24Net%26sessid%3D88b44ba76bc066915e7c6f66bee2ab2c%26backurl%3D%252Fcrm%252Flead%252Fkanban%252F&scope=auth,profile&response_type=code&mode=page&state=site_id%3Ds1%26backurl%3D%252Fauth%252F%253Fcheck_key%253D79e77cfaefd9ebc2c7c6a0108835cd0c%2526backurl%253D%25252Fcrm%25252Flead%25252Fkanban%25252F%26mode%3Dpage&logout=yes")
    #time.sleep(10)
    window.tksleep(5)

def login_bitrix():
    input_email = driver_bitrix.find_element(by=By.CLASS_NAME, value="b24-network-auth-form-field-input")
    input_email.clear()
    input_email.send_keys(login)
    window.tksleep(2)
    #time.sleep(2)
    btn_next = driver_bitrix.find_element(by=By.CLASS_NAME, value="ui-btn-success")
    ActionChains(driver_bitrix).click(btn_next).perform()
    window.tksleep(2)
    #time.sleep(2)
    id_password = driver_bitrix.find_element(by=By.ID, value="password")
    id_password.clear()
    id_password.send_keys(password)
    window.tksleep(2)
    #time.sleep(2)
    btn_next = driver_bitrix.find_element(by=By.CLASS_NAME, value="ui-btn-success")
    ActionChains(driver_bitrix).click(btn_next).perform()
    window.tksleep(2)
    #time.sleep(2)
    try:
        btn_next2 = driver_bitrix.find_element(by=By.CLASS_NAME, value="b24-network-auth-form-user-inner")
        ActionChains(driver_bitrix).click(btn_next2).perform()
        window.tksleep(2)
        #time.sleep(2)
        id_password = driver_bitrix.find_element(by=By.ID, value="password")
        id_password.clear()
        id_password.send_keys(password)
        window.tksleep(2)
        #time.sleep(2)
        btn_next = driver_bitrix.find_element(by=By.CLASS_NAME, value="ui-btn-success")
        ActionChains(driver_bitrix).click(btn_next).perform()
        window.tksleep(2)
        #time.sleep(2)
    except:
        pass
    driver_bitrix.get("https://ekopromkz.bitrix24.kz/crm/lead/kanban/")
    window.tksleep(5)
    #time.sleep(5)

def create_lid(name,value):
    btn_create = driver_bitrix.find_element(by=By.CLASS_NAME, value="crm-kanban-column-add-item-button")
    ActionChains(driver_bitrix).click(btn_create).perform()
    window.tksleep(1)
    #time.sleep(1)
    title_text = driver_bitrix.find_element(by=By.ID, value="title_text")
    title_text.clear()
    title_text.send_keys(value)
    window.tksleep(1)
    #time.sleep(1)
    title_text = driver_bitrix.find_element(by=By.ID, value="name_text")
    title_text.clear()
    title_text.send_keys(name)
    window.tksleep(1)
    #time.sleep(1)
    btn_save = driver_bitrix.find_element(by=By.CLASS_NAME, value="crm-kanban-quick-form-buttons").find_element(by=By.CLASS_NAME, value="ui-btn-primary")
    ActionChains(driver_bitrix).click(btn_save).perform()
    window.tksleep(1)
    #time.sleep(1)

def working():
    global flag_work,img,to_work
    first_in=False
    log_message(f"< -- {datetime.now()} --> // Ожидание сканирования qr кода //")
    while flag_work:
        if to_work:
            if first_in==False:
                img = ImageTk.PhotoImage(Image.open("./qr/zagl.png"))
                label_img.configure(image=img)
                label_img.image = img
                log_message(f"< -- {datetime.now()} --> // Успешный вход в ватсап //")
                window.tksleep(5)
                log_message(f"< -- {datetime.now()} --> // Начало работы //")
            try:
                print("запуск get_mess")
                get_mess()
                print("запуск time_monitor")
                time_monitor()
                window.tksleep(2)
                #time.sleep(5)
                print("Запуск last_mess")
                last_mess()
            except Exception as e:
                log_message(f"< -- {datetime.now()} --> // Ошибка выполнения программы {e} //")
            first_in = True
        else:
            try:
                canvas = driver.find_element(by=By.TAG_NAME, value="canvas")
                canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
                canvas_png = base64.b64decode(canvas_base64)
                with open(r"./qr/qr.png", 'wb') as f:
                    f.write(canvas_png)
            except:
                pass
            img = ImageTk.PhotoImage(Image.open("./qr/qr.png"))
            label_img.configure(image=img)
            label_img.image = img
            to_work = bool_log()
            window.tksleep(5)
            #time.sleep(5)

def start():
    global flag_work,login,password
    if input_login.get()=="":
        messagebox.showinfo("Информация", "Введите логин")
        log_message(f"< -- {datetime.now()} --> // Не введен логин //")
    elif input_password.get()=="":
        messagebox.showinfo("Информация","Введите пароль")
        log_message(f"< -- {datetime.now()} --> // Не введен пароль //")
    else:
        login=input_login.get()
        password=input_password.get()
        login=login.replace(" ","")
        password=password.replace(" ","")
        with open("./logs/in.txt", 'w') as file:
            file.write(login + '\n')
            file.write(password)
        btn_stop.config(state="normal")
        btn_start.config(state="disabled")
        spin.config(state="disabled")
        flag_work=True
        log_message(f"< -- {datetime.now()} --> // Запускаем сайт Битрикса //")
        try:
            open_driver_bitrix()
            log_message(f"< -- {datetime.now()} --> // Успешное открытие сайта Битрикс //")
        except:
            log_message(f"< -- {datetime.now()} --> // Не удалось открыть сайт Битрикс //")
            stop()

        log_message(f"< -- {datetime.now()} --> // Авторизация на сайте Битрикса //")
        try:
            login_bitrix()
            log_message(f"< -- {datetime.now()} --> // Успешная авторизация //")
        except:
            log_message(f"< -- {datetime.now()} --> // Ошибка при авторизации //")
            stop()

        log_message(f"< -- {datetime.now()} --> // Открытие ватсап //")
        try:
            open_driver()
            log_message(f"< -- {datetime.now()} --> // Успешно открыт //")
        except:
            log_message(f"< -- {datetime.now()} --> // Ошибка при открытии //")
            stop()
        working()

def stop():
    global flag_work,to_work,driver,driver_bitrix
    flag_work=False
    to_work=False
    btn_stop.config(state="disabled")
    window.tksleep(3)
    log_message(f"< -- {datetime.now()} --> // Работа программы остановлена //")
    try:
        driver.quit()
        driver_bitrix.quit()
    except:
        pass
    btn_start.config(state="normal")
    spin.config(state="normal")
    img = ImageTk.PhotoImage(Image.open("./qr/zagl.png"))
    label_img.configure(image=img)
    label_img.image=img

with open("./logs/in.txt", 'r') as file:
    lines = file.readlines()
login=lines[0].replace("\n","")
password=lines[1].replace("\n","")

window = Tk()
window.title("SberBot")
window.geometry('380x700')

lbl = Label(window, text="Тайминг обновления буфера   ")
lbl.place(x=50,y=60)

var = IntVar()
var.set(30)
spin = Spinbox(window, from_=1, to=100, width=5,textvariable=var)
spin.place(x=269,y=60)

Label(window, text="Битрикс Логин:").place(x=50,y=100)

input_login = Entry(window, width=20)
input_login.insert(0,login)
input_login.place(x=169,y=100)

Label(window, text="Битрикс Пароль:").place(x=50,y=130)

input_password = Entry(window, width=20)
input_password.insert(0,password)
input_password.place(x=169,y=130)

btn_start = Button(window, text="Start", command=start, )
btn_start.place(x=110,y=180)

btn_stop = Button(window, text="Stop", command=stop)
btn_stop.config(state="disabled")
btn_stop.place(x=190,y=180)

img = ImageTk.PhotoImage(Image.open("./qr/zagl.png"))
label_img = Label(window, image=img)
label_img.place(x=55,y=220)

log_area = scrolledtext.ScrolledText(window, wrap=WORD, width=42, height=10)
log_area.place(x=10, y=500)
window.mainloop()