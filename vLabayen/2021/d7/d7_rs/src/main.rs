use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::cmp::{min, max};

fn p1(filename: &String) {
	let mut data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let hpositions: Vec<i32> = data_gen.next().unwrap().unwrap().split(",").map(|n| n.parse::<i32>().unwrap()).collect();
	let (min_h, max_h) = (*hpositions.iter().min().unwrap(), *hpositions.iter().max().unwrap());
	let best_fuel = (min_h..(max_h + 1)).into_iter().map(|h| hpositions.iter().map(|hp| (hp - h).abs()).sum::<i32>()).min().unwrap();
	println!("{}", best_fuel);
}

fn fuel_usage(start: i32, end: i32) -> i32 {
	let (min_v, max_v) = (min(start, end), max(start, end));
	return (1..(max_v - min_v + 1)).into_iter().sum::<i32>();
}

fn p2(filename: &String) {
	let mut data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let hpositions: Vec<i32> = data_gen.next().unwrap().unwrap().split(",").map(|n| n.parse::<i32>().unwrap()).collect();
	let (min_h, max_h) = (*hpositions.iter().min().unwrap(), *hpositions.iter().max().unwrap());
	let best_fuel = (min_h..(max_h + 1)).into_iter().map(|h| hpositions.iter().map(|&hp| fuel_usage(hp, h)).sum::<i32>()).min().unwrap();
	println!("{}", best_fuel);
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
