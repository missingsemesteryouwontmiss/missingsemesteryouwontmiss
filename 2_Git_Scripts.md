# Topic 2

Lose Yourself to Scripting

---

## Basics of Bash Scripting
- Execution of commands and control flow expressions
- Variables, control flow, and unique syntax
- Tailored for shell-related tasks

---

## Variables and Strings in Bash
- Assign with `foo=bar`
- Access values with `$foo`
- Differentiating `'` and `"` for strings

---

```bash
foo=bar
echo "$foo"  # prints bar
echo '$foo'  # prints $foo
```

---

## Special Variables in Bash
- `$0` - Name of the script
- `$1` to `$9` - Arguments to the script. `$1` is the first argument and so on.
- `$@` - All the arguments
- `$#` - Number of arguments
- `$?` - Return code of the previous command
- `$$` - Process identification number (PID) for the current script
- `!!` - Entire last command, including arguments. A common pattern is to execute a command only for it to fail due to missing permissions; you can quickly re-execute the command with sudo by doing `sudo !!`
- `$_` - Last argument from the last command. If you are in an interactive shell, you can also quickly get this value by typing `Esc` followed by `.` or `Alt+.`
- Comprehensive list: [Special Chars in Bash](https://tldp.org/LDP/abs/html/special-chars.html)

---

## Command Execution and Return Codes
- Conditional execution with `&&`, `||`, `;`
- Understanding `true` and `false` commands

```bash
false || echo "Oops, fail"
# Oops, fail
true || echo "Will not be printed"
#
true && echo "Things went well"
# Things went well
false && echo "Will not be printed"
#
true ; echo "This will always run"
# This will always run
false ; echo "This will always run"
# This will always run
```

---

## Permissions – brief recap

Unix-like permissions are:

1. **Read (r)**: Open and read a file. List contents for directories.
1. **Write (w)**: Modify a file's contents. Add, remove, rename files in directories.
1. **Execute (x)**: Execute a file as a program/script. Access or traverse directories.

Grouped by 3 user categories:

- **User (u)**: The owner of the file.
- **Group (g)**: Users in the file's group.
- **Other (o)**: Users not the owner or in the file's group.

---

## Default permissions

When a file is created in Unix, default permissions are usually:

- Read and Write for the User (rw-)
- Read for the Group (r--)
- Read for Others (r--)

Depicted as: `rw-r--r--`

---

## Script Example

- Prefer `[[ ]]` for comparisons

```bash
#!/bin/bash

echo "Starting program at $(date)" # Date will be substituted

echo "Running program $0 with $# arguments with pid $$"

for file in "$@"; do
    grep foobar "$file" > /dev/null 2> /dev/null
    # When pattern is not found, grep has exit status 1
    # We redirect STDOUT and STDERR to a null register since we do not care about them
    if [[ $? -ne 0 ]]; then
        echo "File $file does not have any foobar, adding one"
        echo "# foobar" >> "$file"
    fi
done
```

---

Command substitution using `$( CMD )`

```docker
    GNUPGHOME="$(mktemp -d)" && \
    export GNUPGHOME && \
    for key in \
        "B46DC71E03FEEB7F89D1F2491F7A8F87B9D8F501" \
      ; do \
        gpg --batch --keyserver "keyserver.ubuntu.com" --recv-keys "$key" ; \
    done && \
    gpg --verify "/tmp/$QD_NAME.tar.gz.sha256.asc" "/tmp/$QD_NAME.tar.gz.sha256" && \
    (cd /tmp && sha256sum --check --status "$QD_NAME.tar.gz.sha256") && \
```

---

## Control Flow and Functions
- Supports `if`, `case`, `while`, `for`
- Function example: Creating and entering a directory

```bash
mcd () {
    mkdir -p "$1"
    cd "$1"
}
```

---

## Shell Functions vs Scripts

- Functions are in the shell's language; scripts can be in any language.
- Functions load once; scripts load each execution.
- Functions can modify the environment; scripts cannot, but receive exported variables.
- Functions promote code modularity, reuse, and clarity, and are often included in scripts.

---

## Bash Comparisons and Globbing
- Globbing with wildcards `?`, `*`, and `{}`

---

# Shell Tools

---

## Discovering Command Usage
- Using `--help`, `man` command, and TLDR pages
- Example: `man rm`, `tldr tar`

---

## Finding Files
- Tools: `find`, `fd`, `locate`
- Usage scenarios for each

---

## Finding Code
- `grep` and alternatives like `ack`, `ag`, `rg`
- Pattern searching examples

---

## Finding Shell Commands
- Utilizing `history`, `Ctrl+R`, `fzf` bindings
- Autosuggestions and protecting sensitive history entries

---

## Directory Navigation
- Fast navigation with `fasd`, `autojump`
- Advanced tools: `tree`, `broot`, `nnn`, `ranger`

---

Let's do a break

---

# Topic 3

Git Lucky

---

## Introduction
- Understanding the use and mechanics of Version Control Systems (VCSs)
- Focus on Git, the de facto standard for version control

---

## What is Version Control?
- Tools to track changes in source code or file collections
- Maintains history, facilitates collaboration
- Uses snapshots to encapsulate the state of files and folders

---

## Why Use Version Control?
- Track changes, understand history
- Collaborate with others seamlessly
- Answer critical questions about code changes

---

## Git's Reputation
- Known for its complexity
- Emphasizing understanding over memorization of commands
- [XKCD Comic on Git](https://xkcd.com/1597/)

![xkcd 1597](https://imgs.xkcd.com/comics/git.png)

---

# Git's Data Model

---

## Snapshots in Git
- Git views history as a series of snapshots (trees and blobs)
- Example tree structure:
  ```
  <root> (tree)
  |
  +- foo (tree)
  |  |
  |  + bar.txt (blob, contents = "hello world")
  |
  +- baz.txt (blob, contents = "git is wonderful")
  ```

---

## Modeling History
- History represented as a Directed Acyclic Graph (DAG) of snapshots
- Snapshots are commits with parent references
- Commits can have multiple parents (merging branches)

---

## Commit History Visualization
- Each commit points to its parent(s)
- Branches and merges in development are clearly visible

```
o <-- o <-- o <-- o
            ^
             \
              --- o <-- o
```

---

## Immutable Commits
- Commits are immutable in Git
- Edits create new commits; references are updated

---

## Data Model as Pseudocode
- Conceptual representation of Git's data model
```typescript
type blob = array<byte>
type tree = map<string, tree | blob>
type commit = struct
{
    parents: array<commit>
    author: string
    message: string
    snapshot: tree
}
```

---

## Objects and Content-Addressing
- Git stores objects (blobs, trees, commits) content-addressed by SHA-1 hash
- Objects refer to other objects via hash

---

## References
- Human-readable names for SHA-1 hashes (e.g., `master`)
- References are mutable, unlike objects

---

## Repositories
- A repository is a collection of objects and references

---

# Staging Area

- Mechanism to specify modifications for the next snapshot
- Allows for clean, organized commits

---

## Git CLI Basics

- `git help <command>`: get help for a git command
- `git init`: creates a new git repo, with data stored in the `.git` directory
- `git status`: tells you what's going on
- `git add <filename>`: adds files to staging area
- `git commit`: creates a new commit
- `git log`: shows a flattened log of history
- `git log --all --graph --decorate`: visualizes history as a DAG
- `git diff <filename>`: show changes you made relative to the staging area
- `git diff <revision> <filename>`: shows differences in a file between snapshots
- `git checkout <revision>`: updates HEAD and current branch

---

- Write [good commit messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)!
- Even more reasons to write [it's helpful](https://chris.beams.io/posts/git-commit/)!

---

## Branching and Merging
- `git branch`: shows branches
- `git branch <name>`: creates a branch
- `git checkout -b <name>`: creates a branch and switches to it
  - same as `git branch <name>; git checkout <name>`
- `git merge <revision>`: merges into current branch
- `git mergetool`: use a fancy tool to help resolve merge conflicts
- `git rebase`: rebase set of patches onto a new base

---

## Remotes
- `git remote`: list remotes
- `git remote add <name> <url>`: add a remote
- `git push <remote> <local branch>:<remote branch>`: send objects to remote, and update remote reference
- `git branch --set-upstream-to=<remote>/<remote branch>`: set up correspondence between local and remote branch
- `git fetch`: retrieve objects/references from a remote
- `git pull`: same as `git fetch; git merge`
- `git clone`: download repository from remote

---

## Undo
- `git commit --amend`: edit a commit's contents/message
- `git reset HEAD <file>`: unstage a file
- `git checkout -- <file>`: discard changes

---

# Advanced Git

- `git config`: Git is [highly customizable](https://git-scm.com/docs/git-config)
- `git clone --depth=1`: shallow clone, without entire version history
- `git add -p`: interactive staging
- `git rebase -i`: interactive rebasing
- `git blame`: show who last edited which line
- `git stash`: temporarily remove modifications to working directory
- `git bisect`: binary search history (e.g. for regressions)
- `.gitignore`: [specify](https://git-scm.com/docs/gitignore) intentionally untracked files to ignore

---

## Miscellaneous 

- GUI clients, shell and editor integration
- Different workflows (e.g., GitFlow, pull requests)
- GitHub and other Git hosting providers

## Resources

- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Oh Shit, Git!?!](https://ohshitgit.com/)
- [Git for Computer Scientists](https://eagain.net/articles/git-for-computer-scientists/)
- [Git from the Bottom Up](https://jwiegley.github.io/git-from-the-bottom-up/)
- [Learn Git Branching](https://learngitbranching.js.org/)
