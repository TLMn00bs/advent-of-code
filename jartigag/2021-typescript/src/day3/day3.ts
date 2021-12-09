import { data } from './data.day3';
import { NamedParameters } from './day3part2';

export const transpose = (array: number[][]) => {
    return array[0].map((_, colIndex) => array.map((row) => row[colIndex]));
};

export const bitCriteria = (countOnes: number, countZeros: number, mostCommonValue: boolean) => {
    if (mostCommonValue) {
        return countOnes >= countZeros;
    }
    return countOnes < countZeros;
};

const getRate = (params: NamedParameters) => {
    let gammaRate = '';
    for (let i = 0; i < params.array.length; i++) {
        let countOnes = params.array[i].filter((x) => x == 1).length;
        let countZeros = params.array[i].filter((x) => x == 0).length;

        if (bitCriteria(countOnes, countZeros, params.mostCommonValue)) {
            gammaRate = gammaRate.concat('1');
        } else {
            gammaRate = gammaRate.concat('0');
        }
    }
    return gammaRate;
};

export const getGammaRate = (array: number[][]) => {
    let transposedArray = transpose(array);
    let gammaRate = getRate({ array: transposedArray, mostCommonValue: true });

    return parseInt(gammaRate, 2);
};

export const getEpsilonRate = (array: number[][]) => {
    let transposedArray = transpose(array);
    let epsilonRate = getRate({ array: transposedArray, mostCommonValue: false });

    return parseInt(epsilonRate, 2);
};

export const getPowerConsumption = (array: number[][]) => {
    return getGammaRate(array) * getEpsilonRate(array);
};

export const day3 = (input: number[][]) => getPowerConsumption(data);

/*
--- Day 3: Binary Diagnostic ---

The submarine has been making some odd creaking noises, so you ask it to produce
a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers
which, when decoded properly, can tell you many useful things about the
conditions of the submarine. The first parameter to check is the power
consumption.

You need to use the binary numbers in the diagnostic report to generate two new
binary numbers (called the gamma rate and the epsilon rate). The power
consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in
the corresponding position of all numbers in the diagnostic report.

[..]

Use the binary numbers in your diagnostic report to calculate the gamma rate and
epsilon rate, then multiply them together. What is the power consumption of the
submarine? (Be sure to represent your answer in decimal, not binary.)
*/
