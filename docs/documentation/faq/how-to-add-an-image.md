---
layout: post
title: FAQ | How to add an image
nav_order: 1
description: ""
permalink: /docs/faq/how-to-add-an-image/

nav_exclude: true
search_exclude: true
---

## FAQ: How to add an image?

When you are editing the _README.md_ file of the given repository templates, you may need to upload images.
You can use one of the following methods for it.

##### Option 1: Using MD image format

You can upload images to a folder inside your GitHub page folder (Ex: _/docs/images/_  &nbsp;folder) and add the relative URL of the image as below.

```md
![Sample Image](./images/sample.png)

Figure 1.1 Sample Image
```

##### Option 2: Using HTML + Bootstrap CSS classes

You can upload images to a folder inside your GitHub page folder (Ex: _/docs/images/_ folder) and add the relative URL of the image as below. You can also use any _Bootstrap-4_ CSS classes to format the image.

```html
<div class="figure container">
<img class="mx-auto d-block" src="./images/sample.png" alt="Sample Image" width="128" />
<p class="caption text-center">Figure 1.1 Sample Image</p>
</div>
```

##### Option 3: Using drag-and-drop upload

If you are editing the _/docs/README.md_ in the GitHub web, you can just drag and drop the image into the text editor, and it will be automatically uploaded to GitHub CDN and provide you a link like below. You can use either **Option 1** or **Option 2** with this link.

```md
![github](https://user-images.githubusercontent.com/11540782/118809291-0e6e1f00-b8c8-11eb-8bd7-66af735c50c5.png)
```

<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/styles/default.min.css">
<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
