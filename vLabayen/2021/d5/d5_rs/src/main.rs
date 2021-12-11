use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::cmp::{min, max};
use std::collections::HashMap;
use itertools::{Itertools, iproduct, izip};
use num::iter::range_step_inclusive;

fn p1(filename: &String) {
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();

	let mut vents_count: HashMap<(i32, i32), i32> = HashMap::new();
	for line in data_gen {
		let ((x1,y1),(x2,y2)) = line.unwrap().splitn(2, " -> ").map(|coords| coords.splitn(2, ",").map(|n| n.parse::<i32>().unwrap()).collect_tuple().unwrap()).collect_tuple().unwrap();
		if !(x1 == x2 || y1 == y2) { continue; }
		let (x_min, x_max, y_min, y_max) = (min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2));

		for (x, y) in iproduct!(x_min..(x_max + 1), y_min..(y_max + 1)) {
			if let Some(n) = vents_count.get_mut(&(x, y)) { *n = *n + 1; }
			else { vents_count.insert((x, y), 1); }
		}
	}

	let mut num_dangerous_vents = 0;
	for (_,_) in vents_count.iter().filter(|(_k,&v)| v >= 2) { num_dangerous_vents += 1; }
	println!("{}", num_dangerous_vents);
}

fn p2(filename: &String) {
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();

	let mut vents_count: HashMap<(i32, i32), i32> = HashMap::new();
	for line in data_gen {
		let ((x1,y1),(x2,y2)) = line.unwrap().splitn(2, " -> ").map(|coords| coords.splitn(2, ",").map(|n| n.parse::<i32>().unwrap()).collect_tuple().unwrap()).collect_tuple().unwrap();

		let x_range = range_step_inclusive(x1, x2, if x2 > x1 { 1 } else { -1});
		let y_range = range_step_inclusive(y1, y2, if y2 > y1 { 1 } else { -1});

		if x1 == x2 || y1 == y2 {
			for (x, y) in iproduct!(x_range, y_range) {
				if let Some(n) = vents_count.get_mut(&(x, y)) { *n = *n + 1; }
				else { vents_count.insert((x, y), 1); }
			}
		}
		else {
			for (x ,y) in izip!(x_range, y_range) {
				if let Some(n) = vents_count.get_mut(&(x, y)) { *n = *n + 1; }
				else { vents_count.insert((x, y), 1); }
			}
		}
	}

	let mut num_dangerous_vents = 0;
	for (_,_) in vents_count.iter().filter(|(_k,&v)| v >= 2) { num_dangerous_vents += 1; }
	println!("{}", num_dangerous_vents);
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
