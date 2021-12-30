---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# <i class="fas fa-We are building a team with diverse background and expertises, from software enigneering, machine learning, image analysis, data analysis to micr0scopy and computational biomedical modeling. users"></i>Team



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

{% include section.html background="images/banner.svg" dark=true%}

We are actively looking for top talents.
{%
  include link.html
  icon="fas fa-hands-helping"
  text="Join the Team"
  link="join"
  style="button"
%}
{:.center}

{% include section.html %}
