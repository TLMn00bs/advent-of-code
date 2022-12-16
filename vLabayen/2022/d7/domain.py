import typing
import os
from dataclasses import dataclass

def split_commands_into_blocks(lines: typing.List[str]) -> typing.List[typing.List[str]]:
	''' Split input lines in blocks of commands & their output
	
	>>> split_commands_into_blocks([
	...		'$ cd /',
	...		'$ ls',
	...		'dir a',
	...		'14848514 b.txt',
	...		'8504156 c.dat',
	...		'dir d',
	...		'$ cd a',
	...		'$ ls',
	...		'dir e',
	...		'29116 f',
	...		'2557 g',
	...		'62596 h.lst',
	...		'$ cd e',
	...		'$ ls',
	...		'584 i',
	...		'$ cd ..',
	...		'$ cd ..',
	...		'$ cd d',
	...		'$ ls',
	...		'4060174 j',
	...		'8033020 d.log',
	...		'5626152 d.ext',
	...		'7214296 k',
	...	])
	[['$ cd /', '$ ls', 'dir a', '14848514 b.txt', '8504156 c.dat', 'dir d'], ['$ cd a', '$ ls', 'dir e', '29116 f', '2557 g', '62596 h.lst'], ['$ cd e', '$ ls', '584 i'], ['$ cd ..', '$ cd ..', '$ cd d', '$ ls', '4060174 j', '8033020 d.log', '5626152 d.ext', '7214296 k']]
	'''
	blocks = []
	current_block = []
	prev_line_was_command = True
	for line in lines:
		is_command = line.startswith('$')

		if not prev_line_was_command and is_command:
			blocks.append(current_block)
			current_block = []

		current_block.append(line)
		prev_line_was_command = is_command

	if len(current_block) > 0: blocks.append(current_block)
	return blocks

def append_path(current, to_add):
	is_absolute = lambda path: path.startswith('/')
	if is_absolute(to_add): return to_add

	if not current.endswith('/'):
		return f'{current}/{to_add}'

	return f'{current}{to_add}'

def extract_block_path(block: typing.List[str], start_path = '/') -> str:
	''' Given a block, returns the location where the ls command is executed
	
	>>> extract_block_path(['$ cd /', '$ ls', 'dir a', '14848514 b.txt', '8504156 c.dat', 'dir d'])
	'/'
	>>> extract_block_path(['$ cd a', '$ ls', 'dir e', '29116 f', '2557 g', '62596 h.lst'])
	'/a'
	>>> extract_block_path(['$ cd e', '$ ls', '584 i'], start_path='/a/')
	'/a/e'
	>>> extract_block_path(['$ cd ..', '$ cd ..', '$ cd d', '$ ls', '4060174 j', '8033020 d.log', '5626152 d.ext', '7214296 k'], start_path='/a/e/')
	'/d'
	'''
	cds_arg = [command.split('$ cd ')[1] for command in block if command.startswith('$ cd')]
	if len(cds_arg) == 0: return start_path

	current_path = start_path
	for move_to in cds_arg:
		current_path = append_path(current_path, move_to)

	return os.path.realpath(current_path)

def extract_block_output(block: typing.List[str]) -> typing.List[str]:
	''' Extract the ls output of a command block
	
	>>> extract_block_output(['$ cd /', '$ ls', 'dir a', '14848514 b.txt', '8504156 c.dat', 'dir d'])
	['dir a', '14848514 b.txt', '8504156 c.dat', 'dir d']
	>>> extract_block_output(['$ cd a', '$ ls', 'dir e', '29116 f', '2557 g', '62596 h.lst'])
	['dir e', '29116 f', '2557 g', '62596 h.lst']
	>>> extract_block_output(['$ cd e', '$ ls', '584 i'])
	['584 i']
	>>> extract_block_output(['$ cd ..', '$ cd ..', '$ cd d', '$ ls', '4060174 j', '8033020 d.log', '5626152 d.ext', '7214296 k'])
	['4060174 j', '8033020 d.log', '5626152 d.ext', '7214296 k']
	'''
	return [line for line in block if not line.startswith('$')]

@dataclass
class File:
	name: str
	size: int

@dataclass
class Dir:
	path: str

def parse_output_line(line: str, location_path: str) -> typing.Union[File, Dir]:
	''' Parses output lines

	>>> parse_output_line('14848514 b.txt', '/')
	File(name='b.txt', size=14848514)
	>>> parse_output_line('8504156 c.dat', '/')
	File(name='c.dat', size=8504156)
	>>> parse_output_line('dir d', '/')
	Dir(path='/d')
	>>> parse_output_line('dir d', '/a')
	Dir(path='/a/d')
	'''
	if line.startswith('dir'):
		_, name = line.split(' ')
		return Dir(append_path(location_path, name))

	size, name = line.split(' ')
	return File(name, int(size))

if __name__ == '__main__':
	import doctest
	doctest.testmod()