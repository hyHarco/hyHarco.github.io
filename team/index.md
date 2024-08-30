---
title: Members
nav:
  order: 5
---
# **Harco Lab Members**

{% include section.html %}

## **Leadership**

<div class="leadership-flex-container">
  <div class="leadership-member pi">
    <h3>PI / Lab Director</h3>
    {%
      include list.html
      data="members"
      component="portrait-spc"
      filters="tier: pi"
    %}
  </div>
  <div class="leadership-member">
    <h3>Research Professor</h3>
    {%
      include list.html
      data="members"
      component="portrait-spc"
      filters="tier: research_professor"
    %}
  </div>
</div>

***

## **Postdoctoral Researcher**
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: second" 
%}

***

## **Ph.D. Student**
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: third" 
%}

***

## **M.S. Student**
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: fourth" 
%}

***

## **B.S. Student**
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: fifth" 
%}

{% include section.html %}

## <i class="fas fa-user-graduate"></i> **Alumni**
{%
  include list.html
  data="members"
  component="portrait"
  filters="tier: alumni" 
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