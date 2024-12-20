import os
import zipfile
import json
import toml
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

# python emulator_shell.py config.toml


class ShellEmulator:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.username = self.config['user']['name']
        self.computername = self.config['user']['computer']
        self.zip_path = self.config['filesystem']['path']
        self.log_file = self.config['log']['path']
        self.cwd = None
        self.temp_dir = tempfile.mkdtemp()
        self.log_data = []
        self.init_filesystem()

    def load_config(self, path):
        try:
            with open(path, 'r') as file:
                return toml.load(file)
        except FileNotFoundError:
            print(f"Config file {path} not found.")
            exit(1)

    def init_filesystem(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
        self.cwd = Path(self.temp_dir)

    def log_action(self, action):
        self.log_data.append({
            "user": self.username,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })

    def save_log(self):
        with open(self.log_file, 'w') as file:
            json.dump(self.log_data, file, indent=4)

    def ls(self):
        items = os.listdir(self.cwd)
        print("\n".join(items))
        self.log_action("ls")

    def cd(self, path):
        target_path = (self.cwd / path).resolve()
        if target_path.exists() and target_path.is_dir():
            self.cwd = target_path
            self.log_action(f"cd {path}")
        else:
            print(f"cd: no such file or directory: {path}")

    def touch(self, filename):
        file_path = self.cwd / filename
        file_path.touch()
        self.log_action(f"touch {filename}")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.log_action("clear")

    def exit(self):
        self.log_action("exit")
        self.save_log()
        try:
            shutil.rmtree(self.temp_dir)
        except FileNotFoundError:
            pass  # Временная папка может быть удалена в тестах
        if hasattr(self, "_testing"):
            raise SystemExit(0)  # Исключение для тестовой среды
        exit(0)

    def run(self):
        while True:
            # Убираем префикс temp_dir из cwd
            prompt = f"{self.username}@{self.computername}:{self.cwd.as_posix().replace(self.temp_dir, '')}$ "
            command = input(prompt).strip()
            if command == "exit":
                self.exit()
            elif command == "ls":
                self.ls()
            elif command.startswith("cd "):
                _, path = command.split(maxsplit=1)
                self.cd(path)
            elif command.startswith("touch "):
                _, filename = command.split(maxsplit=1)
                self.touch(filename)
            elif command == "clear":
                self.clear()
            else:
                print(f"{command}: command not found")


# To execute the shell emulator
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("config", help="Path to the configuration file (TOML format)")
    args = parser.parse_args()

    shell = ShellEmulator(args.config)
    shell.run()
