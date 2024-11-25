from selenium import webdriver
from selenium.webdriver.edge.service import Service

# Путь к EdgeDriver
edge_driver_path = r'C:\EdgeDriver\msedgedriver.exe'

# Создаем объект Service для EdgeDriver
service = Service(edge_driver_path)

# Создаем экземпляр браузера Edge
driver = webdriver.Edge(service=service)

# Переходим на сайт TikTok или любой другой сайт
driver.get("https://www.tiktok.com/")

# Удаляем все куки
driver.delete_all_cookies()

print("Все куки удалены.")

# Закрываем браузер
driver.quit()
