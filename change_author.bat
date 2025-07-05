@echo off
SET OLD_EMAIL=varunlgowda2014@gmail.com
SET CORRECT_NAME=Learningbots79
SET CORRECT_EMAIL=learningbots79@gmail.com

git filter-branch --force --env-filter "
IF %%GIT_COMMITTER_EMAIL%% == %OLD_EMAIL% (
    SET GIT_COMMITTER_NAME=%CORRECT_NAME%
    SET GIT_COMMITTER_EMAIL=%CORRECT_EMAIL%
)
IF %%GIT_AUTHOR_EMAIL%% == %OLD_EMAIL% (
    SET GIT_AUTHOR_NAME=%CORRECT_NAME%
    SET GIT_AUTHOR_EMAIL=%CORRECT_EMAIL%
)
" --tag-name-filter cat -- --branches --tags

echo Author information has been updated.
echo You may need to force push with: git push --force origin main 