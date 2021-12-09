import { data } from "./data.day4";

const transposeBoard = (board: number[][]) => board[0].map((row, col) => board.map((row) => row[col]));

export class Bingo {
    private numbers: number[] = [];
    private boards: number[][][] = [];
    private lastSaidNumber: number = 0;
    private winGames: Set<any> = new Set();

    constructor(data: string) {
        const parts = data.split('\n\n');
        this.numbers = parts.shift()!.split(',').map(Number);
        this.boards = parts.map((board) => board.split('\n').map((row) => row.trim().split(/\s+/g).map(Number)));
    }

    private getScore(checkingLastScore: boolean = false): number {
        for (const [idx,board] of this.boards.entries()) {
            const horizontalMarkedNumbersInARow = board.some((row) => row.every((cell) => cell === -1));
            const verticalMarkedNumbersInARow = transposeBoard(board).some((row) => row.every((cell) => cell === -1));

            if (horizontalMarkedNumbersInARow || verticalMarkedNumbersInARow) {
                const sumUnmarked = ([] as number[])
                    .concat(...board)
                    .filter((cell) => cell !== -1)
                    .reduce((a, b) => a + b);

                if (checkingLastScore) {
                    this.winGames.add(idx);
                }

                if (!checkingLastScore || this.winGames.size === this.boards.length) {
                    return sumUnmarked * this.lastSaidNumber;
                }
            }
        }
        return -1;
    }

    markBoards(number: number) {
        this.boards = this.boards.map((board) =>
            board.map((row) =>
                row.map((cell) => (cell === number ? -1 : cell))
            )
        );
    }

    sayNextNumber(): number {
        this.lastSaidNumber = this.numbers.shift()!;
        return this.lastSaidNumber;
    }

    public solve(checkingLastScore: boolean = false): number {
        let result = -1;
        while (result < 0) {
            this.markBoards(this.sayNextNumber());
            result = this.getScore(checkingLastScore);
        }
        return result;
    }
}

export const day4 = (input: string) => new Bingo(data).solve();

/*
--- Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean,
already so deep that you can't see any sunlight. What you can see, however, is a
giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

[..]

The submarine has a bingo subsystem to help passengers (currently, you and the
giant squid) pass the time. It automatically generates a random order in which
to draw numbers and a random set of boards (your puzzle input).

[..]

The score of the winning board can now be calculated. Start by finding the sum
of all unmarked numbers on that board [..]. Then, multiply that sum by the
number that was just called when the board won to get the final score.

To guarantee victory against the giant squid, figure out which board will win
first. What will your final score be if you choose that board?
*/