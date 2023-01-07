

t_AA_BB = 6
t_AA_CC = 3
t_BB_CC = 3
p_AA = 2
p_BB = 20
p_CC = 12
t_max = 30

print(
	(p_BB * (t_max - t_AA_BB - 1)) + (p_CC * (t_max - t_AA_BB - t_BB_CC - 2)),
	(p_CC * (t_max - t_AA_CC - 1)) + (p_BB * (t_max - t_AA_CC - t_BB_CC - 2))
)

print(
	(p_AA * (t_max - 1)) + (p_BB * (t_max - t_AA_BB - 2)) + (p_CC * (t_max - t_AA_CC - 2)),
	(p_BB * (t_max - t_AA_BB - 1)) + (p_AA * (t_max - t_AA_BB - t_AA_BB - 2)) + (p_CC * (t_max - t_AA_BB - t_BB_CC - 2)),
	(p_CC * (t_max - t_AA_CC - 1)) + (p_AA * (t_max - t_AA_CC - t_AA_CC - 2)) + (p_BB * (t_max - t_AA_CC - t_BB_CC - 2)),
)