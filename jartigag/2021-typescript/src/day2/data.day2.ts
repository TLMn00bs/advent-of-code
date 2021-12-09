import * as fs from 'fs';
import { parseInput } from '../utils/input';

const input = fs.readFileSync(__dirname + '/input').toString();

export const data = parseInput(input).slice(0, -1) as string[];
//                                    ^^^ remove last empty line
