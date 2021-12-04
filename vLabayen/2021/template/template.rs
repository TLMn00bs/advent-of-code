use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn p1(filename: &String) {
	let mut data_gen = BufReader::new(File::open(filename).unwrap()).lines();
}

fn p2(filename: &String) {
	let mut data_gen = BufReader::new(File::open(filename).unwrap()).lines();
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
