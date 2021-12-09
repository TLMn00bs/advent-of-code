import * as fs from 'fs';

const input = fs.readFileSync(__dirname + '/input').toString();

export type signalOutputPair = { signalPatterns: string[]; outputValues: string[] };

const parseInput = (input: string): signalOutputPair[] => {
    let result: signalOutputPair[] = [];
    for (const line of input.split('\n')) {
        let [rawSignalPatterns, rawOutputValues] = line.split(' | ');
        const signalPatterns = rawSignalPatterns.split(' ');
        const outputValues = rawOutputValues.split(' ');
        const element: signalOutputPair = { signalPatterns: signalPatterns, outputValues: outputValues };
        result.push(element);
    }
    return result;
};

export const data = parseInput(input) as signalOutputPair[];
