import os
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from zoneinfo import ZoneInfo
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5

class LottoBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Lotto Bot - WhatsApp Sender")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.account_sid = tk.StringVar()
        self.auth_token = tk.StringVar()
        self.dad_number = tk.StringVar()
        self.whatsapp_from = tk.StringVar(value="whatsapp:+14155238886")
        
        self.setup_ui()
        self.load_saved_credentials()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="🎰 Lotto Bot", 
                              font=("Arial", 20, "bold"), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Credentials section
        cred_frame = tk.LabelFrame(main_frame, text="Twilio Credentials", 
                                  font=("Arial", 12, "bold"), 
                                  bg='#f0f0f0', fg='#2c3e50')
        cred_frame.pack(fill='x', pady=(0, 10))
        
        # Account SID
        tk.Label(cred_frame, text="Account SID:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(cred_frame, textvariable=self.account_sid, width=40, show="*").grid(row=0, column=1, padx=5, pady=5)
        
        # Auth Token
        tk.Label(cred_frame, text="Auth Token:", bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(cred_frame, textvariable=self.auth_token, width=40, show="*").grid(row=1, column=1, padx=5, pady=5)
        
        # Dad Number
        tk.Label(cred_frame, text="Dad's Number:", bg='#f0f0f0').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(cred_frame, textvariable=self.dad_number, width=40).grid(row=2, column=1, padx=5, pady=5)
        
        # WhatsApp From
        tk.Label(cred_frame, text="WhatsApp From:", bg='#f0f0f0').grid(row=3, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(cred_frame, textvariable=self.whatsapp_from, width=40).grid(row=3, column=1, padx=5, pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=10)
        
        # Generate numbers button
        self.gen_button = tk.Button(button_frame, text="🎲 Generate Lotto Numbers", 
                                   command=self.generate_numbers, 
                                   bg='#3498db', fg='white', 
                                   font=("Arial", 12, "bold"),
                                   padx=20, pady=10)
        self.gen_button.pack(side='left', padx=5)
        
        # Send button
        self.send_button = tk.Button(button_frame, text="📱 Send to WhatsApp", 
                                    command=self.send_to_whatsapp, 
                                    bg='#27ae60', fg='white', 
                                    font=("Arial", 12, "bold"),
                                    padx=20, pady=10)
        self.send_button.pack(side='left', padx=5)
        
        # Auto-fill credentials button
        autofill_button = tk.Button(button_frame, text="⚡ Auto-Fill Credentials", 
                                   command=self.auto_fill_credentials, 
                                   bg='#e74c3c', fg='white', 
                                   font=("Arial", 10, "bold"),
                                   padx=10, pady=5)
        autofill_button.pack(side='right', padx=5)
        
        # Save credentials button
        save_button = tk.Button(button_frame, text="💾 Save Credentials", 
                               command=self.save_credentials, 
                               bg='#95a5a6', fg='white', 
                               font=("Arial", 10),
                               padx=10, pady=5)
        save_button.pack(side='right', padx=5)
        
        # Generated numbers display
        numbers_frame = tk.LabelFrame(main_frame, text="Generated Numbers", 
                                     font=("Arial", 12, "bold"), 
                                     bg='#f0f0f0', fg='#2c3e50')
        numbers_frame.pack(fill='both', expand=True, pady=10)
        
        self.numbers_text = scrolledtext.ScrolledText(numbers_frame, height=8, 
                                                     font=("Courier", 12),
                                                     bg='#ecf0f1', fg='#2c3e50')
        self.numbers_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to generate lotto numbers!")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor='w', 
                             bg='#34495e', fg='white')
        status_bar.pack(side='bottom', fill='x')
    
    def load_saved_credentials(self):
        """Load saved credentials from environment or file"""
        self.account_sid.set(os.getenv("TWILIO_ACCOUNT_SID", ""))
        self.auth_token.set(os.getenv("TWILIO_AUTH_TOKEN", ""))
        self.dad_number.set(os.getenv("DAD_NUMBER", ""))
        self.whatsapp_from.set(os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886"))
    
    def auto_fill_credentials(self):
        """Auto-fill the correct credentials"""
        self.account_sid.set("AC8791f70edd64db6e26ac016681d07335")
        self.auth_token.set("1780aa886302c3397d7076f8689f297a")
        self.dad_number.set("+385998167000")
        self.whatsapp_from.set("whatsapp:+14155238886")
        self.status_var.set("✅ Credentials auto-filled!")
        messagebox.showinfo("Auto-Fill", "Credentials have been filled automatically!")
    
    def save_credentials(self):
        """Save credentials to environment variables for this session"""
        os.environ["TWILIO_ACCOUNT_SID"] = self.account_sid.get()
        os.environ["TWILIO_AUTH_TOKEN"] = self.auth_token.get()
        os.environ["DAD_NUMBER"] = self.dad_number.get()
        os.environ["TWILIO_WHATSAPP_FROM"] = self.whatsapp_from.get()
        messagebox.showinfo("Success", "Credentials saved for this session!")
    
    def gen_numbers(self):
        """Generate lotto numbers"""
        main = sorted(random.sample(range(1, 51), 5))
        extra = sorted(random.sample(range(1, 13), 2))
        return main, extra
    
    def build_message(self, tz="Europe/Berlin"):
        """Build the WhatsApp message"""
        try:
            now = datetime.now(ZoneInfo(tz))
        except:
            # Fallback to UTC if timezone not available
            now = datetime.now()
        date_str = now.strftime("%A, %d %B %Y")
        main, extra = self.gen_numbers()
        main_str = " - ".join(f"{n:02d}" for n in main)
        extra_str = " - ".join(f"{n:02d}" for n in extra)
        return (
            f"🎰 *Lotto numbers — {date_str}*\n\n"
            f"📍 Main (1–50): {main_str}\n"
            f"⭐ Extra (1–12): {extra_str}\n\n"
            "Good luck! 🍀\n_Automated Lotto Bot_"
        )
    
    def generate_numbers(self):
        """Generate and display lotto numbers"""
        try:
            message = self.build_message()
            self.numbers_text.delete(1.0, tk.END)
            self.numbers_text.insert(1.0, message)
            self.status_var.set("✅ Numbers generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate numbers: {e}")
            self.status_var.set("❌ Error generating numbers")
    
    def send_to_whatsapp(self):
        """Send the generated message to WhatsApp"""
        if not all([self.account_sid.get(), self.auth_token.get(), self.dad_number.get()]):
            messagebox.showerror("Error", "Please fill in all required credentials!")
            return
        
        if not self.numbers_text.get(1.0, tk.END).strip():
            messagebox.showerror("Error", "Please generate numbers first!")
            return
        
        try:
            self.status_var.set("📱 Sending to WhatsApp...")
            self.root.update()
            
            # Use the displayed message
            body = self.numbers_text.get(1.0, tk.END).strip()
            
            client = Client(self.account_sid.get(), self.auth_token.get())
            
            for attempt in range(1, RETRY_ATTEMPTS + 1):
                try:
                    msg = client.messages.create(
                        from_=self.whatsapp_from.get(),
                        to=f"whatsapp:{self.dad_number.get()}",
                        body=body
                    )
                    self.status_var.set(f"✅ Sent successfully! (SID: {msg.sid})")
                    messagebox.showinfo("Success", f"Message sent successfully!\nSID: {msg.sid}")
                    return
                except TwilioRestException as e:
                    error_msg = f"Twilio error (attempt {attempt}): {e}"
                    if attempt < RETRY_ATTEMPTS:
                        self.status_var.set(f"⚠️ {error_msg} - Retrying...")
                        self.root.update()
                        time.sleep(RETRY_DELAY_SECONDS)
                    else:
                        self.status_var.set(f"❌ {error_msg}")
                        messagebox.showerror("Error", error_msg)
                except Exception as e:
                    error_msg = f"Unexpected error (attempt {attempt}): {e}"
                    if attempt < RETRY_ATTEMPTS:
                        self.status_var.set(f"⚠️ {error_msg} - Retrying...")
                        self.root.update()
                        time.sleep(RETRY_DELAY_SECONDS)
                    else:
                        self.status_var.set(f"❌ {error_msg}")
                        messagebox.showerror("Error", error_msg)
        except Exception as e:
            self.status_var.set(f"❌ Error: {e}")
            messagebox.showerror("Error", f"Failed to send message: {e}")

def main():
    root = tk.Tk()
    app = LottoBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
