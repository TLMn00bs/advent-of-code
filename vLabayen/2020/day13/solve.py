with open('input.txt') as f:
	ts = int(f.readline()[:-1])
	ids = [int(id) for id in f.readline()[:-1].split(',') if id != 'x']

	wait_time = {}
	for id in ids:
		s = 0
		while ts > s: s += id
		wait_time[id] = s - ts

	min_wait = min(wait_time, key = wait_time.get)
#	print(min_wait * wait_time[min_wait])


with open('input.txt') as f:
	f.readline()

	# Ordenamos de mayor a menor intervalo de bus, para hacer los incrementos más rapido
	ids = sorted([(int(id), offset) for offset,id in enumerate(f.readline()[:-1].split(',')) if id != 'x'], key=lambda d: d[0], reverse=True)

	# Comenzamos realizando incrementos de 1 minuto
	ts, incr = 0, 1
	for interval, offset in ids:
		while ((ts + offset) % interval) != 0:
			ts += incr
		# Sabemos que para que se mantenga que el proximo ts sea valido para el bus actual, este ts debe estar
		# separado un numero entero de intervalos del bus
		# Como todos los intervalos son numeros primos, el minimo comun multiplo es el producto de intervalos
		incr *= interval
	print(ts)
