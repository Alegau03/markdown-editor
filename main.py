import flet as ft
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from markdown2pdf import convert_md_2_pdf as convert
from md2pdf.core import md2pdf
import markdown2
from weasyprint import HTML

def main(page: ft.Page):
    page.title = "Editor Markdown Pyton v1.0"  
    page.theme_mode = "dark"   
    def update_preview(e):
        md.value = text_field.value
        page.update()

    def toggle_theme(e):
        
        if page.theme_mode == "dark":
            page.theme_mode = "light"
        else:
            page.theme_mode = "dark"
        page.update()

    def save_file(e):
        file_content = text_field.value
        file_name = filedialog.asksaveasfilename(
            title="Salva file", 
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md")]
        )
        if file_name:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(file_content)

    def import_file(e):
        file_name = filedialog.askopenfilename(
            title="Importa file", 
            filetypes=[("Markdown Files", "*.md")]
        )
        if file_name:
            with open(file_name, "r", encoding="utf-8") as file:
                text_field.value = file.read()
                update_preview(None)
    
    def export_to_pdf(e):
        file_content = text_field.value
        html_content = markdown2.markdown(file_content)
        
        file_name = filedialog.asksaveasfilename(
            title="Esporta come PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if file_name:
            # Genera il PDF utilizzando WeasyPrint
            HTML(string=html_content).write_pdf(file_name)

            messagebox.showinfo("Esportazione completata", "Il testo Markdown è stato esportato come PDF con successo.")

    page.appbar = ft.AppBar(
        title=ft.Text("Markdown Editor", color=ft.colors.RED_ACCENT_700),  
        center_title=True,  
        bgcolor=ft.colors.with_opacity(0.5, '#394145'),  
        actions=[ft.IconButton(icon="brightness_4",on_click=toggle_theme, icon_color=ft.colors.WHITE),
         ft.IconButton(icon="save", on_click=save_file, icon_color=ft.colors.WHITE),
         ft.IconButton(icon="folder_open", on_click=import_file, icon_color=ft.colors.WHITE),
         ft.IconButton(icon="picture_as_pdf", on_click=export_to_pdf, icon_color=ft.colors.WHITE),
         ]
    )

    text_field = ft.TextField(
        value="## Ciao!",  
        multiline=True,  
        on_change=update_preview,
        expand=True,  
        border_color=ft.colors.TRANSPARENT, 
    )
    
    md = ft.Markdown(
        value=text_field.value, 
        selectable=True,  
        extension_set="gitHubWeb",
        on_tap_link=lambda e: page.launch_url(e.data),
       
    )

    page.add(
        ft.Row(  
            controls=[
                text_field,
                ft.VerticalDivider(color=ft.colors.RED),  
                ft.Container(  
                    ft.Column(  
                        [md],
                        scroll="hidden", 
                    ),
                    expand=True, 
                    alignment=ft.alignment.top_left,  
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,  
        )  
    )


ft.app(target=main)