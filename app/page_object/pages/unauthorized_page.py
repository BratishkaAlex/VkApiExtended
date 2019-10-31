from selenium.webdriver.common.by import By

from framework.base.base_page import BasePage
from framework.elements.button import Button
from framework.elements.input_field import InputField


class UnauthorizedPage(BasePage):
    def __init__(self):
        super().__init__(By.ID, "index_login")

    def type_login(self, login):
        InputField(By.ID, "index_email", "Login").send_keys(login)

    def type_password(self, password):
        InputField(By.ID, "index_pass", "Password").send_keys(password)

    def click_submit(self):
        Button(By.ID, "index_login_button", "Submit credentials").click()
