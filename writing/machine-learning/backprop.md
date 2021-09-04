<h1 style="text-align:center">Back-Propegation</h1>
    
The goal of backpropegation is to minimize the difference between the outputs that a network produces for training data, and the known or target outputs of the training data. This difference for a sinlge final layer node is given by, for this demonstration, the *squared error function*.

$\epsilon(t, y) = (t - y)^2$ 

Where:

$t$ is the target output and,

$y$ is the network output.

In general, the full *cost* or *error* of the network for a single training example is given by the sum of every $\epsilon(t_i, y_i)$, that is, every final layer output node error for the training example. This summed error function is the target of minimization:

$E(T, Y) = \sum_{n=0}^m(t_n - y_n)^2 = \sum_{n=0}^m\epsilon_n $



Since the parameters of our network are the weights and biases, we want to determine the gradient of every weight and bias in the network with respect to The Error Function. The components of this vector will be given by:

$\frac{\partial{E}}{\partial{w_{jk}^{l}}}$

and

$\frac{\partial{E}}{\partial{b_{j}^{l}}}$

Note that the subscript $j$ determines the node on layer $l$.  The $k$ terms determines what node from the previous layer the weight is connected to. Biases span an entire layer, so they do not have a $k$ term - this is because there is only one bias for every node in the next layer, where as there are (typically) multiple weights for every node in the next layer; the bias gets added to the sum of weighted nodes.

In words: the partial derivative describing how each weight or bias affects the growth of the cost function. Before it is described how to determine the gradient for a single training example, it is useful to define some terms:

${\text{net}}_j^l = \sum_{k=1}^{n}({o_{k}^{l-1}w^{l}_{jk}}) + b^l_j$

This is the value of node $j$ in layer $l$ before going through the activation ('squishification') function. The inside term: $o_{k}^{l-1}$ ;
refers to the output (after the activation function) of node $k$ from the previous layer. All together this term is the weighted sum of all nodes $k$ from layer $l-1$ that feed into the node $j$ in layer $l$, plus the bias associated with node $j$.

Naturally, the input of this sum  is fed into the activation function and becomes the final, or *output* value of node $j$ in layer $l$; this value is given by:

$o_j^l = \alpha(\text{net}_j^l)$

Where $\alpha$ is the activation function, which is defined for convenience here as *the sigmoid function*:

$\alpha(z) = \frac{1}{1+e^{-z}}$

whose derivative is given by:

$\alpha'(z) = \alpha(z)(1 - \alpha(z))$

With these extra terms the partial derivative of the *error* with respect to the weight or bias can be expanded via the chain rule:

$\frac{\partial{E}}{\partial{w_{jk}^{l}}} = \frac{\partial{E}}{\partial{o_{j}^{l}}} \frac{\partial{o_j^l}}{\partial{\text{net}_j^l}} \frac{\partial{\text{net}_j^l}}{\partial{w_{jk}^{l}}}$


$\frac{\partial{E}}{\partial{b_{j}^{l}}} = \frac{\partial{E}}{\partial{o_{j}^{l}}} \frac{\partial{o_j^l}}{\partial{\text{net}_j^l}} \frac{\partial{\text{net}_j^l}}{\partial{b_{j}^{l}}}$

Breaking these down term by term, starting from the end:

$\frac{\partial{\text{net}_j^l}}{\partial{w_{jk}^{l}}} = \frac{\sum_{k=1}^{n}({o_{j}^{l-1}w^{l}_{jk}) + b_j^l}}{\partial{w_{jk}^{l}}} = o_{j}$

$\frac{\partial{\text{net}_j^l}}{\partial{b_{j}^{l}}} = \frac{\sum_{k=1}^{n}({o_{j}^{l-1}w^{l}_{jk}) + b_j^l}}{\partial{w_{jk}^{l}}} = 1$

Middle term:

$\frac{\partial{o_j^l}}{\partial{\text{net}_j^l}} = \frac{\alpha(\text{net}^l_j)}{\text{net}^l_j} = \alpha'(\text{net}^l_j) = \alpha(\text{net}^l_j)(1 - \alpha(\text{net}^l_j))$ 

For the first term, the partial derivative is straightforward if the output term $o_j$ is a member of the final layer $l$, as $o_j^l = y$, is the direct input to the error function:

$\frac{\partial{E}}{\partial{o_{j}^{l}}} = \frac{\partial{\sum_{n=0}^m(t_n - y_n)^2}}{\partial{y_i}}= \frac{\partial{(t_i - y_i)^2}}{\partial{y_i}} = 2(y - t)$

So for any weight or bias, $w_{jk}^l$ or $b_j^l$ i.e. those affecting the final output layer, the full expressions for the gradient of the *error function* with respect to those terms are given by:

$\frac{\partial{E}}{\partial{w_{jk}^{l}}} = 2(y - t)\alpha(\text{net}^l_j)(1 - \alpha(\text{net}^l_j)) o_j = $


$\frac{\partial{E}}{\partial{b_{j}^{l}}} = 2(y - t) \alpha(\text{net}^l_j)(1 - \alpha(\text{net}^l_j)) $

When the weight or bias term of this in question is not one that directly affects the final layer, meaning it's connected to a hidden layer node, the term $\frac{\partial{E}}{\partial{o_{j}^{l-1}}}$ must have more care taken to it, as the node said weight or bias feeds into: ${o_{j}^{l-1}}$, itself feeds into *multiple* final layer nodes, spreading its error across them. For now we consider just *layer* $l-1$ nodes. Bringing back the first term in the first receded layer, and noting the full *error function* sum:

$\frac{\partial{E}}{\partial{o_{j}^{l-1}}} = \frac{\partial{\sum_{n=0}^m(t_n - y_n)^2}}{\partial{o_{j}^{l-1}}}$

Since $o_j^{l-1}$ now feeds into multiple $o_j^l$ nodes, each one affecting the total error, the partial derivative of the error with respect to node, $o_j^{l-1}$, will include all terms of the sum of $E$, that is, the final layer output nodes, which $o_j^{l-1}$ feeds into. 

Define $A$ as the indices for the nodes that $o_j^{l-1}$ feeds into:

$A = \{g, h, ... z\}$ 

The partial derivative above, for which $o_j^{l-1}$ feeds into $o_a^l$, with $a \in A$, will include as many terms as are in $A$, and since these the partial derivatives of the full *error function* with respect to the $o_j^{l-1}$ nodes and the error is a sum (the full error function is always a sum), the partial derivative above will also be a sum:

$\frac{\partial{E}}{\partial{o_{j}^{l-1}}} = \sum_{a=A}\frac{\partial E}{\partial o_j^{l-1}}$

By again expanding by the chain rule, the sum can be properly evaluated.

$\sum_{a=A}\frac{\partial E}{\partial o_j^{l-1}} = \sum_{a=A}\frac{\partial E}{\text{net}^l_a}\frac{\text{net}^l_a}{\partial o_j^{l-1}} = \sum_{a=A}\frac{\partial E}{\partial o^{l}_a}\frac{\partial o^{l}_a}{\text{net}^l_a}\frac{\text{net}^l_a}{\partial o^{l-1}_j}$

Each term in this expanded expression is now easily computed, and beautifully, the primary term will always be the *error with respect to the output of the current layer minus one*, will always be one less than the layer with the previously computed *error with the respect the the output* - meaning the weight gradient can now be determined for all weights in the network.

The last two terms of this sum can be always determined no matter the layer, and the first term relies on having knowledge of the previous layer's $\frac{\partial E}{\partial 0_j^{l+1}}$ term - the beauty of this first term in the expression is that it *is the same* as the compact partial derivative, meaning that the compact partial derivative can always be determined using outputs from the $l+1$ nodes calculated in the last error. This iterative computation is carried out through the whole network to determine the weight gradient for the entire function of the network.

The change in each weight is expressed by the following, where $\eta$ is the *learning rate* parameter.

$\Delta w_{ji} = -\eta \frac{\partial E}{\partial w_ji} $
