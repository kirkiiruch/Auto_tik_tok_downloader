import pickle
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Путь к EdgeDriver
edge_driver_path = r'C:\EdgeDriver\msedgedriver.exe'

# Настройки для Edge
options = Options()

# Устанавливаем пользовательский агент как в обычном браузере Edge
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36 Edg/131.0.2903.63")

# Отключаем режим автоматизации
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Указываем использование пользовательского профиля (опционально)
# profile_path = r"C:\Users\Кирка\AppData\Local\Microsoft\Edge\User Data\Default"  # Замените на ваш профиль, если необходимо
# options.add_argument(f"user-data-dir={profile_path}")

# Создаем объект Service для EdgeDriver
service = Service(edge_driver_path)

# Создаем экземпляр браузера Edge с указанными опциями
driver = webdriver.Edge(service=service, options=options)

# Убираем свойство webdriver, чтобы не показывать автоматизацию
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Используем уже открытую сессию
driver.get("https://www.tiktok.com/")  # Переходим на TikTok

# Ждем, пока вы вручную войдете в аккаунт
input("Пожалуйста, подтвердите, что вы вошли в TikTok вручную, и нажмите Enter для продолжения...")

# Сохранение куки-файлов
with open("tiktok_cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)

print("Куки-файлы успешно сохранены.")

# Закрываем браузер после сохранения куки
driver.quit()
