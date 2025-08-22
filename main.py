from pos_app import show_main_pos
from registeration import show_login

def launch_main_app(login_window):
    login_window.withdraw()  # close login window first
    show_main_pos()


if __name__ == "__main__":
    show_login(callback_after_login=launch_main_app)
