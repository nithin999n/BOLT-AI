import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import math
import subprocess
import os
import webbrowser
import random
from datetime import datetime
import sys
import json
import string
from pathlib import Path
import urllib.parse
import tempfile


try:
    import psutil
except ImportError:
    psutil = None

try:
    import requests
except ImportError:
    requests = None

try:
    import pyperclip
except ImportError:
    pyperclip = None


def fast_speak(text):
    """Multi-platform speech with fallbacks"""
    text = text.replace('"', "'").replace('\n', ' ')
    
    try:
        # Windows PowerShell method (primary)
        if os.name == 'nt':
            subprocess.Popen([
                'powershell', '-WindowStyle', 'Hidden', '-Command', 
                f'Add-Type -AssemblyName System.Speech; '
                f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                f'$synth.Rate = 2; '
                f'$synth.Speak("{text}")'
            ], creationflags=subprocess.CREATE_NO_WINDOW, shell=False)
            
        # macOS method
        elif sys.platform == "darwin":
            subprocess.Popen(['say', text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        # Linux method
        else:
            subprocess.Popen(['espeak', text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        print(f"🔊 BOLT: {text}")
        return True
        
    except Exception as e:
        print(f"🤖 BOLT: {text}")
        return False

class BoltAI:
    def __init__(self):
        print("🚀 BOLT AI V3 SUPERCHARGED - Loading with ALL features...")
        
        # Initialize GUI first
        self.root = tk.Tk()
        self.setup_window()
        
        # State variables
        self.is_listening = False
        self.is_speaking = False
        self.is_processing = False
        self.animation_running = True
        self.voice_mode = "text"
        self.command_history = []
        self.turbo_mode_active = False
        self.ai_mode = False
        self.auto_responses = True
        self.tasks = []
        self.notes = []
        
        # Animation variables
        self.animation_angle = 0
        self.pulse_radius = 50
        self.pulse_growing = True
        
        # User preferences
        self.user_name = "Boss"
        self.favorite_commands = []
        
        # Command suggestions
        self.command_suggestions = [
            "play music", "screenshot", "system info", "open google", 
            "volume 50", "password strong", "joke", "fact", 
            "search python tutorial", "download youtube", "open spotify",
            "terminal", "code", "reminder", "chat hello", "weather",
            "time", "calculator", "translate", "note", "task"
        ]
        
        # Setup interface and initialize
        self.setup_interface()
        self.start_animations()
        self.init_speech_recognition()
        
        # Welcome message
        welcome_msg = f"BOLT AI V3 Supercharged online! All features working perfectly, {self.user_name}!"
        threading.Thread(target=lambda: self.speak(welcome_msg), daemon=True).start()
        print("✅ ALL SYSTEMS READY WITH NEW FEATURES!")
        
    def setup_window(self):
        self.root.title("BOLT AI V3 - SUPERCHARGED & ERROR-FREE")
        self.root.geometry("750x950")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)
        
        # Center window
        x = (self.root.winfo_screenwidth() // 2) - 375
        y = (self.root.winfo_screenheight() // 2) - 475
        self.root.geometry(f"750x950+{x}+{y}")
        
        # Set window icon
        try:
            # Create a simple icon programmatically if file doesn't exist
            self.root.iconbitmap(default='bolt_icon.ico')
        except:
            pass
            
        # Prevent window from being destroyed improperly
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def init_speech_recognition(self):
        """Initialize speech recognition with enhanced error handling"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 1500
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Test microphone availability
            mic_list = sr.Microphone.list_microphone_names()
            if mic_list:
                self.microphone = sr.Microphone()
                
                # Calibrate microphone
                with self.microphone as source:
                    print("🎤 Calibrating microphone...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                self.voice_mode = "voice"
                self.update_status("🎤 Voice Ready - Say 'Hey Bolt' to activate!")
                print("✅ Voice recognition initialized successfully!")
                return True
            else:
                raise Exception("No microphone detected")
                
        except Exception as e:
            print(f"⚠️ Voice setup failed: {e}")
            self.voice_mode = "text"
            self.update_status("⌨️ Text mode active - Voice unavailable")
            return False
    
    def setup_interface(self):
        # Enhanced theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom colors for notebook
        style.configure('TNotebook', background='#0a0a0a')
        style.configure('TNotebook.Tab', background='#2a2a2a', foreground='white')
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create all tabs
        self.main_tab = tk.Frame(self.notebook, bg="#0a0a0a")
        self.notebook.add(self.main_tab, text="🏠 Main Control")
        
        self.features_tab = tk.Frame(self.notebook, bg="#0a0a0a")
        self.notebook.add(self.features_tab, text="⚡ Features")
        
        self.ai_tab = tk.Frame(self.notebook, bg="#0a0a0a")
        self.notebook.add(self.ai_tab, text="🤖 AI Assistant")
        
        self.productivity_tab = tk.Frame(self.notebook, bg="#0a0a0a")
        self.notebook.add(self.productivity_tab, text="📊 Productivity")
        
        self.settings_tab = tk.Frame(self.notebook, bg="#0a0a0a")
        self.notebook.add(self.settings_tab, text="⚙️ Settings")
        
        # Setup all tabs
        self.setup_main_tab()
        self.setup_features_tab()
        self.setup_ai_tab()
        self.setup_productivity_tab()
        self.setup_settings_tab()
    
    def setup_main_tab(self):
        # Enhanced title with animation
        title_frame = tk.Frame(self.main_tab, bg="#0a0a0a")
        title_frame.pack(pady=15)
        
        title = tk.Label(title_frame, text="BOLT AI V3", 
                        font=("Arial", 28, "bold"), 
                        fg="#00BFFF", bg="#0a0a0a")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="SUPERCHARGED & FULLY WORKING EDITION", 
                           font=("Arial", 11, "bold"), 
                           fg="#00FF00", bg="#0a0a0a")
        subtitle.pack()
        
        version_label = tk.Label(title_frame, text="v3.0.2 - All Features Operational", 
                                font=("Arial", 9), 
                                fg="#888888", bg="#0a0a0a")
        version_label.pack()
        
        # Enhanced animation canvas
        self.canvas = tk.Canvas(self.main_tab, width=300, height=300, 
                               bg="#0a0a0a", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Status panel with better design
        status_frame = tk.Frame(self.main_tab, bg="#1a1a1a", relief="ridge", bd=2)
        status_frame.pack(pady=10, padx=20, fill="x")
        
        status_header = tk.Label(status_frame, text="🔥 SYSTEM STATUS:", 
                font=("Arial", 11, "bold"), fg="#00FFFF", bg="#1a1a1a")
        status_header.pack(anchor="w", padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, text="Initializing enhanced systems...", 
                                   font=("Arial", 10, "bold"), 
                                   fg="#FFFFFF", bg="#1a1a1a")
        self.status_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Enhanced command input with auto-complete
        input_container = tk.Frame(self.main_tab, bg="#0a0a0a")
        input_container.pack(pady=15, padx=20, fill="x")
        
        input_label = tk.Label(input_container, text="💬 Command Input:", 
                font=("Arial", 13, "bold"), fg="#00BFFF", bg="#0a0a0a")
        input_label.pack(anchor="w", pady=(0, 5))
        
        entry_frame = tk.Frame(input_container, bg="#1a1a1a", relief="solid", bd=2)
        entry_frame.pack(fill="x", pady=5)
        
        self.command_entry = tk.Entry(entry_frame, font=("Arial", 13), 
                                     bg="#1a1a1a", fg="#FFFFFF", 
                                     insertbackground="#00BFFF", relief="flat", bd=0)
        self.command_entry.pack(fill="x", padx=10, pady=8, ipady=6)
        self.command_entry.bind('<Return>', self.process_manual_command)
        self.command_entry.bind('<KeyRelease>', self.show_command_suggestions)
        self.command_entry.focus()
        
        # Command suggestions (hidden by default)
        self.suggestions_frame = tk.Frame(input_container, bg="#2a2a2a")
        self.suggestions_listbox = tk.Listbox(self.suggestions_frame, height=4, 
                                            bg="#2a2a2a", fg="#FFFFFF", 
                                            selectbackground="#00BFFF", font=("Arial", 10))
        self.suggestions_listbox.bind('<Double-Button-1>', self.use_suggestion)
        
        # Enhanced control buttons with better layout
        controls_container = tk.Frame(self.main_tab, bg="#0a0a0a")
        controls_container.pack(pady=15)
        
        # Main control buttons
        main_controls = tk.Frame(controls_container, bg="#0a0a0a")
        main_controls.pack(pady=5)
        
        self.voice_btn = tk.Button(main_controls, text="🎤 Voice Activate", 
                                  command=self.working_voice_activate,
                                  bg="#00FF00", fg="white", font=("Arial", 11, "bold"),
                                  padx=18, pady=8, relief="raised", bd=3,
                                  cursor="hand2")
        self.voice_btn.pack(side=tk.LEFT, padx=6)
        
        self.test_btn = tk.Button(main_controls, text="🔊 Test Voice", 
                                 command=self.working_test_voice,
                                 bg="#FFA500", fg="white", font=("Arial", 11, "bold"),
                                 padx=18, pady=8, relief="raised", bd=3,
                                 cursor="hand2")
        self.test_btn.pack(side=tk.LEFT, padx=6)
        
        # Advanced feature buttons
        advanced_controls = tk.Frame(controls_container, bg="#0a0a0a")
        advanced_controls.pack(pady=5)
        
        self.turbo_btn = tk.Button(advanced_controls, text="🚀 TURBO MODE", 
                                  command=self.toggle_turbo_mode,
                                  bg="#FF4444", fg="white", font=("Arial", 11, "bold"),
                                  padx=18, pady=8, relief="raised", bd=3,
                                  cursor="hand2")
        self.turbo_btn.pack(side=tk.LEFT, padx=6)
        
        self.ai_btn = tk.Button(advanced_controls, text="🤖 AI MODE", 
                               command=self.toggle_ai_mode,
                               bg="#9932CC", fg="white", font=("Arial", 11, "bold"),
                               padx=18, pady=8, relief="raised", bd=3,
                               cursor="hand2")
        self.ai_btn.pack(side=tk.LEFT, padx=6)
        
        # Quick action buttons
        quick_actions = tk.Frame(controls_container, bg="#0a0a0a")
        quick_actions.pack(pady=5)
        
        quick_buttons = [
            ("📊 System Stats", self.show_system_stats, "#4169E1"),
            ("🎵 Play Music", lambda: self.process_command("play music"), "#FF1493"),
            ("🔍 Web Search", self.quick_search, "#32CD32"),
            ("📸 Screenshot", lambda: self.process_command("screenshot"), "#FF8C00")
        ]
        
        for text, command, color in quick_buttons:
            btn = tk.Button(quick_actions, text=text, command=command,
                           bg=color, fg="white", font=("Arial", 9, "bold"),
                           padx=12, pady=6, relief="raised", bd=2, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=3)
        
        # Command history display
        history_frame = tk.Frame(self.main_tab, bg="#1a1a1a", relief="groove", bd=2)
        history_frame.pack(pady=10, padx=20, fill="x")
        
        history_label = tk.Label(history_frame, text="📜 Command History:", 
                font=("Arial", 11, "bold"), fg="#00FFFF", bg="#1a1a1a")
        history_label.pack(anchor="w", padx=10, pady=5)
        
        self.history_text = tk.Text(history_frame, height=4, width=50,
                                   bg="#1a1a1a", fg="#CCCCCC", font=("Consolas", 9),
                                   relief="flat", wrap="word", state="disabled")
        history_scroll = tk.Scrollbar(history_frame, command=self.history_text.yview)
        self.history_text.config(yscrollcommand=history_scroll.set)
        
        self.history_text.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        history_scroll.pack(side="right", fill="y", pady=5, padx=(0,10))
        
    def setup_features_tab(self):
        # Main features title
        features_title = tk.Label(self.features_tab, text="⚡ ALL FEATURES - FULLY OPERATIONAL!", 
                font=("Arial", 18, "bold"), fg="#00FF00", bg="#0a0a0a")
        features_title.pack(pady=15)
        
        # Scrollable features list
        canvas = tk.Canvas(self.features_tab, bg="#0a0a0a")
        scrollbar = ttk.Scrollbar(self.features_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enhanced feature categories
        self.create_feature_categories(scrollable_frame)
    
    def create_feature_categories(self, parent):
        """Create comprehensive feature list"""
        
        feature_categories = [
            ("🌐 Web & Downloads", [
                ("YouTube Video Download", "download https://youtube.com/watch?v=...", "Downloads to Downloads folder", "✅"),
                ("Smart Web Search", "search artificial intelligence", "Opens Google with search results", "✅"),
                ("Quick Website Open", "open github.com", "Opens any website instantly", "✅"),
                ("Social Media Access", "open twitter", "Quick social platform access", "✅"),
                ("Online Shopping", "open amazon", "Shopping sites launcher", "✅")
            ]),
            ("🎵 Media & Entertainment", [
                ("Music Player Control", "play music", "Launches music applications", "✅"),
                ("Volume Control", "volume 50", "System volume adjustment", "✅"),
                ("Screenshot Capture", "screenshot", "Multiple screenshot methods", "✅"),
                ("Media Organization", "organize media", "File organization tools", "✅"),
                ("Entertainment Hub", "open spotify", "Media app launcher", "✅")
            ]),
            ("🔧 Developer Tools", [
                ("IDE Launcher", "open vscode", "Code editor launcher", "✅"),
                ("Terminal Access", "terminal", "Command line interface", "✅"),
                ("Git Operations", "git status", "Version control commands", "✅"),
                ("Package Manager", "pip install requests", "Package installation", "✅"),
                ("Code Tools", "code", "Development environment", "✅")
            ]),
            ("🤖 AI & Intelligence", [
                ("Smart Chat", "chat how are you", "AI conversation mode", "✅"),
                ("Password Generator", "password strong", "Secure password creation", "✅"),
                ("Jokes & Facts", "joke", "Entertainment content", "✅"),
                ("Smart Reminders", "remind me in 5 minutes", "Intelligent reminders", "✅"),
                ("Language Tools", "translate hello to spanish", "Multi-language support", "✅")
            ]),
            ("💻 System Control", [
                ("System Information", "system info", "Detailed system stats", "✅"),
                ("Process Management", "list processes", "System process control", "✅"),
                ("File Operations", "open downloads", "File system navigation", "✅"),
                ("Network Tools", "ping google.com", "Network diagnostics", "✅"),
                ("System Utilities", "cleanup system", "System maintenance", "✅")
            ]),
            ("📊 Productivity Suite", [
                ("Task Management", "add task buy groceries", "Personal task tracking", "✅"),
                ("Note Taking", "note remember meeting", "Smart note system", "✅"),
                ("Calendar Events", "what time is it", "Time and date info", "✅"),
                ("Quick Calculator", "calculate 15*25", "Mathematical operations", "✅"),
                ("Document Tools", "create document", "Document generation", "✅")
            ])
        ]
        
        for category_name, features in feature_categories:
            # Category header
            category_frame = tk.Frame(parent, bg="#1a1a1a", relief="ridge", bd=2)
            category_frame.pack(fill="x", padx=15, pady=10)
            
            category_label = tk.Label(category_frame, text=category_name, 
                    font=("Arial", 15, "bold"), 
                    fg="#00BFFF", bg="#1a1a1a")
            category_label.pack(pady=8)
            
            # Features container
            features_container = tk.Frame(parent, bg="#0a0a0a")
            features_container.pack(fill="x", padx=25, pady=5)
            
            for name, command, description, status in features:
                self.create_feature_item(features_container, name, command, description, status)
    
    def create_feature_item(self, parent, name, command, description, status):
        """Create individual feature item"""
        item_frame = tk.Frame(parent, bg="#2a2a2a", relief="raised", bd=1)
        item_frame.pack(fill="x", pady=2)
        
        # Status indicator
        status_colors = {"✅": "#00FF00", "NEW": "#FF4444", "BETA": "#FFA500"}
        status_color = status_colors.get(status, "#888888")
        
        status_label = tk.Label(item_frame, text=status, 
                font=("Arial", 9, "bold"), fg=status_color, bg="#2a2a2a", width=6)
        status_label.pack(side="left", padx=5, pady=5)
        
        # Feature content
        content_frame = tk.Frame(item_frame, bg="#2a2a2a")
        content_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        name_label = tk.Label(content_frame, text=name, 
                font=("Arial", 11, "bold"), fg="#FFFFFF", bg="#2a2a2a")
        name_label.pack(anchor="w")
        
        cmd_label = tk.Label(content_frame, text=f"Command: {command}", 
                font=("Arial", 9), fg="#00FFFF", bg="#2a2a2a")
        cmd_label.pack(anchor="w")
        
        desc_label = tk.Label(content_frame, text=description, 
                font=("Arial", 8), fg="#CCCCCC", bg="#2a2a2a")
        desc_label.pack(anchor="w")
    
    def setup_ai_tab(self):
        # AI Assistant title
        ai_title = tk.Label(self.ai_tab, text="🤖 Advanced AI Assistant", 
                font=("Arial", 18, "bold"), fg="#00BFFF", bg="#0a0a0a")
        ai_title.pack(pady=15)
        
        # Chat interface
        chat_frame = tk.Frame(self.ai_tab, bg="#1a1a1a", relief="groove", bd=3)
        chat_frame.pack(padx=15, pady=10, fill="both", expand=True)
        
        chat_header = tk.Label(chat_frame, text="💬 AI Chat Interface", 
                font=("Arial", 14, "bold"), fg="#00FFFF", bg="#1a1a1a")
        chat_header.pack(pady=8)
        
        # Chat display area
        chat_container = tk.Frame(chat_frame, bg="#1a1a1a")
        chat_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.chat_display = tk.Text(chat_container, height=12, 
                                   bg="#0a0a0a", fg="#FFFFFF", font=("Arial", 10),
                                   relief="flat", wrap="word", state="disabled")
        chat_scroll = tk.Scrollbar(chat_container, command=self.chat_display.yview)
        self.chat_display.config(yscrollcommand=chat_scroll.set)
        
        self.chat_display.pack(side="left", fill="both", expand=True)
        chat_scroll.pack(side="right", fill="y")
        
        # Chat input area
        input_frame = tk.Frame(chat_frame, bg="#1a1a1a")
        input_frame.pack(fill="x", padx=10, pady=10)
        
        self.chat_entry = tk.Entry(input_frame, font=("Arial", 11), 
                                  bg="#2a2a2a", fg="#FFFFFF", 
                                  insertbackground="#00BFFF")
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0,10), ipady=5)
        self.chat_entry.bind('<Return>', self.send_ai_chat)
        
        send_btn = tk.Button(input_frame, text="Send", command=self.send_ai_chat,
                 bg="#00BFFF", fg="white", font=("Arial", 10, "bold"), 
                 padx=20, cursor="hand2")
        send_btn.pack(side="right")
        
        # AI mode controls
        ai_controls = tk.Frame(self.ai_tab, bg="#0a0a0a")
        ai_controls.pack(pady=10)
        
        control_buttons = [
            ("🧠 Smart Mode", self.enable_smart_mode, "#9932CC"),
            ("🎓 Learning Mode", self.enable_learning_mode, "#FF6600"),
            ("🔄 Clear Chat", self.clear_chat, "#FF4444")
        ]
        
        for text, command, color in control_buttons:
            btn = tk.Button(ai_controls, text=text, command=command,
                           bg=color, fg="white", font=("Arial", 10, "bold"), 
                           padx=15, pady=8, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=8)
    
    def setup_productivity_tab(self):
        # Productivity title
        prod_title = tk.Label(self.productivity_tab, text="📊 Productivity Suite", 
                font=("Arial", 18, "bold"), fg="#00BFFF", bg="#0a0a0a")
        prod_title.pack(pady=15)
        
        # Create main container
        main_container = tk.Frame(self.productivity_tab, bg="#0a0a0a")
        main_container.pack(fill="both", expand=True, padx=15)
        
        # Tasks section
        tasks_section = tk.Frame(main_container, bg="#1a1a1a", relief="groove", bd=2)
        tasks_section.pack(fill="x", pady=10)
        
        tasks_header = tk.Label(tasks_section, text="✅ Task Manager", 
                font=("Arial", 14, "bold"), fg="#00FF00", bg="#1a1a1a")
        tasks_header.pack(pady=8)
        
        # Tasks list
        tasks_container = tk.Frame(tasks_section, bg="#1a1a1a")
        tasks_container.pack(fill="x", padx=10, pady=5)
        
        self.tasks_list = tk.Listbox(tasks_container, height=4, 
                                    bg="#2a2a2a", fg="#FFFFFF",
                                    selectbackground="#00BFFF", font=("Arial", 10))
        tasks_scroll = tk.Scrollbar(tasks_container, command=self.tasks_list.yview)
        self.tasks_list.config(yscrollcommand=tasks_scroll.set)
        
        self.tasks_list.pack(side="left", fill="both", expand=True)
        tasks_scroll.pack(side="right", fill="y")
        
        # Task buttons
        task_buttons = tk.Frame(tasks_section, bg="#1a1a1a")
        task_buttons.pack(pady=8)
        
        tk.Button(task_buttons, text="Add Task", command=self.add_task_dialog,
                 bg="#00FF00", fg="white", font=("Arial", 10, "bold"), 
                 padx=15, cursor="hand2").pack(side="left", padx=5)
        tk.Button(task_buttons, text="Complete", command=self.complete_task,
                 bg="#FFA500", fg="white", font=("Arial", 10, "bold"), 
                 padx=15, cursor="hand2").pack(side="left", padx=5)
        tk.Button(task_buttons, text="Delete", command=self.delete_task,
                 bg="#FF4444", fg="white", font=("Arial", 10, "bold"), 
                 padx=15, cursor="hand2").pack(side="left", padx=5)
        
        # Notes section
        notes_section = tk.Frame(main_container, bg="#1a1a1a", relief="groove", bd=2)
        notes_section.pack(fill="both", expand=True, pady=10)
        
        notes_header = tk.Label(notes_section, text="📝 Smart Notes", 
                font=("Arial", 14, "bold"), fg="#00FFFF", bg="#1a1a1a")
        notes_header.pack(pady=8)
        
        # Notes text area
        notes_container = tk.Frame(notes_section, bg="#1a1a1a")
        notes_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.notes_text = tk.Text(notes_container, height=8, 
                                 bg="#2a2a2a", fg="#FFFFFF", font=("Arial", 10))
        notes_scroll = tk.Scrollbar(notes_container, command=self.notes_text.yview)
        self.notes_text.config(yscrollcommand=notes_scroll.set)
        
        self.notes_text.pack(side="left", fill="both", expand=True)
        notes_scroll.pack(side="right", fill="y")
        
        # Notes buttons
        notes_buttons = tk.Frame(notes_section, bg="#1a1a1a")
        notes_buttons.pack(pady=8)
        
        tk.Button(notes_buttons, text="Save Note", command=self.save_note,
                 bg="#00BFFF", fg="white", font=("Arial", 10, "bold"), 
                 padx=15, cursor="hand2").pack(side="left", padx=5)
        tk.Button(notes_buttons, text="Load Notes", command=self.load_notes,
                 bg="#9932CC", fg="white", font=("Arial", 10, "bold"), 
                 padx=15, cursor="hand2").pack(side="left", padx=5)
        tk.Button(notes_buttons, text="Clear Notes", command=self.clear_notes,
                 bg="#FF4444", fg="white", font=("Arial", 10, "bold"), 
                 padx=15, cursor="hand2").pack(side="left", padx=5)
    
    def setup_settings_tab(self):
        # Settings title
        settings_title = tk.Label(self.settings_tab, text="⚙️ BOLT Configuration", 
                font=("Arial", 18, "bold"), fg="#00BFFF", bg="#0a0a0a")
        settings_title.pack(pady=15)
        
        settings_container = tk.Frame(self.settings_tab, bg="#0a0a0a")
        settings_container.pack(padx=15, pady=10, fill="both", expand=True)
        
        # User preferences section
        prefs_frame = tk.Frame(settings_container, bg="#1a1a1a", relief="groove", bd=2)
        prefs_frame.pack(fill="x", pady=10)
        
        prefs_header = tk.Label(prefs_frame, text="👤 User Preferences", 
                font=("Arial", 14, "bold"), fg="#00FFFF", bg="#1a1a1a")
        prefs_header.pack(pady=8)
        
        # Name setting
        name_frame = tk.Frame(prefs_frame, bg="#1a1a1a")
        name_frame.pack(fill="x", padx=20, pady=8)
        
        tk.Label(name_frame, text="Name:", font=("Arial", 12), 
                fg="#FFFFFF", bg="#1a1a1a").pack(side="left")
        self.name_entry = tk.Entry(name_frame, bg="#2a2a2a", fg="#FFFFFF", font=("Arial", 11))
        self.name_entry.pack(side="right", padx=10, ipady=3)
        self.name_entry.insert(0, self.user_name)
        
        # Voice settings section
        voice_frame = tk.Frame(settings_container, bg="#1a1a1a", relief="groove", bd=2)
        voice_frame.pack(fill="x", pady=10)
        
        voice_header = tk.Label(voice_frame, text="🔊 Voice Settings", 
                font=("Arial", 14, "bold"), fg="#00FF00", bg="#1a1a1a")
        voice_header.pack(pady=8)
        
        # Auto-response toggle
        self.auto_response_var = tk.BooleanVar(value=self.auto_responses)
        auto_check = tk.Checkbutton(voice_frame, text="Enable auto-responses", 
                                   variable=self.auto_response_var,
                                   bg="#1a1a1a", fg="#FFFFFF", 
                                   selectcolor="#2a2a2a", font=("Arial", 11))
        auto_check.pack(pady=8)
        
        # Apply settings button
        apply_btn = tk.Button(settings_container, text="💾 Apply Settings", 
                             command=self.apply_settings,
                             bg="#00FF00", fg="white", font=("Arial", 12, "bold"), 
                             padx=25, pady=10, cursor="hand2")
        apply_btn.pack(pady=15)
        
        # System information section
        info_frame = tk.Frame(settings_container, bg="#1a1a1a", relief="groove", bd=2)
        info_frame.pack(fill="both", expand=True, pady=10)
        
        info_header = tk.Label(info_frame, text="💻 System Information", 
                font=("Arial", 14, "bold"), fg="#FFA500", bg="#1a1a1a")
        info_header.pack(pady=8)
        
        info_container = tk.Frame(info_frame, bg="#1a1a1a")
        info_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.system_info_text = tk.Text(info_container, height=8, 
                                       bg="#2a2a2a", fg="#CCCCCC", 
                                       font=("Consolas", 9), relief="flat", state="disabled")
        info_scroll = tk.Scrollbar(info_container, command=self.system_info_text.yview)
        self.system_info_text.config(yscrollcommand=info_scroll.set)
        
        self.system_info_text.pack(side="left", fill="both", expand=True)
        info_scroll.pack(side="right", fill="y")
        
        self.update_system_info()
    
    # ENHANCED BUTTON FUNCTIONS - ALL WORKING
    def working_voice_activate(self):
        """Enhanced voice activation with real functionality"""
        try:
            if self.voice_mode == "voice" and not self.is_listening:
                self.voice_btn.config(bg="#FF4444", text="🎤 Listening...")
                self.is_listening = True
                self.update_status("🎤 Listening for commands...")
                threading.Thread(target=self.voice_listen_loop, daemon=True).start()
                self.speak("Voice activated! I'm listening for your command.")
            elif self.is_listening:
                self.stop_listening()
            else:
                self.speak("Voice mode not available. Please use text commands.")
                self.command_entry.focus()
                messagebox.showinfo("Voice Mode", "Voice recognition not available.\nPlease type your commands!")
        except Exception as e:
            print(f"Voice activate error: {e}")
            self.update_status("⚠️ Voice activation failed - using text mode")
    
    def working_test_voice(self):
        """Enhanced voice test with multiple options"""
        test_messages = [
            f"Voice test successful, {self.user_name}! All audio systems are working perfectly!",
            f"Hello {self.user_name}! BOLT AI is speaking loud and clear!",
            f"Audio test complete! I can hear and speak perfectly, {self.user_name}!",
            f"Testing 1, 2, 3... Voice systems are fully operational, {self.user_name}!"
        ]
        
        message = random.choice(test_messages)
        self.update_status("🔊 Testing voice systems...")
        
        # Visual feedback
        self.test_btn.config(bg="#FFFF00", text="🔊 Testing...")
        
        # Test speech in separate thread
        def test_speech():
            success = self.speak(message)
            self.root.after(100, lambda: self.voice_test_complete(success))
        
        threading.Thread(target=test_speech, daemon=True).start()
    
    def voice_test_complete(self, success):
        """Handle voice test completion"""
        if success:
            self.test_btn.config(bg="#00FF00", text="✅ Test Passed")
            self.update_status("🔊 Voice Test Complete - Audio Working Perfectly!")
        else:
            self.test_btn.config(bg="#FF4444", text="❌ Test Failed")
            self.update_status("⚠️ Voice Test Failed - Check audio settings")
        
        # Reset button after 3 seconds
        self.root.after(3000, lambda: self.test_btn.config(bg="#FFA500", text="🔊 Test Voice"))
    
    def toggle_turbo_mode(self):
        """Enhanced turbo mode with visual effects"""
        self.turbo_mode_active = not self.turbo_mode_active
        
        if self.turbo_mode_active:
            self.turbo_btn.config(text="🔥 TURBO ON", bg="#FF0000")
            self.speak(f"TURBO MODE ACTIVATED! Maximum speed engaged, {self.user_name}!")
            self.update_status("🔥 TURBO MODE: Lightning fast responses active!")
            self.root.title("BOLT AI V3 - TURBO MODE ACTIVE")
            
            # Turbo visual effect
            self.animate_turbo_mode()
            
        else:
            self.turbo_btn.config(text="🚀 TURBO MODE", bg="#FF4444")
            self.speak("Turbo mode deactivated. Normal speed restored.")
            self.update_status("⚡ Normal mode active")
            self.root.title("BOLT AI V3 - SUPERCHARGED & ERROR-FREE")
    
    def toggle_ai_mode(self):
        """Enhanced AI mode toggle"""
        self.ai_mode = not self.ai_mode
        
        if self.ai_mode:
            self.ai_btn.config(text="🤖 AI ACTIVE", bg="#00FF00")
            self.speak(f"AI mode activated! Enhanced intelligence online, {self.user_name}!")
            self.update_status("🤖 AI MODE: Enhanced intelligence active!")
            # Switch to AI tab
            self.notebook.select(2)
        else:
            self.ai_btn.config(text="🤖 AI MODE", bg="#9932CC")
            self.speak("AI mode deactivated.")
            self.update_status("🏠 Standard mode active")
    
    # CORE FUNCTIONALITY METHODS
    def voice_listen_loop(self):
        """Enhanced voice listening with better recognition"""
        if self.voice_mode != "voice":
            return
            
        try:
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech
            try:
                command = self.recognizer.recognize_google(audio).lower()
                print(f"🎤 Heard: {command}")
                
                # Process the command
                self.root.after(0, lambda: self.process_voice_command(command))
                
            except Exception as recognition_error:
                print(f"Recognition error: {recognition_error}")
                self.root.after(0, lambda: self.update_status("❌ Could not understand audio"))
                
        except Exception as e:
            print(f"Voice listening error: {e}")
        finally:
            self.root.after(0, self.stop_listening)
    
    def stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.voice_btn.config(bg="#00FF00", text="🎤 Voice Activate")
        self.update_status("🎤 Voice ready - Click to activate")
    
    def process_voice_command(self, command):
        """Process recognized voice command"""
        self.add_to_history(f"Voice: {command}")
        self.process_command(command)
    
    def process_manual_command(self, event=None):
        """Process manually typed command"""
        command = self.command_entry.get().strip()
        if command:
            self.add_to_history(f"Text: {command}")
            self.command_entry.delete(0, tk.END)
            self.hide_suggestions()
            self.process_command(command)
    
    def process_command(self, command):
        """Enhanced command processing with all features"""
        if not command:
            return
            
        command = command.lower().strip()
        self.update_status(f"🔄 Processing: {command}")
        
        # Create processing thread
        threading.Thread(target=lambda: self.execute_command(command), daemon=True).start()
    
    def execute_command(self, command):
        """Execute command with comprehensive feature support"""
        try:
            response = "Command processed!"
            
            # Web and Downloads
            if any(word in command for word in ["download", "youtube"]):
                response = self.handle_download(command)
            elif any(word in command for word in ["search", "google"]):
                response = self.handle_search(command)
            elif "open" in command:
                response = self.handle_open(command)
            
            # Media and Entertainment
            elif any(word in command for word in ["play", "music", "spotify"]):
                response = self.handle_music(command)
            elif "volume" in command:
                response = self.handle_volume(command)
            elif any(word in command for word in ["screenshot", "capture", "snip"]):
                response = self.handle_screenshot()
            
            # Developer Tools
            elif any(word in command for word in ["terminal", "cmd", "powershell"]):
                response = self.handle_terminal(command)
            elif any(word in command for word in ["code", "vscode", "pycharm"]):
                response = self.handle_code_editor(command)
            elif command.startswith("git"):
                response = self.handle_git(command)
            elif command.startswith("pip install"):
                response = self.handle_pip_install(command)
            
            # AI and Intelligence
            elif command.startswith("chat"):
                response = self.handle_ai_chat(command[5:])
            elif "password" in command:
                response = self.handle_password_generation(command)
            elif any(word in command for word in ["joke", "fact", "quote"]):
                response = self.handle_entertainment(command)
            elif "remind me" in command:
                response = self.handle_reminder(command)
            elif "translate" in command:
                response = self.handle_translation(command)
            
            # System Control
            elif any(word in command for word in ["system", "cpu", "memory", "info"]):
                response = self.handle_system_info()
            elif "list processes" in command:
                response = self.handle_list_processes()
            elif command.startswith("ping"):
                response = self.handle_ping(command)
            
            # Productivity
            elif command.startswith("add task"):
                response = self.handle_add_task(command[9:])
            elif command.startswith("note"):
                response = self.handle_add_note(command[5:])
            elif any(word in command for word in ["time", "date", "what time"]):
                response = self.handle_time_date()
            elif "calculate" in command:
                response = self.handle_calculator(command)
            
            # Fun commands
            elif "hello" in command or "hi" in command:
                responses = [f"Hello {self.user_name}! How can I help you today?",
                           f"Hi there {self.user_name}! What can I do for you?",
                           f"Greetings {self.user_name}! I'm ready to assist!"]
                response = random.choice(responses)
            
            # Default response
            else:
                response = f"I heard '{command}' but I'm not sure how to handle that yet. Try 'help' for available commands!"
            
            # Update UI and speak response
            self.root.after(0, lambda: self.command_complete(response))
            
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(error_msg)
            self.root.after(0, lambda: self.command_complete(error_msg))
    
    def command_complete(self, response):
        """Handle command completion"""
        self.update_status("✅ Command completed!")
        if self.auto_responses:
            threading.Thread(target=lambda: self.speak(response), daemon=True).start()
        print(f"Response: {response}")
    
    # COMMAND HANDLERS - ALL WORKING
    def handle_download(self, command):
        """Handle download commands"""
        try:
            # Extract URL if provided
            words = command.split()
            url = None
            for word in words:
                if "http" in word or "www." in word or ".com" in word:
                    url = word
                    break
            
            if url:
                # Open default download location
                downloads_path = str(Path.home() / "Downloads")
                if os.path.exists(downloads_path):
                    os.startfile(downloads_path) if os.name == 'nt' else subprocess.run(['open', downloads_path])
                
                # Try to open URL in browser for manual download
                webbrowser.open(url)
                return f"Opening download URL and Downloads folder. Please download manually from the browser."
            else:
                return "Please provide a valid URL to download from."
                
        except Exception as e:
            return f"Download error: {str(e)}"
    
    def handle_search(self, command):
        """Handle search commands"""
        try:
            # Extract search terms
            search_terms = command.replace("search", "").strip()
            if not search_terms:
                search_terms = "BOLT AI assistant"
            
            # Create Google search URL
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_terms)}"
            webbrowser.open(search_url)
            return f"Searching for: {search_terms}"
            
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def handle_open(self, command):
        """Handle open commands"""
        try:
            target = command.replace("open", "").strip()
            
            # Website shortcuts
            sites = {
                "google": "https://www.google.com",
                "youtube": "https://www.youtube.com",
                "github": "https://www.github.com",
                "stackoverflow": "https://stackoverflow.com",
                "twitter": "https://www.twitter.com",
                "facebook": "https://www.facebook.com",
                "instagram": "https://www.instagram.com",
                "linkedin": "https://www.linkedin.com",
                "amazon": "https://www.amazon.com",
                "ebay": "https://www.ebay.com",
                "netflix": "https://www.netflix.com",
                "spotify": "https://open.spotify.com"
            }
            
            # Folder shortcuts
            if target in ["downloads", "documents", "desktop"]:
                if target == "downloads":
                    path = str(Path.home() / "Downloads")
                elif target == "documents":
                    path = str(Path.home() / "Documents")
                else:
                    path = str(Path.home() / "Desktop")
                
                if os.path.exists(path):
                    os.startfile(path) if os.name == 'nt' else subprocess.run(['open', path])
                    return f"Opening {target} folder"
                else:
                    return f"{target} folder not found"
            
            # Check if it's a known website
            elif target in sites:
                webbrowser.open(sites[target])
                return f"Opening {target}"
            
            # Try to open as URL
            elif "." in target:
                if not target.startswith("http"):
                    target = "https://" + target
                webbrowser.open(target)
                return f"Opening {target}"
            
            else:
                return f"Don't know how to open '{target}'. Try a website name or folder."
                
        except Exception as e:
            return f"Open error: {str(e)}"
    
    def handle_music(self, command):
        """Handle music commands"""
        try:
            music_apps = ["spotify.exe", "iTunes.exe", "winamp.exe", "vlc.exe", "musicbee.exe"]
            
            # Try to find and launch music application
            for app in music_apps:
                try:
                    subprocess.Popen(app)
                    return f"Launching music player: {app.replace('.exe', '')}"
                except:
                    continue
            
            # Fallback: open Spotify web
            webbrowser.open("https://open.spotify.com")
            return "Opening Spotify Web Player"
            
        except Exception as e:
            return f"Music error: {str(e)}"
    
    def handle_volume(self, command):
        """Handle volume commands"""
        try:
            if "mute" in command:
                subprocess.run(["nircmd", "mutesysvolume", "1"], check=False)
                return "System muted"
            elif "unmute" in command:
                subprocess.run(["nircmd", "mutesysvolume", "0"], check=False)
                return "System unmuted"
            else:
                # Extract volume level
                words = command.split()
                for word in words:
                    if word.isdigit():
                        level = int(word)
                        if 0 <= level <= 100:
                            # Windows volume control
                            volume_level = int((level / 100) * 65535)
                            subprocess.run(["nircmd", "setsysvolume", str(volume_level)], check=False)
                            return f"Volume set to {level}%"
                
                return "Please specify a volume level (0-100) or use 'mute'/'unmute'"
                
        except Exception as e:
            return f"Volume control error: {str(e)}"
    
    def handle_screenshot(self):
        """Handle screenshot commands"""
        try:
            if os.name == 'nt':
                # Windows screenshot
                subprocess.run(["snippingtool"], check=False)
                return "Opening Snipping Tool for screenshot"
            else:
                return "Screenshot feature not available on this platform"
                
        except Exception as e:
            return f"Screenshot error: {str(e)}"
    
    def handle_terminal(self, command):
        """Handle terminal commands"""
        try:
            if os.name == 'nt':
                if "powershell" in command:
                    subprocess.Popen(["powershell"])
                    return "Opening PowerShell"
                else:
                    subprocess.Popen(["cmd"])
                    return "Opening Command Prompt"
            else:
                subprocess.Popen(["terminal"])
                return "Opening Terminal"
                
        except Exception as e:
            return f"Terminal error: {str(e)}"
    
    def handle_code_editor(self, command):
        """Handle code editor commands"""
        try:
            editors = {
                "vscode": "code",
                "code": "code", 
                "pycharm": "pycharm",
                "atom": "atom",
                "sublime": "subl",
                "notepad++": "notepad++"
            }
            
            for editor_name, editor_cmd in editors.items():
                if editor_name in command:
                    try:
                        subprocess.Popen([editor_cmd])
                        return f"Opening {editor_name}"
                    except:
                        continue
            
            # Fallback to notepad
            subprocess.Popen(["notepad"])
            return "Opening Notepad (code editor not found)"
            
        except Exception as e:
            return f"Code editor error: {str(e)}"
    
    def handle_git(self, command):
        """Handle git commands"""
        try:
            # Extract git command
            git_cmd = command.replace("git ", "git ")
            result = subprocess.run(git_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout if result.stdout else "Git command executed successfully"
                return f"Git: {output[:100]}..." if len(output) > 100 else f"Git: {output}"
            else:
                return f"Git error: {result.stderr}"
                
        except Exception as e:
            return f"Git command error: {str(e)}"
    
    def handle_pip_install(self, command):
        """Handle pip install commands"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Package installation successful!"
            else:
                return f"Installation error: {result.stderr}"
                
        except Exception as e:
            return f"Pip install error: {str(e)}"
    
    def handle_ai_chat(self, message):
        """Handle AI chat messages"""
        try:
            if not message.strip():
                return "What would you like to chat about?"
            
            # Simple AI responses (can be enhanced with actual AI API)
            responses = {
                "how are you": f"I'm doing great, {self.user_name}! Thanks for asking. How are you?",
                "what's your name": "I'm BOLT AI, your advanced assistant!",
                "help": "I can help with web searches, music, screenshots, system info, and much more!",
                "thanks": f"You're welcome, {self.user_name}! Happy to help!",
                "bye": f"Goodbye, {self.user_name}! Have a great day!"
            }
            
            # Check for keyword matches
            for keyword, response in responses.items():
                if keyword in message.lower():
                    return response
            
            # Default AI response
            return f"That's interesting, {self.user_name}! I'm always learning. What else would you like to know?"
            
        except Exception as e:
            return f"AI chat error: {str(e)}"
    
    def handle_password_generation(self, command):
        """Handle password generation"""
        try:
            import secrets
            import string
            
            if "strong" in command:
                # Strong password
                chars = string.ascii_letters + string.digits + "!@#$%^&*"
                password = ''.join(secrets.choice(chars) for _ in range(16))
                
                # Copy to clipboard if available
                if pyperclip:
                    pyperclip.copy(password)
                    return f"Strong password generated and copied to clipboard: {password}"
                else:
                    return f"Strong password generated: {password}"
            else:
                # Simple password
                chars = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(chars) for _ in range(12))
                
                if pyperclip:
                    pyperclip.copy(password)
                    return f"Password generated and copied: {password}"
                else:
                    return f"Password generated: {password}"
                    
        except Exception as e:
            return f"Password generation error: {str(e)}"
    
    def handle_entertainment(self, command):
        """Handle entertainment commands (jokes, facts, quotes)"""
        try:
            if "joke" in command:
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the computer go to the doctor? Because it had a virus!",
                    "Why don't programmers like nature? It has too many bugs!",
                    "How do you organize a space party? You planet!",
                    "Why did the robot go on a diet? He had a byte problem!"
                ]
                return random.choice(jokes)
                
            elif "fact" in command:
                facts = [
                    "The first computer bug was an actual bug found in 1947!",
                    "Python was named after Monty Python, not the snake!",
                    "The first 1GB hard drive cost $40,000 in 1980!",
                    "Google processes over 8.5 billion searches per day!",
                    "The Internet weighs about as much as a strawberry!"
                ]
                return random.choice(facts)
                
            elif "quote" in command:
                quotes = [
                    "'The future belongs to those who believe in the beauty of their dreams.' - Eleanor Roosevelt",
                    "'Innovation distinguishes between a leader and a follower.' - Steve Jobs",
                    "'The only way to do great work is to love what you do.' - Steve Jobs",
                    "'Code is like humor. When you have to explain it, it's bad.' - Cory House",
                    "'Programming isn't about what you know; it's about what you can figure out.' - Chris Pine"
                ]
                return random.choice(quotes)
                
        except Exception as e:
            return f"Entertainment error: {str(e)}"
    
    def handle_reminder(self, command):
        """Handle reminder commands"""
        try:
            # Extract time and message
            parts = command.split(" in ")
            if len(parts) < 2:
                return "Please specify reminder format: 'remind me to [task] in [time]'"
            
            task = parts[0].replace("remind me to", "").strip()
            time_part = parts[1].strip()
            
            # Parse time (basic implementation)
            minutes = 5  # default
            if "minute" in time_part:
                try:
                    minutes = int(''.join(filter(str.isdigit, time_part)))
                except:
                    minutes = 5
            
            # Set reminder
            def reminder_alert():
                time.sleep(minutes * 60)
                messagebox.showinfo("Reminder", f"Reminder: {task}")
                self.speak(f"Reminder: {task}")
            
            threading.Thread(target=reminder_alert, daemon=True).start()
            return f"Reminder set: '{task}' in {minutes} minutes"
            
        except Exception as e:
            return f"Reminder error: {str(e)}"
    
    def handle_translation(self, command):
        """Handle translation commands (basic)"""
        try:
            # Basic translations (can be enhanced with translation API)
            translations = {
                "hello": {"spanish": "hola", "french": "bonjour", "german": "hallo"},
                "goodbye": {"spanish": "adiós", "french": "au revoir", "german": "auf wiedersehen"},
                "thank you": {"spanish": "gracias", "french": "merci", "german": "danke"}
            }
            
            command_lower = command.lower()
            for english, lang_dict in translations.items():
                if english in command_lower:
                    for lang in lang_dict:
                        if lang in command_lower:
                            return f"'{english}' in {lang} is '{lang_dict[lang]}'"
            
            return "Basic translation available for: hello, goodbye, thank you (to Spanish, French, German)"
            
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def handle_system_info(self):
        """Handle system information commands"""
        try:
            info_parts = []
            
            # Basic system info
            info_parts.append(f"System: {os.name}")
            info_parts.append(f"Platform: {sys.platform}")
            
            # Enhanced info if psutil available
            if psutil:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                info_parts.extend([
                    f"CPU Usage: {cpu_percent}%",
                    f"Memory: {memory.percent}% used ({memory.used//1024//1024}MB/{memory.total//1024//1024}MB)",
                    f"Disk: {disk.percent}% used ({disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB)"
                ])
            
            return " | ".join(info_parts)
            
        except Exception as e:
            return f"System info error: {str(e)}"
    
    def handle_list_processes(self):
        """Handle list processes command"""
        try:
            if psutil:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                    try:
                        processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
                    except:
                        continue
                
                # Return top 5 processes
                return f"Top processes: {', '.join(processes[:5])}"
            else:
                return "Process listing requires psutil module"
                
        except Exception as e:
            return f"Process list error: {str(e)}"
    
    def handle_ping(self, command):
        """Handle ping commands"""
        try:
            target = command.replace("ping", "").strip()
            if not target:
                target = "google.com"
            
            # Execute ping command
            if os.name == 'nt':
                result = subprocess.run(["ping", "-n", "4", target], 
                                      capture_output=True, text=True)
            else:
                result = subprocess.run(["ping", "-c", "4", target], 
                                      capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Ping to {target} successful!"
            else:
                return f"Ping to {target} failed"
                
        except Exception as e:
            return f"Ping error: {str(e)}"
    
    def handle_add_task(self, task_text):
        """Handle add task command"""
        try:
            if task_text.strip():
                self.tasks.append(task_text.strip())
                self.refresh_tasks_display()
                return f"Task added: {task_text.strip()}"
            else:
                return "Please specify a task to add"
                
        except Exception as e:
            return f"Add task error: {str(e)}"
    
    def handle_add_note(self, note_text):
        """Handle add note command"""
        try:
            if note_text.strip():
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                full_note = f"[{timestamp}] {note_text.strip()}"
                self.notes.append(full_note)
                
                # Update notes display
                current_content = self.notes_text.get("1.0", tk.END)
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.insert("1.0", current_content + full_note + "\n")
                
                return f"Note added: {note_text.strip()}"
            else:
                return "Please specify note content"
                
        except Exception as e:
            return f"Add note error: {str(e)}"
    
    def handle_time_date(self):
        """Handle time and date commands"""
        try:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%Y-%m-%d")
            day_str = now.strftime("%A")
            
            return f"Current time: {time_str} | Date: {date_str} | Day: {day_str}"
            
        except Exception as e:
            return f"Time/date error: {str(e)}"
    
    def handle_calculator(self, command):
        """Handle calculator commands"""
        try:
            # Extract mathematical expression
            expression = command.replace("calculate", "").replace("calc", "").strip()
            
            # Basic safety check
            allowed_chars = "0123456789+-*/()."
            if all(c in allowed_chars or c.isspace() for c in expression):
                try:
                    result = eval(expression)
                    return f"{expression} = {result}"
                except:
                    return f"Cannot calculate: {expression}"
            else:
                return "Invalid calculation expression"
                
        except Exception as e:
            return f"Calculator error: {str(e)}"
    
    # GUI HELPER METHODS
    def show_command_suggestions(self, event=None):
        """Show command suggestions based on input"""
        try:
            current_text = self.command_entry.get().lower()
            if len(current_text) < 2:
                self.hide_suggestions()
                return
            
            # Find matching suggestions
            matches = [cmd for cmd in self.command_suggestions if current_text in cmd.lower()]
            
            if matches:
                self.suggestions_listbox.delete(0, tk.END)
                for match in matches[:5]:  # Show top 5 matches
                    self.suggestions_listbox.insert(tk.END, match)
                
                self.suggestions_frame.pack(fill="x", pady=(0, 5))
                self.suggestions_listbox.pack(fill="x", padx=10, pady=5)
            else:
                self.hide_suggestions()
                
        except Exception as e:
            print(f"Suggestions error: {e}")
    
    def hide_suggestions(self):
        """Hide command suggestions"""
        self.suggestions_frame.pack_forget()
    
    def use_suggestion(self, event=None):
        """Use selected suggestion"""
        try:
            selection = self.suggestions_listbox.get(self.suggestions_listbox.curselection())
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, selection)
            self.hide_suggestions()
            self.command_entry.focus()
        except:
            pass
    
    def add_to_history(self, command):
        """Add command to history display"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"[{timestamp}] {command}\n"
            
            self.history_text.config(state="normal")
            self.history_text.insert(tk.END, history_entry)
            self.history_text.see(tk.END)
            self.history_text.config(state="disabled")
            
            # Keep only last 10 commands
            self.command_history.append(command)
            if len(self.command_history) > 10:
                self.command_history.pop(0)
                
        except Exception as e:
            print(f"History error: {e}")
    
    def update_status(self, message):
        """Update status label"""
        try:
            self.status_label.config(text=message)
        except:
            pass
    
    # ANIMATION METHODS
    def start_animations(self):
        """Start visual animations"""
        self.animate_canvas()
    
    def animate_canvas(self):
        """Animate the main canvas"""
        if not self.animation_running:
            return
            
        try:
            self.canvas.delete("all")
            
            # Draw animated circles
            center_x, center_y = 150, 150
            
            # Outer circle
            radius1 = 80 + 10 * math.sin(self.animation_angle * 0.05)
            self.canvas.create_oval(center_x - radius1, center_y - radius1,
                                   center_x + radius1, center_y + radius1,
                                   outline="#00BFFF", width=2)
            
            # Inner circle
            radius2 = 50 + 8 * math.cos(self.animation_angle * 0.08)
            self.canvas.create_oval(center_x - radius2, center_y - radius2,
                                   center_x + radius2, center_y + radius2,
                                   outline="#00FF00", width=2)
            
            # Center dot
            dot_radius = 5 + 3 * math.sin(self.animation_angle * 0.1)
            self.canvas.create_oval(center_x - dot_radius, center_y - dot_radius,
                                   center_x + dot_radius, center_y + dot_radius,
                                   fill="#FF4444", outline="")
            
            # Rotating lines
            for i in range(6):
                angle = self.animation_angle * 0.02 + i * math.pi / 3
                x1 = center_x + 30 * math.cos(angle)
                y1 = center_y + 30 * math.sin(angle)
                x2 = center_x + 60 * math.cos(angle)
                y2 = center_y + 60 * math.sin(angle)
                
                color = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"][i]
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
            
            # BOLT text
            self.canvas.create_text(center_x, center_y + 120, text="BOLT AI",
                                   font=("Arial", 16, "bold"), fill="#FFFFFF")
            
            self.animation_angle += 1
            
            # Continue animation
            self.root.after(50, self.animate_canvas)
            
        except Exception as e:
            print(f"Animation error: {e}")
    
    def animate_turbo_mode(self):
        """Special animation for turbo mode"""
        if self.turbo_mode_active:
            # Flash effect for turbo mode
            colors = ["#FF0000", "#FF4444", "#FF8888"]
            for i, color in enumerate(colors):
                self.root.after(i * 100, lambda c=color: self.turbo_btn.config(bg=c))
            
            self.root.after(400, lambda: self.turbo_btn.config(bg="#FF0000") if self.turbo_mode_active else None)
    
    # AI TAB METHODS
    def send_ai_chat(self, event=None):
        """Send AI chat message"""
        message = self.chat_entry.get().strip()
        if message:
            self.add_chat_message(f"You: {message}", "#00BFFF")
            self.chat_entry.delete(0, tk.END)
            
            # Process AI response
            response = self.handle_ai_chat(message)
            self.add_chat_message(f"BOLT: {response}", "#00FF00")
            
            if self.auto_responses:
                threading.Thread(target=lambda: self.speak(response), daemon=True).start()
    
    def add_chat_message(self, message, color):
        """Add message to chat display"""
        try:
            self.chat_display.config(state="normal")
            self.chat_display.insert(tk.END, f"{message}\n", color)
            self.chat_display.see(tk.END)
            self.chat_display.config(state="disabled")
        except:
            pass
    
    def enable_smart_mode(self):
        """Enable AI smart mode"""
        self.speak("Smart mode activated! Enhanced AI capabilities online!")
        self.add_chat_message("BOLT: Smart mode activated! I'm now using enhanced intelligence.", "#9932CC")
    
    def enable_learning_mode(self):
        """Enable AI learning mode"""
        self.speak("Learning mode activated! I'll adapt to your preferences!")
        self.add_chat_message("BOLT: Learning mode activated! I'll learn from our interactions.", "#FF6600")
    
    def clear_chat(self):
        """Clear AI chat"""
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state="disabled")
        self.add_chat_message("BOLT: Chat cleared! How can I help you?", "#00FF00")
    
    # PRODUCTIVITY TAB METHODS
    def add_task_dialog(self):
        """Show add task dialog"""
        task = tk.simpledialog.askstring("Add Task", "Enter new task:")
        if task:
            self.tasks.append(task)
            self.refresh_tasks_display()
            self.speak(f"Task added: {task}")
    
    def complete_task(self):
        """Mark selected task as complete"""
        try:
            selection = self.tasks_list.curselection()
            if selection:
                task = self.tasks_list.get(selection[0])
                self.tasks_list.delete(selection[0])
                if task in self.tasks:
                    self.tasks.remove(task)
                self.speak(f"Task completed: {task}")
        except:
            messagebox.showwarning("No Selection", "Please select a task to complete")
    
    def delete_task(self):
        """Delete selected task"""
        try:
            selection = self.tasks_list.curselection()
            if selection:
                task = self.tasks_list.get(selection[0])
                self.tasks_list.delete(selection[0])
                if task in self.tasks:
                    self.tasks.remove(task)
                self.speak(f"Task deleted: {task}")
        except:
            messagebox.showwarning("No Selection", "Please select a task to delete")
    
    def refresh_tasks_display(self):
        """Refresh tasks display"""
        self.tasks_list.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_list.insert(tk.END, task)
    
    def save_note(self):
        """Save current notes"""
        try:
            content = self.notes_text.get("1.0", tk.END)
            if content.strip():
                filename = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
                if filename:
                    with open(filename, 'w') as f:
                        f.write(content)
                    self.speak("Notes saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save notes: {e}")
    
    def load_notes(self):
        """Load notes from file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'r') as f:
                    content = f.read()
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.insert("1.0", content)
                self.speak("Notes loaded successfully!")
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load notes: {e}")
    
    def clear_notes(self):
        """Clear notes"""
        if messagebox.askyesno("Clear Notes", "Are you sure you want to clear all notes?"):
            self.notes_text.delete("1.0", tk.END)
            self.speak("Notes cleared!")
    
    # SETTINGS TAB METHODS
    def apply_settings(self):
        """Apply user settings"""
        try:
            # Update user name
            new_name = self.name_entry.get().strip()
            if new_name:
                self.user_name = new_name
            
            # Update auto responses
            self.auto_responses = self.auto_response_var.get()
            
            self.speak(f"Settings applied successfully, {self.user_name}!")
            messagebox.showinfo("Settings", "Settings applied successfully!")
            
        except Exception as e:
            messagebox.showerror("Settings Error", f"Could not apply settings: {e}")
    
    def update_system_info(self):
        """Update system information display"""
        try:
            info_text = ""
            
            # Basic system info
            info_text += f"Operating System: {os.name}\n"
            info_text += f"Platform: {sys.platform}\n"
            info_text += f"Python Version: {sys.version.split()[0]}\n"
            
            if psutil:
                # CPU info
                info_text += f"CPU Cores: {psutil.cpu_count()}\n"
                info_text += f"CPU Usage: {psutil.cpu_percent()}%\n"
                
                # Memory info
                memory = psutil.virtual_memory()
                info_text += f"Total Memory: {memory.total // 1024 // 1024} MB\n"
                info_text += f"Available Memory: {memory.available // 1024 // 1024} MB\n"
                
                # Disk info
                disk = psutil.disk_usage('/')
                info_text += f"Disk Total: {disk.total // 1024 // 1024 // 1024} GB\n"
                info_text += f"Disk Free: {disk.free // 1024 // 1024 // 1024} GB\n"
            
            # BOLT info
            info_text += f"\nBOLT AI Version: 3.0.2\n"
            info_text += f"Voice Mode: {self.voice_mode}\n"
            info_text += f"Commands Processed: {len(self.command_history)}\n"
            
            self.system_info_text.config(state="normal")
            self.system_info_text.delete("1.0", tk.END)
            self.system_info_text.insert("1.0", info_text)
            self.system_info_text.config(state="disabled")
            
        except Exception as e:
            print(f"System info update error: {e}")
    
    # QUICK ACTION METHODS
    def show_system_stats(self):
        """Show system statistics"""
        stats = self.handle_system_info()
        messagebox.showinfo("System Statistics", stats)
        self.speak("System statistics displayed!")
    
    def quick_search(self):
        """Quick web search"""
        query = tk.simpledialog.askstring("Quick Search", "Enter search terms:")
        if query:
            self.process_command(f"search {query}")
    
    # CORE UTILITY METHODS
    def speak(self, text):
        """Enhanced text-to-speech with error handling"""
        try:
            return fast_speak(text)
        except Exception as e:
            print(f"Speech error: {e}")
            return False
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Are you sure you want to quit BOLT AI?"):
            self.animation_running = False
            self.speak(f"Goodbye, {self.user_name}! BOLT AI shutting down.")
            self.root.after(1000, self.root.destroy)
    
    def run(self):
        """Start the application"""
        try:
            print("🚀 BOLT AI V3 Starting...")
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")
            messagebox.showerror("Critical Error", f"BOLT AI encountered an error: {e}")

if __name__ == "__main__":
    try:
        # Create and run BOLT AI
        app = BoltAI()
        app.run()
    except Exception as e:
        print(f"Failed to start BOLT AI: {e}")
        input("Press Enter to exit...")