# Friday, Feb 23, 2024, 1:37 AM PT
I started coding around 12:12 AM. I'm trying to restrcuture the code into packages.

I found out I can't use circular imports even with packages in Python, if I want to use values at the top-level of modules. Most of these values are for typing.
I'm consdiering using type-stubs.

# Saturday, Mar 02, 2024, 4:47 AM PT
Begin session at 4:47am.

6:26am: end session. I've managed to organise the code into reasonable directories.
There are still type errors for now, but these will be resolved eventually. They mainly deal with imports being done at the right places and using the right aliases, especially for SympyExpression.