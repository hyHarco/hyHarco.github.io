---
title: Research
nav:
  order: 2
  tooltip: Our Research
---

# <i class="fas fa-search"></i> Research

{% include section.html %}
# Exoskeleton Robot Project
<!-- {% include list.html component="card" data="tools" filters="group: featured" %} -->
{% capture text %}
The shape of a human body is different in all the populations of the world. One of the most difficult things about properly controlling exoskeleton robots is that they need to be controlled flexibly, depending on the diversity of these individuals.  
In our lab, we analyze this diversity through AI technology, and are working on how to use it appropriately for robot control. 
<!-- {:.center} -->
{% endcapture %}
{%
  include feature.html
  image="images/Voucher_Res.png"
  headline="AI Lower Exoskeleton Robot Control Project"
  text=text
%}

   
<!-- [External Link](https://www.naver.com) -->
{% include section.html %}


# Mobile Manipulator Project
{%
  include feature.html
  image="images/mobile_Manipulator_Temp.png"
  link="https://hyharco.github.io/research/"
  headline="HeadLines"
  text="This is Our Mobile Manipulator Platform"
%}
{% include list.html component="card" data="tools" filters="group: research_mobile_manipulator" %}

Explanation Explanation Explanation Explanation Explanation Explanation Explanation Explanation Explanation Explanation   
and ~~~~ [External Link](https://www.naver.com)
{% include section.html %}


# Other Project
{%
  include feature.html
  image="images/research2.jpg"
  headline="Other Projects"
  text="this is Example"
%}


{% capture col1 %}
{%
  include figure.html
  image="images/Exorobot_Research_Temp.png"
  caption="Example Image"
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/mobile_Manipulator_Temp.png"
  caption="image_explanation"
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}




<!-- {%
  include feature_imgleft.html
  image="images/harco_drive.png"
  link="http://hyu-harco.myds.me:5000/#/signin"
%} -->




