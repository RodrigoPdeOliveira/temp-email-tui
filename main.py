import requests
import os

# https://www.1secmail.com/api/ - Email service used


class Email:
    def __init__(self) -> None:
        self._address: str = self.__generate_email()[0]
        self._mailbox = self._update_mailbox()

    def __generate_email(self) -> list:
        url: str = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
        r: list = requests.get(url).json()
        return r

    def _update_mailbox(self) -> list[dict]:
        login, domain = self._address.split("@")
        url: str = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        r: list[dict] = requests.get(url).json()
        return r

    def _fetch_message(self, id: int) -> dict:
        login, domain = self._address.split("@")
        url: str = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id}"
        r: dict = requests.get(url).json()
        return r


class Interface():
    def __init__(self) -> None:
        self.__width, self.__height = os.get_terminal_size()
        self.__email = Email()
        self.__response = {}

    def main_menu(self):
        self.__response = {"1": self.mailbox, "2": self.new_address, "q": exit, "Q": exit}

        clear()
        # Email address bar
        print("+", "-" * (self.__width - 4), "+")
        print("|", "".center(self.__width - 4), "|")
        print("|", "-= Temporary Email Interface =-".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("|", f"Email address: {self.__email._address}".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("+", "-" * (self.__width - 4), "+")
        # Options bar
        print("|", "".center(self.__width - 4), "|")
        print("|", "1) - Mailbox".center(self.__width - 4), "|")
        print("|", "2) - Generate new address".center(self.__width - 4), "|")
        print("|", "Q) - Exit".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("+", "-" * (self.__width - 4), "+")

        res = str(input('> '))
        selected = self.__response.get(res, None)

        if selected is None:
            self.main_menu()
        else:
            selected()

    def mailbox(self):
        self.__response = {"1": self.mailbox, "2": self.open_message, "q": exit, "Q": exit, "0": self.main_menu}
        self.__email._mailbox = self.__email._update_mailbox()

        clear()
        # Mailbox bar
        print("+", "-" * (self.__width - 4), "+")
        print("|", "".center(self.__width - 4), "|")
        print("|", "-= Temporary Email Interface =-".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("|", f"You have {len(self.__email._mailbox)} mail(s)".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("+", "-" * (self.__width - 4), "+")
        # Mail logic
        for index, mail in enumerate(self.__email._mailbox):
            print("|", "".center(self.__width - 4), "|")
            print("|", f"{index}) - Subject: {mail['subject']}".center(self.__width - 4), "|")
        # Options bar
        print("|", "".center(self.__width - 4), "|")
        print("|", "1) - Update mailbox".center(self.__width - 4), "|")
        print("|", "2) - Open message".center(self.__width - 4), "|")
        print("|", "0) - Return to main menu".center(self.__width - 4), "|")
        print("|", "Q) - Exit".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("+", "-" * (self.__width - 4), "+")

        res = str(input('> '))
        selected = self.__response.get(res, None)

        if selected is None:
            self.mailbox()
        else:
            selected()

    def new_address(self):
        self.__email = Email()
        self.main_menu()

    def open_message(self):
        res = input('Type the number shown before the desired message >> ')

        try:
            id = self.__email._mailbox[int(res)]['id']
        except IndexError or TypeError:
            self.mailbox()

        message = self.__email._fetch_message(id)

        # Message bar
        print("+", "-" * (self.__width - 4), "+")
        print("|", "".center(self.__width - 4), "|")
        print("|", f"{message['subject']}".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("|", f"{message['date']}".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("|", f"{message['from']}".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("|", f"{message['textBody']}".center(self.__width - 4), "|")
        print("|", "".center(self.__width - 4), "|")
        print("+", "-" * (self.__width - 4), "+")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    interface = Interface()
    interface.main_menu()
