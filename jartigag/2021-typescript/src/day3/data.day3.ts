import * as fs from 'fs';
import { parseInput } from '../utils/input';

const input = fs.readFileSync(__dirname + '/input').toString();

export const data = input.split('\n').map((x) => parseInput(x)) as number[][];
