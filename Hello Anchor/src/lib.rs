// Import anchor
// Let's start by importing Anchor to be used in our program:
use anchor_lang::prelude::*;

/*
With Anchor, we have to declare our program's public key. This is being used by Anchor to improve the security of our program.

We can easily declare our program's id with declare_id! mE9uxVnBnYqYQ2DRp3tRyzvWrJRKfXhyfUBStHk9giQ7Rm with #[program] macro:
/*
This is the syntax for declaring an Anchor program.

You can consider mod in Rust as a different file, it doesn't have access to the outer scope. In order to bring the outer scope inside mod we use use super::* which roughly means: import everything that's from outside of this scope. This way we have access to anchor_lang::prelude::* and other things that we might define.
We create our hello instruction. Every instruction in Anchor takes Context as the first parameter. Accounts that were passed to the instruction can be accessed from ctx parameter. Notice Context takes an inner type Hello, we will define that type next.
We return Ok(()) to indicate that the program call completed successfully.
*/

#[program]
mod hello_world {
    use super::*;

    pub fn hello(ctx: Context<Hello>) -> Result<()> {
        msg!("Hello, World!");
        Ok(())
    }
}

/*
Our hello instruction is ready. Now we need to define the Hello struct that we specified in the instruction parameter.

We define accounts by deriving #[derive(Accounts)] trait in our Hello struct. Since we don't need any accounts for this instruction, we leave the struct empty:
*/
#[derive(Accounts)]
pub struct Hello {}