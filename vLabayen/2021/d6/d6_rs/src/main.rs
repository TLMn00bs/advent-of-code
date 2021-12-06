use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::vec::Vec;

fn p1(filename: &String) {
	let mut data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let fishes_numbers: Vec<i32> = data_gen.next().unwrap().unwrap().split(",").map(|n| n.parse::<i32>().unwrap()).collect();

	let mut fishes_counter: [i32; 9] = [0, 0, 0, 0, 0, 0, 0, 0, 0];
	for n in fishes_numbers {
		fishes_counter[n as usize] += 1;
	}

	for _day in 0..80 {
		let num_zeros = fishes_counter[0];
		for idx in 0..8 {
			fishes_counter[idx] = fishes_counter[idx + 1];
		}
		fishes_counter[6] += num_zeros;
		fishes_counter[8] = num_zeros;
	}

	println!("{}", fishes_counter.iter().sum::<i32>());
}

fn p2(filename: &String) {
	let mut data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let fishes_numbers: Vec<i32> = data_gen.next().unwrap().unwrap().split(",").map(|n| n.parse::<i32>().unwrap()).collect();

	let mut fishes_counter: [u128; 9] = [0, 0, 0, 0, 0, 0, 0, 0, 0];
	for n in fishes_numbers {
		fishes_counter[n as usize] += 1;
	}

	for _day in 0..256 {
		let num_zeros = fishes_counter[0];
		for idx in 0..8 {
			fishes_counter[idx] = fishes_counter[idx + 1];
		}
		fishes_counter[6] += num_zeros;
		fishes_counter[8] = num_zeros;
	}

	println!("{}", fishes_counter.iter().sum::<u128>());
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
