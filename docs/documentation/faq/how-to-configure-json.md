---
layout: post
title: FAQ | How to configure the JSON file | FAQ
nav_order: 1
description: ""
permalink: /docs/faq/how-to-configure-json/

nav_exclude: true
search_exclude: true
---

## FAQ: How to configure the JSON file?

When you are creating a GitHub repository to be shown on this site, you need to place a specific JSON file in the URL,
<i><b>https://cepdnaclk.github.io/{your-repository-name}/data/index.json</b></i>, to provide a few details.

You can follow the guidelines in the below table to fill the JSON file provided in the template.

Note: Different templates may have different set of parameters, but you can use any of the below in your <i>index.json</i> file.

<table class="table table-responsive">
    <thead class="thead-light">
        <tr>
            <th>Field</th>
            <th>Description</th>
            <th>Example</th>
        </tr>
    </thead>
    <tr>
        <td>title</td>
        <td>Title of the project (Better to use the <i>Title Case</i> for this)</td>
        <td>"title": "Example Project for the Demonstration"</td>
    </tr>

    <tr>
        <td>name</td>
        <td>Name (Applicable for both <i>team</i> and <i>supervisor</i> groups)</td>
        <td>"name": "Herath A.B."</td>
    </tr>

    <tr>
        <td>email</td>
        <td>Email address (Applicable for both <i>team</i> and <i>supervisor</i> groups)</td>
        <td>"email": "example@eng.pdn.ac.lk"</td>
    </tr>

    <tr>
        <td>eNumber</td>
        <td>E Number of the student</td>
        <td>"eNumber": "E/15/999",</td>
    </tr>

    <tr>
        <td>github_profile</td>
        <td>(Optional) The link to the GitHub profile of the student</td>
        <td>github_profile": "https://github.com/HerathAB"</td>
    </tr>

    <tr>
        <td>linkedin_profile</td>
        <td>(Optional) The link to the Linkedin profile of the student/supervisor</td>
        <td>"linkedin_profile": "https://www.linkedin.com/in/herath-a-b/"</td>
    </tr>

    <tr>
        <td>researchgate_profile</td>
        <td>(Optional) The link to the Researchgate profile of the student/supervisor</td>
        <td>"researchgate_profile": "https://www.researchgate.net/profile/Roshan-Ragel"</td>
    </tr>

    <tr>
        <td>tags</td>
        <td>(Optional) Add some tags, separated by commas</td>
        <td>"tags": [Machine learning and Data Mining, Final Year Project]</td>
    </tr>
</table>


<br>
<br>
## Publications configurations

If your project has some publications, you can fill them using the following template.
You can include more than one publication, by following the correct <i>JSON list syntax</i> as below.
If you haven’t any, keep it default or remove it from the index.json file.

```json
"publications": [
{
    "title": "Paper Title",
    "journal": "Journal or Conference Name",
    "description": "Sample Description",
    "url": "#"
}
]
```

<table class="table table-responsive">
    <thead class="thead-light">
        <tr>
            <th>Field</th>
            <th>Description</th>
            <th>Example</th>
        </tr>
    </thead>
    <tr>
        <td>title</td>
        <td>(Required) The title of the paper</td>
        <td>"title": "Paper Title"</td>
    </tr>
    <tr>
        <td>journal</td>
        <td>(Required) The Journal or the Conference that paper was published</td>
        <td>"journal": "Journal or Conference Name"</td>
    </tr>
    <tr>
        <td>description</td>
        <td>(Required) A breif description about the paper and the Journal/Conference</td>
        <td>"description": "Sample Description"</td>
    </tr>
    <tr>
        <td>url</td>
        <td>(Required) A URL to the paper in conference website, or journal page</td>
        <td>"url": "#"</td>
    </tr>
</table>


<br>
<br>
## Media Configuration

If you are interested in embedding a video with your project, you can use the following template to define them.
You can include more than one media, by following correct <i>JSON list syntax</i> as below.
If you haven't any, keep it default or remove it from the index.json file.


```json
"media": [
{
    "type": "youtube",
    "title": "",
    "url": "#"
}
]
```

<table class="table table-responsive">
    <thead class="thead-light">
        <tr>
            <th>Field</th>
            <th>Description</th>
            <th>Example</th>
        </tr>
    </thead>
    <tr>
        <td>type</td>
        <td>(Required) Type of the media (It only support YouTube videos for now)</td>
        <td>"type": "youtube",</td>
    </tr>
    <tr>
        <td>title</td>
        <td>(Required) Title of the media content</td>
        <td>"title": "Sample demonstration of the project ABC",</td>
    </tr>
    <tr>
        <td>url</td>
        <td>(Required) URL that embed the video.
            For YouTube, you can find this URL from <i>Share > Embeded</i> section</td>
        <td>"url": "https://www.youtube.com/embed/yqCF_4RPnlA"</td>
    </tr>
</table>
