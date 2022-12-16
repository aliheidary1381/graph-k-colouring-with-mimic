## Graph k-colouring using MIMIC

This project is optimized for maximum readability and not performance.
This is reinventing the wheel for educational purposes.

There are comments, documentations & links to the original article and related wikipedia pages throughout the code.

No external libraries are used, except [fibonacci heap](https://pypi.org/project/fibheap/) for finding MST.

The following is an explanation of the algorithm. you can read it, jump straight into the code or read these

[original paper](https://www.semanticscholar.org/paper/MIMIC%3A-Finding-Optima-by-Estimating-Probability-Bonet-Isbell/5c0cdedfaaf35c2938ffdd76fe0e67185a3afaec)

[useful link](https://www.swyx.io/unsupervised-learning-randomized-optimization-4c1i)

[wikipedia](https://en.wikipedia.org/wiki/Estimation_of_distribution_algorithm#Mutual_information_maximizing_input_clustering_(MIMIC))

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#ed-algorithms">ED Algorithms</a>
    </li>
    <li>
      <a href="#mimic-modeling">MIMIC's Modeling</a>
      <ul>
        <li><a href="#the-permutation">The Permutation</a></li>
        <li><a href="#the-tree">The Tree</a></li>
        <li><a href="#wrapping-up">Wrapping up</a></li>
      </ul>
    </li>
    <li>
      <a href="#eliciting-empirical-probabilities">Eliciting Empirical Probabilities</a>
    </li>
    <li>
      <a href="#sampling">Sampling</a>
    </li>
  </ol>
</details>

### ED Algorithms

Generally, given some cost function `C`, we want to find `x` with minimal `C(x)`.

E.g. In [k-Colouring Problem](https://en.wikipedia.org/wiki/Graph_coloring#Vertex_coloring),
I have defined the cost function to be the number of bad edges,
i.e. edges connecting same-colour vertices.

(Alternatively, we can maximize a utility function. without loss of generality, we will stick to the first problem description)

A `model` (density estimator) represents where we think the minimal `C(x)` is.
At first, we don't know anything about `C`, so the `model` should represent a uniform distribution over all admissible solutions.
We use the `model` to generate new candidate solutions (`x`s) by calling `model.sample()`.
We evaluate `C(x)` to see if our guess was right or wrong.
We then improve our guessing iteratively, learning about the distribution of `C`.

At each iteration:
1. We use this `model` to generate more samples and grow our `population` (using `β_μ`).
2. Candidate solutions with high (bad) `C` values are discarded and the fittest ones survive (using `S`).
3. With this new `population` our `model` could be updated to better estimate the distribution (using `α_MIMIC`).

This idea of guessing intelligently improves performance compared to [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)
and other alternatives witch blindly walk on `C`.

Each [EDA](https://en.wikipedia.org/wiki/Estimation_of_distribution_algorithm) has a unique way of modeling
with its own pros and cons.

### MIMIC Modeling

Learning the structure of the function space helps us to better estimate, sample and model `C`.

For example, in a 2-colouring problem, imagine a graph with only two neighbouring vertices.
Possible valid solutions are 0-1 and 1-0, meaning that each vertex has equal possibility to be coloured 0 and 1.
A modeling witch doesn't learn the relationships would sample 0-0 and 0-1 with equal possibilities. 

We want a modeling to learn about the structure of `x`'s variables (`x = [x_0, x_1]`),
e.g. knowing `x_0 = 0`, the possibility of sampling `x_1 = 0` should decrease drastically.

helpful read: [no free lunch theorem in search and optimization](https://en.wikipedia.org/wiki/No_free_lunch_in_search_and_optimization) -
an explanation of why optimizations can only improve on others if they build in certain assumptions about structure

But learning too much structure would cost us too much time,
i.e. we will reach the goal in less iterations but each iteration would cost more time.
It's all about balancing the two.

Learning the structure perfectly would generate the [joint probability distribution](https://en.wikipedia.org/wiki/Joint_probability_distribution)
like this:
```text
p(x) = p(x_0)*p(x_1 | x_0)*p(x_2 | x_1, x_0)*p(x_3 | x_2, x_1, x_0) ...
```
Witch means: probability of `x1` knowing that `x_0` is `whatever it is`,
probability of `x2` knowing that `x_1, x_0` are `whatever they are`,
probability of `x3` knowing that `x_2, x_1, x_0` are `whatever they are`
and so on and so forth.

But this increases our computational complexity exponentially as `len(x)` grows

MIMIC solves this problem by limiting the learning, sacrificing perfect structure for performance.

MIMIC computes only [pairwise conditional probabilities](https://en.wikipedia.org/wiki/Conditional_dependence)
(using the current `population`),
i.e. `p(x_2 | x_1)` instead of `p(x_2 | x_1, x_0)` and `p(x_3 | x_2)` instead of `p(x_3 | x_2, x_1, x_0)`.
```text
p(x) = p(x_0)*p(x_1 | x_0)*p(x_2 | x_1)*p(x_3 | x_2) ...
```
This decreases accuracy of our estimation. the amount of decrease is rigorously measured by
[Kullback–Leibler divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence).

The divergence between the perfect joint probability distribution and MIMIC's estimation is inevitable,
but we will try to minimize this divergence by finding the best permutation.

#### The Permutation

The permutation is the limited structure that our algorithm learns.

Some variables have more impact on some than on others.

In k-Colouring Problem, neighbouring vertices are intuitively more impactful on each other.
If one is blue, the other is definitely not blue.
[Mutually independent variables](https://en.wikipedia.org/wiki/Independence_(probability_theory))
have zero impact on each other.

The idea is to compute `p(x_i | x_j)`s in an order witch `x_j` has most impact on `x_i`.

so, instead of computing
```text
p(x) = p(x_0)*p(x_1 | x_0)*p(x_2 | x_1)*p(x_3 | x_2) ...
```
we can compute (for example)
```text
p(x) = p(x_0)*p(x_2 | x_0)*p(x_1 | x_2)*p(x_3 | x_2) ...
```
Given that `x_0` and `x_2` are more dependent on each other,
this would increase the accuracy of our estimation.

The amount of impact two variables have on each other is rigorously measured by
[mutual information](https://en.wikipedia.org/wiki/Mutual_information).
It is a measure of the mutual dependence between the two variables.
In other words, it quantifies the amount of information obtained about one random variable by observing the other random variable.

#### The Tree

What's better than a [path/chain](https://en.wikipedia.org/wiki/Path_(graph_theory))?
A [Tree](https://en.wikipedia.org/wiki/Tree_(graph_theory))!

What if `x_0` is so impactful that we would be better with just
```text
p(x) = p(x_0)*p(x_1 | x_0)*p(x_2 | x_0)*p(x_3 | x_0) ...
```
This would be a [star](https://en.wikipedia.org/wiki/Star_(graph_theory)) in a Dependency Tree.

Dependency Trees are [Bayesian Networks](https://en.wikipedia.org/wiki/Bayesian_network)
or [Dependency Graphs](https://en.wikipedia.org/wiki/Dependency_graph)
where every node has exactly one parent (except the `root`, witch has `None`).

This improves our estimation further without any loss in performance.

Instead of computing the best permutation, I have chosen to compute the best tree.
It may be hard to believe, but it was easier for me to implement it.

#### Wrapping up

##### Mutual Information Maximizing (MIM):

To build a `model` from a `sample` population,
we first create a [Mutual Information Graph](https://en.m.wikipedia.org/wiki/Graphical_model) `gmi`:
A complete graph with each edge weighting its ends' mutual information.
We then compute the best tree by finding the [Maximum Spanning Tree](https://en.wikipedia.org/wiki/Minimum_spanning_tree) of `gmi`.
Maximizing M.I. ≡ minimizing [entropy](https://en.wikipedia.org/wiki/Entropy_estimation) ≡ minimizing KL divergence

### Eliciting Empirical Probabilities

In the process of model-building, we must deduce the empirical probabilities for each variable `x_i`.

This can be easily computed as follows:

`p(x_i = c)` is the percentage of `x`s in our `population` with `x_i = c`


### Sampling

Generating samples from our `model` (Dependency Tree) is as you would think.

We choose a colour for `root` based on its [empirical probability](https://en.wikipedia.org/wiki/Empirical_probability) `p(root)`.

For every other node `v`, we choose a colour based on its empirical [conditional probability](https://en.wikipedia.org/wiki/Conditional_probability) `p(v | parent(v))`.

note that `parent(v)`'s colour should be chosen before `v` itself.
This constraint is satisfied with
[BFS](https://en.wikipedia.org/wiki/Breadth-first_search),
[DFS](https://en.wikipedia.org/wiki/Depth-first_search)
and a lot of other [tree traversal algorithms](https://en.wikipedia.org/wiki/Tree_traversal).
I chose DFS for the simplicity of implementation.