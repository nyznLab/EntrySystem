## 常用命令

```python
拉取远程分支到本地：git checkout -b main origin/main

创建并切换分支：git checkout -b XXX

切换分支：git checkout XXX

合并分支：git merge

拉取分支：git pull

# 提交代码步骤
添加暂存区：git add .(所有变更)  git add filename(某个文件)
提交到本地分支：git commit -m"message"
推送到远程分支分支：git push

删除暂存区内容：git restore 文件名

删除分支：git branch -d XXX

强制删除分支：git branch -D XXX

版本回退：git reset --hard HEAD^（上一个版本）
```

## git提交规范

- 拉取main分支，拉取代码

```
git clone XXX
# 拉取远程分支到本地
git checkout -b main origin/main
# 拉取代码
git pull
```

- 创建新分支

```
//创建新分支到本地
git checkout -b feature
//将本地分支推至远端
git push --set-upstream origin feature
```

- 在feature分支下进行代码开发
- 修改的代码添加到暂存区，提交到远端feature分支

```
//都是在feature分支下进行的
git add .
git commit -m"aaa"
git push
```

- 将feature分支merge到main,**merge之前别忘了先pull主分支**

```
git checkout main
git pull
git merge feature
git push
```

如果有几个需求在同时开发，或者某个需求跨度时间较长，可能出现之前拉的master分支已经有更新提交过代码。此时在提PR之前，**最好再拉取并合并一次master分支**，确保没有冲突。

**不要直接在main分支上**进行代码修改，每一个人先在自己的开发分支上修改。

完成一个阶段，假如觉得自己代码没啥问题，再将自己开发分支代码**merge到主分支**。

合并可能会与其他同学代码产生冲突，**不要自己随便删改别人代码**，沟通之后再去改代码。

自己的开发分支merge到main分支之前，**先pull main分支代码，再merge**。

## 解决冲突

多人协作容易发生冲突。当你push到main分支的时候，有可能会发现自己的代码与main分支代码冲突，可能是之前有人提交了新的代码，恰好与你代码冲突。

```python
# 从主分支拉取最新的提交
git pull 
# 处理分支冲突
```

