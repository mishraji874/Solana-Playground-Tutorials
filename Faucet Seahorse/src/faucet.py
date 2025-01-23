from seahorse.prelude import *
from seahorse.pyth import *

declare_id('6XcKvUtssWcxzp6t3UjXVo9VJ25QpD86H9bnJFV7k9CG')

# Faucet
# Our faucet will be represented as an Account class with four fields -- bump which stores the bump used to generate the account (more on bumps later), owner the public key of the account creator, mint the public key of the token mint account for the token that the faucet will dispense (more on mint accounts later) and last_withdraw a timestamp of the last faucet withdrawal time which we will use as a crude way to rate limit access to the faucet.
class BitcornFaucet(Account):
  bump: u8
  owner: Pubkey
  mint: Pubkey
  last_withdraw: i64


# initialize a new faucet
"""
Our program assumes the Bitcorn token we are distributing already exists. This means when we come to testing the program we will have to create the token ourselves which we'll do from the command line. To initialize our faucet we provide four arguments -- a Signer, a TokenMint account, an empty instance of the BitcornFaucet account and an empty instance of a TokenAccount.

A token mint account is a place that stores the essential information related to a token such as the total supply and the creator of the token. Each token has a single mint account. For a user to hold a token, they must first create a token account for that token. Each user can only have one token account per token and that account stores the data for how many tokens the user holds.

Our faucet is initialized with the seeds ['mint', mint], a string and the address of the token mint account. We also store the bump used to generate the PDA in a variable.

For the most part Seahorse abstracts away our need to deal with 'bumps' or 'bump seeds'. A bump is a u8 unsigned integer (0-255) that is used as part of the process to create PDAs. Seahorse deals with this process so you don't have to. If you want to know more about bumps, you can read more here. It's a concept you will need to understand at some point in your Solana developer journey. When building with PDAs it is common to store the bump seed in the account data itself as we do with our faucet.

Finally we also store the mint and owner addresses in the relevant fields of our faucet's account.
"""
@instruction
def init_faucet(
  signer: Signer,
  mint: TokenMint,
  faucet: Empty[BitcornFaucet],
  faucet_account: Empty[TokenAccount]
):
  bump = faucet.bump()

  faucet = faucet.init(
    payer = signer,
    seeds = ['mint', mint]
  )

  faucet_account.init(
    payer = signer,
    seeds = ['mint', mint],
    mint = mint,
    authority = faucet,
  )

  faucet.bump = bump
  faucet.mint = mint.key()
  faucet.owner = signer.key()


# drips tokens to user
# We generate a timestamp with the method clock.unix_timestamp() and then check it against the last withdrawal field on our faucet. If the difference is less than 30 seconds the program will panic and return a message. This is our system of rate limiting faucet usage to limit spam, a true production application would likely use something more sophisticated.
@instruction
def drip_bitcorn_tokens(
  signer: Signer,
  mint: TokenMint,
  faucet: BitcornFaucet,
  faucet_account: TokenAccount,
  user_account: TokenAccount,
  bitcoin_price_account: PriceAccount,
  clock: Clock
):
  timestamp: i64 = clock.unix_timestamp()

  assert mint.key() == faucet.mint, "Faucet token does not match the token provided"
  assert timestamp - 30 > faucet.last_withdraw, "Please try again in 30 seconds"

  btc_price_feed = bitcoin_price_account.validate_price_feed('devnet-BTC/USD')
  btc_price = u64(btc_price_feed.get_price().price)

  print("The Bitcoin price is ", btc_price)

  bump = faucet.bump

  faucet_account.transfer(
    authority = faucet,
    to = user_account,
    amount = btc_price,
    signer = ['mint', mint, bump]
  )


# return unused tokens back to the faucet
# An option to return unused tokens is a feature found on many faucet interfaces. So lastly lets add an instruction to facilitate replenishing the faucet. This instruction fulfills a role identical to that of a token transfer through a wallet interface or the command line using the Solana CLI.
@instruction
def replenish_bitcorn_tokens(
  signer: Signer,
  mint: TokenMint,
  user_account: TokenAccount,
  faucet_account: TokenAccount,
  amount: u64
):
  user_account.transfer(
    authority = signer,
    to = faucet_account,
    amount = u64(amount)
  )

