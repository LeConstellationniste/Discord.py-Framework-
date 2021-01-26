from datetime import datetime
try:
	from colorama import Fore, init
	colorama_imported = True
except ImportError:
	colorama_imported = False


def datetime_log() -> str:
	current_datetime = datetime.now()
	return current_datetime.strftime("%Y-%m-%d to %H:%M:%S")


class Logs:
	if colorama_imported:
		init()  # init colorama for Window
		color_debug = Fore.CYAN
		color_info = Fore.WHITE
		color_warning = Fore.YELLOW
		color_error = Fore.RED
		color_success = Fore.GREEN

	@staticmethod
	def info(msg: str, path_save: str = None):
		msg_log = f"[{datetime_log()}][INFO] {msg}"
		if colorama_imported:
			print(Logs.color_info + msg_log + Fore.RESET)
		else:
			print(msg_log)
		if path_save is not None:
			with open(path_save, 'a') as f:
				f.write(msg_log+"\n")

	@staticmethod
	def debug(msg: str, path_save: str = None):
		msg_log = f"[{datetime_log()}][DEBUG] {msg}"
		if colorama_imported:
			print(Logs.color_debug + msg_log + Fore.RESET)
		else:
			print(msg_log)
		if path_save is not None:
			with open(path_save, 'a') as f:
				f.write(msg_log+"\n")

	@staticmethod
	def error(msg: str, path_save: str = None):
		msg_log = f"[{datetime_log()}][ERROR] {msg}"
		if colorama_imported:
			print(Logs.color_error + msg_log + Fore.RESET)
		else:
			print(msg_log)
		if path_save is not None:
			with open(path_save, 'a') as f:
				f.write(msg_log+"\n")

	@staticmethod
	def warning(msg: str, path_save: str = None):
		msg_log = f"[{datetime_log()}][WARNING] {msg}"
		if colorama_imported:
			print(Logs.color_warning + msg_log + Fore.RESET)
		else:
			print(msg_log)
		if path_save is not None:
			with open(path_save, 'a') as f:
				f.write(msg_log+"\n")

	@staticmethod
	def success(msg: str, path_save: str = None):
		msg_log = f"[{datetime_log()}][SUCCESS] {msg}"
		if colorama_imported:
			print(Logs.color_success + msg_log + Fore.RESET)
		else:
			print(msg_log)
		if path_save is not None:
			with open(path_save, 'a') as f:
				f.write(msg_log+"\n")
