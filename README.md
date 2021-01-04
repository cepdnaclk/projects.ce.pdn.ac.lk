
This repo has the static site for the projects.ce.pdn.ac.lk.

Use following script to maks a clone and copy into the gh-pahes branch of this repository (A copy will be available on this directory, script.sh)

Notes:
- You need root access to the server which runs  this script.
- You need to have write access to this repository.

```
#!/bin/bash

domain="ce-projects.nuwanjaliyagoda.com"

# --------------------------------
echo "install the necessary softwares"
# --------------------------------
apt-get install webhttrack


# --------------------------------
echo "Ready to mirror http://${domain}/ to a local folder"
# --------------------------------
domain=ce-projects.nuwanjaliyagoda.com
rm ./mirror -r --force
mkdir ./mirror
httrack "http://${domain}/" -O "./mirror" "+${domain}/*" -v


# --------------------------------
echo "Clone the github repository (you need to have write access to the repository)"
# --------------------------------

rm ./projects-static -r --force
git clone https://github.com/cepdnaclk/projects-static
cd ./projects-static
git checkout gh-pages

cp ../mirror/${domain}/* ./ -r

git add --all 
git commit --all -m "update the static pages"

git push

echo "Completed"
```
