// Client code...

/*
In order to interact with our on-chain program, we must create a transaction and send it to the Solana cluster via an RPC endpoint.

In playground, we already have useful information to interact with our program globally defined in pg namespace. For example, we can log our program id like this:
*/
console.log(pg.PROGRAM_ID.toString());

// Calling our program with Anchor is very simple:
const txHash = await pg.program.methods.hello().rpc();
console.log(txHash);
