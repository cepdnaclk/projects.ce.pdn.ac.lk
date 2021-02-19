---
layout: default
title: How to add a Project
nav_order: 1
description: ''
permalink: /docs/how-to-add-a-project
nav_exclude: true
search_exclude: true
---

# How to add a Project ?

## Instruction Video

<iframe width="854" height="480" src="https://www.youtube.com/embed/hegEmohtppw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="">
</iframe>

## Templates

- General Template

  - <https://github.com/cepdnaclk/eYY-XXX-project-template>{:target="_blank"}

- Embedded Systems Project Template

  - <https://github.com/cepdnaclk/eYY-3yp-project-template>{:target="_blank"}

- Final Year Project Template

  - <https://github.com/cepdnaclk/eYY-4yp-project-template>{:target="_blank"}

## Naming Convention

Naming format of a project repository

- eXX-CATEGORYTAG-TITLE

CATEGORYTAG assigned as follows,

<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}
</style>

Project Categories                    | Tag
------------------------------------- | -----
Final Year Project                    | 4yp
Embedded Systems Project              | 3yp
Software Engineering Project          | co328
Database Projects                     | co226
Computer Systems Engineering Projects | co326
Image Processing                      | co543

<br>

<div class="alert alert-warning" role="alert"><b>Note</b>:<br>
   Please make sure to fill the description section in the repository.
</div>

![image](https://user-images.githubusercontent.com/11540782/108546315-f7428400-730e-11eb-8974-7f203192b8b1.png)

## Enable GitHub Pages

You can put the things to be shown in GitHub pages into the _docs/_ folder. Both html and md file formats are supported. You need to go to settings and enable GitHub pages and select _main_ branch and _docs_ folder from the dropdowns, as shown in the below image.

![image](https://user-images.githubusercontent.com/11540782/98789936-028d3600-2429-11eb-84be-aaba665fdc75.png)

## Special Configurations

These projects will be automatically added into [https://projects.ce.pdn.ac.lk](). If you like to show more details about your project on this site, you can fill the parameters in the file, _/docs/index.json_ (Note: Different templates may have different sets of parameters, as requested by the course coordinators)

```
{
  "title": "This is the title of the project",
  "team": [
    {
      "name": "Team Member Name 1",
      "email": "email@eng.pdn.ac.lk",
      "eNumber": "E/yy/xxx"
    },
    {
      "name": "Team Member Name 2",
      "email": "email@eng.pdn.ac.lk",
      "eNumber": "E/yy/xxx"
    },
    {
      "name": "Team Member Name 3",
      "email": "email@eng.pdn.ac.lk",
      "eNumber": "E/yy/xxx"
    }
  ],
  "supervisors": [
    {
      "name": "Dr. Supervisor 1",
      "email": "email@eng.pdn.ac.lk"
    },
    {
      "name": "Supervisor 2",
      "email": "email@eng.pdn.ac.lk"
    }
  ],
  "description": "This is a brief introduction of the project. You need to use plain text without any specific characters here",
  "tags": ["Web", "Embedded Systems"]
}
```

Once you filled this _index.json_ file, please verify the syntax is correct. (You can use [this](https://jsonlint.com/) tool).

## Page Theme

A custom theme integrated with this GitHub Page, which is based on [github.com/cepdnaclk/eYY-project-theme](https://github.com/cepdnaclk/eYY-project-theme). If you like to remove this default theme, you can remove the file, _docs/_config.yml_ and use your own one.

--------------------------------------------------------------------------------
