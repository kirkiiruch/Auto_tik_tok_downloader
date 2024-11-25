import subprocess
import os
import yt_dlp
import whisper
from upload_tiktok import upload_video_to_tiktok
import time

def download_video(url, output_path="downloaded_video.mp4"):
    """
    Скачивает видео с YouTube или другого поддерживаемого сайта.

    :param url: Ссылка на видео
    :param output_path: Путь для сохранения видео
    """
    ydl_opts = {
        'format': 'best',  # Выбирает лучшее качество
        'outtmpl': output_path,  # Имя сохраненного файла
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Видео скачано и сохранено как {output_path}")
    except Exception as e:
        print(f"Ошибка при скачивании видео: {e}")

def generate_subtitles(input_file, output_srt="subtitles.srt"):
    """
    Генерирует субтитры из видео с использованием OpenAI Whisper и сохраняет их в формате SRT.

    :param input_file: Путь к видео
    :param output_srt: Имя файла SRT для сохранения
    """
    model = whisper.load_model("base")  # Загружаем модель
    result = model.transcribe(input_file)

    with open(output_srt, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            # Форматируем временные метки в SRT
            f.write(f"{segment['id'] + 1}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(f"{text}\n\n")
    print(f"Субтитры сохранены в {output_srt}")

def format_time(seconds):
    """
    Форматирует время в формате SRT.
    """
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    return f"{hours:02}:{minutes % 60:02}:{seconds % 60:02},{milliseconds:03}"

def crop_video_for_tiktok(input_video, output_video="cropped_video.mp4"):
    """
    Обрезает видео для создания формата, подходящего для TikTok (9:16).

    :param input_video: Исходное видео
    :param output_video: Имя выходного обрезанного видео
    """
    command = [
        r"C:\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe",  # Полный путь к ffmpeg
        "-i", input_video,
        "-vf", "crop=ih*9/16:ih",  # Обрезка видео до формата 9:16 (используется высота как основа)
        output_video
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Видео обрезано и сохранено как {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при обрезке видео: {e}")

def add_subtitles_with_style(input_video, subtitles_file, output_video="video_with_subtitles.mp4"):
    """
    Добавляет субтитры к видео с использованием FFmpeg и стилизует их через drawtext.

    :param input_video: Исходное видео
    :param subtitles_file: Файл субтитров (SRT)
    :param output_video: Имя выходного видео
    """
    # Команда FFmpeg для добавления субтитров
    command = [
        r"C:\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe",  # Полный путь к ffmpeg
        "-i", input_video,
        "-vf", f"subtitles={subtitles_file},drawtext=textfile={subtitles_file}:fontcolor=yellow:fontsize=30:borderw=3:bordercolor=black",
        "-c:a", "copy",  # Копирование аудио
        output_video
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Видео с субтитрами сохранено как {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при добавлении субтитров: {e}")

def split_video_with_reencoding(input_file, output_folder, part_duration):
    """
    Разделяет видео на равные части с перекодировкой, чтобы гарантировать точное разделение.

    :param input_file: Путь к исходному видео
    :param output_folder: Папка для сохранения частей
    :param part_duration: Длительность каждой части (в секундах)
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получение информации о длительности видео
    try:
        result = subprocess.run(
            [
                r"C:\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe",  # Полный путь к ffmpeg
                "-i", input_file,
                "-hide_banner",
                "-f", "null",
                "-"
            ],
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении информации о видео: {e}")
        return

    # Извлечение общей длительности видео
    duration_line = [line for line in result.stderr.split('\n') if "Duration" in line]
    if not duration_line:
        print("Не удалось определить длину видео.")
        return

    duration = duration_line[0].split(",")[0].split("Duration:")[1].strip()
    hours, minutes, seconds = map(float, duration.split(":"))
    total_seconds = int(hours * 3600 + minutes * 60 + seconds)

    # Деление видео на равные части
    for i in range(total_seconds // part_duration + (1 if total_seconds % part_duration else 0)):
        start_time = i * part_duration
        output_file = os.path.join(output_folder, f"part_{i:03d}.mp4")

        command = [
            r"C:\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe",  # Полный путь к ffmpeg
            "-i", input_file,
            "-ss", str(start_time),
            "-t", str(part_duration),
            "-c:v", "libx264",  # Кодек для перекодировки
            "-c:a", "aac",  # Аудиокодек
            output_file
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Сохранён файл: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при создании сегмента {output_file}: {e}")

# Пример использования

# Устанавливаем путь к ffmpeg в переменную окружения
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-7.1-essentials_build\bin"

# Скачивание видео
video_url = "https://m.youtube.com/watch?v=cg32kTwXEiw&pp=ygU4MTUg0YHQtdC60YPQvdC00L3QvtC1INGA0LDQt9Cz0L7QstC-0YDQvdC-0LUg0LLQuNC00LXQviA%3D"
download_video(video_url)

# Генерация субтитров
input_video = "downloaded_video.mp4"
subtitles_file = "subtitles.srt"
generate_subtitles(input_video, subtitles_file)

# Обрезка видео для TikTok (9:16)
cropped_video = "cropped_video.mp4"
crop_video_for_tiktok(input_video, cropped_video)

# Добавление субтитров к видео с использованием стилизованного текста
video_with_subtitles = "video_with_subtitles.mp4"
add_subtitles_with_style(cropped_video, subtitles_file, video_with_subtitles)

# Разделение видео на части
output_folder = "video_parts"
part_duration = 20  # Длительность каждой части (в секундах)
split_video_with_reencoding(video_with_subtitles, output_folder, part_duration)

#upload_video_to_tiktok()