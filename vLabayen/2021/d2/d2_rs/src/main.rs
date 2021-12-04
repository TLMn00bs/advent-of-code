use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use itertools::Itertools;

fn p1(filename: &String) {
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let (mut horizontal, mut depth) = (0, 0);
	for (_, line) in data_gen.enumerate() {
		let line = line.unwrap();
		let (action, x) = line.splitn(2, " ").collect_tuple().unwrap();
		let x = x.parse::<i32>().unwrap();

		//https://github.com/rust-lang/rust/issues/71126
		let (h, d) = match action {
			"forward" => (horizontal + x, depth),
			"down"    => (horizontal, depth + x),
			"up"      => (horizontal, depth - x),
			_         => panic!("Unknown action")
		};
		horizontal = h;
		depth = d;
        }
	println!("horizontal={} * depth={}: {}", horizontal, depth, horizontal * depth);
}

fn p2(filename: &String) {
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let (mut horizontal, mut depth, mut aim) = (0, 0, 0);
	for (_, line) in data_gen.enumerate() {
                let line = line.unwrap();
                let (action, x) = line.splitn(2, " ").collect_tuple().unwrap();
		let x = x.parse::<i32>().unwrap();

                let (h, d, a) = match action {
			"forward" => (horizontal + x, depth + x * aim, aim),
			"down"    => (horizontal, depth, aim + x),
			"up"      => (horizontal, depth, aim - x),
			_         => panic!("Unknown action")
		};
                horizontal = h;
                depth = d;
		aim = a;
	}
	println!("horizontal={} * depth={}: {}", horizontal, depth, horizontal * depth);
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
