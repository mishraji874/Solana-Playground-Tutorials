// Client code...
console.log(pg.PROGRAM_ID.toString())

const txHash = await pg.program.methods.hello().rpc();
console.log(txHash);