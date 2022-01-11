---
title: Members
nav:
  order: 1
  tooltip: About our team
---


# <i class="fas fa-search"></i>HARCO LAB Members


{% include section.html %}

# Team Leader
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: first" 
%}

# Post-doc Reasearch
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: second" 
%}


# Ph.D. Student
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: third " 
%}


# M.S. Candidate
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: fourth " 
%}

# B.S. Candidate
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: fifth " 
%}


{% include section.html background="images/WantedYOU.png" dark=true%}

We are actively looking for top talents.
{%
  include link.html
  icon="fas fa-hands-helping"
  text="Join the Team"
  link="contact"
  style="button"
%}
{:.center}

{% include section.html %}

