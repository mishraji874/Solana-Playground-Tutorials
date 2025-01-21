// Client code...

// In order to interact with our on-chain program, we must create a transaction and send it to the Solana cluster via an RPC endpoint.

// In playground, we already have useful information to interact with our program globally defined in pg namespace. For example, we can log our program id like this:
console.log(pg.PROGRAM_ID.toString());

// In the latest version of @solana/web3.js we need to provide latest blockhash information when creating a transaction. We can easily get it like this:
const blockhashInfo = await pg.connection.getLatestBlockhash();
console.log(blockhashInfo)

// Let's create a transaction to interact with our on-chain program:

const tx = new web3.Transaction({
  ...blockhashInfo,
});

tx.add(
  new web3.TransactionInstruction({
    programId: pg.PROGRAM_ID,
    keys: [],
    data: Buffer.from([]),
  })
);

/* 
If you noticed, the parameters that we entered are the same from our program in lib.rs.

programId: its our hello world program id
keys: its accounts parameter in our program instruction. Since this program doesn't make use of any of the accounts, we leave it empty.
data: its instruction_data paramater in our program instruction. Again, since we are not using any data on-chain, we don't need to specify it here. We put an empty buffer with Buffer.from([]).
*/

// Our transaction is ready, we just need to sign it:
tx.sign(pg.wallet.keypair);

// We can now send the signed transaction to the Solana Cluster:
const txHash = await pg.connection.sendRawTransaction(tx.serialize());
console.log(txHash);