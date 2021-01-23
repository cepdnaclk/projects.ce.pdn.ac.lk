---
layout: default
title: Unified Projects
nav_order: 1
permalink: /3yp
has_children: true
num_projects: 12
parent: Home
---

{% include page_tree_builder.html pages=site.html_pages %}
<div class="row">
    {% unless page.url == "/" %}
    {% if page.parent %}
    {%- for node in pages_list -%}
    {%- if node.parent == nil -%}
    {%- if page.parent == node.title or page.grand_parent == node.title -%}
    {%- assign first_level_url = node.url | absolute_url -%}
    {%- endif -%}
    {%- if node.has_children -%}
    {%- assign children_list = pages_list | where: "parent", node.title -%}
    {%- for child in children_list -%}
    {%- if page.url == child.url or page.parent == child.title -%}
    {%- assign second_level_url = child.url | absolute_url -%}
    {%- endif -%}
    {%- endfor -%}
    {%- endif -%}
    {%- endif -%}
    {%- endfor -%}
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            {% if page.grand_parent %}
            <li class="breadcrumb-item"><a href="{{ first_level_url }}">{{ page.grand_parent }}</a></li>
            <li class="breadcrumb-item"><a href="{{ second_level_url }}">{{ page.parent }}</a></li>
            {% else %}
            <li class="breadcrumb-item"><a href="{{ first_level_url }}">{{ page.parent }}</a></li>
            {% endif %}
            <li class="breadcrumb-item"><span>{{ page.title }}</span></li>
        </ol>
    </nav>

    {% endif %}
    {% endunless %}
</div>

<div class="row">
    <div class="col-md-3">
        <h3>3rd Year Embedded System Projects</h3>

        <p></p>

        <div class="p-1"><a href="../">Back</a>
            | {{ page.num_projects }} Projects<br>
        </div>
        <hr>

        <div class="p-1">
            Filter Projects by:

            <ul class="list-group">
                <li class="list-group-item p-1 align-items-center">
                    <a href="./e15" class="d-flex justify-content-between">
                        <span class="mx-2">eYY Batch</span>
                        <span class="mx-2 badge badge-secondary badge-pill">1</span>
                    </a>
                </li>
            </ul>
        </div>
        <br><br>
    </div>

    <div class="col-md-9">
        {% if page.has_children == true and false %}
        <hr>
        <h2 class="text-delta">Table of contents</h2>
        <ul>
            {%- assign children_list = pages_list | where: "parent", page.title | where: "grand_parent", page.parent -%}
            {% for child in children_list %}
            <li>
                <a href="{{ child.url | absolute_url }}">{{ child.title }}</a>{% if child.summary %} - {{ child.summary }}{% endif %}
            </li>
            {% endfor %}
        </ul>
        {% endif %}

        <div class="container p-3 mw-100">
            <div class="row">
                <div class="col-lg-3 col-md-6 d-flex">
                    <a class="btn" href="./e15/A-GUI-for-controlling-and-supervising-multiple-robots-remotely.html">
                        <div class="card h-100 m-0">
                            <img class="card-img-top" src="https://cepdnaclk.github.io/projects/data/categories/unified/thumbnail.jpg" alt="">
                            <div class="card-body p-0 m-1">

                                <p class="card-title">A GUI for control and supervising multiple robots remotely (e15)</p>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
        <div class="container my-4 d-flex justify-content-center">

        </div>

    </div>
</div>
