import requests

# https://www.1secmail.com/api/ - Email service used


class Email:
    def __init__(self) -> None:
        self.__address: str = self.__generate_email()[0]

    def __generate_email(self) -> list:
        url: str = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
        r: list = requests.get(url).json()
        return r

    def __check_mailbox(self) -> list:
        login, domain = self.__address.split("@")
        url: str = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        r: list = requests.get(url).json()
        return r

    def __fetch_message(self, id: int) -> list:
        login, domain = self.__address.split("@")
        url: str = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id}"
        r: list = requests.get(url).json()
        return r


if __name__ == "__main__":
    email = Email()
