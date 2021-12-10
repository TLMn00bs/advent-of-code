# extra

```
"Right at midnight, some requests were hanging forever, timing out, or getting HTTP 500 responses."
```
Explanation: [Postmortem 2: Scaling Adventures
](https://www.reddit.com/r/adventofcode/comments/k9lt09/postmortem_2_scaling_adventures/)

>  Turns out, the spike right at midnight is so much bigger than the traffic right before it that, some nights, the AWS load balancers weren't scaling fast enough to handle all the requests right at midnight.

> Root cause: still 2020.

`#viz` [Vertical axis is part 1 completions as a % of day one](https://www.reddit.com/r/adventofcode/comments/k9qf0m/maybe_why_it_feels_easier_this_year/)

[![](https://i.imgur.com/vbf72pP.jpg)](https://i.imgur.com/vbf72pP.jpg)
