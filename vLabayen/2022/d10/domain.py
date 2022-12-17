import typing
from dataclasses import dataclass
from collections import deque

@dataclass
class Register:
	X: int

	def add(self, value: int):
		self.X += value
		return self

ExecType = typing.Callable[[Register], None]
ADDX = lambda value: (lambda register: register.add(value))
NOOP = lambda      : (lambda register: None)

@dataclass
class Program:
	instructions: typing.Deque[ExecType]
	register: Register

	@staticmethod
	def from_lines(lines: typing.List[str]):
		''' Returns a Program from it's text definition
		
		>>> Program.from_lines([
		...		'noop',
		...		'addx 3',
		...		'addx -5',
		... ])
		Program(instructions=..., register=Register(X=1))
		'''
		instructions = deque()
		for line in lines:
			if line == 'noop':
				instructions.append(NOOP())
				continue

			if line.startswith('addx'):
				instructions.extend([
					NOOP(),
					ADDX(int(line.split(' ')[1]))
				])
				continue

		return Program(instructions, Register(1))

	def exec(self, cycles: int):
		''' Execute the given number of cycles
		
		>>> p = Program.from_lines([
		...		'noop',
		...		'addx 3',
		...		'addx -5',
		... ])
		>>> p.exec(1)
		Program(instructions=..., register=Register(X=1))
		>>> p.exec(1)
		Program(instructions=..., register=Register(X=1))
		>>> p.exec(1)
		Program(instructions=..., register=Register(X=4))
		>>> p.exec(1)
		Program(instructions=..., register=Register(X=4))
		>>> p.exec(1)
		Program(instructions=..., register=Register(X=-1))

		>>> p = Program.from_lines([
		...		'noop',
		...		'addx 1',
		...		'addx 1',
		...		'addx 1',
		...		'addx 1',
		...		'addx 1',
		... ])
		>>> p.exec(5)
		Program(instructions=..., register=Register(X=3))
		>>> p.exec(5)
		Program(instructions=..., register=Register(X=5))
		'''
		for _ in range(cycles):
			self.instructions.popleft()(self.register)

		return self

if __name__ == '__main__':
	import doctest
	doctest.testmod(optionflags=doctest.ELLIPSIS)