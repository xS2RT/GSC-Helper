import random
import re
import sys
import threading
import webbrowser
import tkinter as tk
import os
import pygments.lexers
import customtkinter

from tkinter import filedialog
from CTkToolTip import *
from chlorophyll import CodeView
from CTkColorPicker import *
from CTkMessagebox import CTkMessagebox
from pathlib import Path
from PIL import Image
from CTkScrollableDropdown import CTkScrollableDropdown

custom_button = {
    "bg_color": "transparent",
    "fg_color": "#a52a2a",
    "text_color": "#ffffff",
    "hover_color": "#8d0d26",
    "text_color_disabled": "#a8a8a8",
    "corner_radius": 2
}


def rgb_to_gsc(r, g, b):
    return round(r / 255, 3), round(g / 255, 3), round(b / 255, 3)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class ShowImageWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Menu Base View")
        window_width = 900
        window_height = 550

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        self.iconbitmap(resource_path("images/logo.ico"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.Menu_Image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "MenuImage.png")),
                                                 size=(833, 521))

        self.home_frame_large_image_label = customtkinter.CTkLabel(self, text="",
                                                                   image=self.Menu_Image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")


class ChangeControlText(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("GSC Code viewer")
        window_width = 1000
        window_height = 550

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        self.iconbitmap(resource_path("images/logo.ico"))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label_title = customtkinter.CTkLabel(self, text="Control Text: ", font=("Roboto", 16))
        self.label_title.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self, corner_radius=0, font=("Roboto", 16))

        self.textbox.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        self.SaveBtn = customtkinter.CTkButton(self, text="Save Changes", command=self.SaveChanges, font=("Roboto", 14),
                                               fg_color="#1e7e34",
                                               hover_color="#155724")
        self.SaveBtn.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        self.CopyBtn = customtkinter.CTkButton(self, text="Copy", command=self.button_event, font=("Roboto", 14))
        self.CopyBtn.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        self.load_gsc_code()

    def SaveChanges(self):
        content = self.textbox.get("1.0", "end-1c").replace("\n", "\\n")
        try:
            with open("MenuMaker/main.gsc", 'r+') as file:
                lines = file.readlines()
                file.seek(0)

                for line in lines:
                    if 'self.txt =' in line:
                        new_line = f'\tself.txt = "{content}";\n'
                        file.write(new_line)
                    else:
                        file.write(line)

                file.truncate()
                CTkMessagebox(message="Control text updated successfully!",
                              icon="check", option_1="OK")
        except FileNotFoundError:
            msg = CTkMessagebox(title="Error", message=f"File 'MenuMaker/main.gsc' not found.", icon="cancel")
            if msg.get() == "OK":
                self.destroy()

    def button_event(self):
        content = self.textbox.get("1.0", "end-1c")  # Get all content from the textbox
        self.clipboard_clear()  # Clear the current clipboard
        self.clipboard_append(content)  # Append the content to the clipboard
        self.update()  # Update the window to ensure clipboard is populated
        CTkMessagebox(message="copied to clipboard!",
                      icon="check", option_1="OK")

    def load_gsc_code(self):
        try:
            with open("MenuMaker/main.gsc", 'r') as file:
                for line in file:
                    if 'self.txt =' in line:
                        match = re.search(r'"(.*?)"', line)
                        if match:
                            Control = match.group(1).replace("\\n", "\n")
            self.insert_code(Control)
        except FileNotFoundError:
            msg = CTkMessagebox(title="Error", message=f"File 'MenuMaker/main.gsc' not found.", icon="cancel")
            if msg.get() == "OK":
                self.destroy()

    def insert_code(self, code):
        self.textbox.insert("0.0", code)


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = item
        self.title("GSC Code viewer")
        window_width = 1000
        window_height = 550

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        self.iconbitmap(resource_path("images/logo.ico"))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.label_title = customtkinter.CTkLabel(self, text=self.item, font=("Roboto", 14))
        self.label_title.grid(row=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        self.textbox = CodeView(
            self,
            lexer=pygments.lexers.ObjectiveCLexer,
            color_scheme="monokai",
            font=("Consolas", 12)
        )

        self.textbox.grid(row=1, columnspan=2, padx=20, pady=5, sticky="nsew")

        self.CopyBtn = customtkinter.CTkButton(self, text="Copy", command=self.button_event, font=("Roboto", 14))
        self.CopyBtn.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        self.addto = customtkinter.CTkButton(self, text="Add to existing file", command=self.add_event,
                                             font=("Roboto", 14))
        self.addto.grid(row=2, column=1, padx=20, pady=5, sticky="nsew")

        self.load_gsc_code(self.item)

    def button_event(self):
        content = self.textbox.get("1.0", "end-1c")  # Get all content from the textbox
        self.clipboard_clear()  # Clear the current clipboard
        self.clipboard_append(content)  # Append the content to the clipboard
        self.update()  # Update the window to ensure clipboard is populated
        CTkMessagebox(message="Code copied to clipboard!",
                      icon="check", option_1="OK")

    def add_event(self):
        content = self.textbox.get("1.0", "end-1c")  # Get all content from the textbox
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'a') as file:
                file.write("\n" + content)
            CTkMessagebox(
                message=f"added to {file_path}\n\nYou will find it at the end of the file\nMake sure its formatted currectly.",
                icon="check", option_1="OK")

    def load_gsc_code(self, item):
        try:
            with open(f"Functions/{item}", 'r') as file:
                code = file.read()
                self.insert_code(code)
        except FileNotFoundError:
            msg = CTkMessagebox(title="Error", message=f"File '{item}' not found.", icon="cancel")
            if msg.get() == "OK":
                self.destroy()

    def insert_code(self, code):
        self.textbox.insert("0.0", code)
        self.textbox.configure(state="disabled")


class ShowMenuCode(customtkinter.CTkToplevel):
    def __init__(self, item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = item
        self.title("GSC Code viewer")
        window_width = 1000
        window_height = 550

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        self.iconbitmap(resource_path("images/logo.ico"))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label_title = customtkinter.CTkLabel(self, text="main.gsc", font=("Roboto", 14))
        self.label_title.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.textbox = CodeView(
            self,
            lexer=pygments.lexers.ObjectiveCLexer,
            color_scheme="monokai",
            font=("Consolas", 12)
        )

        self.textbox.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        self.CopyBtn = customtkinter.CTkButton(self, text="Copy", command=self.button_event, font=("Roboto", 14))
        self.CopyBtn.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        self.load_gsc_code(self.item)

    def button_event(self):
        content = self.textbox.get("1.0", "end-1c")  # Get all content from the textbox
        self.clipboard_clear()  # Clear the current clipboard
        self.clipboard_append(content)  # Append the content to the clipboard
        self.update()  # Update the window to ensure clipboard is populated
        CTkMessagebox(message="Code copied to clipboard!",
                      icon="check", option_1="OK")

    def load_gsc_code(self, item):
        try:
            with open(f"MenuMaker/main.gsc", 'r') as file:
                content = file.read()
                old_method = r'CreateMenu\(\)\s*{([\s\S]*?)\}'
                content = re.sub(old_method, item, content)
                self.insert_code(content)
        except FileNotFoundError as e:
            print(e)
            msg = CTkMessagebox(title="Error", message=f"Something went wrong!", icon="cancel")
            if msg.get() == "OK":
                self.destroy()

    def insert_code(self, code):
        self.textbox.insert("0.0", code)
        self.textbox.configure(state="disabled")


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w",
                                       font=("Roboto", 16))
        button = customtkinter.CTkButton(self, text="Show Code", width=150, height=24, font=("Roboto", 16))
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


def openDiscord():
    webbrowser.open("https://discord.com/invite/wty7y89sHE", new=2)


def openX():
    webbrowser.open("https://twitter.com/rn_1st", new=2)


def openForum():
    webbrowser.open("https://forum.plutonium.pw/", new=2)


def openHowTo():
    webbrowser.open("https://plutonium.pw/docs/modding/gsc/how-to-gsc/#how-to-gsc", new=2)


def openLoadingMods():
    webbrowser.open("https://plutonium.pw/docs/modding/loading-mods/#getting-started-with-gsc-on-t6", new=2)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("GSC Helper")
        self.geometry("1100x700")
        self.iconbitmap(resource_path("images/logo.ico"))
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.minsize(1100, 700)
        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))
        self.picker_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Picker.png")), size=(30, 30))
        self.RGB_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "Picker.png")),
                                                size=(30, 30))
        self.Code_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "GSC.png")),
                                                 size=(30, 30))
        self.Search_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "Search.png")),
                                                   size=(35, 35))

        self.hammer_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "Hammer.png")),
                                                   size=(30, 30))

        self.Help_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "Help.png")),
                                                 size=(30, 30))

        self.discord_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "discord.png")),
                                                    size=(35, 35))

        self.twitter_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "twitter.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "twitterlight.png")),
                                                    size=(30, 30))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure((7, 9), weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  by S2RT",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.Picker_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                     border_spacing=10,
                                                     text="GSC Color Picker",
                                                     fg_color="transparent", text_color=("gray10", "gray90"),
                                                     hover_color=("gray70", "gray30"),
                                                     image=self.RGB_image, anchor="w", command=self.Picker_button_event)
        self.Picker_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Some GSC Functions",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.Code_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Search",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.Search_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=20,
                                                      border_spacing=10, text="Basic Menu Maker",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.hammer_image, anchor="w",
                                                      command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.introduction = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                    border_spacing=10,
                                                    text="Need help?",
                                                    fg_color="transparent", text_color=("gray10", "gray90"),
                                                    hover_color=("gray70", "gray30"),
                                                    image=self.Help_image, anchor="w",
                                                    command=self.introduction_button_event)
        self.introduction.grid(row=5, column=0, sticky="ew")

        self.discord = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                               border_spacing=10,
                                               text="Join Discord",
                                               fg_color="transparent", text_color=("gray10", "gray90"),
                                               hover_color=("gray70", "gray30"),
                                               image=self.discord_image, anchor="w",
                                               command=openDiscord)
        self.discord.grid(row=7, column=0, sticky="sew")

        self.twitter = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                               border_spacing=10,
                                               text="My X/Twitter",
                                               fg_color="transparent", text_color=("gray10", "gray90"),
                                               hover_color=("gray70", "gray30"),
                                               image=self.twitter_image, anchor="w",
                                               command=openX)
        self.twitter.grid(row=8, column=0, sticky="sew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["System", "Dark", "Light"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        self.GSColor = customtkinter.CTkFrame(self.home_frame)
        self.GSColor.grid(padx=20, pady=10, sticky="nsew")
        self.GSColor.grid_columnconfigure(0, weight=1)
        self.GSColor.grid_rowconfigure(2, weight=1)

        self.rgb_label = customtkinter.CTkLabel(self.GSColor, font=("Roboto", 16), text="GSC Color Picker")
        self.rgb_label.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.converted_gsc = customtkinter.StringVar()

        self.ColorPicker = CTkColorPicker(self.GSColor, width=500, orientation="horizontal",
                                          command=lambda e: self.update_color_preview(e))
        self.ColorPicker.grid(row=2, column=0, padx=20, pady=10, sticky="n")
        self.gsc_entry = customtkinter.CTkEntry(self.GSColor, font=("Roboto", 16),
                                                textvariable=self.converted_gsc, justify='center',
                                                fg_color="transparent", border_width=0)
        self.gsc_entry.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.gsc_entry.configure(state='readonly')  # Set to read-only mode
        self.converted_gsc.set(f"(1.000, 1.000, 1.000)")

        self.CopyBtnGSC = customtkinter.CTkButton(self.GSColor, text="Copy",
                                                  command=self.CopyGSC,
                                                  font=("Roboto", 14))
        self.CopyBtnGSC.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        CTkToolTip(self.gsc_entry, delay=0.5, message="GSC color value")

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.grid_rowconfigure(3, weight=1)

        self.func_label = customtkinter.CTkLabel(self.second_frame, font=("Roboto", 16), text="Some GSC Functions")
        self.func_label.grid(row=2, column=0, padx=20, pady=10)

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.second_frame, width=300, height=450,
                                                                        command=self.label_button_frame_event,
                                                                        corner_radius=0)
        self.scrollable_label_button_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.Funcs = []
        self.appendFiles()
        for each in self.Funcs:
            self.scrollable_label_button_frame.add_item(each, image=customtkinter.CTkImage(
                Image.open(os.path.join(current_dir, "images", "GSC.png"))))

        self.toplevel_window = None

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)
        self.third_frame.grid_rowconfigure(1, weight=1)

        self.tabview = customtkinter.CTkTabview(self.third_frame, width=250, height=100, command=self.check_menu)
        self.tabview.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")
        self.tabview.add("MP")
        self.tabview.add("ZM")
        self.tabview.add("MP_ZM")
        self.tabview.add("GSC_Dump")

        self.tabview.tab("MP").grid_columnconfigure((0, 1, 2), weight=1)
        self.tabview.tab("MP").grid_rowconfigure((0, 1), weight=1)

        self.tabview.tab("ZM").grid_columnconfigure((0, 1, 2), weight=1)
        self.tabview.tab("ZM").grid_rowconfigure((0, 1), weight=1)

        self.tabview.tab("MP_ZM").grid_columnconfigure((0, 1, 2), weight=1)
        self.tabview.tab("MP_ZM").grid_rowconfigure((0, 1), weight=1)

        self.tabview.tab("GSC_Dump").grid_columnconfigure((0, 1, 2), weight=1)
        self.tabview.tab("GSC_Dump").grid_rowconfigure((0, 1, 2), weight=1)

        # MP
        self.label_mp = customtkinter.CTkLabel(self.tabview.tab("MP"), text="MP:", fg_color="transparent",
                                               font=("Roboto", 16))
        self.label_mp.grid(row=0, column=1, padx=10, sticky="ew")
        self.values_mp = []
        self.appendFilesMP()
        self.menu_mp = customtkinter.CTkOptionMenu(self.tabview.tab("MP"), dynamic_resizing=False,
                                                   width=200, font=("Roboto", 14))
        self.menu_mp.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="ew")

        self.dropdown_mp = CTkScrollableDropdown(self.menu_mp, values=self.values_mp, command=self.menu_mp_callback,
                                                 width=200, font=("Roboto", 14), button_color="transparent")
        self.menu_mp.set(self.values_mp[0])

        self.entry_mp = customtkinter.CTkEntry(self.tabview.tab("MP"), placeholder_text="Text:", width=200,
                                               font=("Roboto", 14))
        self.entry_mp.grid(row=1, column=1, padx=10, pady=(5, 5), sticky="ew")
        CTkToolTip(self.entry_mp, delay=0.5, message="Search for text")

        self.button_mp = customtkinter.CTkButton(self.tabview.tab("MP"), text="Search", command=self.search_event,
                                                 width=200, font=("Roboto", 14))
        self.button_mp.grid(row=1, column=2, padx=10, pady=(5, 5), sticky="ew")
        # End MP

        # ZM
        self.label_zm = customtkinter.CTkLabel(self.tabview.tab("ZM"), text="ZM:", fg_color="transparent",
                                               font=("Roboto", 16))
        self.label_zm.grid(row=0, column=1, padx=10, sticky="ew")

        self.values_zm = []
        self.appendFilesZM()

        self.menu_zm = customtkinter.CTkOptionMenu(self.tabview.tab("ZM"), dynamic_resizing=False, width=200,
                                                   font=("Roboto", 14))
        self.menu_zm.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="ew")

        self.dropdown_zm = CTkScrollableDropdown(self.menu_zm, values=self.values_zm, command=self.menu_zm_callback,
                                                 width=200, font=("Roboto", 14))
        self.menu_zm.set(self.values_zm[0])

        self.entry_zm = customtkinter.CTkEntry(self.tabview.tab("ZM"), placeholder_text="Text:", width=200,
                                               font=("Roboto", 14))
        self.entry_zm.grid(row=1, column=1, padx=10, pady=(5, 5), sticky="ew")
        CTkToolTip(self.entry_zm, delay=0.5, message="Search for text")

        self.button_zm = customtkinter.CTkButton(self.tabview.tab("ZM"), text="Search", command=self.search_event,
                                                 width=200, font=("Roboto", 14))
        self.button_zm.grid(row=1, column=2, padx=10, pady=(5, 5), sticky="ew")
        # End ZM

        # MP & ZM
        self.label_mp_zm = customtkinter.CTkLabel(self.tabview.tab("MP_ZM"), text="MP & ZM:", fg_color="transparent",
                                                  font=("Roboto", 16))
        self.label_mp_zm.grid(row=0, column=1, padx=10, sticky="ew")

        self.values_mp_zm = []
        self.appendFilesMPZM()

        self.menu_mp_zm = customtkinter.CTkOptionMenu(self.tabview.tab("MP_ZM"), dynamic_resizing=False, width=200,
                                                      font=("Roboto", 14))
        self.menu_mp_zm.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="ew")

        self.dropdown_mp_zm = CTkScrollableDropdown(self.menu_mp_zm, values=self.values_mp_zm,
                                                    command=self.menu_mp_zm_callback, width=250, font=("Roboto", 14))
        self.menu_mp_zm.set(self.values_mp_zm[0])

        self.entry_mp_zm = customtkinter.CTkEntry(self.tabview.tab("MP_ZM"), placeholder_text="Text:", width=200,
                                                  font=("Roboto", 14))
        self.entry_mp_zm.grid(row=1, column=1, padx=10, pady=(5, 5), sticky="ew")
        CTkToolTip(self.entry_mp_zm, delay=0.5, message="Search for text")

        self.button_mp_zm = customtkinter.CTkButton(self.tabview.tab("MP_ZM"), text="Search", command=self.search_event,
                                                    width=200, font=("Roboto", 14))
        self.button_mp_zm.grid(row=1, column=2, padx=10, pady=(5, 5), sticky="ew")
        # End MP & ZM

        # GSC Dump
        self.CaseCheck = customtkinter.CTkCheckBox(self.tabview.tab("GSC_Dump"), text="Case Sensitive", onvalue="on",
                                                   offvalue="off", font=("Roboto", 14))
        self.CaseCheck.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.entry_dump = customtkinter.CTkEntry(self.tabview.tab("GSC_Dump"), placeholder_text="Text:",
                                                 width=200, font=("Roboto", 14))
        self.entry_dump.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")
        CTkToolTip(self.entry_dump, delay=0.5, message="Search for text in all dump files")

        self.button_dump = customtkinter.CTkButton(self.tabview.tab("GSC_Dump"), text="Search",
                                                   command=self.search_dump_event, width=200, font=("Roboto", 14))
        self.button_dump.grid(row=0, column=2, padx=10, pady=(10, 5), sticky="ew")

        self.ProgressBar = customtkinter.CTkProgressBar(self.tabview.tab("GSC_Dump"), orientation="horizontal",
                                                        progress_color="green")
        self.ProgressBar.grid(row=1, columnspan=2, padx=10, pady=(10, 5), sticky="ew")
        self.ProgressBar.set(0)

        self.ProgressLabel = customtkinter.CTkLabel(self.tabview.tab("GSC_Dump"), text="0%", font=("Roboto", 14))
        self.ProgressLabel.grid(row=1, column=2, padx=10, pady=(10, 5), sticky="w")

        self.entry_line = customtkinter.CTkEntry(self.tabview.tab("GSC_Dump"), placeholder_text="Line:",
                                                 width=200, font=("Roboto", 14))
        self.entry_line.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="ew")
        CTkToolTip(self.entry_line, delay=0.5, message="Jump to line")

        self.entry_openFile = customtkinter.CTkEntry(self.tabview.tab("GSC_Dump"), placeholder_text="Path:",
                                                     width=200, font=("Roboto", 14))
        self.entry_openFile.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="ew")
        CTkToolTip(self.entry_openFile, delay=0.5, message="Enter the path to the file you want to open")

        self.button_openFile = customtkinter.CTkButton(self.tabview.tab("GSC_Dump"), text="Show",
                                                       command=self.openFile_event, width=200, font=("Roboto", 14))
        self.button_openFile.grid(row=2, column=2, padx=10, pady=(10, 5), sticky="ew")

        self.code_editor = CodeView(
            self.third_frame,
            lexer=pygments.lexers.ObjectiveCLexer,
            color_scheme="monokai",
            font=("Consolas", 12)
        )

        # End GSC Dump

        self.textboxSearch = customtkinter.CTkTextbox(self.third_frame, width=250, height=310, font=("Roboto", 14),
                                                      corner_radius=5)
        self.textboxSearch.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        self.CopyBtn = customtkinter.CTkButton(self.third_frame, command=self.button_event, text="Copy File",
                                               font=("Roboto", 14))
        self.CopyBtn.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        # fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure((0, 1), weight=1)
        self.fourth_frame.grid_rowconfigure((0, 1), weight=1)

        self.frame_main_menu = customtkinter.CTkFrame(self.fourth_frame)
        self.frame_main_menu.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.frame_main_menu.grid_columnconfigure((0, 1), weight=1)
        self.frame_main_menu.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.frame_colors_text = customtkinter.CTkFrame(self.fourth_frame)
        self.frame_colors_text.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.frame_colors_text.grid_columnconfigure(0, weight=1)
        self.frame_colors_text.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.frame_buttons = customtkinter.CTkFrame(self.fourth_frame)
        self.frame_buttons.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="sew")
        self.frame_buttons.grid_columnconfigure((0, 1), weight=1)
        self.frame_buttons.grid_rowconfigure((0, 1), weight=1)

        # ================================ Menu Structure ================================
        self.menu_structure = {
            "Main Menu": {
                "options": [],
                "submenus": {}
            }
        }
        self.menu_names = list(self.menu_structure.keys())
        # ================================ Menu Structure End ============================

        # ================================ Add Option ================================
        self.addOptionLabel = customtkinter.CTkLabel(self.frame_main_menu, text="Menu Settings", fg_color="transparent",
                                                     font=("Roboto", 16))
        self.addOptionLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")

        self.EntryMenu = customtkinter.CTkOptionMenu(self.frame_main_menu, values=self.menu_names,
                                                     height=30, font=("Roboto", 14))
        self.EntryMenu.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.EntryOption = customtkinter.CTkEntry(self.frame_main_menu, placeholder_text="Option:", height=30,
                                                  font=("Roboto", 14))
        self.EntryOption.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.EntryFunction = customtkinter.CTkEntry(self.frame_main_menu, placeholder_text="Function:", height=30,
                                                    font=("Roboto", 14))
        self.EntryFunction.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.BtnAddOption = customtkinter.CTkButton(self.frame_main_menu, text="Add option", command=self.add_option,
                                                    height=30, font=("Roboto", 14))
        self.BtnAddOption.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        # ================================ Add Option End ==============================

        # ================================ Add Submenu ================================
        self.Entry_Parent_Menu = customtkinter.CTkOptionMenu(self.frame_main_menu, values=self.menu_names, height=30,
                                                             font=("Roboto", 14))
        self.Entry_Parent_Menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.Entry_Menu_Submenu = customtkinter.CTkEntry(self.frame_main_menu, placeholder_text="Sub Menu title:",
                                                         height=30, font=("Roboto", 14))
        self.Entry_Menu_Submenu.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.Entry_Input_Submenu = customtkinter.CTkEntry(self.frame_main_menu,
                                                          placeholder_text="SubMenu Reference tag:", height=30,
                                                          font=("Roboto", 14))
        self.Entry_Input_Submenu.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.BtnAddSubmenu = customtkinter.CTkButton(self.frame_main_menu, text="Add submenu", command=self.add_submenu,
                                                     height=30, font=("Roboto", 14))
        self.BtnAddSubmenu.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        # ================================ Add Submenu End ================================

        # ================================ Remove option ================================
        self.Spacing = customtkinter.CTkLabel(self.frame_main_menu, text="", fg_color="transparent",
                                              font=("Roboto", 16))
        self.Spacing.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        self.EntryMenuRemove = customtkinter.CTkOptionMenu(self.frame_main_menu, values=self.menu_names,
                                                           command=self.setoptionMenu, height=30, font=("Roboto", 14))
        self.EntryMenuRemove.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.EntryOptionRemove = customtkinter.CTkOptionMenu(self.frame_main_menu, values=[], height=30,
                                                             font=("Roboto", 14))
        self.EntryOptionRemove.set("")
        self.EntryOptionRemove.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.BtnRemoveOption = customtkinter.CTkButton(self.frame_main_menu, text="Remove option",
                                                       command=self.remove_option, height=30, font=("Roboto", 14))
        self.BtnRemoveOption.grid(row=8, column=0, padx=10, pady=10, sticky="ew")
        # ================================ Remove option End ================================

        # ================================ Remove Submenu ================================
        self.EntryParentMenuRemove = customtkinter.CTkOptionMenu(self.frame_main_menu,
                                                                 values=["Main Menu"], command=self.setSubMenuMenu,
                                                                 height=30, font=("Roboto", 14))
        self.EntryParentMenuRemove.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        self.EntrySubmenuRemove = customtkinter.CTkOptionMenu(self.frame_main_menu, values=[],
                                                              height=30, font=("Roboto", 14))
        self.EntrySubmenuRemove.set("")
        self.EntrySubmenuRemove.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        self.BtnRemoveSubmenu = customtkinter.CTkButton(self.frame_main_menu, text="Remove Submenu",
                                                        command=self.remove_submenu, height=30, font=("Roboto", 14))
        self.BtnRemoveSubmenu.grid(row=8, column=1, padx=10, pady=10, sticky="ew")

        # ================================ Remove Submenu End ===============================

        # ================================ Change Colors ================================
        self.ColorsLabel = customtkinter.CTkLabel(self.frame_colors_text, text="Color & Text Settings",
                                                  fg_color="transparent",
                                                  font=("Roboto", 16))
        self.ColorsLabel.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.BtnControlText = customtkinter.CTkButton(self.frame_colors_text, text="Change Menu Control text",
                                                      command=self.ChangeControlText, font=("Roboto", 14), height=30)
        self.BtnControlText.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.BtnMenuTitle = customtkinter.CTkButton(self.frame_colors_text, text="Change menu title",
                                                    command=self.ChnageMenuTitle, font=("Roboto", 14), height=30)
        self.BtnMenuTitle.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.BtnColorTitle = customtkinter.CTkButton(self.frame_colors_text, text="Change title color",
                                                     command=self.ChnageTitleColor, font=("Roboto", 14), height=30)
        self.BtnColorTitle.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.BtnGlowTitle = customtkinter.CTkButton(self.frame_colors_text, text="Change title Glow Color",
                                                    command=self.ChnageTitleGlow, font=("Roboto", 14), height=30)
        self.BtnGlowTitle.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.BtnColorLine1 = customtkinter.CTkButton(self.frame_colors_text,
                                                     text="Change Line1 color (Top)",
                                                     command=self.ChangeLine1Color, font=("Roboto", 14), height=30)
        self.BtnColorLine1.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.BtnColorLine2 = customtkinter.CTkButton(self.frame_colors_text,
                                                     text="Change Line2 color (Bottom)",
                                                     command=self.ChangeLine2Color, font=("Roboto", 14), height=30)
        self.BtnColorLine2.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.BtnColorLine3 = customtkinter.CTkButton(self.frame_colors_text, text="Change Line3 color (Left)",
                                                     command=self.ChangeLine3Color, font=("Roboto", 14), height=30)
        self.BtnColorLine3.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.BtnColorLine4 = customtkinter.CTkButton(self.frame_colors_text,
                                                     text="Change Line4 color (Right)",
                                                     command=self.ChangeLine4Color, font=("Roboto", 14), height=30)
        self.BtnColorLine4.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

        self.BtnColorScroller = customtkinter.CTkButton(self.frame_colors_text, text="Change Scroller color",
                                                        command=self.ChangeScrollerColor, font=("Roboto", 14),
                                                        height=30)
        self.BtnColorScroller.grid(row=9, column=0, padx=10, pady=10, sticky="ew")
        # ================================ Change Colors End ===============================

        self.ShowBtn = customtkinter.CTkButton(self.frame_buttons, command=self.ShowCode, text="Show Code",
                                               font=("Roboto", 14), height=35)
        self.ShowBtn.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.MenuImageBtn = customtkinter.CTkButton(self.frame_buttons, command=self.ShowImage,
                                                    text="Show Menu Base Image",
                                                    font=("Roboto", 14), height=35)
        self.MenuImageBtn.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        self.SaveMain = customtkinter.CTkButton(self.frame_buttons, command=self.SaveMainChanges, text="Save As",
                                                font=("Roboto", 14), height=35, fg_color="#1e7e34",
                                                hover_color="#155724")
        self.SaveMain.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.ResetFile = customtkinter.CTkButton(self.frame_buttons, command=self.ResetFileEvent,
                                                 text="Reset main.gsc to default",
                                                 font=("Roboto", 14), height=35, **custom_button)
        self.ResetFile.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        self.ShowMenuCode_window = None

        self.ShowMenuImage_window = None

        self.ShowControlText_window = None

        # introduction Frame
        self.introduction_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.introduction_frame.grid_columnconfigure(0, weight=1)
        self.introduction_frame.grid_rowconfigure(0, weight=1)

        self.helpFrame = customtkinter.CTkFrame(self.introduction_frame)
        self.helpFrame.grid(padx=20, pady=10, sticky="nsew")
        self.helpFrame.grid_columnconfigure(0, weight=1)
        self.helpFrame.grid_rowconfigure(5, weight=1)

        self.space3 = customtkinter.CTkLabel(self.helpFrame, text="", fg_color="transparent")
        self.space3.grid(row=0, column=0, padx=20, pady=30, sticky="new")

        self.OpenLoadMods = customtkinter.CTkButton(self.helpFrame, text="How to load Mods into Plutonium?",
                                                    command=openLoadingMods,
                                                    font=("Roboto", 16), height=40,
                                                    fg_color="#295f83",
                                                    hover_color="#204a66"
                                                    )
        self.OpenLoadMods.grid(row=1, column=0, padx=20, pady=30, sticky="new")

        self.OpenHowToGSC = customtkinter.CTkButton(self.helpFrame, text="How to write GSC?",
                                                    command=openHowTo,
                                                    font=("Roboto", 16), height=40,
                                                    fg_color="#295f83",
                                                    hover_color="#204a66")
        self.OpenHowToGSC.grid(row=2, column=0, padx=20, pady=30, sticky="new")

        self.OpenHowToGSC = customtkinter.CTkButton(self.helpFrame, text="Plutonium Forum",
                                                    command=openForum,
                                                    font=("Roboto", 16), height=40,
                                                    fg_color="#295f83",
                                                    hover_color="#204a66")
        self.OpenHowToGSC.grid(row=3, column=0, padx=20, pady=30, sticky="new")

        self.OpenDiscord = customtkinter.CTkButton(self.helpFrame, text="Join my discord for help",
                                                   command=openDiscord,
                                                   font=("Roboto", 16), height=40,
                                                   fg_color="#295f83",
                                                   hover_color="#204a66")
        self.OpenDiscord.grid(row=4, column=0, padx=20, pady=30, sticky="new")

        self.OpenTwitter = customtkinter.CTkButton(self.helpFrame, text="My X/Twitter account",
                                                   command=openX,
                                                   font=("Roboto", 16), height=40,
                                                   fg_color="#295f83",
                                                   hover_color="#204a66")
        self.OpenTwitter.grid(row=5, column=0, padx=20, pady=30, sticky="new")

        # select default frame
        self.select_frame_by_name("home")

    def SaveMainChanges(self):
        with open(f"MenuMaker/main.gsc", 'r') as file:
            content = file.read()
            old_method = r'CreateMenu\(\)\s*{([\s\S]*?)\}'
            content = re.sub(old_method, self.generate_gsc_code(), content)
        with open("MenuMaker/main.gsc", "w") as file:
            file.write(content)

        file_path = filedialog.asksaveasfilename(initialfile="main.gsc", defaultextension='.gsc', filetypes=(
        ("GSC File", "*.gsc"), ("TXT file", "*.txt"), ("Any file", "*")))
        if file_path:
            with open(file_path, 'w') as file:
                file.write(content)

            CTkMessagebox(title="File saved", message=f"Changes has been saved to {file_path} successfully",
                          icon="check", option_1="OK")

    def appendFiles(self):
        directory = "Functions"
        try:
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    self.Funcs.append(filename)
        except FileNotFoundError:
            CTkMessagebox(title="Error", message=f"Directory '{directory}' not found.", icon="cancel")

    def appendFilesMP(self):
        directory = "Search/MP"
        try:
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    self.values_mp.append(filename)
        except FileNotFoundError:
            CTkMessagebox(title="Error", message=f"Directory '{directory}' not found.", icon="cancel")

    def appendFilesZM(self):
        directory = "Search/ZM"
        try:
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    self.values_zm.append(filename)
        except FileNotFoundError:
            CTkMessagebox(title="Error", message=f"Directory '{directory}' not found.", icon="cancel")

    def appendFilesMPZM(self):
        directory = "Search/MP&ZM"
        try:
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    self.values_mp_zm.append(filename)
        except FileNotFoundError:
            CTkMessagebox(title="Error", message=f"Directory '{directory}' not found.", icon="cancel")

    def ChangeScrollerColor(self):
        pick_color = AskColor()
        color = pick_color.get()
        if color is None:
            return
        CLR = self.update_color_Ask(color)
        self.FileWriteColor(CLR, "ScrollerColor")
        self.BtnColorScroller.configure(border_color=color, border_width=2)

    def ChangeLine1Color(self):
        pick_color = AskColor()
        color = pick_color.get()
        if color is None:
            return
        CLR = self.update_color_Ask(color)
        self.FileWriteColor(CLR, "Line1Color")
        self.BtnColorLine1.configure(border_color=color, border_width=2)

    def ChangeLine2Color(self):
        pick_color = AskColor()
        color = pick_color.get()
        if color is None:
            return
        CLR = self.update_color_Ask(color)
        self.FileWriteColor(CLR, "Line2Color")
        self.BtnColorLine2.configure(border_color=color, border_width=2)

    def ChangeLine3Color(self):
        pick_color = AskColor()
        color = pick_color.get()
        if color is None:
            return
        CLR = self.update_color_Ask(color)
        self.FileWriteColor(CLR, "Line3Color")
        self.BtnColorLine3.configure(border_color=color, border_width=2)

    def ChangeLine4Color(self):
        pick_color = AskColor()
        color = pick_color.get()
        if color is None:
            return
        CLR = self.update_color_Ask(color)
        self.FileWriteColor(CLR, "Line4Color")
        self.BtnColorLine4.configure(border_color=color, border_width=2)

    def ResetFileEvent(self):
        msg = CTkMessagebox(title="Reset File to default", message="Are you sure?",
                            icon="warning", option_1="No", option_2="Yes")

        if msg.get() == "Yes":
            try:
                with open("MenuMaker/Files/Dont_edit_this.gsc", 'r') as infile, open("MenuMaker/main.gsc",
                                                                                     'w') as outfile:
                    outfile.write(infile.read())
                    self.BtnColorTitle.configure(border_color="", border_width=0)
                    self.BtnGlowTitle.configure(border_color="", border_width=0)
                    self.BtnColorLine1.configure(border_color="", border_width=0)
                    self.BtnColorLine2.configure(border_color="", border_width=0)
                    self.BtnColorLine3.configure(border_color="", border_width=0)
                    self.BtnColorLine4.configure(border_color="", border_width=0)
                    self.BtnColorScroller.configure(border_color="", border_width=0)
                CTkMessagebox(title="File Restored", message="'main.gsc' successfully Restored!",
                              icon="check", option_1="OK")
            except FileNotFoundError:
                CTkMessagebox(title="Error",
                              message=f"Make sure 'main.gsc' in MenuMaker folder\nand 'Dont_edit_this.gsc' in MenuMaker/Files",
                              icon="cancel")

    def ChangeControlText(self):
        if self.ShowControlText_window is None or not self.ShowControlText_window.winfo_exists():
            self.ShowControlText_window = ChangeControlText(self)  # create window if its None or destroyed
        else:
            self.ShowControlText_window.focus()  # if window exists focus it

    def ChnageMenuTitle(self):
        dialog = customtkinter.CTkInputDialog(text="New Menu Title:", title="Change Menu Title")
        Text = dialog.get_input()
        if Text == None:
            return
        self.replace_menu_title(Text)

    def replace_menu_title(self, new_title):
        with open("MenuMaker/main.gsc", 'r+') as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                if 'self.MenuTitle =' in line:
                    new_line = f'\t\tself.MenuTitle = "{new_title}";\n'
                    file.write(new_line)
                else:
                    file.write(line)

            file.truncate()

    def ChnageTitleGlow(self):
        pick_color = AskColor()
        color = pick_color.get()
        if color is None:
            return
        CLR = self.update_color_Ask(color)
        self.FileWriteColor(CLR, "TitleGlow")
        self.BtnGlowTitle.configure(border_color=color, border_width=2)

    def ChnageTitleColor(self):
        pick_color = AskColor()
        color = pick_color.get()
        if color is None:
            return
        CLR = self.update_color_Ask(color)
        self.FileWriteColor(CLR, "TitleColor")
        self.BtnColorTitle.configure(border_color=color, border_width=2)

    def FileWriteColor(self, new_color, Name):
        try:
            with open("MenuMaker/main.gsc", 'r+') as file:
                lines = file.readlines()
                file.seek(0)

                for line in lines:
                    if f'self.{Name} =' in line:
                        new_line = f'\tself.{Name} = {new_color};\n'
                        file.write(new_line)
                    else:
                        file.write(line)

                file.truncate()
        except FileNotFoundError:
            CTkMessagebox(title="Error", message=f"File 'MenuMaker/main.gsc' not found.", icon="cancel")

    def ShowImage(self):
        if self.ShowMenuImage_window is None or not self.ShowMenuImage_window.winfo_exists():
            self.ShowMenuImage_window = ShowImageWindow(self)  # create window if its None or destroyed
        else:
            self.ShowMenuImage_window.focus()  # if window exists focus it

    def remove_submenu(self):
        submenu_code_name_to_remove = self.EntrySubmenuRemove.get()
        parent_menu = self.EntryParentMenuRemove.get()
        if submenu_code_name_to_remove not in self.menu_structure:  # If the submenu is not found, exit
            return

        # 1. Remove the submenu from the parent menu's submenus dictionary
        self.menu_structure[parent_menu]['submenus'] = {display_name: code_name for display_name, code_name in
                                                        self.menu_structure[parent_menu]['submenus'].items() if
                                                        code_name != submenu_code_name_to_remove}

        # 2. Delete the submenu's own entry from the menu_structure
        del self.menu_structure[submenu_code_name_to_remove]
        option_names = list(self.menu_structure[parent_menu]['submenus'].values())
        if not option_names:
            self.EntrySubmenuRemove.configure(values=[])
            self.EntrySubmenuRemove.set("")
        else:
            self.EntrySubmenuRemove.configure(values=option_names)
            self.EntrySubmenuRemove.set(option_names[0])

        self.menu_names = list(self.menu_structure.keys())
        self.EntryParentMenuRemove.configure(values=self.menu_names)
        self.Entry_Parent_Menu.configure(values=self.menu_names)
        self.EntryMenu.configure(values=self.menu_names)
        self.EntryMenuRemove.configure(values=self.menu_names)

        self.EntryParentMenuRemove.set(self.menu_names[0])
        self.Entry_Parent_Menu.set(self.menu_names[0])
        self.EntryMenu.set(self.menu_names[0])
        self.EntryMenuRemove.set(self.menu_names[0])

    def remove_option(self):
        menu = self.EntryMenuRemove.get()
        option_name_to_remove = self.EntryOptionRemove.get()

        self.menu_structure[menu]['options'] = [(option_name, function_name) for option_name, function_name in
                                                self.menu_structure[menu]['options'] if
                                                option_name != option_name_to_remove]

        self.option_names = [option[0] for option in self.menu_structure[self.EntryMenuRemove.get()]['options']]
        if self.option_names:
            self.EntryOptionRemove.configure(values=self.option_names)
            self.EntryOptionRemove.set(self.option_names[0])
        else:
            self.EntryOptionRemove.configure(values=[])
            self.EntryOptionRemove.set("")

        self.menu_names = list(self.menu_structure.keys())
        self.EntryParentMenuRemove.configure(values=self.menu_names)
        self.Entry_Parent_Menu.configure(values=self.menu_names)
        self.EntryMenu.configure(values=self.menu_names)
        self.EntryMenuRemove.configure(values=self.menu_names)

        self.EntryParentMenuRemove.set(self.menu_names[0])
        self.Entry_Parent_Menu.set(self.menu_names[0])
        self.EntryMenu.set(self.menu_names[0])
        self.EntryMenuRemove.set(self.menu_names[0])

    def setSubMenuMenu(self, choice):
        option_names = list(self.menu_structure[choice]['submenus'].values())
        if not option_names:
            self.EntrySubmenuRemove.configure(values=[])
            self.EntrySubmenuRemove.set("")
        else:
            self.EntrySubmenuRemove.configure(values=option_names)
            self.EntrySubmenuRemove.set(option_names[0])

    def setoptionMenu(self, choice):
        self.option_names = [option[0] for option in self.menu_structure[choice]['options']]
        if not self.option_names:
            self.EntryOptionRemove.configure(values=[])
            self.EntryOptionRemove.set("")
        else:
            self.EntryOptionRemove.configure(values=self.option_names)
            self.EntryOptionRemove.set(self.option_names[0])

    def ShowCode(self):
        if self.ShowMenuCode_window is None or not self.ShowMenuCode_window.winfo_exists():
            self.ShowMenuCode_window = ShowMenuCode(self.generate_gsc_code())  # create window if its None or destroyed
        else:
            self.ShowMenuCode_window.focus()  # if window exists focus it

    def add_option(self):
        menu = self.EntryMenu.get()
        option_name = self.EntryOption.get().strip()
        if not option_name:
            return
        function_name = self.EntryFunction.get().strip()
        self.menu_structure[menu]['options'].append((option_name, function_name))

        self.option_names = [option[0] for option in self.menu_structure[self.EntryMenuRemove.get()]['options']]
        self.EntryOptionRemove.configure(values=self.option_names)
        self.EntryOptionRemove.set(self.option_names[0])

    def add_submenu(self):
        parent_menu = self.Entry_Parent_Menu.get()
        title = self.Entry_Menu_Submenu.get().strip()
        Input = self.Entry_Input_Submenu.get().strip()
        if not title or not Input:
            return
        self.menu_structure[parent_menu]['submenus'][title] = Input
        self.menu_structure[Input] = {
            "options": [],
            "submenus": {}
        }
        self.menu_names = list(self.menu_structure.keys())
        self.EntryParentMenuRemove.configure(values=self.menu_names)
        self.Entry_Parent_Menu.configure(values=self.menu_names)
        self.EntryMenu.configure(values=self.menu_names)
        self.EntryMenuRemove.configure(values=self.menu_names)

        self.EntryParentMenuRemove.set(self.menu_names[0])
        self.Entry_Parent_Menu.set(self.menu_names[0])
        self.EntryMenu.set(self.menu_names[0])
        self.EntryMenuRemove.set(self.menu_names[0])

        option_names = list(self.menu_structure[self.EntryParentMenuRemove.get()]['submenus'].values())
        if not option_names:
            self.EntrySubmenuRemove.configure(values=[])
            self.EntrySubmenuRemove.set("")
        else:
            self.EntrySubmenuRemove.configure(values=option_names)
            self.EntrySubmenuRemove.set(option_names[0])

    def generate_submenu_code(self, menu_code):
        parent = [key for key, val in self.menu_structure.items() if menu_code in val["submenus"].values()][0]
        code = f'\n    self add_menu("{menu_code}", "{parent}", "User");\n'
        for option, function_name in self.menu_structure[menu_code]['options']:
            if function_name:
                code += f'    self add_option("{menu_code}", "{option}", ::{function_name});\n'
            else:
                code += f'    self add_option("{menu_code}", "{option}");\n'

        for submenu_display, submenu_code in self.menu_structure[menu_code]['submenus'].items():
            code += f'    self add_option("{menu_code}", "{submenu_display}", ::submenu, "{submenu_code}", "{submenu_display}");\n'
            code += self.generate_submenu_code(submenu_code)  # Recursively generate code for nested submenus

        return code

    def generate_gsc_code(self):
        code = "CreateMenu()\n{\n"
        code += f'    self add_menu("Main Menu", undefined, "User");\n'

        # Add Main Menu options
        for option, function_name in self.menu_structure["Main Menu"]['options']:
            if function_name:
                code += f'    self add_option("Main Menu", "{option}", ::{function_name});\n'
            else:
                code += f'    self add_option("Main Menu", "{option}");\n'

        # Add Main Menu's submenus
        for submenu_display, submenu_code in self.menu_structure["Main Menu"]['submenus'].items():
            code += f'    self add_option("Main Menu", "{submenu_display}", ::submenu, "{submenu_code}", "{submenu_display}");\n'

        # Add submenus and their options
        for submenu_display, submenu_code in self.menu_structure["Main Menu"]['submenus'].items():
            code += self.generate_submenu_code(submenu_code)

        code += "}"
        return code

    def CopyGSC(self):
        content = self.gsc_entry.get()
        self.clipboard_clear()
        self.clipboard_append(content)
        self.update()
        CTkMessagebox(message="Color copied to clipboard!",
                      icon="check", option_1="OK")

    def highlight_and_goto_line(self, code_editor, line_number, color="#414141"):
        start_index = f"{line_number}.0"
        end_index = f"{line_number}.end"
        code_editor.tag_add("highlight", start_index, end_index)
        code_editor.tag_configure("highlight", background=color)
        code_editor.see(start_index)  # Make the line visible
        code_editor.mark_set("insert", start_index)  # Move cursor to the line

    def openFile_event(self):
        code = self.entry_openFile.get().strip()
        if not code:
            CTkMessagebox(title="Info", message="Please enter a file path to proceed.")
            return
        try:
            with open(code, 'r') as file:
                content = file.read()
                self.code_editor.delete("1.0", tk.END)
                self.code_editor.insert("1.0", content)
        except FileNotFoundError:
            CTkMessagebox(title="Error", message=f"File '{code}' not found.", icon="cancel")

        # Highlighting and moving to line 5 (change the number as needed)
        self.highlight_and_goto_line(self.code_editor, int(self.entry_line.get()))

    def search_event(self):
        counter = 0
        file_path = ""
        if self.tabview.get() == "MP":
            if not self.entry_mp.get().strip():
                CTkMessagebox(title="Info", message="Please enter a search query to proceed.")
                return
            self.textboxSearch.configure(state="normal")
            self.textboxSearch.delete("0.0", "end")
            search_value = re.escape(self.entry_mp.get().lower())
            file_path = f"Search/MP/{self.menu_mp.get()}"
            with open(file_path, 'r') as file:
                for line in file:
                    if re.search(search_value, line, re.IGNORECASE):
                        counter += 1
                        self.textboxSearch.insert("0.0", line.strip() + "\n")

        elif self.tabview.get() == "ZM":
            if not self.entry_zm.get().strip():
                CTkMessagebox(title="Info", message="Please enter a search query to proceed.")
                return
            self.textboxSearch.configure(state="normal")
            self.textboxSearch.delete("0.0", "end")
            search_value = re.escape(self.entry_zm.get().lower())
            file_path = f"Search/ZM/{self.menu_zm.get()}"
            with open(file_path, 'r') as file:
                for line in file:
                    if re.search(search_value, line, re.IGNORECASE):
                        counter += 1
                        self.textboxSearch.insert("0.0", line.strip() + "\n")

        elif self.tabview.get() == "MP_ZM":
            if not self.entry_mp_zm.get().strip():
                CTkMessagebox(title="Info", message="Please enter a search query to proceed.")
                return
            self.textboxSearch.configure(state="normal")
            self.textboxSearch.delete("0.0", "end")
            search_value = re.escape(self.entry_mp_zm.get().lower())
            file_path = f"Search/MP&ZM/{self.menu_mp_zm.get()}"
            with open(file_path, 'r') as file:
                for line in file:
                    if re.search(search_value, line, re.IGNORECASE):
                        counter += 1
                        self.textboxSearch.insert("0.0", line.strip() + "\n")
        self.textboxSearch.configure(state="disabled")
        CTkMessagebox(message=f"Results: {counter}\nFile Path: {file_path}",
                      icon="check", option_1="OK")

    def search_dump_event(self):
        if self.tabview.get() == "GSC_Dump":
            if not self.entry_dump.get().strip():
                CTkMessagebox(title="Info", message="Please enter a search query to proceed.")
                return
            if int(len(self.entry_dump.get().strip())) == 1:
                CTkMessagebox(title="Info", message="Search length must be higher than 1")
                return

            self.thread = threading.Thread(target=self.do_search_dump)
            self.thread.start()

    def generate_html(self, lines):
        with open('template/template.html', 'r') as f:
            template = f.read()

        rows = ""
        for count, line_data in enumerate(lines, 1):
            rows += f'<tr><td>{count}</td><td>{line_data["line_text"]}</td><td>{line_data["file_path"]}</td><td>{line_data["line_num"]}</td></tr>'

        complete_html = template.replace("{{rows}}", rows)

        with open('results.html', 'w') as f:
            f.write(complete_html)

        webbrowser.open('results.html', new=2)
        self.ProgressBar.set(0)
        self.ProgressLabel.configure(text='0%')
        self.ProgressLabel.update()

    def count_lines(self, file_paths):
        return sum(1 for file_path in file_paths for _ in open(file_path, 'r', encoding='utf-8', errors='ignore'))

    def do_search_dump(self):
        try:
            lines_to_display = []
            root_folder = "gsc-dump"
            gsc_files = list(Path(root_folder).rglob('*.gsc'))
            total_lines = self.count_lines(gsc_files)
            lines_checked = 0

            if self.CaseCheck.get() == "on":  # Case sensitive
                search_pattern = re.compile(re.escape(self.entry_dump.get().strip()))
            else:  # Case insensitive
                search_pattern = re.compile(re.escape(self.entry_dump.get().strip()), re.IGNORECASE)

            update_frequency = max(total_lines // 100,
                                   1)  # Update after every 1% of progress, or every line for small files
            last_update_percentage = 0

            for file_path in gsc_files:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if search_pattern.search(line):
                            lines_to_display.append(
                                {"line_num": line_num, "line_text": line.strip(), "file_path": str(file_path)})
                        lines_checked += 1
                        if lines_checked % update_frequency == 0:
                            percentage_of_completion = (lines_checked / total_lines) * 100
                            if percentage_of_completion - last_update_percentage >= 1:
                                self.ProgressBar.set(percentage_of_completion / 100)
                                self.ProgressLabel.configure(text=f'{int(percentage_of_completion)}%')
                                self.ProgressLabel.update()
                                last_update_percentage = percentage_of_completion

            # Ensure progress bar and label are fully updated at the end
            self.ProgressBar.set(1)
            self.ProgressLabel.configure(text='100%')
            self.ProgressLabel.update()

            if not lines_to_display:
                CTkMessagebox(title="Info", message="Zero results found")
                return
            else:
                self.generate_html(lines_to_display)
        except Exception as e:
            print(e)
            CTkMessagebox(title="Error", message="Something went wrong", icon="cancel")

    def check_menu(self):
        self.textboxSearch.configure(state="normal")
        self.textboxSearch.delete("0.0", "end")
        self.textboxSearch.configure(state="disabled")
        if not self.textboxSearch.grid_info() or not self.CopyBtn.grid_info() or not self.code_editor.grid_info():
            self.CopyBtn.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
            self.textboxSearch.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        if self.tabview.get() == "MP":
            self.dropdown_mp = CTkScrollableDropdown(self.menu_mp, values=self.values_mp,
                                                     command=self.menu_mp_callback, width=200,
                                                     font=("Roboto", 14))
            if not self.dropdown_mp_zm.winfo_exists() and not self.dropdown_zm.winfo_exists():
                self.dropdown_mp_zm.destroy()
                self.dropdown_zm.destroy()
            self.code_editor.grid_forget()
            self.menu_mp_callback(self.menu_mp.get())

        elif self.tabview.get() == "ZM":
            self.dropdown_zm = CTkScrollableDropdown(self.menu_zm, values=self.values_zm,
                                                     command=self.menu_zm_callback, width=200,
                                                     font=("Roboto", 14))
            if not self.dropdown_mp.winfo_exists() and not self.dropdown_mp_zm.winfo_exists():
                self.dropdown_mp.destroy()
                self.dropdown_mp_zm.destroy()
            self.code_editor.grid_forget()
            self.menu_zm_callback(self.menu_zm.get())

        elif self.tabview.get() == "MP_ZM":
            self.dropdown_mp_zm = CTkScrollableDropdown(self.menu_mp_zm, values=self.values_mp_zm,
                                                        command=self.menu_mp_zm_callback, width=250,
                                                        font=("Roboto", 14))
            if not self.dropdown_mp.winfo_exists() and not self.dropdown_zm.winfo_exists():
                self.dropdown_mp.destroy()
                self.dropdown_zm.destroy()
            self.code_editor.grid_forget()
            self.menu_mp_zm_callback(self.menu_mp_zm.get())

        elif self.tabview.get() == "GSC_Dump":
            self.code_editor.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
            self.textboxSearch.grid_forget()

    def button_event(self):
        if self.tabview.get() == "GSC_Dump":
            content = self.code_editor.get("1.0", "end-1c")  # Get all content from the textbox
            self.clipboard_clear()  # Clear the current clipboard
            self.clipboard_append(content)  # Append the content to the clipboard
            self.update()  # Update the window to ensure clipboard is populated
        else:
            content = self.textboxSearch.get("1.0", "end-1c")  # Get all content from the textbox
            self.clipboard_clear()  # Clear the current clipboard
            self.clipboard_append(content)  # Append the content to the clipboard
            self.update()  # Update the window to ensure clipboard is populated
        CTkMessagebox(message="Code copied to clipboard!",
                      icon="check", option_1="OK")

    def menu_mp_callback(self, choice):
        try:
            self.menu_mp.set(choice)
            with open(f"Search/MP/{choice}", 'r') as file:
                self.textboxSearch.configure(state="normal")
                self.textboxSearch.delete("0.0", "end")
                code = file.read()
                self.textboxSearch.insert("0.0", code)
                self.textboxSearch.configure(state="disabled")
        except FileNotFoundError:
            msg = CTkMessagebox(title="Error", message=f"File '{choice}' not found.", icon="cancel")
            if msg.get() == "OK":
                self.destroy()

    def menu_zm_callback(self, choice):
        try:
            self.menu_zm.set(choice)
            with open(f"Search/ZM/{choice}", 'r') as file:
                self.textboxSearch.configure(state="normal")
                self.textboxSearch.delete("0.0", "end")
                code = file.read()
                self.textboxSearch.insert("0.0", code)
                self.textboxSearch.configure(state="disabled")
        except FileNotFoundError:
            msg = CTkMessagebox(title="Error", message=f"File '{choice}' not found.", icon="cancel")
            if msg.get() == "OK":
                self.destroy()

    def menu_mp_zm_callback(self, choice):
        try:
            self.menu_mp_zm.set(choice)
            with open(f"Search/MP&ZM/{choice}", 'r') as file:
                self.textboxSearch.configure(state="normal")
                self.textboxSearch.delete("0.0", "end")
                code = file.read()
                self.textboxSearch.insert("0.0", code)
                self.textboxSearch.configure(state="disabled")
        except FileNotFoundError:
            msg = CTkMessagebox(title="Error", message=f"File '{choice}' not found.", icon="cancel")
            if msg.get() == "OK":
                self.destroy()

    def label_button_frame_event(self, item):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(item, self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def update_color_preview(self, e):
        e = e.lstrip('#')
        r, g, b = tuple(int(e[i:i + 2], 16) for i in (0, 2, 4))
        r_int = int(r)
        g_int = int(g)
        b_int = int(b)
        # Update the R, G, and B value labels
        r_gsc, g_gsc, b_gsc = rgb_to_gsc(r_int, g_int, b_int)
        self.converted_gsc.set(f"({r_gsc:.3f}, {g_gsc:.3f}, {b_gsc:.3f})")

    def update_color_Ask(self, e):
        try:
            e = e.lstrip('#')
            r, g, b = tuple(int(e[i:i + 2], 16) for i in (0, 2, 4))
            r_int = int(r)
            g_int = int(g)
            b_int = int(b)
            # Update the R, G, and B value labels
            r_gsc, g_gsc, b_gsc = rgb_to_gsc(r_int, g_int, b_int)
            return f"({r_gsc:.3f}, {g_gsc:.3f}, {b_gsc:.3f})"
        except AttributeError:
            pass

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.introduction.configure(fg_color=("gray75", "gray25") if name == "introduction" else "transparent")
        self.Picker_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "introduction":
            self.introduction_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.introduction_frame.grid_forget()
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

    def introduction_button_event(self):
        self.select_frame_by_name("introduction")

    def Picker_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        self.check_menu()

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
