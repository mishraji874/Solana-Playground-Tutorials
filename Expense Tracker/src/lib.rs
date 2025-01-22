use anchor_lang::prelude::*;

// Your program Id will be added here when you enter "build" command
declare_id!("EfPrVhgFGgKEL4oWiKK6AhR2vPNg31tcFWC2BZiweRg2");

#[program]
pub mod etracker {

    use super::*;

    pub fn initialize_expense(
        ctx: Context<InitializeExpense>,
        id: u64,
        merchant_name: String,
        amount: u64,
    ) -> Result<()> {
        let expense_account = &mut ctx.accounts.expense_account;

        expense_account.id = id;
        expense_account.merchant_name = merchant_name;
        expense_account.amount = amount;
        expense_account.owner = *ctx.accounts.authority.key;

        Ok(())
    }

    pub fn modify_expense(
        ctx: Context<ModifyExpense>,
        _id: u64,
        merchant_name: String,
        amount: u64,
    ) -> Result<()> {
        let expense_account = &mut ctx.accounts.expense_account;
        expense_account.merchant_name = merchant_name;
        expense_account.amount = amount;

        Ok(())
    }

    pub fn delete_expense(_ctx: Context<DeleteExpense>, _id: u64) -> Result<()> {
        Ok(())
    }
}

/*
In this context, we're first getting the id from our instruction params. This part:


#[instruction(id : u64)]
We're doing this to access the Id and pass it in one of the seeds of our expense_account.

In order to derive expense account PDAs, we need a unique value, and that unique value is this Id which will help us update and get a specific expense account.

Accounts
- Authority: This account has access to add/modify/delete the expense account. It refers to the user's public key, as a user should have control over their expense account.
- Expense Account: This is the actual expense account that will store our expense data.
*/
#[derive(Accounts)]
#[instruction(id : u64)]
pub struct InitializeExpense<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        init,
        payer = authority,
        space = 8 + 8 + 32+ (4 + 12)+ 8 + 1,
        seeds = [b"expense", authority.key().as_ref(), id.to_le_bytes().as_ref()], 
        bump
    )]
    pub expense_account: Account<'info, ExpenseAccount>,

    pub system_program: Program<'info, System>,
}

/*
This is not too different from our initialize context. We're telling anchor that we will be reading and modifying the data in the account defined by the seeds of the expense account here. The seeds are same as InitializeExpense as we are modifying the same account initialized in the previous instruction. We also make sure by using pub authority: Signer<'info>, that the address updating the expense account is also signer.
*/
#[derive(Accounts)]
#[instruction(id : u64)]
pub struct ModifyExpense<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"expense", authority.key().as_ref(), id.to_le_bytes().as_ref()], 
        bump
    )]
    pub expense_account: Account<'info, ExpenseAccount>,

    pub system_program: Program<'info, System>,
}

/*
Since we need to delete the expense entry, we outright close the account which in turn removes all the data stored in it. We also make sure by using pub authority: Signer<'info>, that the address deleting the expense account is also signer.

It is not clear from first sight that which part exactly is responsible for deleting this. Well, have a look at this part:


#[account(
    mut,
    close = authority,
    seeds = [b"expense", authority.key().as_ref(), id.to_le_bytes().as_ref()],
    bump
)]
Notice the close = authority part? Yes, that is responsible for closing our account.
*/
#[derive(Accounts)]
#[instruction(id : u64)]
pub struct DeleteExpense<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        close = authority,
        seeds = [b"expense", authority.key().as_ref(), id.to_le_bytes().as_ref()], 
        bump
    )]
    pub expense_account: Account<'info, ExpenseAccount>,

    pub system_program: Program<'info, System>,
}

/*
Let's go through each of these one by one:

id: We're first defining a unique ID for our expense entries. This ID will be used to modify a particular expense in the future.

owner: The owner value will come in handy when we fetch expense entries in the frontend. We can use the memcmp filter in the getProgramAccount method to get expense accounts of a particular public key. We will learn about it around the end of this tutorial.

merchant_name: This is the merchant name, stored as a string for our expenses.

amount: This is simply the amount we spent.
*/

#[account]
#[derive(Default)]
pub struct ExpenseAccount {
    pub id: u64,
    pub owner: Pubkey,
    pub merchant_name: String,
    pub amount: u64,
}
