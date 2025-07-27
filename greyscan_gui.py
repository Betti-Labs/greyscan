#!/usr/bin/env python3
"""
GreyScan GUI - Adaptive Intelligence Interface
Real-time learning scraper with visual feedback
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import asyncio
import threading
from datetime import datetime
import json
from greyscan_core import GreyScanEngine

class GreyScanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 GreyScan - Adaptive Intelligence Scraper")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Engine instance
        self.engine = None
        self.is_running = False
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Setup modern dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#1a1a1a', 
                       foreground='#00ff88',
                       font=('Arial', 16, 'bold'))
        
        style.configure('Header.TLabel',
                       background='#1a1a1a',
                       foreground='#ffffff',
                       font=('Arial', 12, 'bold'))
        
        style.configure('Modern.TButton',
                       background='#00ff88',
                       foreground='#000000',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Stop.TButton',
                       background='#ff4444',
                       foreground='#ffffff',
                       font=('Arial', 10, 'bold'))
        
    def create_widgets(self):
        """Create the main GUI layout"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, 
                               text="🧠 GreyScan Adaptive Intelligence", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                  text="Self-Learning Web Scraper with Pattern Recognition",
                                  style='Header.TLabel')
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Input forms
        left_frame = tk.Frame(main_frame, bg='#2a2a2a', relief='raised', bd=2)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        self.create_input_panel(left_frame)
        
        # Right panel - Results and logs
        right_frame = tk.Frame(main_frame, bg='#2a2a2a', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.create_results_panel(right_frame)
        
    def create_input_panel(self, parent):
        """Create the input forms panel"""
        
        # Panel title
        input_title = ttk.Label(parent, text="🎯 Target Configuration", style='Header.TLabel')
        input_title.pack(pady=10)
        
        # Target input section
        target_frame = tk.Frame(parent, bg='#2a2a2a')
        target_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(target_frame, text="Target Name:", 
                bg='#2a2a2a', fg='#ffffff', font=('Arial', 10)).pack(anchor='w')
        
        self.target_entry = tk.Entry(target_frame, width=30, font=('Arial', 10))
        self.target_entry.pack(fill='x', pady=2)
        self.target_entry.insert(0, "bitcoin")
        
        # Platform selection
        tk.Label(target_frame, text="Platform:", 
                bg='#2a2a2a', fg='#ffffff', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
        
        self.platform_var = tk.StringVar(value="coingecko")
        platform_combo = ttk.Combobox(target_frame, textvariable=self.platform_var,
                                     values=["coingecko", "coinmarketcap", "defillama", 
                                            "etherscan", "dexscreener", "twitter", "custom"])
        platform_combo.pack(fill='x', pady=2)
        
        # Custom URL section
        tk.Label(target_frame, text="Custom URL (optional):", 
                bg='#2a2a2a', fg='#ffffff', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
        
        self.url_entry = tk.Entry(target_frame, width=30, font=('Arial', 9))
        self.url_entry.pack(fill='x', pady=2)
        self.url_entry.insert(0, "https://api.example.com/{target}")
        
        # Target symbols
        tk.Label(target_frame, text="Target Symbols (comma-separated):", 
                bg='#2a2a2a', fg='#ffffff', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
        
        self.symbols_entry = tk.Entry(target_frame, width=30, font=('Arial', 9))
        self.symbols_entry.pack(fill='x', pady=2)
        self.symbols_entry.insert(0, "price,volume,market,data,api,json")
        
        # Batch targets section
        tk.Label(target_frame, text="Batch Targets (one per line):", 
                bg='#2a2a2a', fg='#ffffff', font=('Arial', 10)).pack(anchor='w', pady=(15,0))
        
        self.batch_text = scrolledtext.ScrolledText(target_frame, height=8, width=35, 
                                                   font=('Arial', 9))
        self.batch_text.pack(fill='x', pady=2)
        self.batch_text.insert('1.0', 
            "bitcoin,coingecko\nethereum,coingecko\nBTC,coinmarketcap\nETH,coinmarketcap\nuniswap,defillama")
        
        # Control buttons
        button_frame = tk.Frame(parent, bg='#2a2a2a')
        button_frame.pack(fill='x', padx=10, pady=15)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Learning", 
                                      style='Modern.TButton',
                                      command=self.start_scraping)
        self.start_button.pack(fill='x', pady=2)
        
        self.stop_button = ttk.Button(button_frame, text="⏹ Stop", 
                                     style='Stop.TButton',
                                     command=self.stop_scraping,
                                     state='disabled')
        self.stop_button.pack(fill='x', pady=2)
        
        self.clear_button = ttk.Button(button_frame, text="🗑 Clear Results",
                                      command=self.clear_results)
        self.clear_button.pack(fill='x', pady=2)
        
    def create_results_panel(self, parent):
        """Create the results and logging panel"""
        
        # Results title
        results_title = ttk.Label(parent, text="📊 Learning Results & Live Log", style='Header.TLabel')
        results_title.pack(pady=10)
        
        # Stats frame
        stats_frame = tk.Frame(parent, bg='#2a2a2a')
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.stats_label = tk.Label(stats_frame, 
                                   text="Ready to start adaptive learning...",
                                   bg='#2a2a2a', fg='#00ff88', 
                                   font=('Arial', 10, 'bold'))
        self.stats_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(stats_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
        # Results notebook
        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Live log tab
        log_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(log_frame, text="🔥 Live Learning Log")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 bg='#000000', fg='#00ff00',
                                                 font=('Consolas', 9),
                                                 wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Results tab
        results_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(results_frame, text="✅ Success Results")
        
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     bg='#001100', fg='#00ff88',
                                                     font=('Consolas', 9),
                                                     wrap='word')
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Learning stats tab
        learning_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(learning_frame, text="🧠 Learning Stats")
        
        self.learning_text = scrolledtext.ScrolledText(learning_frame,
                                                      bg='#000011', fg='#88aaff',
                                                      font=('Consolas', 9),
                                                      wrap='word')
        self.learning_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def log_message(self, message, log_type="log"):
        """Add message to appropriate log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        if log_type == "log":
            self.log_text.insert('end', formatted_msg)
            self.log_text.see('end')
        elif log_type == "result":
            self.results_text.insert('end', formatted_msg)
            self.results_text.see('end')
        elif log_type == "learning":
            self.learning_text.insert('end', formatted_msg)
            self.learning_text.see('end')
            
        self.root.update_idletasks()
        
    def update_stats(self, stats_text):
        """Update the stats display"""
        self.stats_label.config(text=stats_text)
        
    def start_scraping(self):
        """Start the adaptive scraping process"""
        if self.is_running:
            return
            
        # Validate inputs
        if not self.target_entry.get().strip() and not self.batch_text.get('1.0', 'end').strip():
            messagebox.showerror("Error", "Please enter at least one target!")
            return
            
        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress.start()
        
        # Clear previous results
        self.log_text.delete('1.0', 'end')
        self.results_text.delete('1.0', 'end')
        self.learning_text.delete('1.0', 'end')
        
        # Start scraping in separate thread
        thread = threading.Thread(target=self.run_scraping_thread)
        thread.daemon = True
        thread.start()
        
    def stop_scraping(self):
        """Stop the scraping process"""
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress.stop()
        self.update_stats("Stopped by user")
        self.log_message("🛑 Scraping stopped by user", "log")
        
    def clear_results(self):
        """Clear all results"""
        self.log_text.delete('1.0', 'end')
        self.results_text.delete('1.0', 'end')
        self.learning_text.delete('1.0', 'end')
        self.update_stats("Results cleared - Ready to start")
        
    def run_scraping_thread(self):
        """Run the scraping in a separate thread"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the async scraping
            loop.run_until_complete(self.run_adaptive_scraping())
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}", "log")
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.start_button.config(state='normal'))
            self.root.after(0, lambda: self.stop_button.config(state='disabled'))
            self.root.after(0, lambda: self.progress.stop())
            
    async def run_adaptive_scraping(self):
        """Run the adaptive scraping process"""
        try:
            # Initialize engine
            symbols = [s.strip() for s in self.symbols_entry.get().split(',') if s.strip()]
            self.engine = GreyScanEngine(target_symbols=symbols)
            
            self.log_message("🧠 Initializing GreyScan Adaptive Engine...", "log")
            self.root.after(0, lambda: self.update_stats("Initializing adaptive engine..."))
            
            # Prepare targets
            targets = []
            
            # Single target
            if self.target_entry.get().strip():
                target_name = self.target_entry.get().strip()
                platform = self.platform_var.get()
                targets.append((target_name, platform))
                
            # Batch targets
            batch_text = self.batch_text.get('1.0', 'end').strip()
            if batch_text:
                for line in batch_text.split('\n'):
                    line = line.strip()
                    if line and ',' in line:
                        parts = line.split(',', 1)
                        if len(parts) == 2:
                            targets.append((parts[0].strip(), parts[1].strip()))
            
            if not targets:
                self.log_message("❌ No valid targets found!", "log")
                return
                
            self.log_message(f"🎯 Starting adaptive collection for {len(targets)} targets", "log")
            self.root.after(0, lambda: self.update_stats(f"Processing {len(targets)} targets..."))
            
            # Custom progress tracking
            successful = 0
            total = len(targets)
            
            for i, (target_name, platform) in enumerate(targets):
                if not self.is_running:
                    break
                    
                self.log_message(f"🚀 [{i+1}/{total}] Attacking {platform.upper()}: {target_name}", "log")
                
                try:
                    # Run single target
                    result = await self.engine.adaptive_collect([(target_name, platform)])
                    
                    if result:
                        successful += 1
                        result_data = result[0]
                        
                        # Log success
                        success_msg = f"✅ SUCCESS: {target_name} on {platform}"
                        self.log_message(success_msg, "log")
                        
                        # Detailed result
                        detail_msg = f"""
🎉 Target: {result_data['target']} on {result_data['platform']}
📊 Data Size: {result_data['data_size']} bytes
🔗 URL: {result_data['url']}
🧠 Method: {result_data['method']}
📝 Sample: {result_data['content'][:200]}...
"""
                        self.log_message(detail_msg, "result")
                        
                    else:
                        self.log_message(f"❌ FAILED: {target_name} on {platform}", "log")
                        
                except Exception as e:
                    self.log_message(f"❌ ERROR: {target_name} - {str(e)}", "log")
                
                # Update progress
                progress_text = f"Progress: {i+1}/{total} | Success: {successful}/{i+1} ({successful/(i+1)*100:.1f}%)"
                self.root.after(0, lambda pt=progress_text: self.update_stats(pt))
            
            # Final results
            if self.is_running:
                success_rate = successful / total * 100
                final_stats = f"🎉 COMPLETED: {successful}/{total} successful ({success_rate:.1f}%)"
                self.root.after(0, lambda: self.update_stats(final_stats))
                self.log_message(final_stats, "log")
                
                # Learning statistics
                if hasattr(self.engine, 'learned_patterns'):
                    learning_stats = f"""
🧠 LEARNING STATISTICS:
📚 Successful patterns learned: {len(self.engine.learned_patterns)}
❌ Failed patterns recorded: {len(getattr(self.engine, 'failed_patterns', []))}
🎯 Total attempts made: {len(getattr(self.engine, 'all_attempts', []))}

✅ SUCCESSFUL PATTERNS:
"""
                    for platform, patterns in self.engine.learned_patterns.items():
                        learning_stats += f"\n{platform}:\n"
                        for pattern in patterns:
                            learning_stats += f"  - {pattern}\n"
                    
                    self.log_message(learning_stats, "learning")
                
        except Exception as e:
            self.log_message(f"❌ Critical Error: {str(e)}", "log")
        finally:
            if self.engine:
                await self.engine.close()

def main():
    """Launch the GreyScan GUI"""
    root = tk.Tk()
    app = GreyScanGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 GUI closed by user")

if __name__ == "__main__":
    main()