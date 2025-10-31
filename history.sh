cd ~/iris_dvc_pipeline
ls -al
source venv/bin/activate
dvc pull
mkdir -p .github/workflows tests
gsutil cp gs://mlopsga1_data/week4/ci.yml .github/workflows/ci.yml
gsutil cp gs://mlopsga1_data/week4/test_validation_and_evaluation.py tests/test_validation_and_evaluation.py
gsutil cp gs://mlopsga1_data/week4/PULL_REQUEST_TEMPLATE.md .
gsutil cp gs://mlopsga1_data/week4/README.md .
ls .github/workflows
ls tests
git init
git branch -M main
git add .
git commit -m "Initial commit with Week 4 setup"
cat .github/workflows/ci.yml
cat tests/test_validation_and_evaluation.py
# link to your GitHub repo
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/23f3001764/iris_dvc_pipeline_mlops.git

# push main branch
git push -u origin main
git checkout -b dev
git push -u origin dev
echo "# trigger" >> trigger.txt
git add trigger.txt
git commit -m "Trigger CI test"
git push origin dev
# from dev → main
gh pr create --title "Week 4 CI & Tests" --body "Added pytest + DVC CI" --base main --head dev
git checkout main
git pull origin main
git merge dev
git push origin main
git branch -d dev
git push origin --delete dev
