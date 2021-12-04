use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use itertools::Itertools;


//https://www.reddit.com/r/rust/comments/97e9rd/comment/e48s11x/?utm_source=share&utm_medium=web2x&context=3
//https://stackoverflow.com/a/61948093
//https://doc.rust-lang.org/std/result/
fn p1(filename: &String) {
	enum Action { Forward, Down, Up }
	impl Action {
		fn from_str(input: &str) -> Result<Action, &'static str> {
			return match input {
				"forward" => Ok(Action::Forward),
				"down"    => Ok(Action::Down),
				"up"      => Ok(Action::Up),
				_         => Err("Unknown action"),
			}
		}
		fn exec(&self, h:i32, d:i32, x:i32) -> (i32, i32) {
			return match self {
				Action::Forward => (h + x, d),
				Action::Down    => (h, d + x),
				Action::Up      => (h, d - x)
			}
		}
	}

	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let (mut horizontal, mut depth) = (0, 0);
	for (_, line) in data_gen.enumerate() {
		let line = line.unwrap();
		let (action, x) = line.splitn(2, " ").collect_tuple().unwrap();

		let (h, d) = Action::from_str(action).unwrap().exec(horizontal, depth, x.parse::<i32>().unwrap());
		horizontal = h;
		depth = d;
        }
	println!("horizontal={} * depth={}: {}", horizontal, depth, horizontal * depth);
}

fn p2(filename: &String) {
	enum Action { Forward, Down, Up }
	impl Action {
		fn from_str(input: &str) -> Result<Action, &'static str> {
			return match input {
				"forward" => Ok(Action::Forward),
				"down"    => Ok(Action::Down),
				"up"      => Ok(Action::Up),
				_         => Err("unknown action")
			}
		}
		fn exec(&self, h:i32, d:i32, a:i32, x:i32) -> (i32, i32, i32) {
			return match self {
				Action::Forward => (h + x, d + x * a, a),
				Action::Down   => (h, d, a + x),
				Action::Up     => (h, d, a - x)
			}
		}
	}

	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let (mut horizontal, mut depth, mut aim) = (0, 0, 0);
	for (_, line) in data_gen.enumerate() {
                let line = line.unwrap();
                let (action, x) = line.splitn(2, " ").collect_tuple().unwrap();

                let (h, d, a) = Action::from_str(action).unwrap().exec(horizontal, depth, aim, x.parse::<i32>().unwrap());
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
