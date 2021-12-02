use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn p1(filename: &String) {
	let mut n = 0;
	let mut current_depth: i32;

	let file = File::open(filename).unwrap();
	let reader = BufReader::new(file);
	let mut data_gen = reader.lines();

	let next = data_gen.next();
	match next {
		Some(depth) => current_depth = depth.unwrap().parse::<i32>().unwrap(),
		None => process::exit(1)
	}
	
	for (_, line) in data_gen.enumerate() {
		let depth = line.unwrap().parse::<i32>().unwrap();
		if depth > current_depth {
			n += 1;
		}
		current_depth = depth;
	}
	println!("Number of depth increments: {}", n);
}

fn p2(filename: &String) {
	let mut n = 0;
	let mut sliding_window:[i32; 3] = [0, 0, 0];
	let mut last_idx = 0;

	let file = File::open(filename).unwrap();
	let reader = BufReader::new(file);
	let mut data_gen = reader.lines();

	// Read the first 3 items of the file to prefill the sliding window
	for idx in 0..3 {
		let item = data_gen.next();
		match item {
			Some(depth) => sliding_window[idx] = depth.unwrap().parse::<i32>().unwrap(),
			None => process::exit(1)
		}
	}

	// Read the remaining depths
	for (_, line) in data_gen.enumerate() {
		let past_sum:i32 = sliding_window.iter().sum();

		let depth = line.unwrap().parse::<i32>().unwrap();
                sliding_window[last_idx] = depth;

		// To avoid shifting the whole window, that in this case is just 3, but could be larger,
		// keep an index of the last depth to override it each time.
		last_idx = (last_idx + 1) % 3;				// 3 is the length of the sliding_window
                let current_sum:i32 = sliding_window.iter().sum();

                if current_sum > past_sum {
                        n += 1;
                }

        }
        println!("Number of depth increments: {}", n);
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
