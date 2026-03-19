# `Lin` format

The `Lin` format is essentially as follows

```
\{00}\{05}Ident\{00}\{32}register=test%40cb%2elocal@email
```

can be though of as:

```
    5: Ident
    32: register=test%40cb%2elocal@email
```

Where "Ident" is 5 bytes long and "register=test%40cb%2elocal@email" is 32 bytes long.

# `Lin` streaming vs file storage

`Lin` has two variants, one for streaming and one for persistance. The
difference is that `Lin` on disk puts length values after the content so that
it can be read and updated at the end of the file. In other-words `Lin` files
are access by reading the end of the file first.

For socket and network conversations it makes sense to start with the length, and then send the content. For file storage the opposite has more value. This is because files can be added to, and the last value is always the latest one. For this reason the file based `Lin` storage looks as follows.

The `Lin` file storage is the opposite:

```
Ident\{00}\{05}register=test%40cb%2elocal@email\{00}\{32}
```

can be though of as:

```
     Ident, 5, register=test%40cb%2elocal@email, 32
```
