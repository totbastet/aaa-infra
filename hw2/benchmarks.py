import requests
import time
import numpy as np

# Конфиги
url = "http://localhost:8000/embed"
health = "http://localhost:8000/health"
test_text = {"text": "Фраза для замера метрик для модели rubert-mini-frida"}
N = 1000  # сколько раз будем стучаться


def start_bench():
    # Проверяем, жив ли сервис вообще
    try:
        r = requests.get(health)
        if r.status_code != 200:
            print("Сервис ответил ошибкой")
            return
    except:
        print("Не получается достучаться до порта")
        return

    print(f"Погнали! Делаем {N} запросов")

    # Один раз прогоняем вхолостую для прогрева
    requests.post(url, json=test_text)

    times = []
    t_start = time.time()

    for i in range(N):
        t1 = time.time()
        try:
            res = requests.post(url, json=test_text)
            if res.status_code == 200:
                t2 = time.time()
                times.append((t2 - t1) * 1000)  # переводим в мс
            else:
                print(f"Запрос {i} упал с кодом {res.status_code}")
        except Exception as err:
            print(f"Ошибка на {i} итерации: {err}")
            break

    t_end = time.time()

    # Считаем итоги
    total_sec = t_end - t_start
    rps = len(times) / total_sec

    print("\nРезультаты замеров:")
    print(f"Заняло времени: {total_sec:.2f} сек")
    print(f"RPS: {rps:.2f}")
    print(f"P50 (Медиана): {np.percentile(times, 50):.2f} мс")
    print(f"P95: {np.percentile(times, 95):.2f} мс")
    print(f"P99: {np.percentile(times, 99):.2f} мс")


if __name__ == "__main__":
    start_bench()