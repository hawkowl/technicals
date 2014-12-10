Testing & I/O
=============

It is said that a watched pot never boils, and I find that the same is with untested code.
You write it, you run it, it seems to work, you push it into production, and call it a day.
Unfortunately, as soon as you purge the knowledge of that code ever existing from your mind, a user will decide that today is the day that their cat will do some data entry, and everything falls apart.

The most generally accepted approach to preventing your application from having some fatal bug in it is through testing your code -- that is, "watching" your code.
An automated set of eyes to make sure that all is sane, and that when the user decides to set their display name to "H́E̸̡͟ ̵͘C͘O̷M͞ÉS̢" that it doesn't explode with a nasty red page and big letters saying ``UnicodeDecodeError``.

Generally, this testing comes in the form of:



Execution tests that run the code, static analysis that checks for unused variables, and linters that check code style are three things that are in common use for making sure that a project's code is top notch.
These


haha work in progress

*why* testing:

- make sure code is clean (eg. pyflakes)
- make sure code is syntactically correct (eg. free from syntax errors)
- make sure code is computationally correct (eg. the input gives the correct output)
- make sure code fufils business requirements (eg. does a certain thing for a customer)
- unit testing is #2 and #3, code analysis is #1, and functional testing is #3 and #4


*why* unit testing:

- makes sure the units that make up *your* application are correct
- test the pure logic of your application at a near-functional level
- minimises the effect of implementation details on your application's testing (eg. databases)


why i/o in unit tests are bad:

- external dependencies makes it more complex and fragile
- you end up testing the I/O is reliable, rather than your code (and if it's not, you get spurious failures)
- if you're not testing on I/O boundaries, chances are you're not covering certain internal details
- you have to rely on implementation details


what you can do about it:

- write your functions so that they take some state and return some other state, rather than mutating some random state
- write your methods so that they only mutate the state of its object
- have your I/O go through a wrapper that can be faked -- eg. rather than talking to memcache, you can use a dictionary
- don't have anything do I/O without telling you -- for example, importing a module should NOT do any I/O. you should instantiate an object with some parameters that then does the I/O for you, and is given to the code


what you will get:

- code with unit-testable I/O boundaries (eg. through an interface) is less prone to being stuck with one backend implementation
- tests will run much faster, as it works only in memory, and can be parallelised very easily
- zero-setup tests -- no setting up databases or anything to make sure your code is sane
- 100% less sad owls
