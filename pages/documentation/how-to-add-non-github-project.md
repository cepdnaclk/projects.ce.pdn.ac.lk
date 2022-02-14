---
layout: post
title: How to add a Non-GitHub Project | Docs
nav_order: 1
description: ""
permalink: /docs/how-to-add-non-github-project/
nav_exclude: true
search_exclude: true
---

# How to add a 'Non-GitHub' Project?
<br>

<span class="instruction">1. Fork the repository into your GitHub account from <a href="">here</a>, and clone/download it into your device.
</span>

<span class="instruction">2. Use any editor and create files based on the templates provided in the following directory. You can follow the same directory structure already there.
    (Each category/course has a template file named 'template.md' in its relevant  folder.)
</span>

```
./docs/non_github_projects/
```

<span class="instruction">
    If there any description about the project, you can add them to the end of the file, after triple dashes (<i>- - -</i>).
    That content can have basic HTML tags.
</span>

<span class="instruction">
    You can refer to the following guideline when filling the parameters in MD files.
</span>

#### MD File Parameters

<table class="table table-responsive">
    <thead class="thead-light">
        <tr>
            <th>Field</th>
            <th>Description</th>
            <th>Example</th>
        </tr>
    </thead>
    <tr>
        <td>layout</td>
        <td>[Do not change]</td>
        <td>layout: project_old</td>
    </tr>
    <tr>
        <td>title</td>
        <td>Title of the project<br>(use title-case)</td>
        <td>title: Biofeedback inputs for first person shooter games</td>
    </tr>
    <tr>
        <td>permalink</td>
        <td>
            This is the page link of the project. Recommended to use the title with lower case, and replace the 'spaces' with '-'
        </td>
        <td>permalink: /4yp/e12/biofeedback-inputs-for-first-person-shooter-games</td>
    </tr>
    <tr>
        <td>has_children</td>
        <td>[Do not change]</td>
        <td>has_children: false</td>
    </tr>
    <tr>
        <td>parent</td>
        <td>
            This should be the batch and the category name.
            In most categories, it is already provided in the template and only needs to replace the 'xx' with batch number<br>
            (Case-sensitive)
        </td>
        <td>parent: Exx Embedded Systems Projects</td>
    </tr>
    <tr>
        <td>grand_parent</td>
        <td>
            This should be a category name.<br>
            In most categories, it is already provided in the template, and no need for change.<br>
            (Case-sensitive)
        </td>
        <td>grand_parent: Embedded Systems Projects</td>
    </tr>
    <tr>
        <td>cover_url</td>
        <td>
            Need to change the course code, which is between 'categories/' and '/cover_page.jpg'<br>
            In most categories, it is already provided in the template, and no need for change.
        </td>
        <td>cover_url: https://cepdnaclk.github.io/projects.ce.pdn.ac.lk/data/categories/<span class="red">4yp</span>/cover_page.jpg</td>
    </tr>
    <tr>
        <td>thumbnail_url</td>
        <td>
            Need to change the course code, which is between 'categories/' and '/thumbnail.jpg'<br>
            In most categories, it is already provided in the template and no need for change.
        </td>
        <td>thumbnail_url: /data/categories/<span class="red">4yp</span>/thumbnail.jpg</td>
    </tr>
    <tr>
        <td>tags</td>
        <td>(Optional) Add some tags, separated by commas.</td>
        <td>tags: [	Machine learning and Data Mining ]</td>
    </tr>
    <tr>
        <td>team</td>
        <td>Add the names of the team member(s), separated by commas</td>
        <td>team: [ Herath A.B. , Karunaratne S. ]</td>
    </tr>
    <tr>
        <td>supervisors</td>
        <td>Add the names of the supervisor(s), separated by commas</td>
        <td>supervisors: [ Prof. Ragel R.G., Mr. D.S. Deegalla ]</td>
    </tr>
    <tr>
        <td>has_publication</td>
        <td>If there any publication available under this project, mark this field as '<i>true</i>'</td>
        <td>has_publication: false</td>
    </tr>
    <tr>
        <td>publication</td>
        <td>(Optional) Add the publication as a string, including contributors, journal or conference references, etc... </td>
        <td>publication: "Chuah, Chai Wen & Alawatugoda, Janaka & Kumarasiri, Malitha & Navaratna, Iranga & Silva, Rangana. (2019). On Power Analysis Attacks against Hardware Stream Ciphers. International Journal of Information and Computer Security. 11. 1. 10.1504/IJICS.2019.10023739."</td>
    </tr>
</table>
<br>

<span class="instruction">3. Once you completed the file creation, git commit, push into your repository,
    and make a <b>Pull-Request</b> to the repository, <i>https://github.com/cepdnaclk/projects.ce.pdn.ac.lk</i>,
    and inform to the one of the <a href="../contact">maintainer</a>.
</span>

<div class="card">
    <div class="card-body">
        <p class="card-text">
            If you need any clarification, please feel free to contact the Coordinator or one of the Maintainer listed in
            <a href="../contact">this page</a>.
        </p>
    </div>
</div>

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
.red{
    color:red;
}
</style>
