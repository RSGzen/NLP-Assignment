import customtkinter as ctk

# Window for GUI
window = ctk.CTk()
window.title("Movie Recommender - Animation Movies") 

window.geometry('1200x800') # Set window size
window.configure(fg_color = '#1b1e22') # Set background color 

## For Main Title

# Create font
main_title_font = ctk.CTkFont(family="Fixedsys", size=40)

main_title_label = ctk.CTkLabel(window, 
                                width = 150,
                                height = 80,
                                text = " Movie Recommender - Animation Movies ",
                                text_color='white',
                                corner_radius=20,
                                font=main_title_font)

# Declares the position of the main title label with padding of (100, 10)
main_title_label.pack(padx=50, pady=30)

## For Buttons to select the program function and exit button
button_text_font = ctk.CTkFont(family="System", size=29)

button_frame = ctk.CTkFrame(window,
                            fg_color='transparent')

button_frame.pack(pady=2)

option_button_1 = ctk.CTkButton(button_frame, 
                                text="Find a movie via plot description",
                                fg_color = "#4b586a",
                                font=button_text_font)

option_button_2 = ctk.CTkButton(button_frame, 
                                text="Check a movie via name",
                                fg_color = "#4b586a",
                                font=button_text_font)

exit_button = ctk.CTkButton(button_frame,
                            text="Exit Program",
                            text_color='#cbced2',
                            fg_color="#4b586a",
                            font=button_text_font)

option_button_1.pack(side = 'left', padx = 10, pady = 30)
option_button_2.pack(side = 'left', padx = 10, pady = 30)
exit_button.pack(side = 'left', padx = 10, pady = 30)

window.mainloop()