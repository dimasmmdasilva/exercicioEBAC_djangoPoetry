import multiprocessing

bind = "0.0.0.0:8000"
workers = 2  # Um número fixo pequeno para testes
threads = 2
timeout = 30
loglevel = 'debug'
errorlog = '-'
accesslog = '-'
reload = False  # Desative em produção
