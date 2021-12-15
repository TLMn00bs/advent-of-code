use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::{HashSet, HashMap};
use std::cmp::min;
use counter::Counter;

fn get_adjacents_idx(row_idx: usize, col_idx: usize, num_rows: usize, num_cols: usize) -> Vec<(usize, usize)> {
	let mut idxs: Vec<(usize, usize)> = Vec::new();
	if row_idx != 0 { idxs.push((row_idx - 1, col_idx)); }
	if col_idx != 0 { idxs.push((row_idx, col_idx - 1)); }
	if row_idx != num_rows - 1 { idxs.push((row_idx + 1, col_idx)); }
	if col_idx != num_cols - 1 { idxs.push((row_idx, col_idx + 1)); }
	return idxs;
}

fn p1(filename: &String) {
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let heightmap: Vec<Vec<i32>> = data_gen.map(|line| line.unwrap().chars().map(|c| c.to_digit(10).unwrap() as i32).collect()).collect();

	let mut risk_level_sum = 0;
	for (i, row) in heightmap.iter().enumerate() {
		for (j, height) in row.iter().enumerate() {
			let min_adj = get_adjacents_idx(i, j, heightmap.len(), row.len()).iter().map(|(row_idx, col_idx)| heightmap[*row_idx][*col_idx]).min().unwrap();
			if height < &min_adj {
				risk_level_sum += height + 1;
			}
		}
	}
	println!("{}", risk_level_sum);
}

fn follow(row_idx: usize, col_idx: usize, flow_map: &HashMap<(usize, usize), (usize, usize)>, low_points: &HashSet<(usize, usize)>) -> (usize, usize) {
	if low_points.contains(&(row_idx, col_idx)) { return (row_idx, col_idx) }
	let (next_row, next_col) = flow_map[&(row_idx, col_idx)];
	return follow(next_row, next_col, flow_map, low_points);
}

fn p2(filename: &String) {
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let heightmap: Vec<Vec<i32>> = data_gen.map(|line| line.unwrap().chars().map(|c| c.to_digit(10).unwrap() as i32).collect()).collect();

	let mut low_points: HashSet<(usize, usize)> = HashSet::new();
	let mut flow_map: HashMap<(usize, usize), (usize, usize)> = HashMap::new();
	for (i, row) in heightmap.iter().enumerate() {
		for (j, height) in row.iter().enumerate() {
			if height == &9 { continue }
			let (min_adj_height, min_adj_row, min_adj_col) = get_adjacents_idx(i, j, heightmap.len(), row.len()).into_iter().map(|(row_idx, col_idx)| (heightmap[row_idx][col_idx], row_idx, col_idx)).min().unwrap();
			let (_, min_row, min_col) = min((height, i, j), (&min_adj_height, min_adj_row, min_adj_col));

			if height < &min_adj_height {
				low_points.insert((i, j));
			}
			flow_map.insert((i, j), (min_row, min_col));
		}
	}

//	let mut counter: HashMap<(usize, usize), i32> = HashMap::new();
	let mut counter: Counter<(usize, usize), i32> = Counter::new();
	for (i, j) in flow_map.keys() {
		let (row, col) = follow(*i, *j, &flow_map, &low_points);
		match counter.get_mut(&(row, col)) {
			Some(c) => *c += 1,
			None    => {
				counter.insert((row, col), 1);
			}
		};
	}
	let top_basins: i32 = counter.most_common_ordered().iter().map(|(_, size)| size).take(3).product::<i32>();
	println!("{}", top_basins);
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
