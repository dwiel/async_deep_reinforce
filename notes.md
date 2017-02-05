16 hidden LSTM
fully connected in
fully connected outs

reward function: 1 when very close to target, 0 otherwise gets lower
variance higher reward than more smooth reward function (L1 or L2)

adding don't move action and starting at finish line helps, but still
high variance in final reward
should be able to learn to just always stand still, but doesn't

reducing the number of steps until terminate help converge to trivial
case quickly

in some sense the goal should be to chose an environment that isn't too
difficult, but also isn't too easy
- could this be done through a jointly trained teacher?
- chose difficulty such that expected score is about 90% or so
- for this simple problem could just pose it directly:
 if mean(score) > 0.9 increase difficulty otherwise decrease difficulty

# TODO: change logging metric to include current difficulty + goal
difficulty levels
- ie: how well is it doing on curriculum and how well can it extrapolate
  from here to real goal?

changed to pscore which is ratio of score vs max score given initial
conditions

still gets stuck at very small deviations from goal

perhaps it just gets stuck too easily on the simplest policies possible:
always stay
only one step away
* many step is too hard




0 steps away | n time steps long
5 steps away | 5 steps long

0, 5
1, 10
2, 15
3, 20
