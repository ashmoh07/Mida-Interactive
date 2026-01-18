import os, sys, time, socket, json, base64, threading
import tkinter as tk
from tkinter import messagebox
import pyautogui, cv2, numpy as np
import winreg as reg
from flask import Flask, request, jsonify
from flask_socketio import SocketIO

# --- إعدادات الحماية ---
SYSTEM_NAME = "Mida Interactive Pro"
PERMANENT_SERIAL = "MIDA-2026-PRO-99"
TRIAL_DAYS = 15

def check_license_status():
    key_path = r"Software\MidaInteractive"
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS)
        status, _ = reg.QueryValueEx(key, "Status")
        if status == "Active": return "Active"
        first_run, _ = reg.QueryValueEx(key, "FirstRun")
        elapsed = (time.time() - float(first_run)) / (24 * 3600)
        if elapsed > TRIAL_DAYS: return "Expired"
        return "Trial"
    except:
        reg.CreateKey(reg.HKEY_CURRENT_USER, key_path)
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key, "FirstRun", 0, reg.REG_SZ, str(time.time()))
        reg.SetValueEx(key, "Status", 0, reg.REG_SZ, "Trial")
        return "Trial"

def activate_system(serial_input, root):
    if serial_input == PERMANENT_SERIAL:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\MidaInteractive", 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key, "Status", 0, reg.REG_SZ, "Active")
        messagebox.showinfo("نجاح", "تم التفعيل بنجاح!")
        root.destroy()
    else:
        messagebox.showerror("خطأ", "السيريال غير صحيح")

class SetupInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mida Setup")
        self.root.geometry("400x250")
        tk.Label(self.root, text="MIDA INTERACTIVE PRO", font=("Arial", 14, "bold")).pack(pady=20)
        self.entry = tk.Entry(self.root, font=("Arial", 12))
        self.entry.pack(pady=10)
        tk.Button(self.root, text="Activate", command=lambda: activate_system(self.entry.get(), self.root)).pack(pady=10)
        self.root.mainloop()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def screen_capture():
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (640, 360))
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])
        encoded = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('screen_frame', {'image': encoded})
        socketio.sleep(0.1)

if
messagebox.showinfo("نجاح", "تم تفعيل نظام ميدا بنجاح! سيفتح البرنامج الآن.")
        root.destroy()
    else:
        messagebox.showerror("خطأ", "السيريال نمبر غير صحيح!")

# --- واجهة الـ Setup الاحترافية ---
class SetupInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"تثبيت {SYSTEM_NAME}")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")
        
        # تصميم الواجهة
        tk.Label(self.root, text="MIDA INTERACTIVE", fg="white", bg="#2c3e50", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text="برجاء إدخال السيريال نمبر للتفعيل:", fg="#ecf0f1", bg="#2c3e50").pack(pady=5)
        
        self.entry = tk.Entry(self.root, font=("Arial", 14), justify='center')
        self.entry.pack(pady=10, padx=20, fill='x')
        
        btn = tk.Button(self.root, text="تفعيل الآن", command=lambda: activate_system(self.entry.get(), self.root),
                        bg="#27ae60", fg="white", font=("Arial", 12, "bold"), relief='flat')
        btn.pack(pady=20, ipadx=20, ipady=5)
        
        tk.Label(self.root, text="تواصل معنا: 011536404", fg="#bdc3c7", bg="#2c3e50", font=("Arial", 9)).pack(side="bottom", pady=10)
        self.root.mainloop()

# --- قسم السيرفر والبث (بعد التفعيل) ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('control_command')
def handle_control(data):
    # التحكم في الماوس والكيبورد من المدرس أو الطالب المسموح له
    action = data.get('type')
    if action == 'mouse':
        pyautogui.moveRel(data['dx'], data['dy'], _pause=False)
    elif action == 'click':
        pyautogui.click()
    elif action == 'key':
        pyautogui.press(data['key'])

def screen_capture_thread():
    """بث الشاشة لـ 50 جهاز بجودة مضغوطة"""
    while True:
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (854, 480)) # جودة 480p لضمان السرعة
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])
        encoded = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('screen_frame', {'image': encoded})
        socketio.sleep(0.05) # 20 إطار في الثانية

def start_mida_server():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f"--- {SYSTEM_NAME} جاهز للعمل ---")
    print(f"عنوان الاتصال (IP): {ip}")
    
    # تشغيل البث في الخلفية
    socketio.start_background_task(screen_capture_
      
