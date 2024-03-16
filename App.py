import customtkinter as ctk
ctk.set_appearance_mode('dark')
import ctypes
from client import Client

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
ctk.set_window_scaling(scaleFactor)
ctk.set_widget_scaling(scaleFactor)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('DDestination - Fitness App')
        self.geometry('720x480')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.home_screen = Home_Screen(self)
        self.home_screen.configure(corner_radius = 20)
        self.home_screen.grid(column = 0, padx = 20, pady = 20, sticky = 'nsew')
        self.login_screen = Login_Screen(self)
        self.login_screen.configure( corner_radius = 20)
        self.user_screen = User_Screen(self)
        self.signup_screen = SignUp_Screen(self)
        self.client:Client = Client()

    def login_pressed(self)->None:
        self.home_screen.grid_forget()
        self.login_screen.grid(column = 0, padx = 20, pady = 20, sticky = 'nsew')
        
    def signUp_pressed(self)->None:
        self.home_screen.grid_forget()
        self.signup_screen.grid(column = 0, padx = 20, pady = 20, sticky = 'nsew')


    def login_connection(self, data)->None:
        if not self.client.is_connected_to_server():
            self.client.connect_server()
            print('connected to server')
        self.login_idetification(data)
        
    def login_idetification(self, data):
        self.client.send_data(data)
        print(f'{data} was sent')
        permmision = self.client.recieve_data()
        if permmision=='valid user':
            self.login_screen.grid_forget()
            self.user_screen.grid(column = 0, padx = 20, pady = 20, sticky = 'nsew')
        elif permmision=='invalid user':
            self.login_screen.raise_user_error()
            


    def signup_connection(self, data)->None:
        if not self.client.is_connected_to_server():
            self.client.connect_server()
            print('connected to server')
        self.signup_idetification(data)


    def signup_idetification(self, data):
        self.client.send_data(data)
        print(f'{data} was sent')
        permission = self.client.recieve_data()
        if permission=='new user has been succecfuly added':
            self.signup_screen.grid_forget()
            self.user_screen.grid(column = 0, padx = 20, pady = 20, sticky = 'nsew')
        elif permission=='user already exists':
            self.signup_screen.raise_user_error()


class Home_Screen(ctk.CTkFrame, App):
    def __init__(self, master:App):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text="DDestination - Fitness App", text_color = 'white', font = ('Arial', 40, 'bold'))
        self.label.grid(column = 0, row = 0, pady = 20)
        self.login_button = ctk.CTkButton(self, text = 'Login', text_color='white', height = 50, width=150, font= ('Arial', 20, 'bold'), command = lambda: App.login_pressed(master))
        self.login_button.grid(column = 0, row = 5, pady = 90)
        self.signup_button = ctk.CTkButton(self, text = 'SignUp', text_color='white', height = 50, width=150, font= ('Arial', 20, 'bold'), command = lambda: App.signUp_pressed(master))
        self.signup_button.grid(column = 0, row = 6)


class Login_Screen(ctk.CTkFrame, App):
    def __init__(self, master:App):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text="Login", text_color = 'white', font = ('Arial', 40, 'bold'))
        self.label.grid(column = 0, row = 0, pady = 12)
        self.username_label = ctk.CTkLabel(self, text = "Username:",  font = ('Arial', 20, 'bold'))
        self.username_label.grid(column = 0, row = 2, pady = 12)
        self.username_input = ctk.CTkEntry(self, placeholder_text="Enter Your Username",width = 250, height = 50)
        self.username_input.grid(column = 0, row = 3, pady = 5)
        self.password_label = ctk.CTkLabel(self, text = "Password:",  font = ('Arial', 20, 'bold'))
        self.password_label.grid(column = 0, row = 4, pady = 10)
        self.password_input = ctk.CTkEntry(self, placeholder_text="Enter Your Password", width = 250, height = 50, show = '*')
        self.password_input.grid(column = 0, row = 5, pady = 5)
        self.login_button = ctk.CTkButton(self, text = 'Login', text_color='white', height = 40, width=130, font= ('Arial', 20, 'bold'), corner_radius = 30, command = lambda: App.login_connection(master, ('login:'+self.username_input.get()+'&'+self.password_input.get())))
        self.login_button.grid(column = 0, row = 6, pady = 10)

    
    def raise_user_error(self):
        self.error_label = self.password_label = ctk.CTkLabel(self, text = "Invalid User",  font = ('Arial', 15, 'bold'), text_color='red')
        self.error_label.grid(column = 0, row = 7, pady = 15)
        self.username_input.delete(0, len(self.username_input.get()))
        self.password_input.delete(0,len(self.password_input.get()))

class SignUp_Screen(ctk.CTkFrame,App):
    def __init__(self, master:App):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text="SignUp", text_color = 'white', font = ('Arial', 40, 'bold'))
        self.label.grid(column = 0, row = 0, pady = 10)
        self.username_label = ctk.CTkLabel(self, text = "Username:",  font = ('Arial', 20, 'bold'))
        self.username_label.grid(column = 0, row = 2, pady = 12)
        self.username_input = ctk.CTkEntry(self, placeholder_text="Enter Your Username", width = 250, height = 30)
        self.username_input.grid(column = 0, row = 3, pady = 5)
        self.password_label = ctk.CTkLabel(self, text = "Password:",  font = ('Arial', 20, 'bold'))
        self.password_label.grid(column = 0, row = 4, pady = 10)
        self.password_input = ctk.CTkEntry(self, placeholder_text="Enter Your Password", width = 250, height = 30, show = '*')
        self.password_input.grid(column = 0, row = 5, pady = 5)
        #self.confirm_label = ctk.CTkLabel(self, text = "Confirm Password:",  font = ('Arial', 20, 'bold'))
        #self.confirm_input = ctk.CTkEntry(self, placeholder_text="Enter Your Password", width = 250, height = 30, show = '*')
        #self.confirm_label.grid(column = 0, row = 6, pady = 12)
        #self.confirm_input.grid(column = 0, row = 7, pady = 5)
        self.signup_button = ctk.CTkButton(self, text = 'SignUp',  text_color='white', height = 40, width=130, font= ('Arial', 20, 'bold'), corner_radius = 30, command = lambda: App.signup_connection(master, ('signup:'+ self.username_input.get()+'&'+self.password_input.get())))
        self.signup_button.grid(column = 0, row = 8, pady = 10)


    def raise_user_error(self):
        self.error_label = self.password_label = ctk.CTkLabel(self, text = "User already exists",  font = ('Arial', 15, 'bold'), text_color='red')
        self.error_label.grid(column = 0, row = 7, pady = 15)
        self.username_input.delete(0, len(self.username_input.get()))
        self.password_input.delete(0,len(self.password_input.get()))


        


class User_Screen(ctk.CTkFrame,App):
    def __init__(self, master:App):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text="Welcome User", text_color = 'white', font = ('Arial', 40, 'bold'))
        self.label.grid(column = 0, row = 0, pady = 10)


def main():
    app = App()
    app.mainloop()

if __name__=='__main__':
    main()
