# Analysis

## Layer 1, Head 11

This layer displays a diagonal pattern, focusing on consecutive tokens. This head perhaps lends to account for inter-token relationships, especially to identify situations where tokens are complimentary (e.g. intransitive verbs), or if successive tokens provide additional meaning to the former. This is especially prevolent with tenses prior to verbs.

Any other inter-token relationships hold negligible, if any, attention within this head specifically.

Example Sentences:
- The [MASK] slope caused me to fall down, hurting my knee.
- After consuming a large meal, I was concerned how it would affect my [MASK].

## Layer 6, Head 8

Here, attention is strongly allocated to clusters of consecutive tokens which feed into one another to provide context to the following noun/verb. In the first sentence, tokens are fairly disconnected and provide little information sequentially to the overall meaning. In the second however, the head is able to isolate multiple specific clusters of importance to isolate relevant information towards [MASK].

Example Sentences:
- The [MASK] slope caused me to fall down, hurting my knee.
- After consuming a large meal, I was concerned how it would affect my [MASK].
