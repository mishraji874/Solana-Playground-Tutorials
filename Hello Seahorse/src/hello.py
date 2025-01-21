# Seahorse program
from seahorse.prelude import *

declare_id('E7LXqGSzUQoU56rCW4rQ3nxb7PXrYSseqZpXG1QaF5bj')

@instruction
def hello(signer: Signer):
    print('Hello, World!')