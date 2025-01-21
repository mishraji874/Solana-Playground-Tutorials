from seahorse.prelude import *

declare_id('Cwq2KhsGKQbVtZqD6FHqbztqyJmSqpB8uixgjsyTUYYn')

# User profile
# This will be used to create a program derived account (PDA) with two fields, the public address of the owner and the last_todo which is of type u8 i.e. an unsigned integer, 8 bits in size (0 to 255).
class UserProfile(Account):
    owner: Pubkey
    last_todo: u8


# Todo list item
# Our second class TodoAccount will be for the individual todos that the user wishes to store. The text documenting the todo will be stored as a string todo: str and its completion status will be stored as a boolean done: bool. We'll assign each todo an index index: u8 and finally we store a record of the todo's owner owner: Pubkey.
class TodoAccount(Account):
    owner: Pubkey
    index: u8
    todo: str
    done: bool


# initialize user profile
# The function will take two arguments -- an owner and an empty instance of the UserProfile class. We initialize the UserProfile instance with seeds consisting of the raw string "user_profile" and the owner's public key. In this way we ensure that each user can only have one profile and the addresses of those profiles will be unique. We also set the owner and last_todo fields to the owner's public address and 0 respectively.
@instruction
def init_user_profile(owner: Signer, user_profile: Empty[UserProfile]):
    user_profile = user_profile.init(
        payer = owner,
        seeds = ['user_profile', owner]
    )

    user_profile.owner = owner.key()
    user_profile.last_todo = 0


# add task to user's list
# This function has four arguments: an owner, a user profile, an empty instance of TodoAccount and a string describing our todo. First we initialize the todo account. In this case there are three seeds -- the string "todo_account", the owner's public key and the user_profile.last todo field.
@instruction
def add_task(
    owner: Signer,
    user_profile: UserProfile,
    todo_account: Empty[TodoAccount],
    todo: str
):
    todo_account = todo_account.init(
        payer = owner,
        seeds = ['todo_account', owner, user_profile.last_todo]
    )

    # We then proceed to set the fields for the newly initialized todo_account. todo is set to the string we passed into the function and owner is set to the owner's public address. The index of our account is set to the user_profile.last_todo which is then incremented by one. In this way every new todo task the user creates will have a different index. Given the index is stored as a u8, a single user will be able to create up to 256 individual todo items before running out of indexes.

    todo_account.todo = todo
    todo_account.owner = owner.key()

    todo_account.index = user_profile.last_todo
    user_profile.last_todo += 1


# mark task as done
# This function will take two arguments -- an owner and an instance of the todo account. Firstly we need to check that the signer of the transaction is in fact the owner of the account. We do this with an assert statement. Then we set the todo_account.done field to True and print a message confirming the change.
@instruction
def mark_task_as_done(
    owner: Signer,
    todo_account: TodoAccount
):
    assert owner.key() == todo_account.owner, 'Only the owner of the task can mark as done'

    todo_account.done = True

    print('This todo has been marked as done')