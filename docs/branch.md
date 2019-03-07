## git branch

### 查看当前分支状态

```
$git branch
* master

$git status
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```

### 创建分支

创建本地分支：

```
$git branch works      # create a branch
$git checkout works    # checkout to branch works
```
或者直接执行：

```
$git chechout -b works
Switched to a new branch "works"

$git branch
  master
* works
```

星号(\*)表示当前所在分支。现在的状态时成功创建新的分支并且已经切换到新分支上。

把新建的本地分支push到远程服务器，远程分支与本地分支同名(也可以根据需求取名):

```
$git push origin works:works

$git branch -a
  master
* works
  remotes/origin/HEAD ->origin/master
  remotes/origin/master
  remotes/origin/works
```

### 删除本地分支

```
git branch -d dev
```

### 删除远程分支

推送一个空分支到远程分支，其实就相当于删除远程分支：

```
$git push origin :works
```

或者：

```
$git push origin --delete works
```

### 合并分支

```
$git checkout master     # checkout branch to master
$git pull                # pull the newest code
$git merge works
```
