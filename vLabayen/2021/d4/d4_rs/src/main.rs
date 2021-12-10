use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::vec::Vec;
use std::collections::HashSet;
use array2d::Array2D; //https://docs.rs/array2d/0.2.1/array2d/

fn read_file(filename: &String) -> (Vec<i32>, Vec<Array2D<i32>>) {
	let mut data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let numbers: Vec<i32> = data_gen.next().unwrap().unwrap().split(",").map(|n| n.parse::<i32>().unwrap()).collect();

	data_gen.next();	//Skip the first empty line

	let mut boards: Vec<Array2D<i32>> = Vec::new();
	let mut board: Array2D<i32> = Array2D::filled_with(0, 5, 5);
	for (i, line) in (&mut data_gen).enumerate() {
		let line = line.unwrap().trim().replace("  ", " ");
		if line == "" {
			boards.push(board);
			board = Array2D::filled_with(0i32, 5, 5);
			continue;
		}
		for (col, n) in line.split(" ").map(|n| n.parse::<i32>().unwrap()).enumerate() {
			board[(i % 6, col)] = n;
		}
	}
	boards.push(board);

	return (numbers, boards);
}

fn check_board(board: &Array2D<i32>, drawn_numbers: &HashSet<i32>) -> bool {
	if board.as_rows().iter().any(|row| row.iter().all(|&n| drawn_numbers.contains(&n))) { return true };
	if board.as_columns().iter().any(|col| col.iter().all(|&n| drawn_numbers.contains(&n))) { return true };
	return false;
}

fn get_unmarked(board: &Array2D<i32>, drawn_numbers: &HashSet<i32>) -> Vec<i32> {
	return board.as_row_major().iter().filter(|&n| !drawn_numbers.contains(&n)).cloned().collect();
}

fn p1(filename: &String) {
	let (numbers, boards) = read_file(filename);
	let mut drawn_numbers: HashSet<i32> = HashSet::new();

	for n in numbers {
		drawn_numbers.insert(n);
		for b in &boards {
			if check_board(&b, &drawn_numbers) {
				let unmarked: Vec<i32> = get_unmarked(&b, &drawn_numbers);
				println!("Score: {}", unmarked.iter().sum::<i32>() * n);
				return;
			}
		}
	}
}

fn p2(filename: &String) {
	let (numbers, boards) = read_file(filename);
	let mut drawn_numbers: HashSet<i32> = HashSet::new();

	let mut ignore_boards: HashSet<usize> = HashSet::new();
	let n_boards = boards.len();
	for n in numbers {
		drawn_numbers.insert(n);
		let use_idx: Vec<usize> = (0..n_boards).into_iter().filter(|idx| !ignore_boards.contains(idx)).collect();
		for i in use_idx {
			let b = &boards[i];
			if check_board(&b, &drawn_numbers) {
				if n_boards - ignore_boards.len() == 1 {
					let unmarked: Vec<i32> = get_unmarked(&b, &drawn_numbers);
					println!("Score: {}", unmarked.iter().sum::<i32>() * n);
					return;
				}
				ignore_boards.insert(i);
			}
		}
	}
}

fn main() {
	let args: Vec<String> = env::args().collect();
	if args.len() != 2 {
		println!("Usage: {} <filename>", args[0]);
		process::exit(1);
	}

	let filename = &args[1];
	p1(filename);
	p2(filename);
}
