---
title: News
nav:
  order: 7
---

# <i class="fas fa-bell"></i> **HARCO LAB News**
{% include search-info.html %}
{% include section.html %}


{%
  include list.html
  data="posts"
  component="post-excerpt_test" 
  filters="group: news"
%}

{% include section.html %}



<!-- ## News Name

Example List
{% include list.html component="card" data="tools" filters="group: previous" %}

{% include section.html %}

## Site or Datas

{% include list.html component="card" data="tools" filters="group: others" %} -->
