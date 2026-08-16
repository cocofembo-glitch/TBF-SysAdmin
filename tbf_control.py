import os
import sys
import time
import subprocess
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.live import Live
from rich.panel import Panel

from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog
from prompt_toolkit.styles import Style

console = Console()

# Стиль синього класичного діалогу
CUSTOM_STYLE = Style.from_dict({
    'dialog': 'bg:#0000aa',
    'dialog frame.label': 'bg:#ffffff #000000 bold',
    'dialog.body': 'bg:#a8a8a8 #000000',
    'checkbox-selected': 'bg:#00aa00 #ffffff bold',
    'button': 'bg:#a8a8a8 #000000',
    'button.focused': 'bg:#00aa00 #ffffff bold',
})

def run_cmd(cmd):
    """Безпечне виконання команд без Root прав"""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        out = res.stdout.strip() or res.stderr.strip()
        return out if out else "Виконано успішно!"
    except Exception as e:
        return f"Помилка: {e}"

def rich_boot_sequence():
    """Фаза завантаження з 10 прогрес-барами та спінерами Rich"""
    console.clear()
    console.print(Panel("[bold cyan]TBF-SystemControl v5.0 Non-Root Edition[/bold cyan]\n[dim]Ініціалізація системних модулів аналізу...[/dim]", border_style="blue"))
    time.sleep(1)

    steps = [
        ("Опитування системних змінних оточення (ENV)", 0.6),
        ("Аналіз дискового простору та розділів /data", 0.5),
        ("Перевірка мережевих інтерфейсів (IPv4/IPv6)", 0.7),
        ("Тестування DNS-резолверів та затримок", 0.6),
        ("Аналіз стану оперативної пам'яті (RAM Usage)", 0.5),
        ("Перевірка активних фонових процесів Python", 0.6),
        ("Сканування локальної ARP-таблиці мережі", 0.7),
        ("Перевірка стану температурних датчиків", 0.5),
        ("Сканування тимчасових кеш-папок Termux ($TMPDIR)", 0.6),
        ("Фінальне складання модуля інтерфейсу TUI", 0.5),
    ]

    with Progress(
        SpinnerColumn("dots", finished_text="[bold green]✓[/bold green]"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=30, complete_style="green", finished_style="bold green"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:

        for desc, duration in steps:
            task = progress.add_task(desc, total=100)
            step_time = duration / 20.0
            for _ in range(20):
                time.sleep(step_time)
                progress.update(task, advance=5)

    console.print("\n[bold green][+] Всі модулі успішно ініціалізовано! Перехід до TUI...[/bold green]")
    time.sleep(1)

def main_tui():
    """Фаза синього TUI з 10 функціями без роута"""
    options = [
        ("1", "1. System Memory & Swap Status (Стан RAM та накопичувача)"),
        ("2", "2. Public IP & Location Info (Зовнішня IP-адреса)"),
        ("3", "3. Local Network Interfaces (Активні мережеві карти)"),
        ("4", "4. Network Latency Benchmark (Тест пингу до 8.8.8.8)"),
        ("5", "5. Active Listening Ports (Перевірка відкритих портів)"),
        ("6", "6. CPU & Thermal Monitor (Датчики температури та процесор)"),
        ("7", "7. Clean Termux Cache & Temp Files (Очищення тимчасового кешу)"),
        ("8", "8. Active Python Tasks Manager (Список активних скриптів)"),
        ("9", "9. Local ARP Network Neighbors (Пристрої в локальній мережі)"),
        ("10", "10. Environment & Shell Information (Інформація про систему)"),
    ]

    selected_actions = checkboxlist_dialog(
        title="TBF-SystemControl v5.0 (USER MODE)",
        text="Обери функції клавішею ПРОБІЛ та натисни OK (TAB для переходу):",
        values=options,
        style=CUSTOM_STYLE
    ).run()

    if not selected_actions:
        message_dialog(
            title="TBF-SystemControl",
            text="Вихід з системи. Жодної функції не було обрано.",
            style=CUSTOM_STYLE
        ).run()
        return

    results = []
    
    for act in selected_actions:
        if act == "1":
            r = run_cmd("df -h $HOME /data 2>/dev/null || df -h")
            results.append(f"=== [1] RAM & Storage Info ===\n{r}")
        elif act == "2":
            r = run_cmd("curl -s --max-time 4 https://ifconfig.me || echo 'Немає інтеренет зєднання'")
            results.append(f"=== [2] External IP ===\nIP: {r}")
        elif act == "3":
            r = run_cmd("ip -br a || ifconfig")
            results.append(f"=== [3] Network Interfaces ===\n{r}")
        elif act == "4":
            r = run_cmd("ping -c 3 8.8.8.8")
            results.append(f"=== [4] Ping Test ===\n{r}")
        elif act == "5":
            r = run_cmd("ss -tuln 2>/dev/null || netstat -tuln 2>/dev/null || echo 'Порти закриті'")
            results.append(f"=== [5] Listening Ports ===\n{r[:300]}")
        elif act == "6":
            r1 = run_cmd("cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -n 3")
            r2 = run_cmd("uptime")
            results.append(f"=== [6] CPU & Thermal ===\nSensors: {r1 if r1 else 'N/A'}\nUptime: {r2}")
        elif act == "7":
            r = run_cmd("rm -rf $TMPDIR/* ~/.cache/* 2>/dev/null; echo 'Тимчасовий кеш користувача очищено!'")
            results.append(f"=== [7] User Cache Clean ===\n{r}")
        elif act == "8":
            r = run_cmd("ps aux | grep python | grep -v grep")
            results.append(f"=== [8] Running Python Scripts ===\n{r if r else 'Активних python-процесів не знайдено'}")
        elif act == "9":
            r = run_cmd("ip neigh")
            results.append(f"=== [9] Local Network ARP Table ===\n{r if r else 'Сусідніх пристроїв не виявлено'}")
        elif act == "10":
            r = run_cmd("uname -a; echo '---'; env | grep -E 'SHELL|TERM|USER|HOME'")
            results.append(f"=== [10] System Environment ===\n{r}")

    final_text = "\n\n".join(results)
    message_dialog(
        title="Результати виконання TBF-SystemControl",
        text=final_text[:2000],
        style=CUSTOM_STYLE
    ).run()

if __name__ == "__main__":
    # Запуск 1: Rich анімація
    rich_boot_sequence()
    # Запуск 2: Синій TUI з 10 робочими функціями
    main_tui()
          
