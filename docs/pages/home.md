---
layout: default
title: Home
nav_order: 1
description: ""
permalink: /
has_children: true

search_exclude: true
---

{% include page_tree_builder.html pages=site.html_pages %}

<!-- Jumbotron Header -->
<header class="jumbotron my-2">
    <p class="lead">
        Welcome to the student project listing of the Department of Computer Engineering, University of Peradeniya. This website contains the documentation, code and other multimedia resources for the academic and extra curricular projects conducted by the students of the department.
    </p>
</header>

<!-- Page Features -->
<h3 class="pt-3 pb-1">Course Projects</h3>
<div class="row text-center my-2">
    {% if page.has_children == true and page.has_toc != false %}
    {%- assign children_list = pages_list | where: "parent", page.title -%}

    <div class="container p-0 mw-100">
        <div class="row">
            {% for child in children_list %}
            <div class="col-lg-3 col-md-6 mb-2 d-flex {{ child.type }}">
                <a class="btn" href="{{ child.permalink }}">
                    <div class="card h-100">
                        <img class="card-img-top" src="{{ child.default_thumb_image }}" alt="">
                        <div class="card-body">
                            <h5 class="card-title">{{child.title}}</h5>
                        </div>
                    </div>
                </a>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}

</div>

<!-- <h3 class="pt-3 pb-1">Department Projects</h3>
<div class="row text-center my-4">
    {% if page.has_children == true and page.has_toc != false %}
    {%- assign children_list = pages_list | where: "project_type", "DepartmentProject" -%}

    <div class="container p-0 mw-100">
        <div class="row">
            {% for child in children_list %}
            <div class="col-lg-3 col-md-6 mb-2 d-flex">
                <a class="btn" href="{{ child.link }}" target="_blank">
                    <div class="card h-100">
                        <img class="card-img-top" src="{{ child.default_thumb_image | relative_url }}" alt="">
                        <div class="card-body">
                            <h5 class="card-title">{{ child.title }}</h5>
                        </div>
                    </div>
                </a>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}

</div> -->
