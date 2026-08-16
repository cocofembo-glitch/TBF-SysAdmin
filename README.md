# TBF-SysAdmin v5.0 ULTIMATE

Легкий та потужний консольний комбайн для експрес-діагностики та обслуговування пристрою в Termux / NetHunter без необхідності Root-прав.

## 🚀 Особливості
* **Rich Boot Sequence:** Анімована фаза ініціалізації з прогрес-барами та системними спінерами.
* **Classic TUI Interface:** Візуальне діалогове меню в стилі `dialog/whiptail` з можливістю мультивибору функцій.
* **100% Non-Root:** Всі 10 системних утиліт працюють у звичайному режимі користувача.

## 🛠️ Функціонал
1. **System Memory & Storage:** Аналіз накопичувача та доступних розділів.
2. **Public IP & Network Info:** Визначення зовнішньої IP-адреси.
3. **Local Interfaces:** Моніторинг активних мережевих карт (IPv4/IPv6).
4. **Latency Benchmark:** Тест затримки мережі до Google DNS.
5. **Open Ports Scanner:** Перевірка локальних портів, що прослуховуються.
6. **CPU & Thermal Status:** Перевірка датчиків температури та системного Uptime.
7. **Cache Cleanup:** Безпечне видалення тимчасових файлів із `$TMPDIR` та `~/.cache`.
8. **Process Manager:** Перевірка активних фонових Python-процесів.
9. **ARP Network Scanner:** Сканування сусідніх пристроїв у локальній мережі.
10. **Environment Inspection:** Виведення системних змінних та інформації про ядро.

## 📦 Встановлення та запуск

```bash
pkg update && pkg install python git -y
git clone https://github.com/cocofembo-glitch/TBF-SysAdmin.git (https://github.com/cocofembo-glitch/TBF-SysAdmin.git)
cd TBF-SysAdmin
pip install -r requirements.txt
python3 tbf_control.py
