from datetime import datetime
try:
	from colorama import Fore, init
	colorama_imported = True
except ImportError:
	colorama_imported = False


def datetime_log(date_format: str = "%Y-%m-%d to %H:%M:%S") -> str:
	current_datetime = datetime.now()
	return current_datetime.strftime(date_format)


class Logs:
	date_fmt = "%Y-%m-%d to %H:%M:%S"
	path_info = None
	path_debug = None
	path_warninge = None
	path_error = None
	path_success = None
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
		elif Logs.path_info is not None:
			with open(Logs.path_info, 'a') as f:
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
		elif Logs.path_debug is not None:
			with open(Logs.path_debug, 'a') as f:
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
		elif Logs.path_error is not None:
			with open(Logs.path_error, 'a') as f:
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
		elif Logs.path_warning is not None:
			with open(Logs.path_warning, 'a') as f:
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
		elif Logs.path_success is not None:
			with open(Logs.path_success, 'a') as f:
				f.write(msg_log+"\n")
