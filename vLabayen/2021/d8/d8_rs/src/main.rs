use std::env;
use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashSet;
use std::iter::FromIterator;
use itertools::Itertools;

fn digit2len(digit: char) -> Result<i32, &'static str> {
	match digit {
		'0' => Ok(6),
		'1' => Ok(2),
		'2' => Ok(5),
		'3' => Ok(5),
		'4' => Ok(4),
		'5' => Ok(5),
		'6' => Ok(6),
		'7' => Ok(3),
		'8' => Ok(7),
		'9' => Ok(6),
		_   => Err("Invalid digit")
	}
} 

fn p1(filename: &String) {
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	let unique_lengths = {
		let mut hs: HashSet<i32> = HashSet::new();
		hs.insert(digit2len('1').unwrap());
		hs.insert(digit2len('4').unwrap());
		hs.insert(digit2len('7').unwrap());
		hs.insert(digit2len('8').unwrap());
		hs
	};

	let mut n_unique_digits = 0;
	for line in data_gen {
		let (_, output_codes): (_, Vec<String>) = line.unwrap().trim().splitn(2, " | ").map(|c| c.split(" ").map(|s| String::from(s)).collect()).collect_tuple().unwrap();
		n_unique_digits += output_codes.iter().map(|code| code.len() as i32).filter(|code_len| unique_lengths.contains(code_len)).count();
	}
	println!("{}", n_unique_digits);
}

fn one(codes: &Vec<String>) -> HashSet<char> {
	let one = &codes.iter().filter(|c| c.len() as i32  == digit2len('1').unwrap()).cloned().collect::<String>();
	return HashSet::<char>::from_iter(one.chars());
}
fn four(codes: &Vec<String>) -> HashSet<char> {
	let four = &codes.iter().filter(|c| c.len() as i32  == digit2len('4').unwrap()).cloned().collect::<String>();
	return HashSet::<char>::from_iter(four.chars());
}
fn seven(codes: &Vec<String>) -> HashSet<char> {
	let seven = &codes.iter().filter(|c| c.len() as i32  == digit2len('7').unwrap()).cloned().collect::<String>();
	return HashSet::<char>::from_iter(seven.chars());
}
fn eight(codes: &Vec<String>) -> HashSet<char> {
	let eight = &codes.iter().filter(|c| c.len() as i32  == digit2len('8').unwrap()).cloned().collect::<String>();
	return HashSet::<char>::from_iter(eight.chars());
}
fn zero_six_nine(codes: &Vec<String>) -> Vec<HashSet<char>> {
	let zero_six_nine = &codes.iter().filter(|c| c.len() as i32 == digit2len('0').unwrap()).cloned().collect::<Vec<String>>();
	return zero_six_nine.iter().map(|n| HashSet::<char>::from_iter(n.chars())).collect();
}
fn two_three_five(codes: &Vec<String>) -> Vec<HashSet<char>> {
	let two_three_five = &codes.iter().filter(|c| c.len() as i32 == digit2len('2').unwrap()).cloned().collect::<Vec<String>>();
	return two_three_five.iter().map(|n| HashSet::<char>::from_iter(n.chars())).collect();
}

fn e_wire(four: &HashSet<char>, zero_six_nine: &Vec<HashSet<char>>) -> HashSet<char> {
	let all_segments: HashSet<char> = HashSet::<char>::from_iter(['a', 'b', 'c', 'd', 'e', 'f', 'g']);
	for code in zero_six_nine.iter() {
		let diff: HashSet<_> = four.difference(&code).collect();
		if diff.len() == 0 { return all_segments.difference(&code).cloned().collect(); }
	}
	return HashSet::<char>::new();
}

fn six_segment(one: &HashSet<char>, zero_six_nine: &Vec<HashSet<char>>) -> HashSet<char> {
	for code in zero_six_nine.iter() {
		let diff: HashSet<_> = one.difference(&code).collect();
		if diff.len() == 1 { return code.clone(); }
	}
	return HashSet::<char>::new();
}

fn nine_segment(four: &HashSet<char>, zero_six_nine: &Vec<HashSet<char>>) -> HashSet<char> {
	for code in zero_six_nine.iter() {
		let diff: HashSet<_> = four.difference(&code).collect();
		if diff.len() == 0 { return code.clone(); }
	}
	return HashSet::<char>::new();
}

fn zero_segment(six: &HashSet<char>, nine: &HashSet<char>, zero_six_nine: &Vec<HashSet<char>>) -> HashSet<char> {
	for code in zero_six_nine.iter() {
		if code != six && code != nine { return code.clone(); }
	}
	return HashSet::<char>::new();
}

fn three_segment(one: &HashSet<char>, two_three_five: &Vec<HashSet<char>>) -> HashSet<char> {
	for code in two_three_five.iter() {
		let diff: HashSet<_> = one.difference(&code).collect();
		if diff.len() == 0 { return code.clone(); }
	}
	return HashSet::<char>::new();
}

fn two_segment(e_wire: &HashSet<char>, two_three_five: &Vec<HashSet<char>>) -> HashSet<char> {
	for code in two_three_five.iter() {
		let diff: HashSet<_> = e_wire.difference(&code).collect();
		if diff.len() == 0 { return code.clone(); }
	}
	return HashSet::<char>::new();
}

fn five_segment(two: &HashSet<char>, three: &HashSet<char>, two_three_five: &Vec<HashSet<char>>) -> HashSet<char> {
	for code in two_three_five.iter() {
		if code != two && code != three { return code.clone(); }
	}
	return HashSet::<char>::new();
}

fn p2(filename: &String) {
	let mut output_sum = 0;
	let data_gen = BufReader::new(File::open(filename).unwrap()).lines();
	for line in data_gen {
		let (input_codes, output_codes): (Vec<String>, Vec<String>) = line.unwrap().trim().splitn(2, " | ").map(|c| c.split(" ").map(|s| String::from(s)).collect()).collect_tuple().unwrap();

		let one = one(&input_codes);
		let four = four(&input_codes);
		let seven = seven(&input_codes);
		let eight = eight(&input_codes);
		let zero_six_nine = zero_six_nine(&input_codes);
		let two_three_five = two_three_five(&input_codes);

		let e = e_wire(&four, &zero_six_nine);
		let six = six_segment(&one, &zero_six_nine);
		let nine = nine_segment(&four, &zero_six_nine);
		let zero = zero_segment(&six, &nine, &zero_six_nine);
		let three = three_segment(&one, &two_three_five);
		let two = two_segment(&e, &two_three_five);
		let five = five_segment(&two, &three, &two_three_five);

		let messedsegment2digit = |segment: HashSet<char>| {
			if segment == zero  { return Ok('0'); }
			if segment == one   { return Ok('1'); }
			if segment == two   { return Ok('2'); }
			if segment == three { return Ok('3'); }
			if segment == four  { return Ok('4'); }
			if segment == five  { return Ok('5'); }
			if segment == six   { return Ok('6'); }
			if segment == seven { return Ok('7'); }
			if segment == eight { return Ok('8'); }
			if segment == nine  { return Ok('9'); }
			return Err("Unknown segment");
		};
		let output_digits: Vec<char> = output_codes.iter().map(|code| messedsegment2digit(HashSet::<char>::from_iter(code.chars())).unwrap()).collect();
		let output_number: i32 = output_digits.iter().join("").parse::<i32>().unwrap();
		output_sum += output_number;
	}

	println!("{}", output_sum);
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
