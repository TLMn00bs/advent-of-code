use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use itertools::Itertools;
use std::vec::Vec;

fn p1(filename: &String) {
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();

	let mut num_ones: [i32; 12] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
	let mut n_lines = 0;
	for (_, line) in data_gen.enumerate() {
		for (col, c) in line.unwrap().chars().enumerate() {
			if c == '1' { num_ones[col] += 1; }
		}
		n_lines += 1;
	}

	let gamma = num_ones.iter().map(|n| if n >= &(n_lines - n) { '1' } else { '0' }).join("");
	let epsilon = num_ones.iter().map(|n| if n >= &(n_lines - n) { '0' } else { '1' }).join("");

	let gamma_dec = isize::from_str_radix(&gamma, 2).unwrap();
	let epsilon_dec = isize::from_str_radix(&epsilon, 2).unwrap();
	println!("gamma={}: {}, epsilon={}: {} ==> {}", gamma, gamma_dec, epsilon, epsilon_dec, gamma_dec * epsilon_dec);
}

fn p2(filename: &String) {
	let report: Vec<String> = BufReader::new(File::open(filename).unwrap()).lines().map(|line| line.unwrap()).collect();

	let mut oxygen_opts = report.clone();
	for i in 0..12 {
		let oxygen_ones = oxygen_opts.iter().map(|opt| opt.chars().nth(i).unwrap().to_digit(10).unwrap() as i32).sum::<i32>();
		let mcb = if oxygen_ones >= ((&oxygen_opts).len() as i32 - oxygen_ones) { '1' } else { '0' };
		oxygen_opts = oxygen_opts.iter().filter(|opt| opt.chars().nth(i).unwrap() == mcb).cloned().collect();
		if oxygen_opts.len() <= 1 { break; }
	}

	let mut co2_opts = report.clone();
	for i in 0..12 {
		let co2_ones = co2_opts.iter().map(|opt| opt.chars().nth(i).unwrap().to_digit(10).unwrap() as i32).sum::<i32>();
		let mcb = if co2_ones >= ((&co2_opts).len() as i32 - co2_ones) { '0' } else { '1' };
		co2_opts = co2_opts.iter().filter(|opt| opt.chars().nth(i).unwrap() == mcb).cloned().collect();
		if co2_opts.len() <= 1 { break; }
	}

        let oxygen_dec = isize::from_str_radix(&oxygen_opts[0], 2).unwrap();
        let co2_dec = isize::from_str_radix(&co2_opts[0], 2).unwrap();
        println!("oxygen={}: {}, co2={}: {} ==> {}", oxygen_opts[0], oxygen_dec, co2_opts[0], co2_dec, oxygen_dec * co2_dec);
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
