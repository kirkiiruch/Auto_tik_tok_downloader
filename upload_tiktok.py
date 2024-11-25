import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys


def upload_video_to_tiktok():
    # Настройки браузера Edge
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    service = Service(executable_path=r"C:\EdgeDriver\msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)

    try:
        # Открыть TikTok и загрузить cookies
        driver.get("https://www.tiktok.com/tiktokstudio/upload?lang=en")
        if os.path.exists("tiktok_cookies.pkl"):
            import pickle
            with open("tiktok_cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        driver.refresh()

        # Загрузка видео
        time.sleep(5)
        upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
        video_path = r"C:\Users\Кирка\PycharmProjects\AUTOMATIZATIONTT\video_parts\part_001.mp4"
        upload_input.send_keys(video_path)

        # Задержка на загрузку видео
        time.sleep(15)

        # Проверить, доступна ли кнопка "Опубликовать" и нажать на нее
        publish_button = driver.find_element(By.XPATH, "//button[contains(., 'Опубликовать')]")
        driver.execute_script("arguments[0].click();", publish_button)

        # Увеличенная задержка для завершения публикации
        time.sleep(60)

        print("Видео успешно загружено на TikTok.")

    except Exception as e:
        print(f"Произошла ошибка при загрузке видео: {e}")

    finally:
        # Не закрывать браузер автоматически, чтобы можно было проверить
        input("Нажмите Enter для закрытия браузера...")
        driver.quit()


# Запуск функции загрузки видео

