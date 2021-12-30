---
title: Members
nav:
  order: 1
  tooltip: About our team
---


# <i class="fas fa-search"></i>HARCO LAB Members



{% include section.html %}

{%
  include list.html
  data="members"
  component="portrait"
  filters="role: lead"
%}
{%
  include list.html
  data="members"
  component="portrait"
  filters="role: postdoc"
%}
{%
  include list.html
  data="members"
  component="portrait"
  filters="role: phd"
%}
{%
  include list.html
  data="members"
  component="portrait"
  filters="role: programmer"
%}
{:.center}

{% include section.html background="images/WantedYOU.png" dark=true%}

We are actively looking for top talents.

{% include section.html %}
