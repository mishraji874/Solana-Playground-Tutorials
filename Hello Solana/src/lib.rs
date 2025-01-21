// Imports we need
use solana_program::{
    account_info::AccountInfo,
    entrypoint,
    entrypoint::ProgramResult,
    msg,
    pubkey::Pubkey,
};

/*
Entrypoint
In order to interact with our on-chain program, we need to define the program entrypoint. Luckily, we have a very useful macro called entrypoint! inside solana_program crate for this purpose.

Let's add entrypoint! at the top of the file(below the imports):
*/
entrypoint!(process_instruction);

// Let's start by writing the starting point of our program. Every interaction with the program is going to start from this function:

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    msg!("Hello, World!");
    Ok(())
}

/*
process_instruction takes 3 arguments:

program_id: It is the public key of our program.
accounts: We need to specify every account that our program interacts with in the instruction. We won't specify any accounts in this tutorial because our simple Hello world program only logs a message on-chain and doesn't interact with any account.
instruction_data: Instruction data(bytes). For our purposes, this will be empty because we don't need to pass in any data to the program.
We are returning Ok(()) to indicate that the program call completed successfully.

In Rust, we usually log messages with println! macro but in Solana, we use msg! macro. Inside the process_instruction function body, you can type msg and press Enter to use Playground snippet for logging messages. You can log whatever you want but for the purpose of the tutorial let's log Hello, World!

*/

