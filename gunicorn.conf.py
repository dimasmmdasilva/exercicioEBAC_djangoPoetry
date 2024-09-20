# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"  # Endereço IP e porta que o Gunicorn vai ouvir
workers = multiprocessing.cpu_count() * 2 + 1  # Fórmula recomendada para o número de workers
threads = 2  # Número de threads por worker
timeout = 30  # Tempo máximo, em segundos, antes de reiniciar um worker que não responde
loglevel = 'debug'  # Níveis de log: debug, info, warning, error, critical
errorlog = '-'  # Log erros no stderr
accesslog = '-'  # Log acessos no stdout
reload = True  # Recarrega automaticamente o código em desenvolvimento
