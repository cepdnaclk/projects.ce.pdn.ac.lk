---
layout: default
title: How to add a Project
nav_order: 1
description: ""
permalink: /docs/how-to-add-a-project
nav_exclude: true
search_exclude: true
---

# How to add a Project ?

<h2 class="pt-4 pt-2">Instructions <small>- Create the repository using existing template</small></h2>
<br>
<span class="instruction">1. First create a repository on _cepdnaclk_ GitHub organization using one of the following template. (Click on the relevant link)</span>
<ul>
    <li class="pt-2">General Template for Course Projects
        <br>
        <span class="pl-5">
            <a href="https://github.com/cepdnaclk/eYY-XXX-project-template/generate" target="_blank">
                https://github.com/cepdnaclk/eYY-XXX-project-template/
            </a>
        </span>
    </li>

    <li class="pt-2">Embedded Systems Project Template
        <br>
        <span class="pl-5">
            <a href="https://github.com/cepdnaclk/eYY-3yp-project-template/generate/" target="_blank">
                https://github.com/cepdnaclk/eYY-3yp-project-template/
            </a>
        </span>
    </li>

    <li class="pt-2">Final Year Project Template
        <br>
        <span class="pl-5">
            <a href="https://github.com/cepdnaclk/eYY-4yp-project-template/generate/" target="_blank">
                https://github.com/cepdnaclk/eYY-4yp-project-template/
            </a>
        </span>
    </li>
</ul>

<span class="instruction">2. Select the *Owner* as <b>"cepdnaclk"</b></span>

<span class="instruction">3. Name your repository, according to the below naming convention.</span>

<blockquote class="blockquote">
    <p class="mb-0 px-5"><b>eYY-CATEGORY-TITLE</b></p>
</blockquote>

<dd><b>YY</b>: 2 digit batch number</dd>
<dd><b>CATEGORY</b>: One of the following supported category tags</dd>
<dd><b>TITLE</b>: A suitable name for your project</dd>

<br>
<blockquote>
    <span class="px-5">Ex: e15-4yp-project-name</span>
</blockquote>

<br>
*CATEGORY* assigned as follows,

|CATEGORY| Project / Course                     |
| ----- | ------------------------------------- |
| 4yp   | Final Year Project                    |
| 3yp   | Embedded Systems Project              |
| co328 | Software Engineering Project          |
| co226 | Database Projects                     |
| co326 | Computer Systems Engineering Projects |
| co543 | Image Processing                      |
| co542 | Neural Networks                       |

<br>


<span class="instruction">4. Add a proper description about your project in between 100-150 words.</span>

<span class="instruction">5. Select the visibility as **Public**.</span>

<span class="instruction">6. Click on the **Create repository from template** button.</span>

<div class="container">
    <img alt="instructions for step 2 to 6" src="{{ '/assets/images/docs/project_1.jpg' | relative }}"
    style="width:75%" class="img p-3 img-fluid img-thumbnail mx-auto"/>
</div>

<br><br>

<span class="instruction">7. Go to settings and scroll to the GitHub pages section.</span>

<span class="instruction">8. Select branch as **Main** and Folder as  **/docs** and save.</span>

<div class="container">
    <img alt="instructions for step 7 to 8" src="{{ '/assets/images/docs/project_2.jpg' | relative }}"
    style="width:75%" class="img p-3 img-fluid img-thumbnail mx-auto"/>
</div>
<br><br>

<span class="instruction">9. Now you can goto the repository and edit your GitHub page by editing the <b>/docs/README.md</b>.
    (The webpage shown in <i>https://cepdnaclk.github.io/{your-repository-name}</i>
    will be automatically generated. <a href="https://cepdnaclk.github.io/eYY-4yp-project-template/" target="_blank">[Example]</a>)
</span>

You can share your project's source code / implementations into this repository, by uploading them into the root folder of the repository.

<span class="instruction">10. </span>
These projects will be automatically added into [https://projects.ce.pdn.ac.lk](), with given title and description.
If you like to show more details about your project on this site, you can fill the JSON file, <b>/docs/index.json</b> (Note: Different templates may have different sets of parameters, as requested by the course coordinators)

<div class="container">
    <pre><code class="json dracula">
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
    </code></pre>
</div>

<br><br>
NOTES:
<ol>
    <li>
        Once you filled this <b>index.json</b> file, please make sure the syntax is correct.
        (You can use <a href="https://jsonlint.com/">this</a> tool to identify syntax errors)
    </li>

    <li>
        If your followed all the given instructions correctly, your repository will be
        automatically added to the department's project web site (Update once a week)
    </li>

    <li>
        A HTML template integrated with the given GitHub repository templates,
        based on <a href="https://github.com/cepdnaclk/eYY-project-theme">github.com/cepdnaclk/eYY-project-theme</a>.
        If you like to remove this default theme and make your own web page, you can remove the file, <b>docs/_config.yml</b> and create the site using HTML.
    </li>
</ol>

<br><br>


## Instructions - Fork your existing repository into <i>cepdnaclk</i>
<br>
<iframe width="854" height="480" src="https://www.youtube.com/embed/hegEmohtppw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="">
</iframe>

---

<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/styles/default.min.css">
<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>

<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    /* width: 75%; */
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}
</style>
